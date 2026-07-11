from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class DocumentRead:
    id: UUID
    title: str
    current_version_id: UUID
    description: str
    status: str
    document_type: str
    version: int


@dataclass(frozen=True)
class PaginatedResponse:
    total: int
    size: int
    page: int

    items: list[DocumentRead]
