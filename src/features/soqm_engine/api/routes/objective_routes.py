from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from uuid import UUID
from src.features.soqm_engine.application.usecases.objective_uc import ObjectiveUC
from src.features.soqm_engine.api.dependencies.objective_deps import (
    get_objective_uc,
    get_queries,
)
from src.features.soqm_engine.api.commands.writes.objective_writes import (
    CreateObjectiveRequest,
    UpdateObjectiveRequest,
)
from src.features.soqm_engine.application.dtos.objective_dtos import (
    CreateObjective,
    UpdateObjective,
)
from src.features.soqm_engine.infra.queries import ObjectiveQueryService
from src.features.soqm_engine.application.filters.objective_filters import (
    ObjectiveFilters,
)
from src.core.pagination import Pagination
from src.features.soqm_engine.api.commands.reads.objective_reads import (
    ReadObjective,
    ObjectiveList,
    PaginatedResponse,
    ObjectiveOption,
)
from src.features.auth.security.dependencies import require_auth


router = APIRouter(prefix="/objectives", tags=["Quality Objectives"])


@router.get("/options")
async def list_options(
    filters: ObjectiveFilters = Depends(),
    queries: ObjectiveQueryService = Depends(get_queries),
    user=Depends(require_auth),
):
    options = await queries.list_options()
    return [ObjectiveOption.model_validate(opt) for opt in options]


@router.get("")
async def list_objectives(
    pagination: Pagination = Depends(),
    filters: ObjectiveFilters = Depends(),
    queries: ObjectiveQueryService = Depends(get_queries),
    user=Depends(require_auth),
):
    objectives = await queries.list_objectives(pagination, filters)

    return PaginatedResponse.model_validate(objectives)


@router.get("/{objective_id}")
async def get_objective_details(
    objective_id: UUID,
    queries: ObjectiveQueryService = Depends(get_queries),
    user=Depends(require_auth),
):
    objective = await queries.get_objective_details(objective_id)
    if not objective:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Objective not found",
        )

    return ReadObjective.model_validate(objective)


@router.post("")
async def create_new_objective(
    data: CreateObjectiveRequest,
    uc: ObjectiveUC = Depends(get_objective_uc),
    user=Depends(require_auth),
):
    return await uc.create(
        CreateObjective(
            description=data.description,
            review_date=data.review_date,
            component_id=data.component_id,
        ),
    )


@router.patch("/{objective_id}")
async def update_objective(
    objective_id: UUID,
    data: UpdateObjectiveRequest,
    uc: ObjectiveUC = Depends(
        get_objective_uc,
    ),
    user=Depends(require_auth),
):
    return await uc.update_objective(
        objective_id,
        data=UpdateObjective(
            description=data.description,
            review_date=data.review_date,
            component_id=data.component_id,
        ),
    )


@router.post("/{objective_id}/approve")
async def approve_objective(
    objective_id: UUID,
    uc: ObjectiveUC = Depends(get_objective_uc),
    user=Depends(require_auth),
):
    return await uc.approve(
        objective_id,
    )
