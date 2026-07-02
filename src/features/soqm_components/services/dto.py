from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class SOQMComponentBase:
    id: UUID
    name: str


@dataclass(frozen=True)
class SOQMComponentDetails(SOQMComponentBase):
    description: str
    isqm_reference: str
    status: str
    display_order: int


@dataclass(frozen=True)
class SOQMComponentList(SOQMComponentBase):
    status: str
    display_order: int
    isqm_reference: str


@dataclass(frozen=True)
class SOQMComponentOption(SOQMComponentBase):
    pass
