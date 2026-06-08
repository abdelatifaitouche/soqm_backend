from src.infra.db.uow import get_db
from src.features.soqm_components.repositories.components_repository import (
    ComponentRepository,
)
from src.features.soqm_components.services.component_service import ComponentService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_service(db: AsyncSession = Depends(get_db)) -> ComponentService:
    repo: ComponentRepository = ComponentRepository(db)
    return ComponentService(repo)
