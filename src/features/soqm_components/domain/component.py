from dataclasses import dataclass
from uuid import UUID


@dataclass
class SOQMComponent:
    id: UUID
    name: str
    isqm_reference: str
