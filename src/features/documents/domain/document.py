from dataclasses import dataclass
from uuid import UUID, uuid4
from src.features.documents.domain.exceptions import (
    FileNameErrorException,
    FileSizeErrorException,
)
from src.features.documents.domain.document_version import DocumentVersion
from src.features.documents.domain.enums import DocumentStatus, DocumentType


@dataclass
class Document:
    id: UUID
    title: str
    description: str
    document_type: str
    status: str
    current_version_id: UUID | None = None

    @classmethod
    def create(cls, *, title: str, description: str, document_type: str) -> "Document":
        doc = cls(
            id=uuid4(),
            title=title,
            description=description,
            document_type=document_type,
            status=DocumentStatus.ACTIVE.value,
        )
        return doc

    def update_version(self, version: DocumentVersion):
        """NEEDS SOME CHECKS BASED ON THE VERSION I GUESS"""
        self.current_version_id = version.id
