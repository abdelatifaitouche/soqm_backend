from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UUID, ForeignKey, Enum, DateTime
from src.features.findings.domain.enums import ActionState
import uuid
from datetime import datetime


class Action(Base):
    __tablename__ = "actions"

    title: Mapped[str] = mapped_column(String, nullable=False)
    finding_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("findings.id"),
        nullable=False,
    )
    status: Mapped[ActionState] = mapped_column(
        Enum(ActionState, name="action_state", native_enum=True),
        nullable=False,
        default=ActionState.DRAFT,
    )
    estimated_completion_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    completion_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
    )

    finding: Mapped["Finding"] = relationship(back_populates="actions")
