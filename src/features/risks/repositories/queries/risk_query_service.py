from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Select, func
from src.features.risks.models.risk import Risk as RiskDB, RISK_ORDER_FIELDS
from src.features.risks.filters.risk_filters import (
    RiskFilters,
)
from typing import Any
from src.core.pagination import Pagination
from src.core.ordering import apply_ordering, resolve_order_column, OrderBy
from src.infra.db.pagination import apply_pagination
from src.features.risks.services.risk_dto import PaginatedResponse, RiskList


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

    async def list_options(self, filters: RiskFilters):
        stmt = select(RiskDB.id, RiskDB.risk_ref, RiskDB.score)
        stmt = self.apply_filters(stmt, filters)

        results = (await self.db.execute(stmt)).mappings().all()

        return [
            {"id": res["id"], "risk_ref": res["risk_ref"], "score": res["score"]}
            for res in results
        ]

    async def list(
        self,
        pagination: Pagination,
        filters: RiskFilters,
        order: OrderBy,
    ):

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

        items = [
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

    """
    async def list_by_objective(self, objective_id: UUID):

        stmt = (
            select(self.model)
            .join(RiskObjectiveAssociation)
            .where(
                RiskObjectiveAssociation.objective_id == objective_id,
            )
        )

        results = (await self.db.execute(stmt)).scalars().all()

        return [self._to_domain(risk, options=False) for risk in results]

    async def get_risk_details(self, entity_id: UUID):
        from src.features.quality_objectives.models.quality_objective import (
            QualityObjective,
        )
        from src.features.risks.models.risk_objective_association import (
            RiskObjectiveAssociation,
        )
        from sqlalchemy.orm import selectinload

        risk = await self.db.get(
            self.model,
            entity_id,
            options=[
                selectinload(self.model.objective_association)
                .selectinload(RiskObjectiveAssociation.objective)
                .load_only(
                    QualityObjective.id,
                    QualityObjective.objective_reference,
                    QualityObjective.status,
                ),
                selectinload(self.model.component),
            ],
        )
        from typing import Any

        if not risk:
            return
        risk_details: dict[str, Any] = {
            "score": risk.score,
            "id": risk.id,
            "risk_discription": risk.risk_discription,
            "date_last_assessed": risk.date_last_assessed,
            "occurence": risk.occurence,
            "next_review_date": risk.next_review_date,
            "significance": risk.significance,
            "created_by": risk.created_by,
            "date_identified": risk.date_identified,
            "status": risk.status,
            "created_at": risk.created_at,
            "updated_at": risk.updated_at,
            "risk_ref": risk.risk_ref,
            "residual_score": risk.residual_score,
            "component": risk.component,
        }

        objectives: list[dict[str, Any]] = [
            {
                "objective_id": obj.objective.id,
                "status": obj.objective.status,
                "objective_reference": obj.objective.objective_reference,
            }
            for obj in risk.objective_association
        ]

        risk_details["objectives"] = objectives

        return risk_details

        """
