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


class ComponentService:
    def __init__(self, repo: ComponentRepository):
        self.repo: ComponentRepository = repo

    async def list(self) -> list[SOQMComponent]:
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

        return await self.repo.save(entity)

    def _change_state(self, entity: SOQMComponent, next_state: str) -> str:
        """
        Tranistion checking are handled by the state_machine.transition(from, to)
        """

        return transition(entity.status, next_state)

    async def update(self, entity_id: UUID, data: UpdateComponent):
        entity: SOQMComponent = await self.get_by_id(entity_id)

        if data.name:
            entity.name = data.name

        if data.isqm_reference:
            entity.isqm_reference = data.isqm_reference

        if data.status:
            entity.status = self._change_state(entity, data.status)

        return await self.repo.update(entity)

    async def delete(self, entity_id: UUID):
        entity: SOQMComponent | None = await self.repo.get_by_id(entity_id)

        if not entity:
            raise NotFoundError(
                message=f"Entity with ID: {entity_id} was not found",
            )

        await self.repo.delete(entity_id)
