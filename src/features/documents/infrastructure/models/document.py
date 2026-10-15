import uuid

from sqlalchemy import UUID, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.features.documents.domain.enums import DocumentStatus, DocumentType
from src.infra.db.base import Base


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
