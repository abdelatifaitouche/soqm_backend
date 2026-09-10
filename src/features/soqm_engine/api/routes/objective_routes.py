from fastapi import APIRouter, Depends
from uuid import UUID
from src.features.soqm_engine.application.usecases.objective_uc import ObjectiveUC
from src.features.soqm_engine.api.dependencies.objective_deps import (
    get_objective_uc,
    get_queries,
)
from src.features.soqm_engine.api.commands.writes.objective_writes import (
    CreateObjectiveRequest,
)
from src.features.soqm_engine.application.dtos.objective_dtos import CreateObjective
from src.features.soqm_engine.infra.queries import ObjectiveQueryService

router = APIRouter(prefix="/objectives", tags=["Quality Objectives"])


@router.get("")
async def list_objectives(
    queries: ObjectiveQueryService = Depends(get_queries),
):
    return await queries.list()


@router.get("/{objective_id}")
async def get_objective_details(
    objective_id: UUID, queries: ObjectiveQueryService = Depends(get_queries)
):
    return await queries.get_objective_details(objective_id)


@router.post("")
async def create_new_objective(
    data: CreateObjectiveRequest,
    uc: ObjectiveUC = Depends(get_objective_uc),
):
    return await uc.create(
        CreateObjective(
            description=data.description,
            review_date=data.review_date,
            component_id=data.component_id,
        ),
    )


@router.post("/{objective_id}/approve")
async def approve_objective(
    objective_id: UUID,
    uc: ObjectiveUC = Depends(get_objective_uc),
):
    return await uc.approve(
        objective_id,
    )
