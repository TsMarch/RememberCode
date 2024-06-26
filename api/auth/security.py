from datetime import datetime, timedelta

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from api.auth import security_utils
from api.config import SECRET_KEY as SECRET

SECRET_KEY = SECRET
ALGORITHM = "HS256"


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/jwt/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password, hashed_password):
        return pwd_context.verify(password, hashed_password)


class TokenCreation:
    @staticmethod
    def create_access_token(data: dict):
        expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode = data.copy()
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict):
        expire = datetime.utcnow() + timedelta(days=30)
        to_encode = data.copy()
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


class TokenVerifier:
    @staticmethod
    async def verify_token(token_type: str = "access_token", **kwargs):
        try:
            print(kwargs['token'])
            decoded_data = jwt.decode(kwargs['token'], SECRET_KEY, algorithms=[ALGORITHM])
            current_time = int(datetime.utcnow().timestamp())
            return decoded_data
        except Exception as e:
            return None
