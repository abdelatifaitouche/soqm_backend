from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from src.features.documents.infrastructure.models.document import Document
from src.features.documents.application.dto.read_cmd import (
    DocumentRead,
    PaginatedResponse,
)
from src.features.documents.infrastructure.models.document_version import (
    DocumentVersion,
)
from src.core.pagination import Pagination
from src.infra.db.pagination import apply_pagination
from src.features.documents.application.dto.document_filters import DocumentFilters


class DocumentQueryService:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    def apply_filters(self, stmt, filters: DocumentFilters):
        if filters.status:
            stmt = stmt.where(Document.status == filters.status)

        if filters.document_type:
            stmt = stmt.where(Document.document_type == filters.document_type)
        return stmt

    async def list(
        self, pagination: Pagination, filters: DocumentFilters
    ) -> PaginatedResponse:

        total_query = select(func.count()).select_from(Document)
        total_query = self.apply_filters(total_query, filters)
        total = await self.db.scalar(total_query)

        if not total:
            return PaginatedResponse(
                total=0,
                size=0,
                page=0,
                items=[],
            )

        stmt = (
            select(Document, DocumentVersion.version)
            .join(DocumentVersion, DocumentVersion.id == Document.current_version_id)
            .order_by(desc("created_at"))
        )
        stmt = self.apply_filters(stmt, filters)
        stmt = apply_pagination(stmt, pagination)

        results = (await self.db.execute(stmt)).all()
        items: list[DocumentRead] = [
            DocumentRead(
                id=doc.id,
                title=doc.title,
                current_version_id=doc.current_version_id,
                status=doc.status,
                document_type=doc.document_type,
                description=doc.description,
                version=version,
            )
            for doc, version in results
        ]

        return PaginatedResponse(
            total=total,
            size=pagination.limit,
            page=pagination.page,
            items=items,
        )
