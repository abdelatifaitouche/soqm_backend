import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db.base import Base


class RootCauseIndicator(Base):
    __tablename__ = "root_cause_indicator"

    indicator: Mapped[str] = mapped_column(String, nullable=False)

    root_cause_category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("root_cause_category.id"),
        nullable=False,
    )
    root_cause_category: Mapped["RootCauseCategory"] = relationship(
        back_populates="root_cause_indicators",
    )

    potential_root_causes: Mapped[list["PotentialRootCause"]] = relationship(
        back_populates="root_cause_indicator",
    )
