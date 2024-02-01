from fastapi import Depends, FastAPI, HTTPException, status
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth.models import User
from api.auth.schemas import Token, TokenData, User
from api.database import get_async_session
from api.auth.auth_config import get_password_hash, verify_password, oauth2_scheme, SECRET_KEY, ALGORITHM
from sqlalchemy import exc
from jose import JWTError, jwt


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


async def get_hashed_password(session: AsyncSession, nickname: str):
    result = await session.execute(select(User.hashed_password).where(User.nickname == nickname))
    return result.scalar_one()


async def authenticate_user(session: AsyncSession, nickname: str, password: str):
    user_check = await get_user_by_nickname(session, nickname)
    match user_check:
        case _:
            get_hash = await get_hashed_password(session, nickname)
            check_pass = verify_password(password, get_hash)
            return check_pass


async def get_current_user(session: AsyncSession, token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        nickname: str = payload.get("sub")
        if nickname is None:
            raise credential_exception

        token_data = TokenData(nickname=nickname)
    except JWTError:
        raise credential_exception

    user = get_user_by_nickname(session, nickname=token_data.nickname)
    if user is None:
        raise credential_exception

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user

