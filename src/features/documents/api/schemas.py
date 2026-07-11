from pydantic import BaseModel
from uuid import UUID


class DocumentFilters(BaseModel):
    status: str | None = None
    document_type: str | None = None


class CreateDocument(BaseModel):
    title: str
    description: str
    document_type: str


class ReadDocument(BaseModel):
    id: UUID
    title: str
    document_type: str
    current_version_id: UUID
    status: str
    description: str
    version: int
    model_config = {"from_attributes": True}


class PaginatedResponse(BaseModel):
    total: int
    size: int
    page: int
    items: list[ReadDocument]

    model_config = {
        "from_attributes": True,
    }
