from abc import ABC, abstractmethod

import redis.asyncio
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from api.configs.settings import settings


class AbstractConnection(ABC):
    @abstractmethod
    def connection(self):
        pass


class DatabaseUser(AbstractConnection):
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, expire_on_commit=False
        )

    async def connection(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()


class MonostateRedisConnection(AbstractConnection):
    connection = {}

    def __init__(self, host: str, port: int):
        self.__dict__ = self.connection
        if not self.connection:
            self.connection[1] = redis.asyncio.Redis(
                host=host, port=port, db=1, decode_responses=True
            )
            self.connection[2] = redis.asyncio.Redis(
                host=host, port=port, db=2, decode_responses=True
            )
            self.connection[0] = redis.asyncio.Redis(
                host=host, port=port, db=0, decode_responses=True
            )


db_user_helper = DatabaseUser(url=settings.db.url)

redis_helper = MonostateRedisConnection(
    host=settings.redis.host, port=settings.redis.port
)
#redis.asyncio.Redis.rpush()
# ("redis://localhost:6379?decode_responses=True?db=1")
