from dataclasses import asdict
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.organizations.application.ports import IDepartmentRepository
from src.features.organizations.domain.entities import Department
from src.features.organizations.infra.models import Department as DepartmentDB


class DepartmentRepository(IDepartmentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, department: Department) -> None:
        values = asdict(department)

        excluded = {
            "id",
            "created_at",
        }

        insert_stmt = (
            insert(DepartmentDB)
            .values(values)
            .on_conflict_do_update(
                index_elements=["id"],
                set_={k: v for k, v in values.items() if k not in excluded},
            )
        )
        await self.session.execute(insert_stmt)

    async def get(self, department_id: UUID) -> Department | None:
        stmt = select(DepartmentDB).where(DepartmentDB.id == department_id)
        res = (await self.session.execute(stmt)).scalar_one_or_none()

        if not res:
            return None

        return Department(
            id=res.id,
            name=res.name,
            parent_id=res.parent_id,
            created_at=res.created_at,
            updated_at=res.updated_at,
        )
