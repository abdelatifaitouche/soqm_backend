from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from src.api.deps.ordering import parse_ordering
from src.core.ordering import OrderBy
from src.core.pagination import Pagination
from src.features.auth.security.dependencies import require_auth
from src.features.soqm_engine.api.commands.writes.response_writes import (
    CreateRiskResponseRequest,
    UpdateResponseRequest,
    UpdateResponsesRisksRequest,
)
from src.features.soqm_engine.api.dependencies.response_deps import (
    get_response_queries,
    get_response_uc,
)
from src.features.soqm_engine.application.dtos.response_dtos import (
    CreateRiskResponse,
    UpdateRiskResponse,
)
from src.features.soqm_engine.application.filters.response_filters import (
    ResponseFilters,
)
from src.features.soqm_engine.application.usecases import ResponseUC
from src.features.soqm_engine.infra.queries import ResponseQueryService

router = APIRouter(prefix="/responses", tags=["Risk Responses"])


@router.post("")
async def create_response(
    response: CreateRiskResponseRequest,
    uc: ResponseUC = Depends(get_response_uc),
    user=Depends(require_auth),
):
    return await uc.create_response(
        user.get("sub"),
        CreateRiskResponse(**dict(response)),
    )


@router.get("")
async def list_responses(
    pagination: Pagination = Depends(),
    filters: ResponseFilters = Depends(),
    ordering: OrderBy = Depends(parse_ordering),
    queries: ResponseQueryService = Depends(get_response_queries),
    user=Depends(require_auth),
):
    return await queries.list(pagination, filters, ordering)


@router.get("/{response_id}")
async def get_response_details(
    response_id: UUID,
    queries: ResponseQueryService = Depends(get_response_queries),
    user=Depends(require_auth),
):
    response = await queries.get_response_details(response_id)

    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return response


@router.patch("/{response_id}")
async def update_response(
    response_id: UUID,
    data: UpdateResponseRequest,
    uc: ResponseUC = Depends(get_response_uc),
    user=Depends(require_auth),
):
    return await uc.update_response(
        response_id,
        UpdateRiskResponse(
            **dict(data),
        ),
    )


@router.post("/{response_id}/risks")
async def add_risk_response(
    response_id: UUID,
    risk: UpdateResponsesRisksRequest,
    uc: ResponseUC = Depends(get_response_uc),
    user=Depends(require_auth),
):
    return await uc.add_risk(
        response_id,
        risk_id=risk.risk_id,
    )


@router.delete("/{response_id}/risks")
async def remove_risk_response(
    response_id: UUID,
    risk: UpdateResponsesRisksRequest,
    uc: ResponseUC = Depends(get_response_uc),
    user=Depends(require_auth),
):
    return await uc.remove_risk(
        response_id,
        risk.risk_id,
    )
