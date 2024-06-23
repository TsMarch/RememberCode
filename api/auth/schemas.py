import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field("bearer")
    access_token_expiration: datetime.datetime
    refresh_token_expiration: datetime.datetime


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nickname: str = Field(max_length=10)
    email: EmailStr
    hashed_password: Annotated[str, Field(exclude=True)]
    _id: UUID


class UserAdditional(User):
    user_level: str | None = None
    is_premium: bool | None = None
    disabled: bool | None = None
