from sqlalchemy.ext.asyncio import AsyncSession
from src.features.risks.models.risk_response import RiskResponse as ResponseDB
from src.features.risks.domain.risk_response import RiskResponse as ResponseEntity
from src.infra.db.exception_utils import translate_db_errors
from sqlalchemy import select
from src.core.pagination import Pagination
from src.infra.db.pagination import apply_pagination
from uuid import UUID


class RiskResponseRepository:
    model = ResponseDB

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    def _to_orm(self, entity: ResponseEntity) -> ResponseDB:
        return ResponseDB(
            id=entity.id,
            risk_id=entity.risk_id,
            created_by=entity.created_by,
            date_implementation=entity.date_implementation,
            date_monitored_design=entity.date_monitored_design,
            evidence_notes=entity.evidence_notes,
            response_type=entity.response_type,
            status=entity.status,
            date_monitored_operating=entity.date_monitored_operating,
            responsible_employee=entity.responsible_employee,
            response_description=entity.response_description,
        )

    def _to_domain(self, orm: ResponseDB) -> ResponseEntity:
        return ResponseEntity(
            id=orm.id,
            risk_id=orm.risk_id,
            response_description=orm.response_description,
            status=orm.status,
            created_by=orm.created_by,
            evidence_notes=orm.evidence_notes,
            responsible_employee=orm.responsible_employee,
            date_implementation=orm.date_implementation,
            date_monitored_design=orm.date_monitored_design,
            date_monitored_operating=orm.date_monitored_operating,
            response_type=orm.response_type,
        )

    async def create(self, entity: ResponseEntity) -> ResponseEntity:
        try:
            orm = self._to_orm(entity)
            self.db.add(orm)
            await self.db.flush()
            await self.db.refresh(orm)
            return self._to_domain(orm)
        except Exception as e:
            raise translate_db_errors(e)

    async def list(self, risk_id: UUID, pagination: Pagination):
        stmt = select(self.model).where(self.model.risk_id == risk_id)
        stmt = apply_pagination(stmt, pagination)

        results = (await self.db.execute(stmt)).scalars().all()

        return [self._to_domain(resp) for resp in results]

    async def get_by_id(self, entity_id: UUID) -> ResponseEntity | None:
        stmt = select(self.model).where(self.model.id == entity_id)

        result = (await self.db.execute(stmt)).scalar_one_or_none()

        if not result:
            return None

        return self._to_domain(result)

    async def update(self):
        return

    async def delete(self):
        return
