from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, Integer, DateTime, ForeignKey, UniqueConstraint
import uuid
from datetime import datetime


class ComponentObjectiveSeq(Base):
    __tablename__ = "component_objective_seq"

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
        DateTime,
        nullable=False,
        default=datetime.now(),
    )

    __table_args__ = (
        UniqueConstraint("component_id", "sequence", name="uq_component_seq"),
    )
