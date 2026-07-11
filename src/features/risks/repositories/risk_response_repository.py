from sqlalchemy.ext.asyncio import AsyncSession
from src.features.risks.models.risk_response import RiskResponse as ResponseDB
from src.features.risks.domain.risk_response import RiskResponse as ResponseEntity
from src.infra.db.exception_utils import translate_db_errors
from sqlalchemy import select, Select
from sqlalchemy.orm import joinedload
from src.core.pagination import Pagination
from src.infra.db.pagination import apply_pagination
from uuid import UUID
from src.features.risks.filters.response_filters import ResponseFilters
from typing import Any
from src.features.risks.models.risk_response_association import RiskResponseAssociation


class RiskResponseRepository:
    model = ResponseDB

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    def _to_orm(self, entity: ResponseEntity) -> ResponseDB:
        return ResponseDB(
            id=entity.id,
            response_name=entity.response_name,
            response_ref=entity.response_ref,
            created_by=entity.created_by,
            date_implementation=entity.date_implementation,
            date_monitored_design=entity.date_monitored_design,
            evidence_notes=entity.evidence_notes,
            response_type=entity.response_type,
            status=entity.status,
            date_monitored_operating=entity.date_monitored_operating,
            owner=entity.owner,
            response_description=entity.response_description,
            component_id=entity.component_id,
            frequency=entity.frequency,
            execution_type=entity.execution_type,
        )

    def _to_domain(self, orm: ResponseDB, options: bool = False) -> ResponseEntity:
        return ResponseEntity(
            id=orm.id,
            response_ref=orm.response_ref,
            owner=orm.owner,
            response_name=orm.response_name,
            component_id=orm.component_id,
            response_description=orm.response_description,
            status=orm.status,
            created_by=orm.created_by,
            evidence_notes=orm.evidence_notes,
            date_implementation=orm.date_implementation,
            date_monitored_design=orm.date_monitored_design,
            date_monitored_operating=orm.date_monitored_operating,
            response_type=orm.response_type,
            frequency=orm.frequency,
            execution_type=orm.execution_type,
        )

    async def create(self, entity: ResponseEntity) -> ResponseEntity:
        try:
            orm = self._to_orm(entity)
            self.db.add(orm)

            if entity.risks:
                self.db.add_all(
                    [
                        RiskResponseAssociation(
                            risk_id=r,
                            response_id=orm.id,
                        )
                        for r in entity.risks
                    ]
                )

            await self.db.flush()
            return self._to_domain(orm, options=False)
        except Exception as e:
            raise translate_db_errors(e)

    async def get_by_id(self, entity_id: UUID) -> ResponseEntity | None:
        stmt = select(self.model).where(self.model.id == entity_id)

        result = (await self.db.execute(stmt)).scalar_one_or_none()

        if not result:
            return None

        return self._to_domain(result, options=True)

    async def update(self):
        return

    async def delete(self):
        return
