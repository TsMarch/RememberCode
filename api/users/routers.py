from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import security_utils, user_utils
from api.auth.schemas import User, UserAdditional
from api.configs.database import db_user_helper

router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)


@router.post("/registration/", response_model=User)
async def add_user(
    user: User, session: AsyncSession = Depends(db_user_helper.connection)
):
    user = await user_utils.add_user(
        session, user.nickname, user.email, user.hashed_password
    )
    return user


@router.post(
    "/me",
    response_model=UserAdditional | dict,
    response_model_exclude={"hashed_password"},
)
async def read_users_me(
    current_user: Annotated[User, Depends(security_utils.get_from_redis)]
):
    return current_user


# Get user by nickname
@router.post(
    "/get_user/nickname",
    response_model=User,
    response_model_exclude={"hashed_password", "id", "disabled", "is_premium"},
)
async def get_user_by_nickname(
    nickname: str, session: AsyncSession = Depends(db_user_helper.connection)
):
    check = await user_utils.get_user_by_nickname(session, nickname)
    return check


# Get user by id
@router.post(
    "/get_user/id",
    response_model=User,
    response_model_exclude={"hashed_password", "id", "disabled", "is_premium"},
)
async def get_user_by_id(
    user_id: str, session: AsyncSession = Depends(db_user_helper.connection)
):
    check = await user_utils.get_user_by_id(session, user_id)
    return check


@router.patch(
    "/update_level",
    response_model=User,
    response_model_exclude={"hashed_password", "disabled"},
)
async def promote_user(
    update_user: Annotated[User, Depends(user_utils.update_user_utils)]
):
    return update_user
