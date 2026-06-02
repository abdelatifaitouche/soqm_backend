from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UniqueConstraint


class Permission(Base):
    __tablename__ = "permissions"

    resource: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)

    role_permissions: Mapped[list["RolePermissions"]] = relationship(
        "RolePermissions", back_populates="permission", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("resource", "action", name="uq_resource_action_permisisson"),
    )
