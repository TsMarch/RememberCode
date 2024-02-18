import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from pydantic import EmailStr

from api.auth.database import engine


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "reg-users"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, index=True)
    nickname: Mapped[str] = mapped_column(String(length=20), unique=True, nullable=False)
    email: Mapped[EmailStr] = mapped_column(String(length=320), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    user_level: Mapped[str] = mapped_column(String(length=20), default="Beginner", nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
