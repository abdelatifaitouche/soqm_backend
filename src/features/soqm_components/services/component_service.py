from uuid import UUID
from src.core.exceptions import ValidationError, NotFoundError
from src.features.soqm_components.repositories.components_repository import (
    ComponentRepository,
)
from src.features.soqm_components.domain.component import (
    SOQMComponent,
    CreateComponent,
    UpdateComponent,
)
from src.features.soqm_components.domain.state_machine import transition
import logging

logger = logging.getLogger(__name__)


class ComponentService:
    def __init__(self, repo: ComponentRepository):
        self.repo: ComponentRepository = repo

    async def list(self) -> list[SOQMComponent]:
        logger.info("service listing")
        return await self.repo.list()

    async def get_by_id(self, entity_id: UUID) -> SOQMComponent:
        entity: SOQMComponent | None = await self.repo.get_by_id(entity_id)

        if not entity:
            raise NotFoundError(
                message=f"Entity with ID {entity_id} not Found",
            )

        return entity

    async def create(self, entity: CreateComponent) -> SOQMComponent:
        cps = await self.repo.list()

        if len(cps) >= 8:
            raise ValidationError(
                message="Cannot add SOQM Components",
            )

        return await self.repo.create(entity)

    async def update(self, entity_id: UUID, data: UpdateComponent):
        """
        NOTE:
            status transition is handled by the state_machine.transition(from, to)
                returns :
                    to : next_transition str
                raises :
                    InvalidStateTransition()
        """
        entity: SOQMComponent = await self.get_by_id(entity_id)

        if data.name:
            entity.name = data.name

        if data.isqm_reference:
            entity.isqm_reference = data.isqm_reference

        if data.status:
            entity.status = transition(entity.status, data.status)

        return await self.repo.update(entity)

    async def delete(self, entity_id: UUID):
        entity: SOQMComponent = await self.get_by_id(entity_id)
        if entity.status != "ARCHIVED":
            raise ValidationError(
                message="Cannot delete a component at this state {entity.status}"
            )

        await self.repo.delete(entity_id)
