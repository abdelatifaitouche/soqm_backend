from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Text, Integer, Enum
from src.features.soqm_components.enums.soqm_component import ComponentState


class SOQMComponent(Base):
    __tablename__ = "soqm_components"

    name: Mapped[str] = mapped_column(
        String(200), nullable=False, unique=True, index=True
    )
    description: Mapped[str] = mapped_column(Text, nullable=True)
    isqm_reference: Mapped[str] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=ComponentState.ACTIVE.value,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False)

    quality_objectives: Mapped[list["QualityObjective"]] = relationship(
        "QualityObjective",
        cascade="all, delete",
        back_populates="component",
    )
