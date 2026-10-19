from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.features.organizations.application.dtos import Department as DepartmentDTO
from src.features.organizations.infra.models import Department


class DepartmentQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self):
        stmt = select(Department.id, Department.name)

        res = (await self.session.execute(stmt)).mappings().all()

        return [DepartmentDTO(**dept) for dept in res]

    async def tree_view(self):
        return

    async def get_department_details(self, department_id: UUID):
        stmt = (
            select(Department)
            .where(Department.id == department_id)
            .options(selectinload(Department.children))
        )

        res = (await self.session.execute(stmt)).mappings().one_or_none()

        return res
