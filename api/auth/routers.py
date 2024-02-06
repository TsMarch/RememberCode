from typing import Annotated
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from api.auth import utils
from api.auth.schemas import UserVerify, UserRead, User, Token
from api.auth.utils import authenticate_user, get_current_user
from api.database import get_async_session
from datetime import datetime, timedelta
from api.auth.auth_config import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, oauth2_scheme

router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not found"}},
)


@router.post("/registration/")
async def add_user(user: User, session: AsyncSession = Depends(get_async_session)):
    user = await utils.add_user(session, user.nickname, user.email, user.hashed_password)
    try:
        await session.commit()
        return user
    except IntegrityError as ex:
        await session.rollback()
        raise IntegrityError("This user already exists")


# Get user by nickname
@router.post("/get_user/")
async def get_user_by_nickname(nickname: str, session: AsyncSession = Depends(get_async_session)):
    check = await utils.get_user_by_nickname(session, nickname)
    return check


@router.post("/get_user/id", response_model=UserRead)
async def get_user_by_id(user_id: str, session: AsyncSession = Depends(get_async_session)):
    check = await utils.get_user_by_id(session, user_id)
    return check


# WIP
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession = Depends(get_async_session)
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": jsonable_encoder(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/me", response_model=UserRead)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
