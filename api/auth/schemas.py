import uuid
from pydantic import BaseModel, EmailStr


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


class UserAuth(BaseModel):
    nickname: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    nickname: str


class Hashed(BaseModel):
    hashed_password: str