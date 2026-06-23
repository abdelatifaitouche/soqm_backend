from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, Select
from src.infra.db.exception_utils import translate_db_errors
from src.features.quality_objectives.domain.objective import (
    Objective as ObjectiveEntity,
    UpdateObjective as UpdateDTO,
)
from src.features.quality_objectives.models.quality_objective import (
    QualityObjective as ObjectiveDB,
)
from src.infra.db.pagination import apply_pagination, apply_ordering
from src.core.pagination import Pagination
from uuid import UUID
from src.core.exceptions import NotFoundError
from src.features.quality_objectives.enums.objective_states import ObjectiveState
from src.features.quality_objectives.filters.filters import ObjectiveFilters
from typing import Any


class ObjectiveRepository:
    model = ObjectiveDB

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    def _to_orm(self, entity: ObjectiveEntity) -> ObjectiveDB:
        return ObjectiveDB(
            id=entity.id,
            description=entity.description,
            component_id=entity.component_id,
            review_date=entity.review_date,
            objective_reference=entity.objective_reference,
            status=entity.status,
        )

    def _to_domain(self, orm: ObjectiveDB) -> ObjectiveEntity:
        return ObjectiveEntity(
            id=orm.id,
            description=orm.description,
            review_date=orm.review_date,
            status=orm.status,
            objective_reference=orm.objective_reference,
            component_id=orm.component_id,
            updated_at=orm.updated_at,
        )

    def apply_filters(
        self, stmt: Select[Any], filters: ObjectiveFilters
    ) -> Select[Any]:
        if filters.component_id:
            stmt = stmt.where(self.model.component_id == filters.component_id)

        if filters.status:
            stmt = stmt.where(self.model.status == filters.status.value)

        return stmt

    async def list(self, pagination: Pagination) -> list[ObjectiveEntity]:
        stmt = select(self.model)
        stmt = apply_pagination(stmt, pagination)
        stmt = apply_ordering(stmt, self.model, "created_at")

        results = await self.db.execute(stmt)

        data = results.scalars().all()
        if not data:
            return []

        return [self._to_domain(d) for d in data]

    async def list_options(self, filters: ObjectiveFilters):
        stmt = select(
            self.model.id,
            self.model.objective_reference,
        ).where(
            self.model.status.not_in(
                [ObjectiveState.DRAFT.value, ObjectiveState.SUSPENDED.value],
            )
        )
        stmt = self.apply_filters(stmt, filters)
        results = (await self.db.execute(stmt)).mappings().all()

        return [
            {
                "id": obj["id"],
                "objective_reference": obj["objective_reference"],
            }
            for obj in results
        ]

    async def list_by_component(self, component_id: UUID, pagination: Pagination):
        stmt = select(self.model).where(self.model.component_id == component_id)

        stmt = apply_pagination(stmt, pagination)

        results = (await self.db.execute(stmt)).scalars().all()

        return [self._to_domain(obj) for obj in results]

    async def create(self, entity: ObjectiveEntity) -> ObjectiveEntity:
        orm: ObjectiveDB = self._to_orm(entity)

        try:
            self.db.add(orm)
            await self.db.flush()
            return entity
        except Exception as e:
            raise translate_db_errors(e)

    async def get_by_id(self, entity_id: UUID) -> ObjectiveEntity | None:
        stmt = select(self.model).where(self.model.id == entity_id)

        result = await self.db.execute(stmt)

        data = result.scalar_one_or_none()

        if not data:
            return None

        return self._to_domain(data)

    async def delete(self, entity_id: UUID):
        try:
            stmt = delete(self.model).where(self.model.id == entity_id)
            await self.db.execute(stmt)
        except Exception as e:
            raise translate_db_errors(e)

    async def update(
        self,
        entity: ObjectiveEntity,
    ) -> ObjectiveEntity:
        try:
            result = await self.db.execute(
                update(self.model)
                .where(self.model.id == entity.id)
                .values(
                    description=entity.description,
                    review_date=entity.review_date,
                    status=entity.status,
                    component_id=entity.component_id,
                    updated_at=entity.updated_at,
                )
                .returning(self.model),
            )
            updated = result.scalar_one_or_none()

            if not updated:
                raise NotFoundError(
                    message=f"Objective {entity.id} not found",
                )
            return self._to_domain(updated)
        except Exception as e:
            raise translate_db_errors(e)
