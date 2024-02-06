from uuid import UUID

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    nickname: str or None = None


class User(BaseModel):
    nickname: str
    email: EmailStr
    hashed_password: str
    user_level: str


class UserVerify(BaseModel):
    nickname: str
    email: EmailStr
    user_level: str


class UserRead(BaseModel):
    nickname: str
    email: EmailStr
    user_level: str
    is_premium: bool | None


class UserAuth(BaseModel):
    nickname: str
    password: str


class Hashed(BaseModel):
    hashed_password: str
