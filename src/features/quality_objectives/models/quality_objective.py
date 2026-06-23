from src.infra.db.base import Base
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UUID, String, DateTime
from src.features.quality_objectives.enums.objective_states import ObjectiveState
from datetime import datetime


class QualityObjective(Base):
    __tablename__ = "quality_objectives"

    objective_reference: Mapped[str] = mapped_column(String, nullable=True)
    objective_text: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(
        String, nullable=False, default=ObjectiveState.DRAFT.value
    )
    review_date: Mapped[datetime] = mapped_column(DateTime)
    component_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("soqm_components.id")
    )

    component: Mapped["SOQMComponent"] = relationship(
        "SOQMComponent",
        back_populates="quality_objectives",
    )

    risks: Mapped[list["Risk"]] = relationship(
        "Risk", back_populates="objective", cascade="all, delete"
    )
