from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.features.risks.models.risk import Risk as RiskDB
from src.features.risks.domain.risk import Risk as RiskEntity
from src.infra.db.exception_utils import translate_db_errors
from src.core.pagination import Pagination
from src.infra.db.pagination import apply_pagination, apply_ordering
from src.features.risks.filters.risk_filters import RiskFilters
from uuid import UUID


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
        )

    def _to_domain(self, orm: RiskDB) -> RiskEntity:
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
            component=orm.component,
            objective=orm.objective,
        )

    async def create(self, entity: RiskEntity) -> RiskEntity:
        try:
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

        if filters.score:
            stmt = stmt.where(self.model.score < filters.score)

        return stmt

    async def list(self, pagination: Pagination, filters: RiskFilters):
        """
        UPDATE THIS METHOD TO  :
            SELECT ONLY SOME COLUMNS, NOT ALL
            BUILDS AND RETURN a RiskSummary Dataclass for listing endpoint
        """

        stmt = select(self.model)

        stmt = self.apply_filters(stmt, filters)
        stmt = apply_pagination(stmt, pagination)

        stmt = apply_ordering(stmt, self.model, "created_at")

        results = await self.db.execute(stmt)

        data = results.scalars().all()

        return [self._to_domain(r) for r in data]

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

        return self._to_domain(data) if data else None
