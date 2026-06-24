from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, Integer, DateTime
from datetime import datetime
import uuid


class ComponentRiskSequence(Base):
    __tablename__ = "component_risk_sequence"

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
        default=datetime.now(),
    )
