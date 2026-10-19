from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.core.pagination import Pagination
from src.features.auth.security.dependencies import require_auth
from src.features.soqm_engine.api.commands.reads.component_reads import (
    ReadComponentDetails,
)
from src.features.soqm_engine.api.commands.writes.component_writes import (
    CreateComponentRequest,
    UpdateComponentRequest,
)
from src.features.soqm_engine.api.dependencies.component_deps import (
    get_component_queries,
    get_component_uc,
)
from src.features.soqm_engine.application.dtos.component_dtos import (
    CreateComponentDTO,
    UpdateComponentDTO,
)
from src.features.soqm_engine.application.filters.component_filters import (
    ComponentFilters,
)
from src.features.soqm_engine.application.usecases.component_uc import ComponentUC
from src.features.soqm_engine.infra.queries.component_query_service import (
    ComponentQueryService,
)

router = APIRouter(prefix="/components", tags=["Soqm Components"])


@router.get("")
async def list_components(
    user=Depends(require_auth),
    pagination: Pagination = Depends(),
    filters: ComponentFilters = Depends(),
    queries: ComponentQueryService = Depends(get_component_queries),
):
    return await queries.list(pagination, filters)


@router.get("/options")
async def list_options(
    user=Depends(require_auth),
    queries: ComponentQueryService = Depends(get_component_queries),
):
    return await queries.list_options()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_component(
    data: CreateComponentRequest,
    user=Depends(require_auth),
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
    user=Depends(require_auth),
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
    user=Depends(require_auth),
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
    user=Depends(require_auth),
):
    await service.delete(component_id)


@router.patch("/{component_id}/activate/", status_code=status.HTTP_200_OK)
async def activate_component(
    component_id: UUID,
    uc: ComponentUC = Depends(get_component_uc),
    user=Depends(require_auth),
):
    updated = await uc.activate_component(component_id)
    return ReadComponentDetails.model_validate(updated)


@router.patch("/{component_id}/deactivate/", status_code=status.HTTP_200_OK)
async def deactivate_component(
    component_id: UUID,
    uc: ComponentUC = Depends(get_component_uc),
    user=Depends(require_auth),
):
    deactivated = await uc.deactivate_component(component_id)
    return ReadComponentDetails.model_validate(deactivated)


@router.patch("/{component_id}/archive/", status_code=status.HTTP_200_OK)
async def archive_component(
    component_id: UUID,
    uc: ComponentUC = Depends(get_component_uc),
    user=Depends(require_auth),
):
    archived = await uc.archive_component(component_id)
    return ReadComponentDetails.model_validate(archived)
