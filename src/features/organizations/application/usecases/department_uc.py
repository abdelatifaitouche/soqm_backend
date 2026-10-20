from uuid import UUID

from src.core.shared.interfaces.unit_of_work import IUnitOfWork
from src.features.organizations.application.dtos import (
    CreateDepartment,
    UpdateDepartment,
    UpdateDepartmentParent,
)
from src.features.organizations.application.ports import IDepartmentRepository
from src.features.organizations.domain.entities import Department


class DepartmentUC:
    def __init__(self, uow: IUnitOfWork, repo: IDepartmentRepository):
        self.uow = uow
        self.repo = repo

    async def get(self, dept_id: UUID):

        dept = await self.repo.get(dept_id)

        if not dept:
            raise Exception("No Deparetment found")

        return dept

    async def create(self, data: CreateDepartment):
        async with self.uow:
            parent_dept = None
            if data.parent_id:
                parent_dept = await self.get(data.parent_id)

            if not parent_dept:
                parent_dept_id = None
            else:
                parent_dept_id = parent_dept.id

            dept = Department.create(data.name, parent_dept_id)

            await self.repo.save(dept)

    async def update(self, dept_id: UUID, update_data: UpdateDepartment):
        async with self.uow:
            dept = await self.get(dept_id)

            dept.rename(new_name=update_data.name)

            await self.repo.save(dept)

    async def change_parent_dept(self, dept_id: UUID, parent: UpdateDepartmentParent):
        async with self.uow:
            dept = await self.get(dept_id)

            parent_dept = await self.get(parent.parent_id)

            dept.change_parent(parent_dept.id)

            # this code needs to be worked on to avoid cycles, and parent child checking
            await self.repo.save(dept)
