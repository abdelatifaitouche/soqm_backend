from src.infra.db.uow import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.features.risks.repositories.queries.response_query_service import (
    ResponseQueryService,
)
from src.features.risks.repositories.risk_repository import RiskRepository
from src.features.risks.services.response_service import ResponseService
from src.features.risks.repositories.risk_response_repository import (
    RiskResponseRepository,
)
from src.features.organizations.repositories.employee_repository import (
    EmployeeRepository,
)
from src.features.soqm_components.repositories.components_repository import (
    ComponentRepository,
)


def get_service(db: AsyncSession = Depends(get_db)) -> ResponseService:
    risk_repo: RiskRepository = RiskRepository(db)
    response_repo: RiskResponseRepository = RiskResponseRepository(db)
    employee_repo: EmployeeRepository = EmployeeRepository(db)
    component_repo: ComponentRepository = ComponentRepository(db)
    return ResponseService(response_repo, risk_repo, component_repo, employee_repo)


def get_queries(
    db: AsyncSession = Depends(get_db),
):
    return ResponseQueryService(db)
