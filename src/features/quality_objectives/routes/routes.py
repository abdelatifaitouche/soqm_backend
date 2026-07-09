from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from src.infra.db.uow import get_db
from src.features.quality_objectives.dependencies import get_service, get_queries
from src.features.quality_objectives.services.objective_service import ObjectiveService
from src.features.quality_objectives.schemas.objective import (
    CreateObjective,
    ReadObjective,
    UpdateObjective,
    ObjectiveOption,
    PaginatedResponse,
)

from src.features.quality_objectives.domain.objective import Objective
from src.core.pagination import Pagination
from src.features.quality_objectives.filters.filters import ObjectiveFilters
from src.features.quality_objectives.repository.queries.objective_query_service import (
    ObjectiveQueries,
)

from uuid import UUID

router = APIRouter(prefix="/objectives")


@router.get("/options")
async def list_options(
    filters: ObjectiveFilters = Depends(),
    queries: ObjectiveQueries = Depends(get_queries),
):
    options = await queries.list_options(filters)
    return [ObjectiveOption.model_validate(opt) for opt in options]


@router.get("", status_code=status.HTTP_200_OK)
async def list_objectives(
    pagination: Pagination = Depends(),
    filters: ObjectiveFilters = Depends(),
    queries: ObjectiveQueries = Depends(get_queries),
):
    paginated_dto = await queries.list_objectives(pagination, filters)
    return PaginatedResponse.model_validate(paginated_dto)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_objective(
    data: CreateObjective,
    service: ObjectiveService = Depends(get_service),
):
    obj: Objective = await service.create(data)
    return ReadObjective.model_validate(obj)


@router.get("/{objective_id}", status_code=status.HTTP_200_OK)
async def get_by_id(
    objective_id: UUID,
    queries: ObjectiveQueries = Depends(get_queries),
):
    obj = await queries.get_objective_details(objective_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Objective not found",
        )
    return ReadObjective.model_validate(obj)


@router.delete("/{objective_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_objective(
    objective_id: UUID,
    service: ObjectiveService = Depends(get_service),
):
    await service.delete(objective_id)
    return


@router.patch("/{objective_id}/", status_code=status.HTTP_200_OK)
async def update(
    objective_id: UUID,
    data: UpdateObjective,
    service: ObjectiveService = Depends(get_service),
):
    obj = await service.update(objective_id, data)
    return ReadObjective.model_validate(obj)


"""
from src.features.risks.dependencies import get_service as get_risk_service
from src.features.risks.schemas.risk import ListRisk


@router.get("/{objective_id}/risks")
async def list_objective_risks(
    objective_id: UUID,
    service=Depends(get_risk_service),
):
    risks = await service.list_risks_by_objective(objective_id)
    return [ListRisk.model_validate(risk) for risk in risks]
"""
