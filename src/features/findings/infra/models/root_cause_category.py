from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db.base import Base


class RootCauseCategory(Base):
    __tablename__ = "root_cause_category"

    category: Mapped[str] = mapped_column(String, nullable=False)

    root_cause_indicators: Mapped[list["RootCauseIndicator"]] = relationship(
        back_populates="root_cause_category"
    )
