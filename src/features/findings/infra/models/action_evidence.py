from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UUID, Text, Enum, VARCHAR, DateTime
import uuid
from datetime import datetime
from src.features.findings.domain.enums import ActionEvidenceState


class ActionEvidence(Base):
    __tablename__ = "action_evidences"

    action_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("actions.id"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[ActionEvidenceState] = mapped_column(
        Enum(
            ActionEvidenceState,
            name="action_evidence_state",
            native_enum=True,
        ),
        default=ActionEvidenceState.DRAFT,
    )

    action: Mapped["Action"] = relationship(
        back_populates="action_completion_evidences",
    )
