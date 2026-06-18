from src.features.risks.domain.risk import Risk as RiskEntity
from src.features.risks.schemas.risk import CreateRisk, UpdateRisk
import uuid


class RiskMapper:
    @staticmethod
    def from_create(user_id: uuid.UUID, data: CreateRisk) -> RiskEntity:
        return RiskEntity.create(
            objective_id=data.objective_id,
            component_id=data.component_id,
            risk_ref=data.risk_ref,
            risk_discription=data.risk_discription,
            occurence=data.occurence,
            significance=data.significance,
            created_by=user_id,
            next_review_date=data.next_review_date,
        )

    @staticmethod
    def from_update(user_id: uuid.UUID, data: UpdateRisk):
        return
