from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class Token(BaseModel):
    access_token: str
    # refresh_token: str
    token_type: str


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nickname: str = Field(max_length=10)
    email: EmailStr
    _hashed_password: str
    _id: UUID


class UserAdditional(User):
    user_level: str | None = None
    is_premium: bool | None = None
    disabled: bool | None = None
