from src.features.organizations.repositories.employee_repository import (
    EmployeeRepository,
)
from src.features.organizations.repositories.department_repository import (
    DepartmentRepository,
)
from src.features.auth.domain.user import User
from src.features.auth.repositories.user_repository import UserRepository
from src.features.organizations.domain.employee import Employee as EmployeeEntity
from src.features.organizations.schemas.employee import CreateEmployee
from src.core.exceptions import UserNotFoundError, NotFoundError, ValidationError
from typing import Any
from uuid import UUID


class EmployeeService:
    def __init__(
        self,
        repo: EmployeeRepository,
        user_repo: UserRepository,
        dept_repo: DepartmentRepository,
    ):
        self.repo: EmployeeRepository = repo
        self.user_repo: UserRepository = user_repo
        self.department_repo: DepartmentRepository = dept_repo

    async def create_employee(self, data: CreateEmployee) -> EmployeeEntity:

        user: User | None = None

        if data.user_id:
            user: User | None = await self.user_repo.get_by_id(data.user_id)
            if user is None:
                raise UserNotFoundError(
                    message=f"User with ID {data.user_id} not found",
                )

            if not user.is_active:
                raise ValidationError(
                    "User selected is not active in the platform",
                )

        department = await self.department_repo.get_by_id(data.department_id)

        if not department:
            raise NotFoundError(
                message=f"Department with ID {data.department_id} not found",
            )

        employee: EmployeeEntity = EmployeeEntity.add_profile(
            first_name=data.first_name,
            last_name=data.last_name,
            user_id=data.user_id,
            department_id=data.department_id,
            job_title=data.job_title,
            level=data.level,
        )

        return await self.repo.create(employee)

    async def list_employees(self, pagination, filters):
        return await self.repo.list(pagination, filters)

    async def list_options(self) -> list[dict[str, Any]] | None:
        return await self.repo.list_options()

    async def get_user_profile(self, user_id: UUID):

        profile = await self.repo.get_by_user_id(user_id)

        if not profile:
            raise NotFoundError(
                message="Profile Not Found",
            )

        return profile

    async def update(self):
        return

    async def delete(self):
        return
