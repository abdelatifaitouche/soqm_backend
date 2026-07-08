from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, ForeignKey, String, Date
from src.features.risks.enums.risk_response import (
    ResponseState,
    ResponseType,
    ExecutionType,
    Frequency,
)
from datetime import date
import uuid


class RiskResponse(Base):
    __tablename__ = "risk_responses"

    response_ref: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    response_name: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    response_description: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    response_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=ResponseType.DETECTIVE.value,
    )
    date_implementation: Mapped[date] = mapped_column(Date, nullable=True)
    date_monitored_design: Mapped[date] = mapped_column(
        Date,
        nullable=True,
    )
    date_monitored_operating: Mapped[date] = mapped_column(
        Date,
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=ResponseState.DRAFT.value,
    )
    owner: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id")
    )

    component_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
    evidence_notes: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
    )

    frequency: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=Frequency.CONTINUOUS.value,
    )
    execution_type: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=ExecutionType.MANUAL.value,
    )

    created_by_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="created_risk_responses",
    )
    assigned_employee: Mapped["Employee"] = relationship(
        foreign_keys=[owner],
        back_populates="assigned_responses",
    )

    risk_associations: Mapped[list["RiskResponseAssociation"]] = relationship(
        back_populates="response"
    )


RESPONSE_ORDER_FIELDS = {
    "created_at": RiskResponse.created_at,
}
