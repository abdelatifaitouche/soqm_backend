from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, Integer, UniqueConstraint, DateTime
import uuid
from datetime import datetime


class ComponentResponseSeq(Base):
    __tablename__ = "component_response_seq"

    component_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
    sequence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    last_generated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now()
    )

    __table_args__ = (
        UniqueConstraint("component_id", "sequence", name="component_response_uq"),
    )
