import os

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()

DB_POSTGRES_HOST = os.environ.get("DB_HOST")
DB_POSTGRES_PORT = os.environ.get("DB_PORT")
DB_POSTGRES_NAME = os.environ.get("DB_NAME")
DB_POSTGRES_USER = os.environ.get("DB_USER")
DB_POSTGRES_PASS = os.environ.get("DB_PASS")
DB_PORT_MONGO = os.environ.get("DB_PORT_MONGO")
DB_SECRET_AUTH = os.environ.get("AUTH_SECRET")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
SECRET_KEY = os.environ.get("SECRET_KEY")


class PostgresSettings(BaseModel):
    url: str = (
        f"postgresql+asyncpg://{DB_POSTGRES_USER}:{DB_POSTGRES_PASS}@{DB_POSTGRES_HOST}:{DB_POSTGRES_PORT}"
        f"/{DB_POSTGRES_NAME}"
    )


class RedisSettings(BaseModel):
    port: int = REDIS_PORT
    host: str = REDIS_HOST


class Settings(BaseSettings):
    db: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
