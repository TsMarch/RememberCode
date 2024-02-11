from typing import Annotated
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from api.auth import utils
from api.auth.schemas import User, Token
from api.auth.utils import authenticate_user, get_current_user, get_from_redis
from api.auth.database import get_async_session
from api.auth.auth_config import create_access_token, verify_access_token

router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not found"}},
)


@router.post("/registration/", response_model=User,
             response_model_exclude={"hashed_password", "id", "disabled", "is_premium"}
             )
async def add_user(user: User, session: AsyncSession = Depends(get_async_session)):
    user = await utils.add_user(session, user.nickname, user.email, user.hashed_password)
    try:
        await session.commit()

        return user
    except IntegrityError as ex:
        await session.rollback()
        raise IntegrityError("This user already exists")


# Get user by nickname
@router.post("/get_user/nickname", response_model=User,
             response_model_exclude={"hashed_password", "id", "disabled", "is_premium"}
             )
async def get_user_by_nickname(nickname: str, session: AsyncSession = Depends(get_async_session)):
    check = await utils.get_user_by_nickname(session, nickname)
    return check


@router.post("/get_user/id", response_model=User,
             response_model_exclude={"hashed_password", "id", "disabled", "is_premium"}
             )
async def get_user_by_id(user_id: str, session: AsyncSession = Depends(get_async_session)):
    check = await utils.get_user_by_id(session, user_id)
    return check


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(get_async_session)
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": jsonable_encoder(user.id)})
    auth_check = await verify_access_token(access_token)
    if not auth_check:
        raise HTTPException(status_code=400, detail="Fake token")
    await utils.write_to_redis(jsonable_encoder(user.id), access_token)
    return {"access_token": access_token, "token_type": "bearer"}


# Secured path
@router.post("/users/me", response_model=User,
             response_model_exclude={"hashed_password", "nickname", "disabled", "email"}
             )
async def read_users_me(current_user: Annotated[User, Depends(get_from_redis)]):
    return current_user


@router.patch("/users/update_level", #response_model=User,
              #response_model_exclude={"hashed_password", "disabled"}
              )
async def promote_user(user_id: str, session: AsyncSession = Depends(get_async_session)):
    result = await utils.update_user(session, user_id)
    try:
        await session.commit()
    finally:
        return result

