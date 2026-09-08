from uuid import UUID
from fastapi import APIRouter, status, Depends
from src.features.soqm_engine.application.dtos.component_dtos import (
    CreateComponentDTO,
    UpdateComponentDTO,
)
from src.features.soqm_engine.api.commands.writes.component_writes import (
    CreateComponentRequest,
    UpdateComponentRequest,
)
from src.features.soqm_engine.api.commands.reads.component_reads import (
    ReadComponentDetails,
)
from src.features.soqm_engine.application.usecases.component_uc import ComponentUC
from src.features.soqm_engine.api.dependencies.component_deps import (
    get_component_uc,
    get_component_queries,
)
from src.features.soqm_engine.infra.queries.component_query_service import (
    ComponentQueryService,
)

router = APIRouter(prefix="/components", tags=["Soqm Components"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_component(
    data: CreateComponentRequest,
    uc: ComponentUC = Depends(get_component_uc),
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
    query_service: ComponentQueryService = Depends(get_component_queries),
):
    component = await query_service.get_component_details(
        component_id,
    )

    return ReadComponentDetails.model_validate(component)


@router.patch("/{component_id}/", status_code=status.HTTP_200_OK)
async def update(
    component_id: UUID,
    data: UpdateComponentRequest,
    uc: ComponentUC = Depends(get_component_uc),
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
    service: ComponentUC = Depends(get_component_uc),
):
    await service.delete(component_id)


@router.patch("/{component_id}/activate/", status_code=status.HTTP_200_OK)
async def activate_component(
    component_id: UUID,
    uc: ComponentUC = Depends(get_component_uc),
):
    updated = await uc.activate_component(component_id)
    return ReadComponentDetails.model_validate(updated)


@router.patch("/{component_id}/deactivate/", status_code=status.HTTP_200_OK)
async def deactivate_component(
    component_id: UUID,
    uc: ComponentUC = Depends(get_component_uc),
):
    deactivated = await uc.deactivate_component(component_id)
    return ReadComponentDetails.model_validate(deactivated)


@router.patch("/{component_id}/archive/", status_code=status.HTTP_200_OK)
async def archive_component(
    component_id: UUID,
    uc: ComponentUC = Depends(get_component_uc),
):
    archived = await uc.archive_component(component_id)
    return ReadComponentDetails.model_validate(archived)
