from fastapi import APIRouter, status, Depends
from src.features.soqm_engine.api.commands.writes.risk_writes import CreateRisk
from src.features.soqm_engine.api.dependencies.risk_dependenices import get_risk_uc
from src.features.soqm_engine.application.usecases import RiskUC
from src.features.soqm_engine.application.dtos.risk_dtos import (
    CreateRisk as CreateRiskDTO,
)
from uuid import uuid4


router = APIRouter(prefix="/risks", tags=["Quality Risks"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_risk(
    data: CreateRisk,
    uc: RiskUC = Depends(get_risk_uc),
):

    risk = await uc.create_risk(uuid4(), CreateRiskDTO(**data.model_dump()))

    return risk
