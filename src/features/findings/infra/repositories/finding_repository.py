from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from src.features.findings.application.ports.ifinding_repository import (
    IFindingRepository,
)
from src.features.findings.domain.entities.finding import Finding
from src.features.findings.infra.models import Finding as FindingDB


class FindingRepository(IFindingRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, finding: Finding):
        stmt = insert(FindingDB).values(
            {
                "id": finding.id,
                "finding_ref": finding.finding_ref,
                "description": finding.description,
                "finding_source": finding.finding_source,
                "status": finding.status,
                "department": finding.department,
                "deficiency_severity": finding.deficiency_severity,
            },
        )
        upsert_stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                "finding_ref": finding.finding_ref,
                "description": finding.description,
                "finding_source": finding.finding_source,
                "status": finding.status,
                "department": finding.department,
                "deficiency_severity": finding.deficiency_severity,
            },
        )
        result = await self.session.execute(upsert_stmt)

    async def get(self, finding_id: UUID) -> Finding | None:
        stmt = select(FindingDB).where(FindingDB.id == finding_id)

        finding_orm = (await self.session.execute(stmt)).scalar_one_or_none()

        if not finding_orm:
            return None

        return Finding(
            id=finding_orm.id,
            finding_ref=finding_orm.finding_ref,
            description=finding_orm.description,
            finding_source=finding_orm.finding_source,
            department=finding_orm.department,
            deficiency_severity=finding_orm.deficiency_severity,
            status=finding_orm.status,
            created_at=finding_orm.created_at,
            updated_at=finding_orm.updated_at,
        )
