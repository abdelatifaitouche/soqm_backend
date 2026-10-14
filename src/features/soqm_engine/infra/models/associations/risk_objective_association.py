from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, ForeignKey, UniqueConstraint
import uuid


class RiskObjectiveAssociation(Base):
    __tablename__ = "risks_objectives_association"
    __table_args__ = (
        UniqueConstraint(
            "risk_id",
            "objective_id",
            name="uq_risk_objective_association",
        ),
    )
    risk_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("risks.id"),
        primary_key=True,
    )
    objective_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("quality_objectives.id"),
        primary_key=True,
    )

    risk: Mapped["Risk"] = relationship(back_populates="objective_association")

    objective: Mapped["QualityObjective"] = relationship(
        back_populates="risk_association"
    )
