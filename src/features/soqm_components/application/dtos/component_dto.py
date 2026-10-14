from dataclasses import dataclass
from uuid import UUID

# WRITE DTO


@dataclass(frozen=True)
class CreateComponentDTO:
    name: str
    description: str
    isqm_reference: str
    display_order: int


@dataclass(frozen=True)
class UpdateComponentDTO:
    name: str | None = None
    description: str | None = None
    isqm_reference: str | None = None
    display_order: int | None = None


# READ DTOS
@dataclass(frozen=True)
class SOQMComponentDetails:
    id: UUID
    name: str
    description: str
    isqm_reference: str
    status: str
    display_order: int


@dataclass(frozen=True)
class SOQMComponentList:
    id: UUID
    name: str
    status: str
    display_order: int
    isqm_reference: str


@dataclass(frozen=True)
class SOQMComponentOption:
    id: UUID
    name: str
