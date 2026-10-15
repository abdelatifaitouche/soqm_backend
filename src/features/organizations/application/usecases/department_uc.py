from src.features.organizations.application.ports import IDepartmentRepository
from src.core.shared.interfaces.unit_of_work import IUnitOfWork
from src.features.organizations.domain.entities import Department
from src.features.organizations.application.dtos import CreateDepartment
from uuid import UUID


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
