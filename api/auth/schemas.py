from typing import Union
from uuid import UUID

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    #refresh_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None = None


class UserReg(BaseModel):
    nickname: str
    email: EmailStr
    hashed_password: str


class User(BaseModel):
    nickname: str
    email: EmailStr
    id: UUID
    user_level: str | None = None
    is_premium: bool | None = None
    disabled: bool | None = None


class UserNonSensitive(BaseModel):
    nickname: str
    user_level: str | None = None
    is_premium: bool | None = None
    disabled: bool | None = None

