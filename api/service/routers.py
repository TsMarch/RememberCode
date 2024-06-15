from typing import Annotated

from fastapi import APIRouter, Header, Query

from api.auth import security_utils

router = APIRouter(
    prefix="/service",
    responses={404: {"description": "Not found"}},
)


@router.post("/delete/redis", response_model=dict)
async def delete_token(
    type_of_token: str = Query(
        None, description="access_token or refresh_token or all"
    ),
    token: Annotated[str | None, Header()] = None,
):
    result = await security_utils.delete_token(type_of_token, token)
    return result
