from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select, Select, func

from src.features.findings.infra.models import Action as ActionDB
from src.features.findings.application.dtos import (
    ActionDetails,
    PaginatedActionResponse,
    ActionListItem,
)
from src.features.findings.application.filters import ActionFilters
from src.core.pagination import Pagination
from src.infra.db.pagination import apply_pagination
from typing import Any


class ActionQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _apply_filters(self, stmt: Select[Any], filters: ActionFilters) -> Select[Any]:
        if filters.status:
            stmt = stmt.where(ActionDB.status == filters.status)
        return stmt

    async def list(
        self,
        pagination: Pagination,
        filters: ActionFilters,
        finding_id: UUID | None,
    ):

        if finding_id:
            total_count = (
                select(func.count())
                .select_from(ActionDB)
                .where(ActionDB.finding_id == finding_id)
            )
        else:
            total_count = select(func.count()).select_from(ActionDB)
        total_count = self._apply_filters(total_count, filters)
        total_items: int | None = await self.session.scalar(total_count)

        if not total_items:
            return PaginatedActionResponse(
                items=[],
                total=0,
                page=pagination.page,
                size=pagination.limit,
            )

        stmt = select(ActionDB)

        if finding_id:
            stmt = stmt.where(ActionDB.finding_id == finding_id)

        stmt = self._apply_filters(stmt, filters)
        stmt = apply_pagination(stmt, pagination)

        result = (await self.session.execute(stmt)).scalars().all()

        return PaginatedActionResponse(
            total=total_items,
            page=pagination.page,
            size=pagination.limit,
            items=[
                ActionListItem(
                    id=act.id,
                    title=act.title,
                    status=act.status,
                    estimated_completion_date=act.estimated_completion_date,
                    completion_date=act.completion_date,
                )
                for act in result
            ],
        )

    async def get_action_details(self, action_id: UUID) -> ActionDetails | None:
        stmt = select(ActionDB).where(ActionDB.id == action_id)

        res = (await self.session.execute(stmt)).scalar_one_or_none()

        if not res:
            return None

        return ActionDetails(
            id=res.id,
            title=res.title,
            finding_id=res.finding_id,
            status=res.status,
            estimated_completion_date=res.estimated_completion_date,
            completion_date=res.completion_date,
            created_at=res.created_at,
            updated_at=res.updated_at,
        )
