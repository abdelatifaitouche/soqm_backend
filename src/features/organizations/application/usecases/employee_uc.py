from src.core.shared.interfaces.unit_of_work import IUnitOfWork
from src.features.organizations.application.ports import (
    IEmployeeRepository,
    IDepartmentRepository,
)
from uuid import UUID
from src.features.organizations.domain.entities import Employee
from src.features.organizations.application.dtos import CreateEmployee, UpdateEmployee
from src.features.auth.repositories.user_repository import UserRepository


class EmployeeUC:
    def __init__(
        self,
        uow: IUnitOfWork,
        repo: IEmployeeRepository,
        dept_repo: IDepartmentRepository,
        user_repo: UserRepository,
    ):
        self.uow = uow
        self.repo = repo
        self.dept_repo = dept_repo
        self.user_repo = user_repo

    async def create(self, emp_data: CreateEmployee):
        async with self.uow:
            dept = await self.dept_repo.get(emp_data.department_id)

            if not dept:
                raise Exception(
                    "Department Doesnt exists",
                )

            user_id = emp_data.user_id

            if user_id:
                user = await self.user_repo.get_by_id(user_id)

                if not user:
                    raise Exception(
                        f"Cannot find user with ID : {user_id}",
                    )

                if not user.is_active:
                    raise Exception(
                        f"Cannot assign disabled users",
                    )

            emp = Employee.create(
                first_name=emp_data.first_name,
                last_name=emp_data.last_name,
                job_title=emp_data.job_title,
                department_id=dept.id,
                level=emp_data.level,
                user_id=user_id,
            )

            await self.repo.save(emp)

        return emp.id

    async def get(self, emp_id: UUID) -> Employee:

        emp = await self.repo.get(emp_id)

        if not emp:
            raise Exception(f"Cannot Find employee with provided ID {emp_id}")

        return emp

    async def update(self, emp_id: UUID, update_data: UpdateEmployee):
        async with self.uow:
            emp = await self.get(emp_id)

            emp.update(
                first_name=update_data.first_name,
                last_name=update_data.last_name,
                job_title=update_data.job_title,
            )

            await self.repo.save(emp)

    async def block(self, emp_id: UUID):
        async with self.uow:
            emp = await self.get(emp_id)

            emp.deactivate()

            await self.repo.save(emp)

    async def activate(self, emp_id: UUID):
        async with self.uow:
            emp = await self.get(emp_id)

            emp.activate()

            await self.repo.save(emp)

    async def delete(self):
        return
