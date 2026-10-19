import uuid

from sqlalchemy import UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db.base import Base


class RiskResponseAssociation(Base):
    __tablename__ = "risk_response_association"
    __table_args__ = (
        UniqueConstraint(
            "risk_id",
            "response_id",
            name="uq_risk_response_association",
        ),
    )

    risk_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("risks.id"), primary_key=True
    )

    response_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("risk_responses.id"),
        primary_key=True,
    )

    risk: Mapped["Risk"] = relationship(back_populates="response_associations")

    response: Mapped["RiskResponse"] = relationship(back_populates="risk_associations")
