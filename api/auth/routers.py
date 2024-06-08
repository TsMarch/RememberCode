from datetime import datetime, timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import security_utils, user_utils
from api.auth.databases_helper import get_async_session
from api.auth.schemas import User
from api.auth.security import AccessToken

router = APIRouter(
    prefix="/auth/jwt",
    responses={404: {"description": "Not found"}},
)


@router.get('/logout')
async def logout(token: Annotated[User, Depends(user_utils.get_current_users_token)]):
    result = await security_utils.delete_token(token)
    if result:
        return {"result": "success"}
    raise HTTPException(status_code=401, detail="Not authorized")


# Get token
@router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(get_async_session)
):
    user = await user_utils.authenticate_user(session, form_data.username, form_data.password)
    access_token = AccessToken.create_access_token(data={"sub": jsonable_encoder(user.id)})
    refresh_token = AccessToken.create_refresh_token(data={"sub": jsonable_encoder(user.id)})
    await security_utils.write_to_redis(refresh_token=[refresh_token, jsonable_encoder(user.id)],
                                        access_token=[access_token, jsonable_encoder(user.id)])
    return {"access_token": access_token,  "refresh_token": refresh_token, "token_type": "bearer",
            "access_token_expiration": datetime.utcnow()+timedelta(minutes=30),
            "refresh_token_expiration": datetime.utcnow()+timedelta(days=30)}


@router.post("/refresh")
async def refresh(refresh_token: Annotated[str, Header()]):
    refresh_token = await security_utils.get_new_token(refresh_token)
    return refresh_token


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
