from fastapi import APIRouter
from uuid import UUID

router = APIRouter(prefix="/risks")


@router.get("")
async def list_risks():
    return


@router.get("/{risk_id}")
async def get_risk_by_id(risk_id: UUID):
    return


@router.post("")
async def create_risk():
    return
