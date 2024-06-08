from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from api.databases_helper import RedisConnection, redis_helper, db_user_helper
from api.auth.security import oauth2_scheme, AccessToken
from api.auth.user_utils import get_user_by_id


async def delete_token(*args):
    token = args[1]
    match args[0]:
        case "refresh_token":
            result = await redis_helper.redis_connection(1).delete(token)
            if not result:
                await redis_helper.redis_connection(1).aclose()
                return {"status": "no such token"}
            await redis_helper.redis_connection(1).aclose()
            return {"status": "refresh_token deleted"}
        case "access_token":
            result = await RedisConnection.url_connection(2).delete(token)
            if not result:
                await RedisConnection.url_connection(2).aclose()
                return {"status": "no such token"}
            await RedisConnection.url_connection(2).aclose()
            return {"status": "token deleted"}
        case "all":
            await RedisConnection.url_connection(1).flushall()
            await RedisConnection.url_connection(1).aclose()
            return {"status": "deleted all tokens"}
        case _:
            return {"status": "нужно вставить тип токена который хочешь удалить (и сам токен). "
                              "Можно полностью дропнуть redis (all)"}


async def write_to_redis(**kwargs):
    for i in kwargs:
        match i:
            case "access_token":
                await RedisConnection.url_connection(2).set(kwargs[i][0], kwargs[i][1], ex=1800)
            case "refresh_token":
                await RedisConnection.url_connection(1).set(kwargs[i][0], kwargs[i][1], ex=2592000)
    await RedisConnection.url_connection(2).aclose()
    await RedisConnection.url_connection(1).aclose()


async def check_blacklist(token):
    check = await RedisConnection.url_connection(0).get(token)
    await RedisConnection.url_connection(0).aclose()
    if check:
        return True
    return False


async def get_from_redis(token: Annotated[str, Depends(oauth2_scheme)],
                         session: AsyncSession = Depends(db_user_helper.get_async_session)):
    """
    This function decodes the token, then passing subjects uuid key to redis, and finally checks if tokens
    (value in redis) are equal.
    """
    check_token_db = await RedisConnection.url_connection(2).exists(token)
    match check_token_db:
        case 1:
            user_id = await RedisConnection.url_connection(2).get(token)
            await RedisConnection.url_connection(2).aclose()
            user_data = await get_user_by_id(session, user_id)
            return user_data
        case 0:
            await RedisConnection.url_connection(2).aclose()
            return {"status": "no token in redis"}


async def get_new_token(token):
    decoded_data = await AccessToken.verify_access_token(token)
    check_token = await RedisConnection.url_connection(1).exists(token)
    if not check_token:
        await RedisConnection.url_connection(1).aclose()
        raise HTTPException(status_code=401)
    await RedisConnection.url_connection(1).aclose()
    await delete_token("refresh_token", token)
    new_acc_token = AccessToken.create_access_token(data={"sub": jsonable_encoder(decoded_data["sub"])})
    new_ref_token = AccessToken.create_refresh_token(data={"sub": jsonable_encoder(decoded_data["sub"])})
    await write_to_redis(refresh_token=[new_ref_token, jsonable_encoder(decoded_data["sub"])],
                         access_token=[new_acc_token, jsonable_encoder(decoded_data["sub"])])
    return {"access_token": new_acc_token, "refresh_token": new_ref_token, "token_type": "bearer",
            "access_token_expiration": datetime.utcnow()+timedelta(minutes=30),
            "refresh_token_expiration": datetime.utcnow()+timedelta(days=30)}
