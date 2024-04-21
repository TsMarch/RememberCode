from dotenv import load_dotenv
import os

load_dotenv()

DB_POSTGRES_HOST = os.environ.get("DB_HOST")
DB_POSTGRES_PORT = os.environ.get("DB_PORT")
DB_POSTGRES_NAME = os.environ.get("DB_NAME")
DB_POSTGRES_USER = os.environ.get("DB_USER")
DB_POSTGRES_PASS = os.environ.get("DB_PASS")
DB_PORT_MONGO = os.environ.get("DB_PORT_MONGO")
DB_SECRET_AUTH = os.environ.get("AUTH_SECRET")

REDIS_HOST = os.environ.get("REDIS_HOST")

SECRET_KEY = os.environ.get("SECRET_KEY")
