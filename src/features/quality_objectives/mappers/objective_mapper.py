from src.features.quality_objectives.domain.objective import (
    Objective as ObjectiveEntity,
    UpdateObjective as UpdateDTO,
)
from src.features.quality_objectives.schemas.objective import (
    CreateObjective,
    UpdateObjective,
)
import uuid


class ObjectiveMapper:
    @staticmethod
    def from_create(data: CreateObjective):
        return ObjectiveEntity(
            id=uuid.uuid4(),
            objective_text=data.objective_text,
            description=data.description,
            review_date=data.review_date,
            component_id=data.component_id,
        )

    @staticmethod
    def from_update(data: UpdateObjective):
        return UpdateDTO(
            **data.model_dump(exclude_unset=True),
        )
