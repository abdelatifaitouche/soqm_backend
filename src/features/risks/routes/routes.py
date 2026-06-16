from fastapi import APIRouter, Depends, status
from uuid import UUID
from src.features.risks.dependencies import get_service
from src.features.risks.schemas.risk import CreateRisk, Risk
from src.features.risks.services.risk_service import RiskService
from src.features.risks.mappers.risk_mapper import RiskMapper
from src.features.risks.domain.risk import Risk as RiskEntity

router = APIRouter(prefix="/risks")


@router.get("")
async def list_risks():
    return


@router.get("/{risk_id}")
async def get_risk_by_id(risk_id: UUID):
    return


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Risk)
async def create_risk(
    data: CreateRisk,
    service: RiskService = Depends(get_service),
):
    risk: RiskEntity = await service.create_risk(RiskMapper.from_create(data))
    return Risk.model_validate(risk)
