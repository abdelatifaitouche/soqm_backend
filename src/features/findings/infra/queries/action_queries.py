from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select, Select, func
from sqlalchemy.orm import selectinload, joinedload

from src.features.findings.infra.models import Action as ActionDB
from src.features.findings.application.dtos import (
    ActionDetails,
    PaginatedActionResponse,
    ActionListItem,
    EmployeeItem,
)
from src.features.findings.application.filters import ActionFilters
from src.core.pagination import Pagination
from src.infra.db.pagination import apply_pagination
from src.features.organizations.infra.models import Employee as EmployeeDB
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
                .where(ActionDB.finding_id == finding_id, ActionDB.soft_delete == False)
            )
        else:
            total_count = (
                select(func.count())
                .select_from(ActionDB)
                .where(ActionDB.soft_delete == False)
            )
        total_count = self._apply_filters(total_count, filters)
        total_items: int | None = await self.session.scalar(total_count)

        if not total_items:
            return PaginatedActionResponse(
                items=[],
                total=0,
                page=pagination.page,
                size=pagination.limit,
            )

        stmt = (
            select(
                ActionDB.id,
                ActionDB.title,
                ActionDB.status,
                ActionDB.completion_date,
                ActionDB.estimated_completion_date,
                EmployeeDB.id.label("employee_id"),
                EmployeeDB.first_name,
                EmployeeDB.last_name,
            )
            .outerjoin(ActionDB.owner)
            .where(ActionDB.soft_delete == False)
        )

        if finding_id:
            stmt = stmt.where(ActionDB.finding_id == finding_id)

        stmt = self._apply_filters(stmt, filters)
        stmt = apply_pagination(stmt, pagination)

        result = (await self.session.execute(stmt)).all()

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
                    owner=EmployeeItem(
                        id=act.employee_id,
                        first_name=act.first_name,
                        last_name=act.last_name,
                    ),
                )
                for act in result
            ],
        )

    async def get_action_details(self, action_id: UUID) -> ActionDetails | None:

        stmt = (
            select(ActionDB)
            .where(
                ActionDB.id == action_id,
                ActionDB.soft_delete == False,
            )
            .options(
                joinedload(ActionDB.owner)
            )  # LEFT OUTER JOIN under the hood for nullable FK
        )
        res = (await self.session.execute(stmt)).scalar_one_or_none()
        if not res:
            return None

        owner = (
            EmployeeItem(
                id=res.owner.id,
                first_name=res.owner.first_name,
                last_name=res.owner.last_name,
            )
            if res.owner
            else None
        )

        return ActionDetails(
            id=res.id,
            title=res.title,
            finding_id=res.finding_id,
            status=res.status,
            estimated_completion_date=res.estimated_completion_date,
            completion_date=res.completion_date,
            owner=owner,
            created_at=res.created_at,
            updated_at=res.updated_at,
        )
