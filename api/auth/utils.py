import json
from typing import Annotated, Union

from fastapi import Depends, HTTPException

from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth.models import User as UserModel
from api.auth.schemas import User as UserSchema
from api.auth.database import get_async_session, url_connection
from api.auth.auth_config import get_password_hash, verify_password, oauth2_scheme, verify_access_token


async def get_conn(session: AsyncSession):
    result = await session.execute(select(UserSchema))
    return result.all()


async def add_user(session: AsyncSession, nickname: str, email: str, password: str) -> UserSchema | None:
    new_user = UserModel(nickname=nickname, email=email, hashed_password=get_password_hash(password))
    session.add(new_user)
    return new_user


async def get_user_by_nickname(session: AsyncSession, nickname: str) -> UserSchema | None:
    result = await session.execute(select(UserModel).where(UserModel.nickname == nickname))
    return result.fetchone()[0]


async def get_hashed_password(session: AsyncSession, nickname: str) -> UserSchema | None:
    result = await session.execute(select(UserModel.hashed_password).where(UserModel.nickname == nickname))
    return result.fetchone()[0]


async def get_user_by_id(session: AsyncSession, user_id: str) -> UserSchema | None:
    result = await session.execute(select(UserModel).where(UserModel.id == user_id))
    return result.fetchone()[0]


async def authenticate_user(session: AsyncSession, nickname: str, password: str) -> UserSchema | None:
    user = await get_user_by_nickname(session, nickname)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    password_check = verify_password(password, await get_hashed_password(session, nickname))
    if not password_check:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return user


async def update_user(session: AsyncSession, user_id) -> bool:
    await session.execute(update(UserModel).where(UserModel.id == user_id).values(user_level="upper"))
    return True


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           session: AsyncSession = Depends(get_async_session)) -> UserSchema | None:
    decoded_data = await verify_access_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Token credentials error")
    user = await get_user_by_id(session, decoded_data["sub"])
    if not user:
        raise HTTPException(status_code=400, detail="No such user")
    return user


async def write_to_redis(key, value):
    await url_connection.set(key, value)


async def get_from_redis(token: Annotated[str, Depends(oauth2_scheme)],
                         session: AsyncSession = Depends(get_async_session)):
    """
    This function decodes the token, then passing subjects uuid key to redis, and finally checks if tokens
    (value in redis) are equal.
    """
    decoded_data = await verify_access_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Bad token")
    check_token = await url_connection.get(decoded_data["sub"])
    if not check_token:
        raise HTTPException(status_code=400, detail="No such token in database")
    if check_token == token:
        user = await get_user_by_id(session, decoded_data["sub"])
        return user
