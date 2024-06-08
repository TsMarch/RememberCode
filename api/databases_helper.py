from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import redis.asyncio
from api.config import (settings,
                        REDIS_HOST)


class DatabaseUser:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False
        )

    async def get_async_session(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()


class RedisConnection:
    def __init__(self, host: str, port: int, decode_responses=True):
        self.host = host
        self.port = port
        self.decode_responses = decode_responses

    def redis_connection(self, db) -> redis.asyncio.Redis:
        return redis.asyncio.Redis(
            host=self.host,
            port=self.port,
            db=db,
            decode_responses=self.decode_responses
        )

    def redis_connection_close(self, db):
        return self.redis_connection(db).close()

    def __str__(self):
        return f"{self.db}, {self.host}, {self.port}"

    @classmethod
    def update_db_number(cls, value):
        cls.db = value

    @staticmethod
    def url_connection(db: int) -> redis.asyncio.Redis:
        url_connection_redis = redis.asyncio.Redis(host="localhost", port=6379, db=db, decode_responses=True)
        return url_connection_redis


db_user_helper = DatabaseUser(
    url=settings.db.url
)

redis_helper = RedisConnection(
    host=settings.redis.host,
    port=settings.redis.port
)
