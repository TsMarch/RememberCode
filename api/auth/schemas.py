from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Optional


class Token(BaseModel):
    access_token: str
    # refresh_token: str
    token_type: str


class User(BaseModel):
    nickname: str
    email: EmailStr
    hashed_password: Annotated[str, Field(exclude=True)]
    _id: UUID


class UserAdditional(User):
    id: UUID
    user_level: str | None = None
    is_premium: bool | None = None
    disabled: bool | None = None
