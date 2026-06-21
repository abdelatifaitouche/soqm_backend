from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UUID, String
import uuid


class RiskAuditLog(Base):
    __tablename__ = "risk_audit_logs"

    risk_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("risks.id"),
        nullable=False,
    )
    field_changed: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    old_value: Mapped[str] = mapped_column(String, nullable=True)
    new_value: Mapped[str] = mapped_column(String, nullable=True)
    change_comment: Mapped[str] = mapped_column(String, nullable=True)
    changed_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id")
    )

    risk: Mapped["Risk"] = relationship(
        "Risk",
        back_populates="risk_audit_logs",
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="risk_audit_log",
    )
