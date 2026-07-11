from fastapi import APIRouter, Depends
from src.infra.db.uow import get_db
from src.features.auth.security.dependencies import require_auth, require_permissions
from uuid import UUID
from src.features.risks.services.response_service import ResponseService
from src.core.pagination import Pagination
from src.features.risks.schemas.risk_response import (
    RiskSummary,
    Response,
    RiskResponse,
    CreateRiskResponse,
    PaginatedResponse,
)
from src.features.risks.filters.response_filters import ResponseFilters
from src.features.risks.routes.response_deps import get_service, get_queries
from src.features.risks.repositories.queries.response_query_service import (
    ResponseQueryService,
)
from src.api.deps.ordering import parse_ordering
from src.core.ordering import OrderBy

router = APIRouter(prefix="/responses")


@router.get("")
async def list(
    pagination: Pagination = Depends(),
    filters: ResponseFilters = Depends(),
    order: OrderBy = Depends(parse_ordering),
    user=Depends(require_auth),
    queries: ResponseQueryService = Depends(get_queries),
):
    responses = await queries.list(pagination, filters, order)

    return PaginatedResponse.model_validate(responses)


@router.post("/")
async def create_response(
    data: CreateRiskResponse,
    user=Depends(require_auth),
    service: ResponseService = Depends(get_service),
):
    response = await service.create_response(user.get("sub"), data)
    return RiskResponse.model_validate(response)


@router.get("/{response_id}")
async def get_by_id(
    response_id: UUID,
    creds=Depends(require_auth),
    queries: ResponseQueryService = Depends(get_queries),
):
    response = await queries.get_response_details(response_id)
    return response
