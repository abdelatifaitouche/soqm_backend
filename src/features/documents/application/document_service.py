from src.features.documents.infrastructure.storage.file_storage_interface import (
    FileStorage,
)
from src.features.documents.infrastructure.repositories.document_repository import (
    DocumentRepository,
)
from src.features.documents.domain.document import Document
from src.features.documents.domain.document_version import DocumentVersion
from typing import BinaryIO
from src.features.documents.application.dto.create_cmd import CreateDocument
from src.features.documents.infrastructure.repositories.document_version_repository import (
    DocumentVersionRepository,
)
from uuid import UUID


class DocumentService:
    def __init__(
        self,
        file_storage: FileStorage,
        document_repo: DocumentRepository,
        document_version_repo: DocumentVersionRepository,
    ):
        self.file_storage: FileStorage = file_storage
        self.document_repo: DocumentRepository = document_repo
        self.document_version_repo: DocumentVersionRepository = document_version_repo

    async def upload_file(self, data: CreateDocument) -> Document:
        doc: Document = Document.create(
            title=data.title,
            document_type=data.document_type,
            description=data.description,
        )
        version: DocumentVersion = DocumentVersion.create(
            document_id=doc.id,
            version=1,
            filename=data.filename,
            content_type=data.content_type,
            size_bytes=data.filesize,
        )

        doc.update_version(version)
        doc: Document = await self.document_repo.create(doc)
        version: DocumentVersion = await self.document_version_repo.create(version)
        self.file_storage.upload(data.file, data.filename)

        return doc

    async def download_document(self, document_id: UUID):

        doc: Document | None = await self.document_repo.get_by_id(document_id)

        if not doc or not doc.current_version_id:
            raise

        version: DocumentVersion | None = await self.document_version_repo.get_by_id(
            doc.current_version_id
        )

        if not version:
            raise

        return (
            self.file_storage.download(version.filename),
            version.content_type,
            version.filename,
        )
