from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RcaCategory:
    id: UUID
    category: str
