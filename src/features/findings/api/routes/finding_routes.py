from fastapi import APIRouter

router = APIRouter(prefix="/finding")


@router.post("")
async def identify_finding():
    return "hello"
