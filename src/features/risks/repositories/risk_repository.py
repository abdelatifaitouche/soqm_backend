from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from src.features.risks.models.risk import Risk as RiskDB
from src.features.risks.domain.risk import Risk as RiskEntity
from src.infra.db.exception_utils import translate_db_errors
from src.core.pagination import Pagination
from src.infra.db.pagination import apply_pagination, apply_ordering
from src.features.risks.filters.risk_filters import RiskFilters
from uuid import UUID
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class RiskRepository:
    model = RiskDB

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    def _to_orm(self, entity: RiskEntity) -> RiskDB:
        return RiskDB(
            id=entity.id,
            component_id=entity.component_id,
            objective_id=entity.objective_id,
            risk_ref=entity.risk_ref,
            risk_discription=entity.risk_discription,
            score=entity.score,
            occurence=entity.occurence,
            significance=entity.significance,
            status=entity.status,
            date_identified=entity.date_identified,
            date_last_assessed=entity.date_last_assessed,
            next_review_date=entity.next_review_date,
            residual_score=entity.residual_score,
            created_by=entity.created_by,
        )

    def _to_domain(self, orm: RiskDB, options: bool = False) -> RiskEntity:
        return RiskEntity(
            id=orm.id,
            objective_id=orm.objective_id,
            component_id=orm.component_id,
            risk_ref=orm.risk_ref,
            status=orm.status,
            occurence=orm.occurence,
            significance=orm.significance,
            score=orm.score,
            date_identified=orm.date_identified,
            date_last_assessed=orm.date_last_assessed,
            next_review_date=orm.next_review_date,
            residual_score=orm.residual_score,
            risk_discription=orm.risk_discription,
            created_by=orm.created_by,
            component=orm.component if options else None,
            objective=orm.objective if options else None,
        )

    async def create(self, entity: RiskEntity) -> RiskEntity:
        try:
            logger.debug("am i here ??")
            logger.debug(entity)
            orm: RiskDB = self._to_orm(entity)

            self.db.add(orm)

            await self.db.flush()
            await self.db.refresh(orm)
            return self._to_domain(orm)
        except Exception as e:
            raise translate_db_errors(e)

    def apply_filters(self, stmt, filters: RiskFilters):
        if filters.status:
            stmt = stmt.where(self.model.status == filters.status)

        if filters.component_id:
            stmt = stmt.where(self.model.component_id == filters.component_id)

        if filters.objective_id:
            stmt = stmt.where(self.model.objective_id == filters.objective_id)

        return stmt

    async def list(self, pagination: Pagination, filters: RiskFilters):
        stmt = select(
            self.model.id,
            self.model.risk_ref,
            self.model.score,
            self.model.occurence,
            self.model.significance,
            self.model.objective_id,
            self.model.risk_discription,
        )

        stmt = self.apply_filters(stmt, filters)
        stmt = apply_pagination(stmt, pagination)

        results = await self.db.execute(stmt)
        rows = results.mappings().all()

        return [
            {
                "id": r["id"],
                "risk_ref": r["risk_ref"],
                "score": r["score"],
                "occurence": r["occurence"],
                "significance": r["significance"],
                "objective_id": r["objective_id"],
                "risk_discription": r["risk_discription"],
            }
            for r in rows
        ]

    async def list_by_objective(self, objective_id: UUID):
        stmt = select(self.model).where(self.model.objective_id == objective_id)

        results = (await self.db.execute(stmt)).scalars().all()

        return [self._to_domain(risk, options=False) for risk in results]

    async def get_by_id(self, entity_id: UUID) -> RiskEntity | None:
        stmt = (
            select(self.model)
            .where(self.model.id == entity_id)
            .options(
                joinedload(
                    self.model.component,
                ),
                joinedload(
                    self.model.objective,
                ),
            )
        )

        result = await self.db.execute(stmt)

        data = result.scalar_one_or_none()

        return self._to_domain(data, options=True) if data else None

    async def update(self, entity: RiskEntity) -> RiskEntity:

        try:
            updated_risk = (
                await self.db.execute(
                    update(self.model)
                    .where(self.model.id == entity.id)
                    .values(
                        status=entity.status,
                        risk_ref=entity.risk_ref,
                        risk_discription=entity.risk_discription,
                        occurence=entity.occurence,
                        significance=entity.significance,
                        score=entity.score,
                        next_review_date=entity.next_review_date,
                        date_last_assessed=entity.date_last_assessed,
                        residual_score=entity.residual_score,
                        updated_at=datetime.now(),
                    )
                    .returning(self.model)
                )
            ).scalar_one()

            return self._to_domain(updated_risk)
        except Exception as e:
            raise translate_db_errors(e)
