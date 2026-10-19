from pydantic import BaseModel
from src.features.findings.domain.enums import ActionState


class ActionFilters(BaseModel):
    status: ActionState | None = None
