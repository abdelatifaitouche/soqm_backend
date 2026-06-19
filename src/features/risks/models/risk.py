from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, UUID, ForeignKey, Integer, Date, Float
import uuid
from datetime import date
from src.features.risks.enums.risk_states import RiskStatus


class Risk(Base):
    __tablename__ = "risks"

    objective_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("quality_objectives.id"),
        nullable=False,
    )
    component_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("soqm_components.id"),
        nullable=False,
    )
    risk_ref: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    risk_discription: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    occurence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    significance: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    date_identified: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=RiskStatus.IDENTIFIED.value,
    )
    residual_score: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    date_last_assessed: Mapped[date] = mapped_column(
        Date,
        nullable=True,
    )
    next_review_date: Mapped[date] = mapped_column(
        Date,
        nullable=True,
    )

    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="risks",
    )

    component: Mapped["SOQMComponent"] = relationship(
        "SOQMComponent",
        back_populates="risks",
    )

    objective: Mapped["QualityObjective"] = relationship(
        "QualityObjective",
        back_populates="risks",
    )

    risk_responses: Mapped["RiskResponse"] = relationship(
        "RiskResponse",
        back_populates="risk",
    )

    risk_audit_log: Mapped[list["RiskAuditLog"]] = relationship(
        "RiskAuditLog",
        back_populates="risk",
    )
