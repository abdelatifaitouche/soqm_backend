from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infra.db.exception_utils import translate_db_errors
from src.features.risks.models.risk_audit_log import RiskAuditLog as LogDB
from src.features.risks.domain.risk_audit_log import RiskAuditLog as LogEntity
from src.core.pagination import Pagination
from src.infra.db.pagination import apply_pagination


class RiskAuditLogRepository:
    model = LogDB

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    def _to_domain(self, orm: LogDB) -> LogEntity:
        return LogEntity(
            id=orm.id,
            changed_by=orm.changed_by,
            field_changed=orm.field_changed,
            change_comment=orm.change_comment,
            old_value=orm.old_value,
            new_value=orm.new_value,
            risk_id=orm.risk_id,
        )

    def _to_orm(self, entity: LogEntity) -> LogDB:
        return LogDB(
            id=entity.id,
            risk_id=entity.risk_id,
            change_comment=entity.change_comment,
            field_changed=entity.field_changed,
            new_value=entity.new_value,
            old_value=entity.old_value,
            changed_by=entity.changed_by,
        )

    async def create(self, entity: LogEntity):
        try:
            orm = self._to_orm(entity)
            self.db.add(orm)
            await self.db.flush()
        except Exception as e:
            raise translate_db_errors(e)

    async def list(self, pagination: Pagination):

        stmt = select(self.model).order_by(
            self.model.created_at.desc,
        )

        stmt = apply_pagination(stmt, pagination)

        results = (await self.db.execute(stmt)).scalars().all()

        return [self._to_domain(log) for log in results]

    async def get_by_id(self, log_id: UUID) -> LogEntity | None:

        stmt = select(self.model).where(self.model.id == log_id)

        result = (await self.db.execute(stmt)).scalar_one_or_none()

        if result is None:
            return None

        return self._to_domain(result)

    async def list_for_risk(self, risk_id: UUID, pagination: Pagination):
        """RISK EXISTANCE IS ASSURED BY THE CALLER"""
        stmt = (
            select(self.model)
            .where(self.model.risk_id == risk_id)
            .order_by(self.model.created_at.desc)
        )
        stmt = apply_pagination(stmt, pagination)
        results = (await self.db.execute(stmt)).scalars().all()

        return [self._to_domain(log) for log in results] if results else []
