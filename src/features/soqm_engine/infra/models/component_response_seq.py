import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.db.base import Base


class ComponentResponseSeq(Base):
    __tablename__ = "component_response_seq"

    component_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True,
    )
    sequence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    last_generated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now()
    )

    __table_args__ = (UniqueConstraint("component_id", name="component_response_uq"),)
