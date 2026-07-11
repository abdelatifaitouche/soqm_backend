from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentFilters:
    status: str | None = None
    document_type: str | None = None
