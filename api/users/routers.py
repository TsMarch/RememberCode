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
    prefix="/users",
    responses={404: {"description": "Not found"}},
)


@router.post("/registration/", response_model=User | dict
             )
async def add_user(user: UserReg, session: AsyncSession = Depends(get_async_session)):
    user = await user_utils.add_user(session, user.nickname, user.email, user.hashed_password)
    return user


@router.post("/me", response_model=User | Any,
             response_model_exclude={"hashed_password", "nickname", "disabled", "email"}
             )
async def read_users_me(current_user: Annotated[User, Depends(security_utils.get_from_redis)],
                        session: AsyncSession = Depends(get_async_session),
                        refresh_token: Annotated[str | None, Header()] = None):
    return current_user


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


@router.patch("/update_level", response_model=User | bool,
              response_model_exclude={"hashed_password", "disabled"}
              )
async def promote_user(update_user: Annotated[User, Depends(user_utils.update_user_utils)]):
    return update_user
