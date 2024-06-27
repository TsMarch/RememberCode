import uuid

from pydantic import EmailStr
from sqlalchemy import Boolean, String
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)

from api.configs.database import db_user_helper


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"reg-{cls.__name__.lower()}s"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)


class User(Base):

    nickname: Mapped[str] = mapped_column(String(length=20), unique=True)
    email: Mapped[EmailStr] = mapped_column(String(length=320), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024))
    user_level: Mapped[str] = mapped_column(String(length=20), default="Beginner")
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)


async def create_tables():
    async with db_user_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
