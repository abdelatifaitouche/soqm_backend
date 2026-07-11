from src.features.documents.application.document_service import DocumentService
from src.features.documents.infrastructure.storage.file_system_storage import (
    FileSystemStorage,
)
from src.features.documents.infrastructure.repositories.document_repository import (
    DocumentRepository,
)
from src.infra.db.uow import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.documents.infrastructure.repositories.document_version_repository import (
    DocumentVersionRepository,
)
from src.features.documents.application.query_service import DocumentQueryService


def get_service(db: AsyncSession = Depends(get_db)):
    """Construct the file Upload service, and pass in the file storage system"""
    return DocumentService(
        FileSystemStorage(),
        DocumentRepository(db),
        DocumentVersionRepository(db),
    )


def get_queries(
    db: AsyncSession = Depends(get_db),
) -> DocumentQueryService:
    return DocumentQueryService(db)
