from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Select, func
from sqlalchemy.orm import Load, joinedload
from uuid import UUID
from src.features.soqm_engine.infra.models import (
    QualityObjective as ObjectiveDB,
    SOQMComponent as ComponentDB,
)
from src.features.soqm_engine.application.dtos.objective_dtos import (
    ObjectiveDetails,
    ObjectiveList,
    PaginatedResponse,
    BaseObjective,
)
from src.infra.db.pagination import apply_pagination, apply_ordering
from src.core.pagination import Pagination
from src.features.soqm_engine.application.filters.objective_filters import (
    ObjectiveFilters,
)
from typing import Any
from src.features.soqm_engine.infra.models import SOQMComponent
from sqlalchemy.orm import joinedload, selectinload


class ObjectiveQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def apply_filters(
        self, stmt: Select[Any], filters: ObjectiveFilters
    ) -> Select[Any]:
        """NEEDS TO ADD ?search=objective_ref"""
        if filters.component_id:
            stmt = stmt.where(ObjectiveDB.component_id == filters.component_id)

        if filters.status:
            stmt = stmt.where(ObjectiveDB.status == filters.status.value)
        return stmt

    async def list_objectives(
        self, pagination: Pagination, filters: ObjectiveFilters
    ) -> PaginatedResponse:
        total_count = select(func.count()).select_from(ObjectiveDB)
        total_count = self.apply_filters(total_count, filters)
        total_items: int | None = await self.session.scalar(total_count)

        if not total_items:
            return PaginatedResponse(
                items=[],
                total=0,
                page=pagination.page,
                size=pagination.limit,
            )

        stmt = (
            select(
                ObjectiveDB.id,
                ObjectiveDB.status,
                ObjectiveDB.objective_reference,
                ObjectiveDB.review_date,
                SOQMComponent.name,
            )
            .join(SOQMComponent)
            .order_by(
                "objective_reference",
            )
        )
        stmt = self.apply_filters(stmt, filters)
        stmt = apply_pagination(stmt, pagination)

        results = (await self.session.execute(stmt)).mappings().all()

        items = [
            ObjectiveList(
                id=obj.id,
                status=obj.status,
                review_date=obj.review_date,
                objective_reference=obj.objective_reference,
                component_name=obj.name,
            )
            for obj in results
        ]

        return PaginatedResponse(
            total=total_items,
            items=items,
            page=pagination.page,
            size=pagination.limit,
        )

    async def get_objective_details(
        self, objective_id: UUID
    ) -> ObjectiveDetails | None:
        stmt = select(
            ObjectiveDB.id,
            ObjectiveDB.objective_reference,
            ObjectiveDB.description,
            ObjectiveDB.review_date,
            ObjectiveDB.component_id,
            ObjectiveDB.created_at,
            ObjectiveDB.updated_at,
            ObjectiveDB.status,
        ).where(ObjectiveDB.id == objective_id)

        objective = (await self.session.execute(stmt)).mappings().fetchone()

        if not objective:
            return None

        return ObjectiveDetails(**objective)

    async def list_options(self) -> list[BaseObjective]:
        stmt = select(
            ObjectiveDB.id,
            ObjectiveDB.objective_reference,
        )

        results = (await self.session.execute(stmt)).mappings().all()

        return [
            BaseObjective(
                id=obj.id,
                objective_reference=obj.objective_reference,
            )
            for obj in results
        ]
