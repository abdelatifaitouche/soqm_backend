import uuid
from src.features.quality_objectives.domain.objective import (
    Objective,
    UpdateObjective as UpdateDTO,
)
from src.features.soqm_components.domain.component import SOQMComponent
from datetime import datetime, UTC
from src.features.quality_objectives.repository.objective_repository import (
    ObjectiveRepository,
)
from src.features.soqm_components.repositories.components_repository import (
    ComponentRepository,
)
from src.core.exceptions import NotFoundError, ValidationError
from src.features.soqm_components.enums.soqm_component import ComponentState
from src.features.quality_objectives.enums.objective_states import ObjectiveState
from src.core.pagination import Pagination
from src.features.quality_objectives.filters.filters import ObjectiveFilters
from uuid import UUID


class ObjectiveService:
    def __init__(self, obj_repo: ObjectiveRepository):
        self.repo: ObjectiveRepository = obj_repo
        self.component_repo: ComponentRepository = ComponentRepository(self.repo.db)

    async def create(self, entity: Objective) -> Objective:

        component: SOQMComponent | None = await self.component_repo.get_by_id(
            entity.component_id
        )

        if not component:
            raise NotFoundError(
                message=f"Component with {entity.component_id} was not found",
            )

        if component.status in (
            ComponentState.ARCHIVED.value,
            ComponentState.IN_ACTIVE.value,
        ):
            raise ValidationError(
                message=f"Cannot add objective to component with state : {component.status}",
            )

        if entity.review_date <= datetime.now():
            raise ValidationError(
                message="Invalid review date",
            )

        return await self.repo.create(entity)

    async def list_options(self, filters: ObjectiveFilters):
        return await self.repo.list_options(filters)

    async def list(self, pagination: Pagination) -> list[Objective]:
        return await self.repo.list(pagination)

    async def get_by_id(self, entity_id: UUID):
        entity: Objective | None = await self.repo.get_by_id(entity_id)

        if not entity:
            raise NotFoundError(
                message=f"Objective with ID {entity_id} was not found",
            )

        return entity

    async def update(self, entity_id: UUID, data: UpdateDTO):
        """
        For now we are handling the state transitions inside the self._transition()
        update later to handle each transition inside its own methods/usecase once we define the whole workflow
        """
        entity: Objective = await self.get_by_id(entity_id)

        if data.objective_text:
            if entity.status != "draft":
                raise ValidationError("Cannot update non draft")
            entity.objective_text = data.objective_text

        if data.component_id:
            if entity.status != "draft":
                raise ValidationError("")
            component: SOQMComponent | None = await self.component_repo.get_by_id(
                data.component_id
            )

            if not component:
                raise NotFoundError(
                    message=f"Assigned SOQM component does not exists",
                    details={"component_id": data.component_id},
                )

            entity.component_id = data.component_id

        if data.description:
            if entity.status != "draft":
                raise ValidationError("Cannot update non draft")
            entity.description = data.description

        if data.review_date:
            if data.review_date <= datetime.now():
                raise ValidationError(
                    "Invalid review date",
                    details={
                        "review_date": data.review_date,
                    },
                )
            entity.review_date = data.review_date
        if data.status:
            entity = self._transition(entity, data.status)

        entity.updated_at = datetime.now()
        return await self.repo.update(entity)

    def _transition(self, entity: Objective, next_state: str) -> Objective:
        match next_state:
            case "approved":
                entity: Objective = entity.approve()
            case "active":
                entity: Objective = entity.activate()
            case "suspended":
                entity: Objective = entity.suspend()
            case "resume":
                entity: Objective = entity.resume()
            case "archived":
                entity: Objective = entity.archive()

        return entity

    async def delete(self, entity_id: UUID):
        entity: Objective = await self.get_by_id(entity_id)

        if entity.status != "draft":
            raise ValidationError(
                message="Cannot delete non draft objectives, transition to archive",
            )

        await self.repo.delete(entity_id)

    async def list_objectives_by_component(
        self, component_id: UUID, pagination: Pagination
    ):
        # first check for the existance of the component

        return await self.repo.list_by_component(component_id, pagination)
