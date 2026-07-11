from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.features.documents.domain.document import Document
from src.features.documents.domain.document_version import DocumentVersion
from src.features.documents.infrastructure.models.document import Document as DocumentDB
from src.features.documents.infrastructure.models.document_version import (
    DocumentVersion as DocumentVersionDB,
)
from uuid import UUID


class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def create(self, doc: Document) -> Document:
        doc_orm: DocumentDB = DocumentDB(
            id=doc.id,
            title=doc.title,
            current_version_id=doc.current_version_id,
            description=doc.description,
            document_type=doc.document_type,
            status=doc.status,
        )

        self.db.add(doc_orm)
        await self.db.flush()
        return doc

    async def get_by_id(self, document_id: UUID) -> Document | None:

        stmt = select(DocumentDB).where(DocumentDB.id == document_id)

        result = (await self.db.execute(stmt)).scalar_one_or_none()

        if not result:
            return None

        return Document(
            id=result.id,
            title=result.title,
            description=result.description,
            current_version_id=result.current_version_id,
            document_type=result.document_type,
            status=result.status,
        )
