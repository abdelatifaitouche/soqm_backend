from uuid import UUID
from src.core.exceptions import NotFoundError, ValidationError
from src.core.shared.interfaces.unit_of_work import IUnitOfWork
from src.features.soqm_engine.domain.entities.component import SOQMComponent
from src.features.soqm_engine.domain.enums.component_state import ComponentState
from src.features.soqm_engine.application.dtos.component_dtos import (
    CreateComponentDTO,
    UpdateComponentDTO,
)
from src.features.soqm_engine.application.ports.icomponent_repo import (
    IComponentRepository,
)


class ComponentUC:
    def __init__(
        self,
        uow: IUnitOfWork,
        component_repo: IComponentRepository,
    ):
        self.uow = uow
        self.component_repo = component_repo

    async def create(self, data: CreateComponentDTO) -> SOQMComponent:
        async with self.uow:
            entity: SOQMComponent = SOQMComponent.create(
                name=data.name,
                isqm_reference=data.isqm_reference,
                display_order=data.display_order,
                description=data.description,
            )

            await self.component_repo.save(entity)

        return entity

    async def get_by_id(self, entity_id: UUID) -> SOQMComponent:
        entity: SOQMComponent | None = await self.component_repo.get(entity_id)

        if not entity:
            raise NotFoundError(
                message=f"Entity with ID {entity_id} not Found",
            )

        return entity

    async def update(self, entity_id: UUID, data: UpdateComponentDTO):
        async with self.uow:
            entity: SOQMComponent = await self.get_by_id(entity_id)

            entity.update_details(
                name=data.name,
                order=data.display_order,
                reference=data.isqm_reference,
                description=data.description,
            )
            await self.component_repo.save(entity)

        return entity

    async def deactivate_component(self, entity_id: UUID):
        """
        THERE MIGHT BE TOO MUCH REPITIION BETWEEN THESE THREE FUNCTIONS ,
        I chose readability over abstraction here
        """
        async with self.uow:
            entity: SOQMComponent = await self.get_by_id(entity_id)
            entity.deactivate()
            await self.component_repo.save(entity)
        return entity

    async def activate_component(self, entity_id: UUID):
        async with self.uow:
            entity: SOQMComponent = await self.get_by_id(entity_id)
            entity.activate()
            await self.component_repo.save(entity)
        return entity

    async def archive_component(self, entity_id: UUID):
        async with self.uow:
            entity: SOQMComponent = await self.get_by_id(entity_id)
            entity.archive()
            await self.component_repo.save(entity)
        return entity

    async def delete(self, entity_id: UUID):
        """
        this may needs to be inside the domain if it has its business logic,
        Dont forget to wrap this in the unit of work
        """
        entity: SOQMComponent = await self.get_by_id(entity_id)
        if entity.get_status() != ComponentState.ARCHIVED.value:
            raise ValidationError(
                message="Cannot delete a component at this state {entity.status}"
            )

        await self.component_repo.delete(entity_id)
