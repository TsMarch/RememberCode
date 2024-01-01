import uuid
import redis.asyncio
from fastapi_users import FastAPIUsers

from fastapi_users.authentication import AuthenticationBackend, RedisStrategy


from src.auth.manager import get_user_manager
from src.auth.models import User

from src.config import DB_SECRET_AUTH

from fastapi_users.authentication import BearerTransport


redis = redis.asyncio.from_url("redis://redis:6379", decode_responses=True)

SECRET = "SECRET"

bearer_transport = BearerTransport(tokenUrl="auth/login")


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(redis, lifetime_seconds=None)


auth_backend = AuthenticationBackend(
    name="redis",
    transport=bearer_transport,
    get_strategy=get_redis_strategy,
)


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
