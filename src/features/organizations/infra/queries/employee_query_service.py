from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Select, func, join
from sqlalchemy.orm import selectinload
from src.features.organizations.infra.models import (
    Employee as EmployeeDB,
    Department as DepartmentDB,
)
from src.features.organizations.application.dtos import (
    EmployeeDetails,
    Department,
    EmployeeListItem,
    PaginatedEmployeeResponse,
)
from src.features.organizations.application.filters import EmployeeFilters
from src.core.pagination import Pagination
from src.infra.db.pagination import apply_pagination
from uuid import UUID
from typing import Any


class EmployeeQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _apply_filters(
        self, stmt: Select[Any], filters: EmployeeFilters
    ) -> Select[Any]:

        if filters.status:
            stmt = stmt.where(EmployeeDB.status == filters.status)

        if filters.job_title:
            stmt = stmt.where(EmployeeDB.job_title == filters.job_title)

        if filters.level:
            stmt = stmt.where(EmployeeDB.level == filters.level)

        if filters.department_id:
            stmt = stmt.where(EmployeeDB.department_id == filters.department_id)

        return stmt

    async def list(
        self, pagination: Pagination, filters: EmployeeFilters
    ) -> PaginatedEmployeeResponse:
        total_count = select(func.count()).select_from(EmployeeDB)
        total_count = self._apply_filters(total_count, filters)
        total_items: int | None = await self.session.scalar(total_count)

        if not total_items:
            return PaginatedEmployeeResponse(
                items=[],
                total=0,
                page=pagination.page,
                size=pagination.limit,
            )

        stmt = select(
            EmployeeDB.id,
            EmployeeDB.first_name,
            EmployeeDB.last_name,
            EmployeeDB.job_title,
            EmployeeDB.level,
            EmployeeDB.status,
            DepartmentDB.id.label("department_id"),
            DepartmentDB.name.label("department_name"),
        ).join(DepartmentDB, DepartmentDB.id == EmployeeDB.department_id)
        stmt = self._apply_filters(stmt, filters)
        stmt = apply_pagination(stmt, pagination)

        rows = (await self.session.execute(stmt)).mappings().all()

        items = [
            EmployeeListItem(
                id=row["id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                status=row["status"],
                job_title=row["job_title"],
                level=row["level"],
                department=Department(
                    id=row["department_id"],
                    name=row["department_name"],
                ),
            )
            for row in rows
        ]

        return PaginatedEmployeeResponse(
            total=total_items,
            items=items,
            page=pagination.page,
            size=pagination.limit,
        )

    async def list_options(self):
        stmt = select(EmployeeDB.id, EmployeeDB.first_name, EmployeeDB.last_name)
        results = (await self.session.execute(stmt)).mappings().all()
        return (
            [
                {
                    "id": res.id,
                    "first_name": res.first_name,
                    "last_name": res.last_name,
                }
                for res in results
            ]
            if results
            else None
        )

    async def get_employee_details(self, employee_id: UUID) -> EmployeeDetails | None:
        stmt = (
            select(EmployeeDB)
            .where(EmployeeDB.id == employee_id)
            .options(
                selectinload(
                    EmployeeDB.department,
                ),
            )
        )

        emp = (await self.session.execute(stmt)).scalar_one_or_none()

        if not emp:
            return None

        return EmployeeDetails(
            id=emp.id,
            first_name=emp.first_name,
            last_name=emp.last_name,
            status=emp.status,
            job_title=emp.job_title,
            level=emp.level,
            created_at=emp.created_at,
            updated_at=emp.updated_at,
            department=Department(
                id=emp.department.id,
                name=emp.department.name,
            ),
        )
