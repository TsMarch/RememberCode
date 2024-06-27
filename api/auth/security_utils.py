from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.schemas import Token
from api.auth.security import TokenCreation, TokenVerifier, oauth2_scheme
from api.auth.user_utils import get_user_by_id
from api.configs.database import db_user_helper, redis_helper


async def get_pair_of_tokens(**kwargs) -> Token:
    if "refresh_token" in kwargs:
        decoded_data = await TokenVerifier.verify_token(token_type='refresh_token', token=kwargs['refresh_token'])
        check_token = await redis_helper.connection[1].exists(kwargs['refresh_token'])
        if not check_token:
            await redis_helper.connection[1].close()
            raise HTTPException(status_code=401)
        await redis_helper.connection[1].close()
        await delete_token("refresh_token", kwargs['refresh_token'])
        return await get_pair_of_tokens(user_id=decoded_data['sub'])
    access_token = TokenCreation.create_access_token(
        data={"sub": jsonable_encoder(kwargs["user_id"])}
    )
    refresh_token = TokenCreation.create_refresh_token(
        data={"sub": jsonable_encoder(kwargs["user_id"])}
    )
    await write_to_redis(
        refresh_token=[refresh_token, jsonable_encoder(kwargs["user_id"])],
        access_token=[access_token, jsonable_encoder(kwargs["user_id"])],
    )
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        access_token_expiration=datetime.utcnow() + timedelta(minutes=30),
        refresh_token_expiration=datetime.utcnow() + timedelta(days=30),
    )


async def delete_token(*args):
    token = args[1]
    match args[0]:
        case "refresh_token":
            result = await redis_helper.connection[1].delete(token)
            if not result:
                await redis_helper.connection[1].close()
                return {"status": "no such token"}
            await redis_helper.connection[1].close()
            return {"status": "refresh_token deleted"}
        case "access_token":
            result = await redis_helper.connection[2].delete(token)
            if not result:
                await redis_helper.connection[2].close()
                return {"status": "no such token"}
            await redis_helper.connection[2].close()
            return {"status": "token deleted"}
        case "all":
            await redis_helper.connection[1].flushall()
            await redis_helper.connection[1].close()
            return {"status": "deleted all tokens"}
        case _:
            return {
                "status": "нужно вставить тип токена который хочешь удалить (и сам токен). "
                "Можно полностью дропнуть redis (all)"
            }


async def write_to_redis(**kwargs):
    for i in kwargs:
        match i:
            case "access_token":
                print(kwargs[i][1])
               # await redis_helper.connection[2].rpush(
                #   kwargs[i][1], kwargs[i][0]
                #)
                await redis_helper.connection[2].set(
                    kwargs[i][0], kwargs[i][1], ex=1800
                )
            case "refresh_token":
                await redis_helper.connection[1].set(
                    kwargs[i][0], kwargs[i][1], ex=2592000
                )

    await redis_helper.connection[2].close()
    await redis_helper.connection[1].close()


async def check_blacklist(token):
    check = await redis_helper.connection[0].get(token)
    await redis_helper.connection[0].close()
    if check:
        return True
    return False


async def get_from_redis(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(db_user_helper.connection),
):
    print(await TokenVerifier.verify_token(token))
    check_token_db = await redis_helper.connection[2].exists(token)
    match check_token_db:
        case 1:
            user_id = await redis_helper.connection[2].get(token)
            await redis_helper.connection[2].aclose()
            user_data = await get_user_by_id(session, user_id)
            return user_data
        case 0:
            await redis_helper.connection[2].close()
            return {"status": "no token in redis"}
