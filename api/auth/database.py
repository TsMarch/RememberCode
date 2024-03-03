from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import redis.asyncio
from redis import Redis
from api.config import DB_PORT, DB_USER, DB_PASS, DB_NAME, DB_HOST

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Dependency for postgresql
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


url_connection_redis = redis.asyncio.Redis(host='redis', port=6379, db=1, decode_responses=True)

url_connection_redis_blacklist = redis.asyncio.Redis(host='redis', port=6379, db=0, decode_responses=True)




