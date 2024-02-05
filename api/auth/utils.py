from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth.models import User as UserModel
from api.auth.schemas import User as UserSchema, TokenData
from api.database import get_async_session
from api.auth.auth_config import get_password_hash, verify_password, oauth2_scheme, SECRET_KEY, ALGORITHM, verify_access_token
from sqlalchemy import exc
from jose import JWTError, jwt


async def get_conn(session: AsyncSession):
    result = await session.execute(select(UserSchema))
    return result.all()


async def add_user(session: AsyncSession, nickname: str, email: str, password: str):
    new_user = UserModel(nickname=nickname, email=email, hashed_password=get_password_hash(password))
    session.add(new_user)
    return new_user.nickname, new_user.email


async def get_user_by_nickname(session: AsyncSession, nickname: str):
    result = await session.execute(select(UserModel).where(UserModel.nickname == nickname))
    return result.scalar_one()


async def get_hashed_password(session: AsyncSession, nickname: str):
    result = await session.execute(select(UserModel.hashed_password).where(UserModel.nickname == nickname))
    return result.scalar_one()


async def authenticate_user(session: AsyncSession, nickname: str, password: str):
    user = await get_user_by_nickname(session, nickname)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    password_check = verify_password(password, await get_hashed_password(session, nickname))
    if not password_check:
        raise HTTPException(status_code=400, detail="Inoorrect username or password")

    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(get_async_session)):
    decoded_data = verify_access_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Token expired")
    user = await get_user_by_nickname(session, decoded_data["sub"])
    if not user:
        raise HTTPException(status_code=400, detail="No such user")
    return user
