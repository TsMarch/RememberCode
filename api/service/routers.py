import json
from datetime import datetime, timedelta
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
    prefix="/service",
    responses={404: {"description": "Not found"}},
)


@router.post("/delete/redis", response_model=dict)
async def delete_token(type_of_token: str = Query(None, description="access_token or refresh_token or all"),
                       token: Annotated[str | None, Header()] = None):
    result = await security_utils.delete_token(type_of_token, token)
    return result
