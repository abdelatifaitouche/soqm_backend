from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, UUID
from src.features.documents.domain.enums import DocumentStatus, DocumentType
import uuid


class Document(Base):
    __tablename__ = "documents"

    title: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    document_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=DocumentType.POLICY.value,
    )
    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=DocumentStatus.ACTIVE.value,
    )

    current_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    versions: Mapped[list["DocumentVersion"]] = relationship(
        back_populates="document",
        foreign_keys="DocumentVersion.document_id",
    )
