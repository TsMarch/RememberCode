from fastapi import APIRouter

router = APIRouter(
    prefix="/service",
    responses={404: {"description": "Not found"}},
)


@router.get("/ping")
async def ping():
    return {"Success": True}
