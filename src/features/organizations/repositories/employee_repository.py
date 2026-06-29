from src.features.organizations.models.employee import Employee as EmployeeDB
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.organizations.domain.employee import Employee as EmployeeEntity
from src.infra.db.exception_utils import translate_db_errors
from uuid import UUID
from sqlalchemy import select, Select
from sqlalchemy.orm import selectinload
from src.core.pagination import Pagination
from src.features.organizations.filters.employee_filters import EmployeeFilters
from typing import Any


class EmployeeRepository:
    model = EmployeeDB

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    def _to_orm(self, entity: EmployeeEntity) -> EmployeeDB:
        return EmployeeDB(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            user_id=entity.user_id,
            department_id=entity.department_id,
            level=entity.level,
            status=entity.status,
            job_title=entity.job_title,
        )

    def _to_domain(self, orm: EmployeeDB) -> EmployeeEntity:
        return EmployeeEntity(
            id=orm.id,
            first_name=orm.first_name,
            last_name=orm.last_name,
            user_id=orm.user_id,
            department_id=orm.department_id,
            job_title=orm.job_title,
            status=orm.status,
            level=orm.level,
        )

    async def create(self, entity: EmployeeEntity):
        try:
            orm = self._to_orm(entity)
            self.db.add(orm)

            await self.db.flush()
            # this line is not necessary just to keep the whole codebase consistent
            return self._to_domain(orm)

        except Exception as e:
            raise translate_db_errors(e)

    def _apply_filters(self, stmt: Select[Any], filters: EmployeeFilters):

        if filters.department:
            stmt = stmt.where(self.model.department.name == filters.department)

        if filters.level:
            stmt = stmt.where(self.model.level == filters.level)

        if filters.status:
            stmt = stmt.where(self.model.status == filters.status)

        return stmt

    def _apply_pagination(self, stmt: Select[Any], pagination: Pagination):
        return stmt.offset(pagination.offset).limit(pagination.limit)

    async def list(self, pagination, filters):
        stmt = select(self.model).options(selectinload(self.model.department))
        stmt = self._apply_filters(stmt, filters)
        stmt = self._apply_pagination(stmt, pagination)
        results = (await self.db.execute(stmt)).scalars().all()
        return [
            {
                "id": res.id,
                "first_name": res.first_name,
                "last_name": res.last_name,
                "department": res.department.name,
                "job_title": res.job_title,
                "status": res.status,
                "level": res.level,
            }
            for res in results
        ]

    async def get_by_id(self, entity_id: UUID) -> EmployeeEntity | None:
        stmt = select(self.model).where(self.model.id == entity_id)
        result = (await self.db.execute(stmt)).scalar_one_or_none()
        return self._to_domain(result) if result else None

    async def get_by_user_id(self, user_id: UUID):
        stmt = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .options(
                selectinload(
                    self.model.department,
                ),
                selectinload(
                    self.model.user,
                ),
            )
        )
        result = (await self.db.execute(stmt)).scalar_one_or_none()

        return (
            {
                "id": result.id,
                "first_name": result.first_name,
                "last_name": result.last_name,
                "level": result.level,
                "job_title": result.job_title,
                "email": result.user.email,
                "department": result.department.name,
            }
            if result
            else None
        )

    async def list_options(self):

        stmt = select(self.model.id, self.model.first_name, self.model.last_name)

        results = (await self.db.execute(stmt)).mappings().all()

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

    async def update(self):
        return

    async def delete(self):
        return
