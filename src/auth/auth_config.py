from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Shows authentication status
@router.get("/auth_status/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
