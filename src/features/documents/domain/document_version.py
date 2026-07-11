from uuid import UUID, uuid4
from dataclasses import dataclass
from src.features.documents.domain.enums import DocumentProcessingStatus


@dataclass(frozen=True)
class DocumentVersion:
    id: UUID
    document_id: UUID
    version: int
    filename: str
    content_type: str
    size_bytes: int
    processing_status: str = DocumentProcessingStatus.UPLOADING.value

    @classmethod
    def create(
        cls,
        *,
        document_id: UUID,
        version: int,
        filename: str,
        content_type: str,
        size_bytes: int,
    ) -> "DocumentVersion":
        """
        NEEDS VALIDAATION ON CONTENT TYPE (PDF,WORD,EXCEL,PPT) Only, and versioning needs to be
        handled automaticaly,also size_bytes needs a ceiling on 100mb
        """
        return cls(
            id=uuid4(),
            document_id=document_id,
            version=version,
            filename=filename,
            content_type=content_type,
            size_bytes=size_bytes,
        )
