from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.findings.infra.models import Finding as FindingDB
from sqlalchemy import select, Select, func
from src.features.findings.application.dtos.finding_dtos import (
    FindingListItem,
    FindingDetails,
    PaginatedResponse,
)
from src.features.findings.domain.entities.finding import RootCauseAnalysis
from src.core.pagination import Pagination
from src.infra.db.pagination import apply_pagination
from src.features.findings.application.filters.finding_filters import FindingFilters
from typing import Any


class FindingQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _apply_filters(self, stmt: Select[Any], filters: FindingFilters):
        if filters.status:
            stmt = stmt.where(FindingDB.status == filters.status)

        if filters.deficiency_severity:
            stmt = stmt.where(
                FindingDB.deficiency_severity == filters.deficiency_severity
            )

        if filters.finding_source:
            stmt = stmt.where(FindingDB.finding_source == filters.finding_source)

        return stmt

    async def list(self, pagination: Pagination, filters: FindingFilters):
        total_count = select(func.count()).select_from(FindingDB)
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
            FindingDB.id,
            FindingDB.status,
            FindingDB.finding_ref,
            FindingDB.deficiency_severity,
            FindingDB.finding_source,
        )

        stmt = self._apply_filters(stmt, filters)

        stmt = apply_pagination(stmt, pagination)

        result = (await self.session.execute(stmt)).mappings().all()

        return PaginatedResponse(
            total=total_items,
            page=pagination.page,
            size=pagination.limit,
            items=[FindingListItem(**f) for f in result],
        )

    async def get_finding_details(self, finding_id: UUID):
        stmt = select(FindingDB).where(FindingDB.id == finding_id)

        res = (await self.session.execute(stmt)).scalar_one_or_none()

        if not res:
            return None
        root_cause_analysis = RootCauseAnalysis(
            cause_analysis_status=res.cause_analysis_status,
            analysis=res.analysis,
            category_id=res.category_id,
            indicator_id=res.indicator_id,
            potential_root_cause_id=res.potential_root_cause_id,
            soqm_component_id=res.soqm_component_id,
            analysis_completed_at=res.analysis_completed_at,
        )

        return FindingDetails(
            id=res.id,
            description=res.description,
            deficiency_severity=res.deficiency_severity,
            finding_ref=res.finding_ref,
            finding_source=res.finding_source,
            department=res.department,
            status=res.status,
            root_cause_analysis=root_cause_analysis,
            created_at=res.created_at,
            updated_at=res.updated_at,
        )
