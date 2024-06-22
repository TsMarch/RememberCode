from typing import Annotated, Any

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import security_utils, user_utils
from api.auth.schemas import Token, User
from api.databases_helper import db_user_helper

router = APIRouter(
    prefix="/auth/jwt",
    responses={404: {"description": "Not found"}},
)


@router.get("/logout")
async def logout(token: Annotated[User, Depends(user_utils.get_current_users_token)]):
    result = await security_utils.delete_token(token)
    if result:
        return {"result": "success"}
    raise HTTPException(status_code=401, detail="Not authorized")


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(db_user_helper.connection),
):
    tokens = await security_utils.return_tokens(
        session, username=form_data.username, password=form_data.password
    )
    return tokens


@router.post("/refresh", response_model=Token)
async def refresh(refresh_token: Annotated[str, Header()]):
    refresh_token = await security_utils.get_new_token(refresh_token)
    return refresh_token


@router.post(
    "/testrouter",
    response_model=User | Any,
    response_model_exclude={"hashed_password", "nickname", "email"},
)
async def test(
    token: Annotated[str, Depends(security_utils.get_from_redis)],
    refresh_token: Annotated[str | None, Header()] = None,
):
    match token:
        case {"status": "no token in redis"}:
            refresh_token = await security_utils.get_new_token(refresh_token)
            return refresh_token
        case _:
            return token
