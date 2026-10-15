from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, UUID
import uuid


class PotentialRootCause(Base):
    __tablename__ = "potential_root_cause"

    potential_root_cause: Mapped[str] = mapped_column(String, nullable=False)

    root_cause_indicator_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("root_cause_indicator.id"),
        nullable=False,
    )

    component_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("soqm_components.id"),
        nullable=False,
    )

    root_cause_indicator: Mapped["RootCauseIndicator"] = relationship(
        back_populates="potential_root_causes"
    )
