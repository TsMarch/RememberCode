from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import redis.asyncio
from api.config import (DB_POSTGRES_HOST, DB_POSTGRES_USER, DB_POSTGRES_PASS, DB_POSTGRES_NAME, DB_POSTGRES_PORT,
                        REDIS_HOST)

DATABASE_URL = (f"postgresql+asyncpg://{DB_POSTGRES_USER}:{DB_POSTGRES_PASS}@{DB_POSTGRES_HOST}:{DB_POSTGRES_PORT}"
                f"/{DB_POSTGRES_NAME}")


engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Dependency for postgresql
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


class RedisConnection:
    @staticmethod
    def url_connection(db: int) -> redis.asyncio.Redis:
        url_connection_redis = redis.asyncio.Redis(host=REDIS_HOST, port=6379, db=db, decode_responses=True)
        return url_connection_redis

