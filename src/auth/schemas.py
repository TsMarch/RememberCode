import uuid

from pydantic import EmailStr


class UserRead(BaseUser[uuid.UUID]):
    email: EmailStr
    nickname: str
    user_level: str

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    nickname: str
    user_level: str


class UserUpdate(schemas.BaseUserUpdate):
    password: str
    email: EmailStr
    is_active: str


