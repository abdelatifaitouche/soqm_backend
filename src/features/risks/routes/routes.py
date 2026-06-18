from fastapi import APIRouter, Depends, status
from uuid import UUID
from src.features.risks.dependencies import get_service
from src.features.risks.schemas.risk import CreateRisk, Risk, ListRisk
from src.features.risks.services.risk_service import RiskService
from src.features.risks.mappers.risk_mapper import RiskMapper
from src.features.risks.domain.risk import Risk as RiskEntity
from src.core.pagination import Pagination
from src.features.risks.filters.risk_filters import RiskFilters
from src.features.auth.security.dependencies import require_auth
import logging


logger = logging.getLogger(__name__)


router = APIRouter(prefix="/risks")


@router.get("")
async def list_risks(
    pagination: Pagination = Depends(),
    filters: RiskFilters = Depends(),
    service: RiskService = Depends(get_service),
    user=Depends(require_auth),
):
    logger.debug(user.get("sub"))
    risks = await service.list(pagination, filters)
    return [ListRisk(**r) for r in risks]


@router.get("/{risk_id}")
async def get_risk_by_id(
    risk_id: UUID,
    service: RiskService = Depends(get_service),
):
    risk = await service.get_risk_by_id(risk_id)
    return Risk.model_validate(risk)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Risk)
async def create_risk(
    data: CreateRisk,
    service: RiskService = Depends(get_service),
    user=Depends(require_auth),
):

    risk: RiskEntity = await service.create_risk(RiskMapper.from_create(data))
    return Risk.model_validate(risk)
