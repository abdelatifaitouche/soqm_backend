import uuid
from src.features.quality_objectives.domain.objective import (
    Objective,
)
from src.features.soqm_components.domain.component import SOQMComponent
from datetime import datetime, UTC
from src.features.quality_objectives.repository.objective_repository import (
    ObjectiveRepository,
)
from src.features.soqm_components.infra.repositories.component_repository import (
    ComponentRepository,
)
from src.core.exceptions import NotFoundError, ValidationError
from src.features.soqm_components.enums.soqm_component import ComponentState
from src.features.quality_objectives.enums.objective_states import ObjectiveState
from src.core.pagination import Pagination
from src.features.quality_objectives.filters.filters import ObjectiveFilters
from uuid import UUID
from src.features.quality_objectives.repository.component_objective_seq_repository import (
    ComponentObjectiveSeqRepository,
)
from src.features.quality_objectives.domain.objective_ref_generator import (
    ObjectiveRefGenerator,
)
from src.features.quality_objectives.schemas.objective import (
    CreateObjective,
    UpdateObjective,
)


class ObjectiveService:
    def __init__(self, obj_repo: ObjectiveRepository):
        self.repo: ObjectiveRepository = obj_repo
        self.component_repo: ComponentRepository = ComponentRepository(self.repo.db)
        self.seq_repo: ComponentObjectiveSeqRepository = (
            ComponentObjectiveSeqRepository(self.repo.db)
        )

    async def create(self, data: CreateObjective) -> Objective:
        component: SOQMComponent | None = await self.component_repo.get(
            data.component_id
        )
        if not component:
            raise NotFoundError(
                message=f"Component with {data.component_id} was not found",
            )
        if component.status in (
            ComponentState.ARCHIVED.value,
            ComponentState.IN_ACTIVE.value,
        ):
            raise ValidationError(
                message=f"Cannot add objective to component with state : {component.status}",
            )
        next_seq: int = await self.seq_repo.get_next_val(component.id)
        seq: str = ObjectiveRefGenerator.generate_objective_ref(
            component.display_order, next_seq
        )
        entity = Objective.create(
            description=data.description,
            review_date=data.review_date,
            objective_reference=seq,
            component_id=component.id,
        )

        return await self.repo.create(entity)

    async def get_by_id(self, entity_id: UUID):
        entity: Objective | None = await self.repo.get_by_id(entity_id)

        if not entity:
            raise NotFoundError(
                message=f"Objective with ID {entity_id} was not found",
            )

        return entity

    async def update(self, entity_id: UUID, data: UpdateObjective):
        entity: Objective = await self.get_by_id(entity_id)

        entity.update(
            data.description,
            data.review_date,
            data.component_id,
        )

        if data.status:
            entity = self._transition(entity, data.status)

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
