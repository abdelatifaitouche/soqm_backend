from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UniqueConstraint


class Permission(Base):
    __tablename__ = "permissions"

    resource: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("resource", "action", name="uq_resource_action_permisisson"),
    )
