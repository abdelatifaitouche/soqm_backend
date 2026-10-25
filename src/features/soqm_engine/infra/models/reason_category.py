from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean


class ReasonCategory(Base):
    __tablename__ = "reason_categories"

    code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )
    context: Mapped[str] = mapped_column(String(50), nullable=False)
    display_text: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
