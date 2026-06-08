from fastapi import APIRouter, Depends
from src.features.soqm_components.dependencies import get_service
from src.features.soqm_components.schemas.component import BaseComponent
from src.features.auth.security.dependencies import require_permissions
from src.features.soqm_components.permissions.components_permissions import (
    ComponentPermissions,
)

router = APIRouter(prefix="/components")


@router.get("")
async def list(
    service=Depends(get_service),
    creds=Depends(require_permissions(ComponentPermissions.READ)),
):
    components = await service.list()
    return [BaseComponent.model_validate(cp) for cp in components]
