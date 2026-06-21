from fastapi import APIRouter, Depends, status
from src.infra.db.uow import get_db
from src.features.quality_objectives.dependencies import get_service
from src.features.quality_objectives.services.objective_service import ObjectiveService
from src.features.quality_objectives.mappers.objective_mapper import ObjectiveMapper
from src.features.quality_objectives.schemas.objective import (
    CreateObjective,
    ReadObjective,
    UpdateObjective,
)
from src.features.quality_objectives.domain.objective import Objective
from src.core.pagination import Pagination
from uuid import UUID

router = APIRouter(prefix="/objectives")


@router.get("", status_code=status.HTTP_200_OK)
async def list_objectives(
    pagination: Pagination = Depends(),
    service: ObjectiveService = Depends(get_service),
):
    objs: list[Objective] = await service.list(pagination)
    return [ReadObjective.model_validate(obj) for obj in objs]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_objective(
    data: CreateObjective,
    service: ObjectiveService = Depends(get_service),
):
    obj: Objective = await service.create(ObjectiveMapper.from_create(data))
    return ReadObjective.model_validate(obj)


@router.get("/{objective_id}", status_code=status.HTTP_200_OK)
async def get_by_id(
    objective_id: UUID,
    service: ObjectiveService = Depends(get_service),
):
    obj: Objective = await service.get_by_id(objective_id)
    return obj


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
    obj = await service.update(objective_id, ObjectiveMapper.from_update(data))
    return ReadObjective.model_validate(obj)


from src.features.risks.dependencies import get_service as get_risk_service
from src.features.risks.schemas.risk import ListRisk


@router.get("/{objective_id}/risks")
async def list_objective_risks(
    objective_id: UUID,
    service=Depends(get_risk_service),
):
    risks = await service.list_risks_by_objective(objective_id)
    return [ListRisk.model_validate(risk) for risk in risks]
