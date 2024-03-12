from json import dumps, loads
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.database import url_connection_redis, get_async_session, url_connection_redis_blacklist, \
    url_connection_redis_acc
from api.auth.security import oauth2_scheme, AccessToken
from api.auth.user_utils import get_user_by_id


async def delete_token(token):
    decoded_data = await AccessToken.verify_access_token(token)
    delete = await url_connection_redis.delete(token)
    await url_connection_redis.aclose()
    match delete:
        case 1:
            await url_connection_redis_blacklist.set(token, decoded_data["sub"])
            await url_connection_redis_blacklist.aclose()
            return {"Token status": "Blacklisted"}
        case _:
            return False


async def write_to_redis(*args):
    match args[0]:
        case "refresh_token":
            await url_connection_redis.set(args[1], args[2], ex=2592000)
        case "access_token":
            await url_connection_redis_acc.set(args[1], args[2], ex=1800)
    await url_connection_redis.aclose()


async def check_blacklist(token):
    check = await url_connection_redis_blacklist.get(token)
    await url_connection_redis_blacklist.aclose()
    if check:
        return True
    return False


async def get_from_redis(token: Annotated[str, Depends(oauth2_scheme)],
                         session: AsyncSession = Depends(get_async_session)):
    """
    This function decodes the token, then passing subjects uuid key to redis, and finally checks if tokens
    (value in redis) are equal.
    """
    check_token_db = await url_connection_redis_acc.exists(token)
    if not check_token_db:
        return {"status": "no such token"}

    user_id = await url_connection_redis_acc.get(token)
    await url_connection_redis_acc.aclose()

    user = await get_user_by_id(session, user_id)
    return user


async def get_new_token(token):
    """
    This function decodes the token, then passing subjects uuid key to redis, and finally checks if tokens
    (value in redis) are equal.
    """
    decoded_data = await AccessToken.verify_access_token(token)
    check_token = await url_connection_redis.get(token)
    await url_connection_redis.aclose()
    if not check_token:
        raise HTTPException(status_code=401)

    await delete_token(token)
    new_acc_token = AccessToken.create_access_token(data={"sub": jsonable_encoder(decoded_data["sub"])})
    new_ref_token = AccessToken.create_refresh_token(data={"sub": jsonable_encoder(decoded_data["sub"])})
    write_new_ref_token = await write_to_redis("refresh_token", new_ref_token, decoded_data["sub"])
    write_new_acc_token = await write_to_redis("access_token", new_acc_token, decoded_data["sub"])

    return {"access_token": new_acc_token, "refresh_token": new_ref_token}
