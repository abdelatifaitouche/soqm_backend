from fastapi import APIRouter, Depends, status
from uuid import UUID
from .dependencies import get_uc, get_query_service
from src.features.soqm_components.application.usecases.component_usecases import (
    ComponentUC,
)
from src.features.soqm_components.infra.queries.component_query_service import (
    ComponentQueryService,
)
from .commands.write_commands import CreateComponentRequest, UpdateComponentRequest
from .commands.read_commands import ReadComponentDetails
from src.features.soqm_components.application.dtos.component_dto import (
    CreateComponentDTO,
    UpdateComponentDTO,
)


router = APIRouter(prefix="/components")


@router.get("/options", status_code=status.HTTP_200_OK)
async def list_options(
    queries: ComponentQueries = Depends(get_queries), creds=Depends(require_auth)
):
    options = await queries.list_options()
    return [ComponentOption.model_validate(opt) for opt in options]


@router.get("", status_code=status.HTTP_200_OK)
async def list(
    queries: ComponentQueries = Depends(get_queries),
    filters: ComponentFilters = Depends(),
    creds=Depends(require_auth),
):
    components = await queries.list(filters)
    return [BaseComponent.model_validate(cp) for cp in components]


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_component(
    data: CreateComponentRequest,
    uc: ComponentUC = Depends(get_uc),
):
    return await uc.create(
        data=CreateComponentDTO(
            name=data.name,
            description=data.description,
            isqm_reference=data.isqm_reference,
            display_order=data.display_order,
        )
    )


@router.get("/{component_id}", status_code=status.HTTP_200_OK)
async def get_component_details(
    component_id: UUID,
    query_service: ComponentQueryService = Depends(get_query_service),
):
    component = await query_service.get_component_details(
        component_id,
    )

    return ReadComponentDetails.model_validate(component)


@router.patch("/{component_id}/", status_code=status.HTTP_200_OK)
async def update(
    component_id: UUID,
    data: UpdateComponentRequest,
    uc: ComponentUC = Depends(get_uc),
):
    component = await uc.update(
        component_id,
        data=UpdateComponentDTO(
            name=data.name,
            description=data.description,
            isqm_reference=data.isqm_reference,
            display_order=data.display_order,
        ),
    )
    return ReadComponentDetails.model_validate(component)


@router.delete("/{component_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    component_id: UUID,
    service: ComponentUC = Depends(get_uc),
):
    await service.delete(component_id)


@router.patch("/{component_id}/activate/", status_code=status.HTTP_200_OK)
async def activate_component(
    component_id: UUID,
    uc: ComponentUC = Depends(get_uc),
):
    updated = await uc.activate_component(component_id)
    return ReadComponentDetails.model_validate(updated)


@router.patch("/{component_id}/deactivate/", status_code=status.HTTP_200_OK)
async def deactivate_component(
    component_id: UUID,
    uc: ComponentUC = Depends(get_uc),
):
    deactivated = await uc.deactivate_component(component_id)
    return ReadComponentDetails.model_validate(deactivated)


@router.patch("/{component_id}/archive/", status_code=status.HTTP_200_OK)
async def archive_component(
    component_id: UUID,
    uc: ComponentUC = Depends(get_uc),
):
    archived = await uc.archive_component(component_id)
    return ReadComponentDetails.model_validate(archived)
