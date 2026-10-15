from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.auth.repositories.user_repository import UserRepository
from src.features.organizations.repositories.employee_repository import (
    EmployeeRepository,
)
from src.features.organizations.services.employee_service import EmployeeService
from src.infra.db.uow import get_db
from src.features.organizations.infra.repositories import DepartmentRepository


def get_service(db: AsyncSession = Depends(get_db)) -> EmployeeService:
    dept_repo = DepartmentRepository(db)
    user_repo = UserRepository(db)
    employee_repo = EmployeeRepository(db)
    return EmployeeService(
        repo=employee_repo,
        user_repo=user_repo,
        dept_repo=dept_repo,
    )
