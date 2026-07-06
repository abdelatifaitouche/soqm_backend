from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Select, func
from typing import Any
from src.features.quality_objectives.filters.filters import ObjectiveFilters
from src.features.quality_objectives.models.quality_objective import (
    QualityObjective as ObjectiveDB,
)
from uuid import UUID
from src.features.quality_objectives.enums.objective_states import ObjectiveState
from src.features.quality_objectives.services.dto import (
    BaseObjective,
    ObjectiveList,
    ObjectiveDetails,
    PaginatedResponse,
)
from src.infra.db.pagination import apply_pagination
from src.core.pagination import Pagination


class ObjectiveQueries:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_objective_details(
        self, objective_id: UUID
    ) -> ObjectiveDetails | None:
        """Might change by adding joints to component etc ... depends on what the UI needs"""
        stmt = select(ObjectiveDB).where(ObjectiveDB.id == objective_id)
        result = (await self.db.execute(stmt)).scalar_one_or_none()

        return (
            ObjectiveDetails(
                id=result.id,
                objective_reference=result.objective_reference,
                review_date=result.review_date,
                component_id=result.component_id,
                created_at=result.created_at,
                updated_at=result.updated_at,
                description=result.description,
                status=result.status,
            )
            if result
            else None
        )

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
        total_items: int | None = await self.db.scalar(total_count)

        if not total_items:
            return PaginatedResponse(
                items=[],
                total=0,
                page=pagination.page,
                size=pagination.limit,
            )
        from src.features.soqm_components.models.soqm_component import SOQMComponent
        from sqlalchemy.orm import joinedload, selectinload

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

        results = (await self.db.execute(stmt)).mappings().all()

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

    async def list_options(self, filters: ObjectiveFilters) -> list[BaseObjective]:
        stmt = select(
            ObjectiveDB.id,
            ObjectiveDB.objective_reference,
        ).where(
            ObjectiveDB.status.not_in(
                [ObjectiveState.DRAFT.value, ObjectiveState.SUSPENDED.value],
            )
        )
        stmt = self.apply_filters(stmt, filters)
        results = (await self.db.execute(stmt)).mappings().all()

        return [
            BaseObjective(
                id=obj.id,
                objective_reference=obj.objective_reference,
            )
            for obj in results
        ]

    async def list_by_component(self, component_id: UUID):
        stmt = select(ObjectiveDB).where(ObjectiveDB.component_id == component_id)
        results = (await self.db.execute(stmt)).scalars().all()
        return results
