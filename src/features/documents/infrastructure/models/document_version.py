from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, Integer, String, String, ForeignKey
import uuid
from src.features.documents.domain.enums import DocumentProcessingStatus


class DocumentVersion(Base):
    __tablename__ = "document_versions"

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id"),
        nullable=False,
    )
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    processing_status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=DocumentProcessingStatus.UPLOADING.value,
    )

    document: Mapped["Document"] = relationship(
        back_populates="versions",
        foreign_keys=[document_id],
    )
