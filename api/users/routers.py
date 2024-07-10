from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import security_utils, user_utils
from api.auth.schemas import User as UserSchema, UserAdditional
from api.configs.database import db_user_helper
from api.auth.services.UserService import UserService

router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=UserSchema)
async def add_user(
    user: UserSchema, userService: UserService = Depends(),
):
    return userService.create(user)




# Get user by nickname
@router.post(
    "/get_user/nickname",
    response_model=UserSchema,
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
    response_model=UserSchema,
    response_model_exclude={"hashed_password", "id", "disabled", "is_premium"},
)
async def get_user_by_id(
    user_id: str, session: AsyncSession = Depends(db_user_helper.connection)
):
    check = await user_utils.get_user_by_id(session, user_id)
    return check


@router.patch(
    "/update_level",
    response_model=UserSchema,
    response_model_exclude={"hashed_password", "disabled"},
)
async def promote_user(
    update_user: Annotated[UserSchema, Depends(user_utils.update_user_utils)]
):
    return update_user
