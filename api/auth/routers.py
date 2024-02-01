from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from api.auth import utils
from api.auth.schemas import UserVerify, UserRead, User, UserAuth, Hashed, Token
from api.database import get_async_session
from datetime import datetime, timedelta
from api.auth.auth_config import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token


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
@router.post("/get_user/", response_model=list[UserVerify])
async def get_user_by_nickname(user: UserRead, session: AsyncSession = Depends(get_async_session)):
    check = await utils.get_user_by_nickname(session, user.nickname)
    return check


@router.post("/auth_user/")
async def authenticate_user(user: UserAuth, session: AsyncSession = Depends(get_async_session)):
    auth = await utils.authenticate_user(session, user.nickname, user.password)
    return auth

# WIP
#@router.post("/token", response_model=Token)
#async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#    user = authenticate_user(AsyncSession, form_data.username, form_data.password)
 #   if not user:
  #      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
   #                         detail="Incorrent username or password",
          #                  headers={"WWW-Authenticate": "Bearer"})
   # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
   # access_token = create_access_token(data={"sub": user.username}, expires_delt=access_token_expires)
   # return {"access_token": access_token, "token_type": "bearer"}