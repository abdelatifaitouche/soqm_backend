from src.features.organizations.application.ports import IEmployeeRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.organizations.domain.entities import Employee
from src.features.organizations.infra.models import Employee as EmployeeDB
from uuid import UUID
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from dataclasses import asdict


class EmployeeRepository(IEmployeeRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, employee: Employee) -> None:

        values = asdict(employee)

        excluded_values = {
            "id",
            "created_at",
        }

        insert_stmt = (
            insert(EmployeeDB)
            .values(**values)
            .on_conflict_do_update(
                index_elements=[EmployeeDB.id],
                set_={k: v for k, v in values.items() if k not in excluded_values},
            )
        )

        await self.session.execute(insert_stmt)

    async def get(self, employee_id: UUID) -> Employee | None:
        stmt = select(EmployeeDB).where(EmployeeDB.id == employee_id)

        emp = (await self.session.execute(stmt)).scalar_one_or_none()

        if not emp:
            return None

        return Employee(
            id=emp.id,
            first_name=emp.first_name,
            last_name=emp.last_name,
            department_id=emp.department_id,
            user_id=emp.user_id,
            job_title=emp.job_title,
            level=emp.level,
            status=emp.status,
            created_at=emp.created_at,
            updated_at=emp.updated_at,
        )
