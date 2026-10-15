from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import Response

from src.api.deps.ordering import parse_ordering
from src.core.ordering import OrderBy
from src.core.pagination import Pagination
from src.features.auth.security.dependencies import require_auth
from src.features.soqm_engine.api.commands.writes.risk_writes import (
    CreateRisk,
    UpdateRiskObjectiveRequest,
    UpdateRiskRequest,
    UpdateRiskResponseRequest,
)
from src.features.soqm_engine.api.dependencies.risk_dependenices import (
    get_risk_matrix_query,
    get_risk_queries,
    get_risk_uc,
)
from src.features.soqm_engine.application.dtos.risk_dtos import (
    CreateRisk as CreateRiskDTO,
)
from src.features.soqm_engine.application.dtos.risk_dtos import (
    RiskUpdate as RiskUpdateDTO,
)
from src.features.soqm_engine.application.filters.risk_filters import RiskFilters
from src.features.soqm_engine.application.usecases import RiskUC
from src.features.soqm_engine.infra.queries import RiskMatrixQuery, RiskQueryService

router = APIRouter(prefix="/risks", tags=["Quality Risks"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_risk(
    data: CreateRisk,
    uc: RiskUC = Depends(get_risk_uc),
    user=Depends(require_auth),
):

    risk = await uc.create_risk(user.get("sub"), CreateRiskDTO(**data.model_dump()))

    return risk


@router.get("")
async def list_risks(
    pagination: Pagination = Depends(),
    filters: RiskFilters = Depends(),
    order: OrderBy = Depends(parse_ordering),
    queries: RiskQueryService = Depends(get_risk_queries),
    user=Depends(require_auth),
):
    return await queries.list(pagination, filters, order)


@router.get("/{risk_id}")
async def get_risk_details(
    risk_id: UUID,
    queries: RiskQueryService = Depends(get_risk_queries),
    user=Depends(require_auth),
):
    risk = await queries.get_risk_details(risk_id)

    if not risk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return risk


@router.patch("/{risk_id}")
async def update_risk(
    risk_id: UUID,
    data: UpdateRiskRequest,
    uc: RiskUC = Depends(get_risk_uc),
    user=Depends(require_auth),
):
    return await uc.update_risk(
        risk_id,
        RiskUpdateDTO(**dict(data)),
    )


@router.post("/{risk_id}/objectives", status_code=status.HTTP_200_OK)
async def add_objective_to_risk(
    risk_id: UUID,
    objective: UpdateRiskObjectiveRequest,
    uc: RiskUC = Depends(get_risk_uc),
    user=Depends(require_auth),
):
    return await uc.add_objective(
        risk_id,
        objective.objective_id,
    )


@router.delete("/{risk_id}/objectives", status_code=204)
async def remove_objective_to_risk(
    risk_id: UUID,
    objective: UpdateRiskObjectiveRequest,
    uc: RiskUC = Depends(get_risk_uc),
    user=Depends(require_auth),
):
    await uc.remove_objective(
        risk_id,
        objective.objective_id,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{risk_id}/responses", status_code=status.HTTP_200_OK)
async def add_risk_response(
    risk_id: UUID,
    response_id: UpdateRiskResponseRequest,
    uc: RiskUC = Depends(get_risk_uc),
    user=Depends(require_auth),
):
    return await uc.add_response(risk_id, response_id.response_id)


@router.delete("/{risk_id}/responses", status_code=status.HTTP_204_NO_CONTENT)
async def remove_risk_response(
    risk_id: UUID,
    response_id: UpdateRiskResponseRequest,
    uc: RiskUC = Depends(get_risk_uc),
    user=Depends(require_auth),
):
    await uc.remove_response(risk_id, response_id.response_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/matrix/summary", status_code=status.HTTP_200_OK)
async def get_risk_matrix(
    filters: RiskFilters = Depends(),
    queries: RiskMatrixQuery = Depends(get_risk_matrix_query),
    user=Depends(require_auth),
):
    matrix = await queries.query(filters)
    return matrix
