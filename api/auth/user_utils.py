from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.database import get_async_session
from api.auth.models import User as UserModel
from api.auth.schemas import User as UserSchema
from api.auth.security import Hash, oauth2_scheme, AccessToken


async def get_conn(session: AsyncSession):
    result = await session.execute(select(UserSchema))
    await session.close()
    return result.all()


async def add_user(session: AsyncSession, nickname: str, email: str, password: str) -> UserSchema | dict:
    new_user = UserModel(nickname=nickname, email=email, hashed_password=Hash.get_password_hash(password))
    try:
        session.add(new_user)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        return {"Error": "User with such credentials already exists"}
    return new_user


async def get_user_by_nickname(session: AsyncSession, nickname: str) -> UserSchema | None:
    result = await session.execute(
        select(UserModel).where(UserModel.nickname == nickname)
    )
    return result.fetchone()[0]


async def get_hashed_password(session: AsyncSession, nickname: str) -> UserSchema | None:
    result = await session.execute(
        select(UserModel.hashed_password).where(UserModel.nickname == nickname)
    )
    return result.fetchone()[0]


async def get_user_by_id(session: AsyncSession, user_id: str) -> UserSchema | None:
    result = await session.execute(
        select(UserModel).where(UserModel.id == user_id)
    )
    return result.fetchone()[0]


async def authenticate_user(session: AsyncSession, nickname: str, password: str) -> UserSchema | None:
    user = await get_user_by_nickname(session, nickname)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    password_check = Hash.verify_password(password, await get_hashed_password(session, nickname))
    if not password_check:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return user


async def update_user_utils(token: Annotated[str, Depends(oauth2_scheme)],
                            session: AsyncSession = Depends(get_async_session)) -> bool | dict:
    user_id = await AccessToken.verify_access_token(token)
    promotion = await session.execute(
        update(UserModel).where(UserModel.id == user_id["sub"]).values(user_level="upper")
    )
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        return {"Error": "User with such credentials already exists"}

    if not promotion:
        return False
    return True


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           session: AsyncSession = Depends(get_async_session)) -> UserSchema | None:
    decoded_data = await AccessToken.verify_access_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Token credentials error")
    user = await get_user_by_id(session, decoded_data["sub"])
    if not user:
        raise HTTPException(status_code=400, detail="No such user")
    return user