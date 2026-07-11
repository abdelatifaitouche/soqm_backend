from sqlalchemy.ext.asyncio import AsyncSession
from src.features.documents.domain.document_version import DocumentVersion
from src.features.documents.infrastructure.models.document_version import (
    DocumentVersion as DocumentVersionDB,
)
from uuid import UUID
from sqlalchemy import select


class DocumentVersionRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def create(self, version: DocumentVersion) -> DocumentVersion:
        version_orm: DocumentVersionDB = DocumentVersionDB(
            id=version.id,
            document_id=version.document_id,
            filename=version.filename,
            content_type=version.content_type,
            size_bytes=version.size_bytes,
            processing_status=version.processing_status,
            version=version.version,
        )
        self.db.add(version_orm)
        await self.db.flush()
        return version

    async def get_by_id(self, version_id: UUID) -> DocumentVersion | None:
        stmt = select(DocumentVersionDB).where(DocumentVersionDB.id == version_id)
        result = (await self.db.execute(stmt)).scalar_one_or_none()

        if not result:
            return None

        return DocumentVersion(
            id=result.id,
            document_id=result.document_id,
            version=result.version,
            filename=result.filename,
            content_type=result.content_type,
            size_bytes=result.size_bytes,
            processing_status=result.processing_status,
        )
