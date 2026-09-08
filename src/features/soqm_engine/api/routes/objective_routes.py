from fastapi import APIRouter, Depends
from src.features.soqm_engine.application.usecases.objective_uc import ObjectiveUC
from src.features.soqm_engine.api.dependencies.objective_deps import get_objective_uc
from src.features.soqm_engine.api.commands.writes.objective_writes import (
    CreateObjectiveRequest,
)
from src.features.soqm_engine.application.dtos.objective_dtos import CreateObjective


router = APIRouter(prefix="/objectives", tags=["Quality Objectives"])


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
