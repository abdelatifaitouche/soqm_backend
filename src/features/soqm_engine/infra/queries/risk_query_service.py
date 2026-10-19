from typing import Any
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.ordering import OrderBy, apply_ordering, resolve_order_column
from src.core.pagination import Pagination
from src.features.soqm_engine.application.dtos.risk_dtos import (
    ComponentSummary,
    ObjectiveSummary,
    PaginatedResponse,
    RiskList,
)
from src.features.soqm_engine.application.dtos.risk_dtos import (
    Risk as RiskDetails,
)
from src.features.soqm_engine.application.filters.risk_filters import RiskFilters
from src.features.soqm_engine.infra.models import (
    QualityObjective,
    RiskObjectiveAssociation,
    RiskResponseAssociation,
)
from src.features.soqm_engine.infra.models import (
    Risk as RiskDB,
)
from src.features.soqm_engine.infra.models.risk import RISK_ORDER_FIELDS
from src.infra.db.pagination import apply_pagination


class RiskQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _apply_filters(self, stmt: Select[Any], filters: RiskFilters) -> Select[Any]:
        if filters.status:
            stmt = stmt.where(RiskDB.status == filters.status)

        if filters.component_id:
            stmt = stmt.where(RiskDB.component_id == filters.component_id)
        if filters.response_id:
            stmt = stmt.where(
                select(RiskResponseAssociation.risk_id)
                .where(
                    RiskResponseAssociation.risk_id == RiskDB.id,
                    RiskResponseAssociation.response_id == filters.response_id,
                )
                .exists()
            )

        if filters.objective_id:
            stmt = stmt.where(
                select(RiskObjectiveAssociation.risk_id)
                .where(
                    RiskObjectiveAssociation.risk_id == RiskDB.id,
                    RiskObjectiveAssociation.objective_id == filters.objective_id,
                )
                .exists(),
            )

        return stmt

    async def list(
        self, pagination: Pagination, filters: RiskFilters, order: OrderBy
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
            RiskDB.date_identified,
        )

        stmt = self._apply_filters(stmt, filters)

        columns = resolve_order_column(RiskDB, order.columns, RISK_ORDER_FIELDS)

        stmt = apply_ordering(stmt, columns, direction=order.direction)

        stmt = apply_pagination(stmt, pagination)

        res = (await self.session.execute(stmt)).mappings().all()

        return PaginatedResponse(
            total=total_items,
            page=pagination.page,
            size=pagination.limit,
            items=[RiskList(**r) for r in res],
        )

    async def get_risk_details(self, entity_id: UUID) -> RiskDetails | None:

        risk = await self.session.get(
            RiskDB,
            entity_id,
            options=[
                selectinload(RiskDB.objective_association)
                .selectinload(RiskObjectiveAssociation.objective)
                .load_only(
                    QualityObjective.id,
                    QualityObjective.objective_reference,
                    QualityObjective.status,
                ),
                selectinload(RiskDB.component),
            ],
        )

        if not risk:
            return None
        objectives: list[ObjectiveSummary] = [
            ObjectiveSummary(
                id=obj.objective.id,
                status=obj.objective.status,
                objective_reference=obj.objective.objective_reference,
            )
            for obj in risk.objective_association
        ]

        component: ComponentSummary = ComponentSummary(
            id=risk.component.id,
            name=risk.component.name,
            description=risk.component.description,
        )

        risk_details = RiskDetails(
            id=risk.id,
            risk_ref=risk.risk_ref,
            risk_description=risk.risk_description,
            score=risk.score,
            occurence=risk.occurence,
            significance=risk.significance,
            status=risk.status,
            date_identified=risk.date_identified,
            next_review_date=risk.next_review_date,
            residual_score=risk.residual_score,
            date_last_assessed=risk.date_last_assessed,
            objectives=objectives,
            component=component,
            risk_rational=risk.risk_rational,
        )

        return risk_details
