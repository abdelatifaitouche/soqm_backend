from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps.db_session import get_db
from fastapi import Depends
from src.features.organizations.infra.repositories import (
    EmployeeRepository,
    DepartmentRepository,
)
from src.features.auth.repositories.user_repository import UserRepository
from src.infra.db.unit_of_work import UnitOfWork
from src.features.organizations.application.usecases import EmployeeUC
from src.features.organizations.infra.queries import EmployeeQueryService


async def get_emp_queries(db: AsyncSession = Depends(get_db)):
    return EmployeeQueryService(db)


async def get_emp_uc(db: AsyncSession = Depends(get_db)):
    uow = UnitOfWork(db)
    repo = EmployeeRepository(db)
    dept_repo = DepartmentRepository(db)
    user_repo = UserRepository(db)
    return EmployeeUC(
        uow,
        repo,
        dept_repo,
        user_repo,
    )
