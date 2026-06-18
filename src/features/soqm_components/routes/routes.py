import logging
from fastapi import APIRouter, Depends, status
from uuid import UUID
from src.features.soqm_components.dependencies import get_service
from src.features.soqm_components.schemas.component import (
    BaseComponent,
    CreateComponent,
    UpdateComponent,
)
from src.features.auth.security.dependencies import require_permissions
from src.features.soqm_components.permissions.components_permissions import (
    ComponentPermissions,
)
from src.features.soqm_components.mappers.component_mapper import ComponentMapper
from src.features.soqm_components.services.component_service import ComponentService


logger = logging.getLogger("app.soqm_component.routes")

router = APIRouter(prefix="/components")


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
    cp = await service.create(ComponentMapper.from_create(data))
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
    return BaseComponent.model_validate(component)


@router.patch("/{component_id}/", status_code=status.HTTP_200_OK)
async def update(
    component_id: UUID,
    data: UpdateComponent,
    service: ComponentService = Depends(get_service),
    creds=Depends(
        require_permissions(ComponentPermissions.UPDATE),
    ),
):
    component = await service.update(
        component_id,
        ComponentMapper.from_update(data),
    )
    return BaseComponent.model_validate(component)


@router.delete("/{component_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    component_id: UUID,
    service: ComponentService = Depends(get_service),
    creds=Depends(
        require_permissions(ComponentPermissions.DELETE),
    ),
):
    await service.delete(component_id)
