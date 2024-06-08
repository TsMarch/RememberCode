from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


from api.databases_helper import db_user_helper


class Base(DeclarativeBase):
    pass


class Questions(Base):
    __tablename__ = "questions"

    index: Mapped[int] = mapped_column(default=int, primary_key=True, index=True)
    question: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    answer: Mapped[str] = mapped_column(String, unique=True, nullable=False)


async def create_tables():
    async with db_user_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

