import uuid

from sqlalchemy import UUID, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db.base import Base


class Employee(Base):
    __tablename__ = "employees"

    first_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    department_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    job_title: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    level: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    department: Mapped["Department"] = relationship(back_populates="employees")
    user: Mapped["User"] = relationship(back_populates="profile")
    assigned_responses: Mapped[list["RiskResponse"]] = relationship(
        back_populates="assigned_employee"
    )
    __table_args__ = (UniqueConstraint("user_id"),)
