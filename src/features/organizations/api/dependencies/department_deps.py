from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps.db_session import get_db
from src.features.organizations.application.usecases import DepartmentUC
from src.features.organizations.infra.repositories import DepartmentRepository
from src.infra.db.unit_of_work import UnitOfWork
from src.features.organizations.infra.queries import DepartmentQueryService


def get_dept_uc(db: AsyncSession = Depends(get_db)):
    uow = UnitOfWork(db)
    repo = DepartmentRepository(db)
    return DepartmentUC(
        uow=uow,
        repo=repo,
    )


def get_dept_queries(db: AsyncSession = Depends(get_db)):
    return DepartmentQueryService(db)
