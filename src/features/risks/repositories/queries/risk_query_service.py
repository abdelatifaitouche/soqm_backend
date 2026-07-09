from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Select, func, text
from src.features.risks.models.risk import Risk as RiskDB, RISK_ORDER_FIELDS
from src.features.risks.filters.risk_filters import (
    RiskFilters,
)
from typing import Any
from src.core.pagination import Pagination
from src.core.ordering import apply_ordering, resolve_order_column, OrderBy
from src.infra.db.pagination import apply_pagination
from src.features.risks.services.risk_dto import (
    PaginatedResponse,
    RiskList,
    RiskMatrix,
    RiskMatrixCell,
    RiskOption,
    Risk,
    ComponentSummary,
    ObjectiveSummary,
)
from src.features.quality_objectives.models.quality_objective import (
    QualityObjective,
)
from src.features.risks.models.risk_objective_association import (
    RiskObjectiveAssociation,
)
from uuid import UUID


class RiskQueryService:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    def apply_filters(self, stmt: Select[Any], filters: RiskFilters) -> Select[Any]:
        if filters.status:
            stmt = stmt.where(RiskDB.status == filters.status)

        if filters.component_id:
            stmt = stmt.where(RiskDB.component_id == filters.component_id)

        if filters.objective_id:
            stmt = stmt.where(RiskDB.objective_id == filters.objective_id)

        return stmt

    async def list_options(self, filters: RiskFilters) -> list[RiskOption]:
        stmt = select(RiskDB.id, RiskDB.risk_ref, RiskDB.score)
        stmt = self.apply_filters(stmt, filters)

        results = (await self.db.execute(stmt)).mappings().all()

        return [
            RiskOption(
                id=res["id"],
                risk_ref=res["risk_ref"],
                score=res["score"],
            )
            for res in results
        ]

    async def list(
        self,
        pagination: Pagination,
        filters: RiskFilters,
        order: OrderBy,
    ) -> PaginatedResponse:

        total_query = select(func.count()).select_from(RiskDB)
        total_result = await self.db.scalar(total_query)

        if not total_result:
            return PaginatedResponse(
                total=0,
                page=0,
                size=0,
                items=None,
            )

        stmt = select(
            RiskDB.id,
            RiskDB.risk_ref,
            RiskDB.score,
            RiskDB.occurence,
            RiskDB.significance,
            RiskDB.risk_discription,
            RiskDB.status,
        )

        stmt = self.apply_filters(stmt, filters)

        column = resolve_order_column(RiskDB, order.column, RISK_ORDER_FIELDS)
        stmt = apply_ordering(stmt, column, direction=order.direction)
        stmt = apply_pagination(stmt, pagination)

        results = (await self.db.execute(stmt)).mappings().all()

        items: list[RiskList] = [
            RiskList(
                id=r["id"],
                risk_ref=r["risk_ref"],
                score=r["score"],
                occurence=r["occurence"],
                significance=r["significance"],
                risk_description=r["risk_discription"],
                status=r["status"],
            )
            for r in results
        ]

        return PaginatedResponse(
            total=total_result,
            page=pagination.page,
            size=pagination.limit,
            items=items,
        )

    async def get_risk_matrix_summary(self) -> RiskMatrix:
        """
        Builds a 3 X 3 risk matrix (fixed by the isqm requirements)

        Returns:
            RiskMatrix object of  RiskMatrixCells, occurence/significance fetched
            calculate the total from the database otherwise set to 0
        """
        significance_range = range(1, 4)  # 1 to 3 values for significance
        occurence_range = range(1, 4)  # 1 to 3 values for occurence
        stmt = (
            select(
                RiskDB.occurence,
                RiskDB.significance,
                func.count(RiskDB.id).label("total"),
            )
            .select_from(RiskDB)
            .group_by(
                RiskDB.occurence,
                RiskDB.significance,
            )
        )

        result = (await self.db.execute(stmt)).mappings().all()

        total: int = sum(r.total for r in result)

        counts = {(r["occurence"], r["significance"]): r["total"] for r in result}

        cells = [
            RiskMatrixCell(
                occurence=occurence,
                significance=significance,
                percent=counts.get((occurence, significance), 0) / total * 100,
            )
            for occurence in range(1, 4)
            for significance in range(1, 4)
        ]

        return RiskMatrix(
            cells=cells,
        )

    async def get_risk_details(self, entity_id: UUID) -> Risk | None:
        from src.features.quality_objectives.models.quality_objective import (
            QualityObjective,
        )
        from src.features.risks.models.risk_objective_association import (
            RiskObjectiveAssociation,
        )
        from sqlalchemy.orm import selectinload

        risk = await self.db.get(
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

        risk_details: Risk = Risk(
            id=risk.id,
            risk_ref=risk.risk_ref,
            risk_discreption=risk.risk_discription,
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
        )

        return risk_details

    async def list_by_objective(self, objective_id: UUID):

        stmt = (
            select(RiskDB)
            .join(RiskObjectiveAssociation)
            .where(
                RiskObjectiveAssociation.objective_id == objective_id,
            )
        )

        results = (await self.db.execute(stmt)).scalars().all()

        return
