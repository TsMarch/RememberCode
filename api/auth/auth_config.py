from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from api.config import SECRET_KEY as secret
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = secret
ALGORITHM = "HS256"

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

# Shows authentication status
@router.get("/auth_status/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
