import uuid

from sqlalchemy import UUID, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.db.base import Base


class FindingDeptSeq(Base):
    __tablename__ = "finding_dept_sequence"

    department_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True,
    )
    seq: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
