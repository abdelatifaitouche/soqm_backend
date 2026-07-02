import logging
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from uuid import UUID
from src.features.soqm_components.dependencies import get_service, get_queries
from src.features.soqm_components.schemas.component import (
    BaseComponent,
    CreateComponent,
    UpdateComponent,
    Component,
    ComponentOption,
)
from src.features.auth.security.dependencies import require_permissions
from src.features.soqm_components.permissions.components_permissions import (
    ComponentPermissions,
)
from src.features.soqm_components.services.component_service import ComponentService
from src.core.pagination import Pagination
from src.features.soqm_components.repositories.queries.component_query_service import (
    ComponentQueries,
)
from src.features.soqm_components.filters.filters import ComponentFilters

logger = logging.getLogger("app.soqm_component.routes")

router = APIRouter(prefix="/components")


@router.get("/options", status_code=status.HTTP_200_OK)
async def list_options(
    queries: ComponentQueries = Depends(get_queries),
):
    options = await queries.list_options()
    return [ComponentOption.model_validate(opt) for opt in options]


@router.get("", status_code=status.HTTP_200_OK)
async def list(
    queries: ComponentQueries = Depends(get_queries),
    filters: ComponentFilters = Depends(),
    creds=Depends(require_permissions(ComponentPermissions.READ)),
):
    components = await queries.list(filters)
    return [BaseComponent.model_validate(cp) for cp in components]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    data: CreateComponent,
    service: ComponentService = Depends(get_service),
    crds=Depends(require_permissions(ComponentPermissions.CREATE)),
):
    cp = await service.create(data)
    return BaseComponent.model_validate(cp)


@router.get("/{component_id}", status_code=status.HTTP_200_OK)
async def get_component_details(
    component_id: UUID,
    queries: ComponentQueries = Depends(get_queries),
    creds=Depends(
        require_permissions(
            ComponentPermissions.READ,
        ),
    ),
):
    component = await queries.get_component_details(component_id)

    if not component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Component Not Found",
        )

    return Component.model_validate(component)


@router.patch("/{component_id}/", status_code=status.HTTP_200_OK)
async def update(
    component_id: UUID,
    data: UpdateComponent,
    service: ComponentService = Depends(get_service),
    creds=Depends(
        require_permissions(ComponentPermissions.UPDATE),
    ),
):
    component = await service.update(component_id, data)
    return Component.model_validate(component)


@router.delete("/{component_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    component_id: UUID,
    service: ComponentService = Depends(get_service),
    creds=Depends(
        require_permissions(ComponentPermissions.DELETE),
    ),
):
    await service.delete(component_id)


@router.patch("/{component_id}/activate/", status_code=status.HTTP_200_OK)
async def activate_component(
    component_id: UUID,
    service: ComponentService = Depends(get_service),
):
    updated = await service.activate_component(component_id)
    return BaseComponent.model_validate(updated)


@router.patch("/{component_id}/deactivate/", status_code=status.HTTP_200_OK)
async def deactivate_component(
    component_id: UUID,
    service: ComponentService = Depends(get_service),
):
    deactivated = await service.deactivate_component(component_id)
    return BaseComponent.model_validate(deactivated)


@router.patch("/{component_id}/archive/", status_code=status.HTTP_200_OK)
async def archive_component(
    component_id: UUID,
    service: ComponentService = Depends(get_service),
):
    archived = await service.archive_component(component_id)
    return BaseComponent.model_validate(archived)


from src.features.quality_objectives.dependencies import get_service as get_obj_service
from src.features.quality_objectives.schemas.objective import ReadObjective


@router.get("/{component_id}/objectives")
async def list_objectives(
    component_id: UUID,
    service=Depends(get_obj_service),
    pagination: Pagination = Depends(),
):
    objectives = await service.list_objectives_by_component(component_id, pagination)
    return [ReadObjective.model_validate(obj) for obj in objectives]
