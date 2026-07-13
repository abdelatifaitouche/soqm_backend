from fastapi import APIRouter, Depends, status
from uuid import UUID
from src.features.risks.dependencies import get_service, get_queries
from src.features.risks.schemas.risk import (
    CreateRisk,
    Risk,
    ListRisk,
    UpdateRisk,
    RiskOption,
    PaginatedResponse,
)
from src.features.risks.services.risk_service import RiskService
from src.features.risks.mappers.risk_mapper import RiskMapper
from src.features.risks.domain.risk import Risk as RiskEntity
from src.core.pagination import Pagination
from src.features.risks.filters.risk_filters import RiskFilters
from src.features.auth.security.dependencies import require_auth
from src.features.risks.repositories.queries.risk_query_service import RiskQueryService
from src.core.ordering import OrderBy
from src.api.deps.ordering import parse_ordering
import logging


logger = logging.getLogger(__name__)


router = APIRouter(prefix="/risks")


@router.get("")
async def list_risks(
    pagination: Pagination = Depends(),
    filters: RiskFilters = Depends(),
    order: OrderBy = Depends(parse_ordering),
    queries: RiskQueryService = Depends(get_queries),
    user=Depends(require_auth),
):
    risks = await queries.list(pagination, filters, order)
    return PaginatedResponse.model_validate(risks)


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
    queries: RiskQueryService = Depends(get_queries),
):
    risk = await queries.get_risk_details(risk_id)
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


@router.get("/matrix/summary")
async def get_risk_matrix(
    queries: RiskQueryService = Depends(get_queries),
):
    matrix = await queries.get_risk_matrix_summary()
    return matrix


@router.get("/{response_id}/list")
async def list_response_risks(
    response_id: UUID,
    pagination: Pagination = Depends(),
    filters: RiskFilters = Depends(),
    queries: RiskQueryService = Depends(get_queries),
):
    risks = await queries.get_response_risks(response_id, filters)
    return [ListRisk.model_validate(risk) for risk in risks]


@router.get("/objective/{objective_id}/risks")
async def list_objective_risks(
    objective_id: UUID,
    pagination: Pagination = Depends(),
    filters: RiskFilters = Depends(),
    order: OrderBy = Depends(
        parse_ordering,
    ),
    queries: RiskQueryService = Depends(get_queries),
):
    risks = await queries.list_by_objective(objective_id, pagination, filters, order)
    return PaginatedResponse.model_validate(risks)


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
