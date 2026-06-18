from src.features.risks.domain.risk import Risk as RiskEntity
from src.features.risks.schemas.risk import CreateRisk
import uuid


class RiskMapper:
    @staticmethod
    def from_create(user_id: uuid.UUID, data: CreateRisk) -> RiskEntity:
        return RiskEntity(
            id=uuid.uuid4(),
            objective_id=data.objective_id,
            component_id=data.component_id,
            risk_ref=data.risk_ref,
            risk_discription=data.risk_discription,
            occurence=data.occurence,
            date_identified=data.date_identified,
            significance=data.significance,
            date_last_assessed=data.date_last_assessed,
            created_by=user_id,
        )
