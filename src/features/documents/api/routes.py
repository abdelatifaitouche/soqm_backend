from fastapi import APIRouter


router = APIRouter(prefix="/documents")


@router.get("")
async def home():
    return "hello docs"
