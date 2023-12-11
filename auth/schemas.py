from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    nickname: str
    user_level: str

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    email: str
    password: str
    nickname: str
    user_level: str



