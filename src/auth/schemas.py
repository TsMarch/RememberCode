from fastapi_users import schemas
import datetime
import uuid
from pydantic import EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):
    nickname: str
    email: EmailStr
    user_level: str

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    nickname: str
    password: str
    user_level: str


class UserUpdate(schemas.BaseUserUpdate):
    password: str
    email: EmailStr
    is_active: str
    is_superuser: str
    is_verified: str


