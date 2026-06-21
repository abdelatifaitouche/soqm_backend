from sqlalchemy.ext.asyncio import AsyncSession
from src.features.risks.models.risk_response import RiskResponse as ResponseDB
from src.features.risks.domain.risk_response import RiskResponse as ResponseEntity
from src.infra.db.exception_utils import translate_db_errors
from sqlalchemy import select, Select
from sqlalchemy.orm import joinedload
from src.core.pagination import Pagination
from src.infra.db.pagination import apply_pagination
from uuid import UUID
from src.features.risks.filters.response_filters import ResponseFilters
from typing import Any


class RiskResponseRepository:
    model = ResponseDB

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    def _to_orm(self, entity: ResponseEntity) -> ResponseDB:
        return ResponseDB(
            id=entity.id,
            risk_id=entity.risk_id,
            created_by=entity.created_by,
            date_implementation=entity.date_implementation,
            date_monitored_design=entity.date_monitored_design,
            evidence_notes=entity.evidence_notes,
            response_type=entity.response_type,
            status=entity.status,
            date_monitored_operating=entity.date_monitored_operating,
            responsible_employee=entity.responsible_employee,
            response_description=entity.response_description,
        )

    def _to_domain(self, orm: ResponseDB) -> ResponseEntity:
        return ResponseEntity(
            id=orm.id,
            risk_id=orm.risk_id,
            response_description=orm.response_description,
            status=orm.status,
            created_by=orm.created_by,
            evidence_notes=orm.evidence_notes,
            responsible_employee=orm.responsible_employee,
            date_implementation=orm.date_implementation,
            date_monitored_design=orm.date_monitored_design,
            date_monitored_operating=orm.date_monitored_operating,
            response_type=orm.response_type,
            risk=orm.risk,
        )

    async def create(self, entity: ResponseEntity) -> ResponseEntity:
        try:
            orm = self._to_orm(entity)
            self.db.add(orm)
            await self.db.flush()
            await self.db.refresh(orm)
            return self._to_domain(orm)
        except Exception as e:
            raise translate_db_errors(e)

    def apply_filters(self, stmt: Select[Any], filters: ResponseFilters) -> Select[Any]:

        if filters.risk_id:
            stmt = stmt.where(self.model.risk_id == filters.risk_id)

        if filters.status:
            stmt = stmt.where(self.model.status == filters.status)

        if filters.created_by:
            stmt = stmt.where(self.model.created_by == filters.created_by)

        if filters.assigned_employee:
            stmt = stmt.where(
                self.model.responsible_employee == filters.assigned_employee
            )

        return stmt

    async def list(self, pagination: Pagination, filters: ResponseFilters):
        stmt = select(
            self.model.id,
            self.model.risk_id,
            self.model.status,
            self.model.response_type,
            self.model.responsible_employee,
            self.model.response_description,
        )
        stmt = self.apply_filters(stmt, filters)
        stmt = apply_pagination(stmt, pagination)

        results = await self.db.execute(stmt)
        rows = results.mappings().all()

        return [
            {
                "id": resp["id"],
                "risk_id": resp["risk_id"],
                "status": resp["status"],
                "response_type": resp["response_type"],
                "responsible_employee": resp["responsible_employee"],
                "response_description": resp["response_description"],
            }
            for resp in rows
        ]

    async def get_by_id(self, entity_id: UUID) -> ResponseEntity | None:
        stmt = (
            select(self.model)
            .where(self.model.id == entity_id)
            .options(
                joinedload(self.model.risk),
            )
        )

        result = (await self.db.execute(stmt)).scalar_one_or_none()

        if not result:
            return None

        return self._to_domain(result)

    async def update(self):
        return

    async def delete(self):
        return
