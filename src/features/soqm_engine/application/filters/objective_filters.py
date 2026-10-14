from pydantic import BaseModel
from uuid import UUID
from src.features.soqm_engine.domain.enums.objective_state import ObjectiveState


class ObjectiveFilters(BaseModel):
    component_id: UUID | None = None
    status: ObjectiveState | None = None
