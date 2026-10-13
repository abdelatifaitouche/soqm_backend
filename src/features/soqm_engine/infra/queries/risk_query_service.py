from src.features.soqm_engine.infra.models import Risk as RiskDB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Select, func
from src.core.pagination import Pagination
from src.infra.db.pagination import apply_pagination
from src.features.soqm_engine.application.filters.risk_filters import RiskFilters
from src.features.soqm_engine.application.dtos.risk_dtos import (
    RiskList,
    PaginatedResponse,
    Risk as RiskDetails,
)
from typing import Any
from uuid import UUID


class RiskQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _apply_filters(self, stmt: Select[Any], filters: RiskFilters) -> Select[Any]:
        if filters.status:
            stmt = stmt.where(RiskDB.status == filters.status)

        if filters.component_id:
            stmt = stmt.where(RiskDB.component_id == filters.component_id)

        return stmt

    async def list(
        self, pagination: Pagination, filters: RiskFilters
    ) -> PaginatedResponse:
        total_count = select(func.count()).select_from(RiskDB)
        total_count = self._apply_filters(total_count, filters)
        total_items: int | None = await self.session.scalar(total_count)

        if not total_items:
            return PaginatedResponse(
                items=[],
                total=0,
                page=pagination.page,
                size=pagination.limit,
            )

        stmt = select(
            RiskDB.id,
            RiskDB.risk_ref,
            RiskDB.significance,
            RiskDB.occurence,
            RiskDB.score,
            RiskDB.status,
            RiskDB.risk_description,
        )

        stmt = self._apply_filters(stmt, filters)

        stmt = apply_pagination(stmt, pagination)

        res = (await self.session.execute(stmt)).mappings().all()

        return PaginatedResponse(
            total=total_items,
            page=pagination.page,
            size=pagination.limit,
            items=[RiskList(**r) for r in res],
        )

    async def get_risk_details(self, risk_id: UUID):

        stmt = select(
            RiskDB.id,
            RiskDB.status,
            RiskDB.risk_ref,
            RiskDB.risk_description,
            RiskDB.score,
            RiskDB.occurence,
            RiskDB.significance,
            RiskDB.date_last_assessed,
            RiskDB.next_review_date,
            RiskDB.date_identified,
            RiskDB.residual_score,
            RiskDB.risk_rational,
        ).where(RiskDB.id == risk_id)

        res = (await self.session.execute(stmt)).mappings().one_or_none()

        if not res:
            return None

        return RiskDetails(**res)
