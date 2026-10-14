from fastapi import Depends
from src.api.deps.db_session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.soqm_engine.application.usecases import ResponseUC
from src.infra.db.unit_of_work import UnitOfWork
from src.features.soqm_engine.infra.repositories import (
    SequenceRepository,
    ComponentRepository,
    ResponseRepository,
)
from src.features.organizations.repositories.employee_repository import (
    EmployeeRepository,
)
from src.features.soqm_engine.infra.queries import ResponseQueryService


def get_response_uc(db: AsyncSession = Depends(get_db)) -> ResponseUC:
    response_repo = ResponseRepository(db)
    uow = UnitOfWork(db)
    employee_repo = EmployeeRepository(db)
    seq_repo = SequenceRepository(db)
    component_repo = ComponentRepository(db)
    return ResponseUC(
        uow=uow,
        response_repo=response_repo,
        seq_repo=seq_repo,
        component_repo=component_repo,
        employee_repo=employee_repo,
    )


def get_response_queries(db: AsyncSession = Depends(get_db)):
    return ResponseQueryService(db)
