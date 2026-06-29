from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean


class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    risks: Mapped[list["Risk"]] = relationship(
        "Risk",
        back_populates="user",
    )

    user_roles: Mapped[list["UserRoles"]] = relationship(
        "UserRoles",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    risk_audit_log: Mapped[list["RiskAuditLog"]] = relationship(
        "RiskAuditLog",
        back_populates="user",
    )

    created_risk_responses: Mapped[list["RiskResponse"]] = relationship(
        "RiskResponse",
        foreign_keys="RiskResponse.created_by",
        back_populates="created_by_user",
    )

    assigned_responses: Mapped[list["RiskResponse"]] = relationship(
        "RiskResponse",
        foreign_keys="RiskResponse.responsible_employee",
        back_populates="assigned_employee",
    )

    profile: Mapped["Employee"] = relationship(
        back_populates="user",
    )
