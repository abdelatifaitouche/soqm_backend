import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.features.findings.domain.enums.finding import (
    DeficiencySeverity,
    FindingSource,
    FindingStatus,
    ProcessStatus,
)
from src.infra.db.base import Base


class Finding(Base):
    __tablename__ = "findings"

    finding_ref: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    finding_title: Mapped[str] = mapped_column(String, nullable=True)

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    finding_source: Mapped[FindingSource] = mapped_column(
        Enum(
            FindingSource,
            name="finding_source",
            native_enum=True,
        ),
        nullable=True,
    )
    department: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    deficiency_severity: Mapped[DeficiencySeverity] = mapped_column(
        Enum(
            DeficiencySeverity,
            name="finding_deficiency_severity",
            native_enum=True,
        ),
        nullable=False,
        default=DeficiencySeverity.SIGNIFICANT_DEFICIENCY,
    )

    status: Mapped[FindingStatus] = mapped_column(
        Enum(
            FindingStatus,
            name="finding_status",
            native_enum=True,
        ),
        nullable=False,
        default=FindingStatus.OPEN,
    )
    cause_analysis_status: Mapped[ProcessStatus] = mapped_column(
        String,
        default=ProcessStatus.NOT_STARTED.value,
        nullable=False,
    )
    analysis: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    indicator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    potential_root_cause_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    soqm_component_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    analysis_completed_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
    )

    actions: Mapped[list["Action"]] = relationship(back_populates="finding")
