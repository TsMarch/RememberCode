import json
from datetime import datetime, timedelta
from typing import Annotated, Optional, Any, List, Type, Tuple, Dict

from fastapi import APIRouter, Depends, HTTPException, Header, Query
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import security_utils, user_utils
from api.auth.database import get_async_session
from api.auth.schemas import User, Token, UserReg
from api.auth.security import AccessToken, oauth2_scheme

router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not found"}},
)


@router.get('/logout')
async def logout(token: Annotated[User, Depends(user_utils.get_current_users_token)]):
    result = await security_utils.delete_token(token)
    if result:
        return {"result": "success"}
    raise HTTPException(status_code=401, detail="Not authorized")


# Registration
@router.post("/registration/", response_model=User | dict
             )
async def add_user(user: UserReg, session: AsyncSession = Depends(get_async_session)):
    user = await user_utils.add_user(session, user.nickname, user.email, user.hashed_password)
    return user


# Get user by nickname
@router.post("/get_user/nickname", response_model=User,
             response_model_exclude={"hashed_password", "id", "disabled", "is_premium"}
             )
async def get_user_by_nickname(nickname: str, session: AsyncSession = Depends(get_async_session)):
    check = await user_utils.get_user_by_nickname(session, nickname)
    return check


# Get user by id
@router.post("/get_user/id", response_model=User,
             response_model_exclude={"hashed_password", "id", "disabled", "is_premium"}
             )
async def get_user_by_id(user_id: str, session: AsyncSession = Depends(get_async_session)):
    check = await user_utils.get_user_by_id(session, user_id)
    return check


# Get token
@router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(get_async_session)
):
    user = await user_utils.authenticate_user(session, form_data.username, form_data.password)
    access_token = AccessToken.create_access_token(data={"sub": jsonable_encoder(user.id)})
    refresh_token = AccessToken.create_refresh_token(data={"sub": jsonable_encoder(user.id)})
   # auth_check = await AccessToken.verify_access_token(access_token)
   # if not auth_check:
    #    raise HTTPException(status_code=400, detail="Fake token")
    await security_utils.write_to_redis("refresh_token", refresh_token, jsonable_encoder(user.id))
    await security_utils.write_to_redis("access_token", access_token, jsonable_encoder(user.id))
    return {"access_token": access_token,  "refresh_token": refresh_token, "token_type": "bearer",
            "access_token_expiration": datetime.utcnow()+timedelta(minutes=30),
            "refresh_token_expiration": datetime.utcnow()+timedelta(days=30)}


@router.post("/refresh")
async def refresh(refresh_token: Annotated[str, Header()],
                  session: AsyncSession = Depends(get_async_session)):
    refresh_token = await security_utils.get_new_token(refresh_token)
    return refresh_token


# Secured path (depends on token)
@router.post("/users/me", response_model=User | Any,
             response_model_exclude={"hashed_password", "nickname", "disabled", "email"}
             )
async def read_users_me(current_user: Annotated[User, Depends(security_utils.get_from_redis)],
                        session: AsyncSession = Depends(get_async_session),
                        refresh_token: Annotated[str | None, Header()] = None):
    return current_user
#    match current_user:
 #       case {"status": "no such token"}:
  #          refresh_token = await security_utils.get_new_token(refresh_token)
   #         cur_user = await security_utils.get_from_redis(refresh_token["access_token"], session)
    #        return cur_user
     #   case _:
      #      return current_user


@router.post("/testrouter", response_model=User | Any,
             response_model_exclude={"hashed_password", "nickname", "email"})
async def test(token: Annotated[str, Depends(security_utils.get_from_redis)],
               refresh_token: Annotated[str | None, Header()] = None):
    match token:
        case {"status": "no token in redis"}:
            refresh_token = await security_utils.get_new_token(refresh_token)
            return refresh_token
        case _:
            return token


# Route to update user
@router.patch("/users/update_level", response_model=User | bool,
              response_model_exclude={"hashed_password", "disabled"}
              )
async def promote_user(update_user: Annotated[User, Depends(user_utils.update_user_utils)]):
    return update_user


@router.post("/delete/redis", response_model=dict)
async def delete_token(type_of_token: str = Query(None, description="access_token or refresh_token or all"),
                       token: Annotated[str | None, Header()] = None):
    result = await security_utils.delete_token(type_of_token, token)
    return result
