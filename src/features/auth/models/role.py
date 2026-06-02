from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    is_system: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
