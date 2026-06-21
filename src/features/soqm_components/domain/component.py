from dataclasses import dataclass
from uuid import UUID
from src.features.quality_objectives.domain.objective import Objective


@dataclass
class CreateComponent:
    name: str
    isqm_reference: str
    description: str
    display_order: int


@dataclass
class SOQMComponent:
    id: UUID
    name: str
    isqm_reference: str
    status: str
    display_order: int
    description: str | None = None


@dataclass
class UpdateComponent:
    name: str | None = None
    status: str | None = None
    isqm_reference: str | None = None
    description: str | None = None
