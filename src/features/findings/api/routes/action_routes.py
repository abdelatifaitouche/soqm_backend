from fastapi import APIRouter, Depends, status, HTTPException
from src.features.findings.api.commands.action_writes import (
    CreateActionRequest,
    UpdateActionRequest,
)
from src.features.findings.application.dtos import CreateAction, UpdateAction
from uuid import UUID
from src.features.findings.api.dependencies.action_deps import (
    get_action_uc,
    get_action_queries,
)
from src.features.findings.application.usecases import ActionUC
from src.features.findings.infra.queries import ActionQueryService
from src.core.pagination import Pagination
from src.features.findings.application.filters import ActionFilters


router = APIRouter(tags=["Actions"])


@router.post("/finding/{finding_id}/actions")
async def create_action(
    finding_id: UUID,
    action_request: CreateActionRequest,
    uc: ActionUC = Depends(get_action_uc),
):
    return await uc.create_action(
        CreateAction(
            title=action_request.title,
            finding_id=finding_id,
            estimated_completion_date=action_request.estimated_completion_date,
        )
    )


@router.get("/finding/{finding_id}/actions")
async def list_finding_actions(
    finding_id: UUID,
    pagination: Pagination = Depends(),
    filters: ActionFilters = Depends(),
    queries: ActionQueryService = Depends(get_action_queries),
):
    return await queries.list(pagination, filters, finding_id)


@router.get("/action")
async def list_actions(
    pagination: Pagination = Depends(),
    filters: ActionFilters = Depends(),
    queries: ActionQueryService = Depends(get_action_queries),
):
    return await queries.list(pagination, filters, None)


@router.get("/action/{action_id}", status_code=status.HTTP_200_OK)
async def get_action_details(
    action_id: UUID, queries: ActionQueryService = Depends(get_action_queries)
):
    return await queries.get_action_details(action_id)


@router.patch("/action/{action_id}", status_code=status.HTTP_200_OK)
async def update_action(
    action_id: UUID,
    update_request: UpdateActionRequest,
    uc: ActionUC = Depends(get_action_uc),
):
    return await uc.update_action(
        action_id,
        UpdateAction(
            title=update_request.title,
            finding_id=update_request.finding_id,
            estimated_completion_date=update_request.estimated_completion_date,
        ),
    )


@router.post("/action/{action_id}/start", status_code=status.HTTP_200_OK)
async def start_action(
    action_id: UUID,
    uc: ActionUC = Depends(get_action_uc),
):
    return await uc.start_action(action_id)


@router.post("/action/{action_id}/complete", status_code=status.HTTP_200_OK)
async def mark_action_complete(
    action_id: UUID,
    uc: ActionUC = Depends(get_action_uc),
):
    return await uc.complete_action(action_id)
