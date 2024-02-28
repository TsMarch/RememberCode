from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.database import url_connection_redis, get_async_session
from api.auth.security import oauth2_scheme, AccessToken
from api.auth.user_utils import get_user_by_id


async def delete_token(token):
    delete = await url_connection_redis.delete(token)
    await url_connection_redis.close()
    match delete:
        case 1:
            return True
        case _:
            return False


async def write_to_redis(key, value):
    await url_connection_redis.set(key, value, ex=180)
    await url_connection_redis.aclose()


async def get_from_redis(token: Annotated[str, Depends(oauth2_scheme)],
                         session: AsyncSession = Depends(get_async_session)):
    """
    This function decodes the token, then passing subjects uuid key to redis, and finally checks if tokens
    (value in redis) are equal.
    """
    decoded_data = await AccessToken.verify_access_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Bad token")
    check_token = await url_connection_redis.get(token)
    print(check_token)
    await url_connection_redis.aclose()
    if not check_token:
        raise HTTPException(status_code=401)
    user = await get_user_by_id(session, decoded_data["sub"])
    return user
