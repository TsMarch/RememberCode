from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import utils
from api.auth.schemas import UserVerify, UserRead, User
from api.database import get_async_session

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
