from uuid import UUID

from pydantic import BaseModel

from src.features.quality_objectives.enums.objective_states import ObjectiveState


class ObjectiveFilters(BaseModel):
    component_id: UUID | None = None
    status: ObjectiveState | None = None
