from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import redis.asyncio
from api.config import (DB_POSTGRES_HOST, DB_POSTGRES_USER, DB_POSTGRES_PASS, DB_POSTGRES_NAME, DB_POSTGRES_PORT,
                        REDIS_HOST)

DATABASE_URL = f"postgresql+asyncpg://{DB_POSTGRES_USER}:{DB_POSTGRES_PASS}@{DB_POSTGRES_HOST}:{DB_POSTGRES_PORT}/{DB_POSTGRES_NAME}"


engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Dependency for postgresql
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


url_connection_redis = redis.asyncio.Redis(host=REDIS_HOST, port=6379, db=1, decode_responses=True)

url_connection_redis_blacklist = redis.asyncio.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

url_connection_redis_acc = redis.asyncio.Redis(host=REDIS_HOST, port=6379, db=2, decode_responses=True)


