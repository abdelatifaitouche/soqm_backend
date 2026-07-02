from fastapi import APIRouter, Depends, status
from uuid import UUID
from src.features.risks.dependencies import get_service
from src.features.risks.schemas.risk import (
    CreateRisk,
    Risk,
    ListRisk,
    UpdateRisk,
    RiskOption,
)
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
    risks = await service.list(filters, options=False, pagination=pagination)
    return [ListRisk(**r) for r in risks]


@router.get("/options")
async def list_options(
    filters: RiskFilters = Depends(),
    service: RiskService = Depends(get_service),
    creds=Depends(require_auth),
):
    risks = await service.list(filters=filters, options=True)
    return [RiskOption.model_validate(opt) for opt in risks]


@router.get("/{risk_id}")
async def get_risk_by_id(
    risk_id: UUID,
    service: RiskService = Depends(get_service),
):
    risk = await service.get_risk_details(risk_id)
    return risk


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Risk)
async def create_risk(
    data: CreateRisk,
    service: RiskService = Depends(get_service),
    user=Depends(require_auth),
):

    risk: RiskEntity = await service.create_risk(user.get("sub"), data)
    return Risk.model_validate(risk)


@router.patch("/{risk_id}")
async def update(
    risk_id: UUID,
    data: UpdateRisk,
    user=Depends(require_auth),
    service: RiskService = Depends(get_service),
):
    updated_risk: RiskEntity = await service.update(user.get("sub"), risk_id, data)
    return Risk.model_validate(updated_risk)


@router.patch("/{risk_id}/assess")
async def assess_risk(
    risk_id: UUID,
    user=Depends(require_auth),
    service: RiskService = Depends(get_service),
):
    updated_risk: RiskEntity = await service.assess_risk(user.get("sub"), risk_id)
    return Risk.model_validate(updated_risk)


@router.patch("/{risk_id}/close")
async def close_risk(
    risk_id: UUID,
    user=Depends(require_auth),
    service: RiskService = Depends(get_service),
):
    updated_risk: RiskEntity = await service.close_risk(user.get("sub"), risk_id)
    return Risk.model_validate(updated_risk)
