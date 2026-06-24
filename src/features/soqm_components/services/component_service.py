from uuid import UUID
from src.core.exceptions import ValidationError, NotFoundError
from src.features.soqm_components.repositories.components_repository import (
    ComponentRepository,
)
from src.features.soqm_components.domain.component import (
    SOQMComponent,
)
from src.features.soqm_components.schemas.component import (
    CreateComponent,
    UpdateComponent,
)
from src.features.soqm_components.domain.state_machine import transition
from src.features.soqm_components.enums.soqm_component import ComponentState
import logging

logger = logging.getLogger(__name__)


class ComponentService:
    def __init__(self, repo: ComponentRepository):
        self.repo: ComponentRepository = repo

    async def list(self) -> list[SOQMComponent]:
        logger.info("service listing")
        return await self.repo.list()

    async def list_options(self):
        return await self.repo.list_options()

    async def get_by_id(self, entity_id: UUID) -> SOQMComponent:
        entity: SOQMComponent | None = await self.repo.get_by_id(entity_id)

        if not entity:
            raise NotFoundError(
                message=f"Entity with ID {entity_id} not Found",
            )

        return entity

    async def create(self, data: CreateComponent) -> SOQMComponent:
        cps = await self.repo.list()

        if len(cps) >= 8:
            raise ValidationError(
                message="Cannot add SOQM Components",
            )

        entity: SOQMComponent = SOQMComponent.create(
            name=data.name,
            isqm_reference=data.isqm_reference,
            display_order=data.display_order,
            description=data.description,
        )

        return await self.repo.create(entity)

    async def update(self, entity_id: UUID, data: UpdateComponent):
        entity: SOQMComponent = await self.get_by_id(entity_id)

        entity.update(
            name=data.name,
            display_order=data.display_order,
            description=data.description,
            isqm_reference=data.isqm_reference,
        )

        return await self.repo.update(entity)

    async def deactivate_component(self, entity_id: UUID):
        """
        THERE MIGHT BE TOO MUCH REPITIION BETWEEN THESE THREE FUNCTIONS ,
        I chose readability over abstraction here
        """
        entity: SOQMComponent = await self.get_by_id(entity_id)
        entity.deactivate()
        return await self.repo.update(entity)

    async def activate_component(self, entity_id: UUID):
        entity: SOQMComponent = await self.get_by_id(entity_id)
        entity.activate()
        return await self.repo.update(entity)

    async def archive_component(self, entity_id: UUID):
        entity: SOQMComponent = await self.get_by_id(entity_id)
        entity.archive()
        return await self.repo.update(entity)

    async def delete(self, entity_id: UUID):
        entity: SOQMComponent = await self.get_by_id(entity_id)
        if entity.get_status() != ComponentState.ARCHIVED.value:
            raise ValidationError(
                message="Cannot delete a component at this state {entity.status}"
            )

        await self.repo.delete(entity_id)
