import logging
from fastapi import APIRouter, Depends, status
from uuid import UUID
from src.features.soqm_components.dependencies import get_service
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

logger = logging.getLogger("app.soqm_component.routes")

router = APIRouter(prefix="/components")


@router.get("/options")
async def list_options(
    service: ComponentService = Depends(get_service),
):
    options = await service.list_options()
    return [ComponentOption.model_validate(opt) for opt in options]


@router.get("")
async def list(
    service=Depends(get_service),
    creds=Depends(require_permissions(ComponentPermissions.READ)),
):
    components = await service.list()
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
async def get_component_by_id(
    component_id: UUID,
    service: ComponentService = Depends(get_service),
    creds=Depends(
        require_permissions(
            ComponentPermissions.READ,
        ),
    ),
):
    component = await service.get_by_id(component_id)
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
