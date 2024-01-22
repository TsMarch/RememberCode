from typing import List

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth.models import User
from api.database import get_async_session
from api.auth.auth_config import get_password_hash


async def get_conn(session: AsyncSession):
    result = await session.execute(select(User))
    return result.all()


async def add_user(session: AsyncSession, nickname: str, email: str, password: str):
    new_user = User(nickname=nickname, email=email, hashed_password=get_password_hash(password))
    session.add(new_user)
    return new_user


async def get_user_by_nickname(session: AsyncSession, nickname: str):
    result = await session.execute(select(User).where(User.nickname == nickname))
    return result.scalars()
