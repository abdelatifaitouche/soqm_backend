from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UUID, ForeignKey
import uuid


class Department(Base):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("departments.id"),
        nullable=True,
    )

    parent: Mapped["Department | None"] = relationship(
        "Department",
        remote_side="Department.id",
        back_populates="children",
    )

    children: Mapped[list["Department"]] = relationship(
        "Department",
        back_populates="parent",
    )
