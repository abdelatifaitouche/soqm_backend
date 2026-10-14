from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.db.uow import get_db
from src.features.risks.repositories.risk_repository import RiskRepository
from src.features.quality_objectives.repository.objective_repository import (
    ObjectiveRepository,
)
from src.features.soqm_components.infra.repositories.component_repository import (
    ComponentRepository,
)
from src.features.risks.services.risk_service import RiskService
from src.features.risks.repositories.queries.risk_query_service import RiskQueryService


def get_service(
    db: AsyncSession = Depends(get_db),
) -> RiskService:

    risk_repo = RiskRepository(db)
    component_repo = ComponentRepository(db)
    objective_repo = ObjectiveRepository(db)

    return RiskService(
        repo=risk_repo,
        objective_repo=objective_repo,
        component_repo=component_repo,
    )


def get_queries(db: AsyncSession = Depends(get_db)):
    return RiskQueryService(db)
