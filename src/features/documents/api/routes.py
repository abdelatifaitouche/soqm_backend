from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import StreamingResponse, FileResponse
from src.features.documents.application.document_service import DocumentService
from src.features.documents.api.deps import get_service, get_queries
from src.features.documents.domain.document import Document
from src.features.documents.api.schemas import (
    CreateDocument,
    ReadDocument,
    PaginatedResponse,
    DocumentFilters,
)
from src.features.documents.application.dto.create_cmd import (
    CreateDocument as CreateDocumentDTO,
)
from src.features.documents.application.query_service import DocumentQueryService
from src.core.pagination import Pagination
from src.features.documents.application.dto.document_filters import (
    DocumentFilters as FiltersDTO,
)

router = APIRouter(prefix="/documents")
from uuid import UUID


@router.post("/upload/")
async def upload_file(
    data: CreateDocument = Depends(),
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_service),
):
    document: Document = await service.upload_file(
        CreateDocumentDTO(
            title=data.title,
            document_type=data.document_type,
            description=data.description,
            content_type=file.content_type,
            filesize=file.size,
            filename=file.filename,
            file=file.file,
        ),
    )
    return document


@router.get("/{document_id}/download")
async def download_document(
    document_id: UUID,
    service: DocumentService = Depends(get_service),
):
    path, content_type, filename = await service.download_document(document_id)
    return FileResponse(
        path,
        media_type=content_type,
    )


@router.get("")
async def list_documents(
    pagination: Pagination = Depends(),
    filters: DocumentFilters = Depends(),
    queries: DocumentQueryService = Depends(get_queries),
):
    docs = await queries.list(
        pagination,
        filters=FiltersDTO(
            status=filters.status,
            document_type=filters.document_type,
        ),
    )
    return PaginatedResponse.model_validate(docs)
