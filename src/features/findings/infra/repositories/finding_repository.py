from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.findings.application.ports.ifinding_repository import (
    IFindingRepository,
)
from src.features.findings.domain.entities.finding import Finding, RootCauseAnalysis
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
                "cause_analysis_status": finding.root_cause_analysis.cause_analysis_status,
                "analysis": finding.root_cause_analysis.analysis,
                "category_id": finding.root_cause_analysis.category_id,
                "indicator_id": finding.root_cause_analysis.indicator_id,
                "potential_root_cause_id": finding.root_cause_analysis.potential_root_cause_id,
                "soqm_component_id": finding.root_cause_analysis.soqm_component_id,
                "analysis_completed_at": finding.root_cause_analysis.analysis_completed_at,
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
                "cause_analysis_status": finding.root_cause_analysis.cause_analysis_status,
                "analysis": finding.root_cause_analysis.analysis,
                "category_id": finding.root_cause_analysis.category_id,
                "indicator_id": finding.root_cause_analysis.indicator_id,
                "potential_root_cause_id": finding.root_cause_analysis.potential_root_cause_id,
                "soqm_component_id": finding.root_cause_analysis.soqm_component_id,
                "analysis_completed_at": finding.root_cause_analysis.analysis_completed_at,
            },
        )
        result = await self.session.execute(upsert_stmt)

    async def get(self, finding_id: UUID) -> Finding | None:
        stmt = select(FindingDB).where(FindingDB.id == finding_id)

        finding_orm = (await self.session.execute(stmt)).scalar_one_or_none()

        if not finding_orm:
            return None

        root_cause_analysis = RootCauseAnalysis(
            cause_analysis_status=finding_orm.cause_analysis_status,
            analysis=finding_orm.analysis,
            category_id=finding_orm.category_id,
            indicator_id=finding_orm.indicator_id,
            potential_root_cause_id=finding_orm.potential_root_cause_id,
            soqm_component_id=finding_orm.soqm_component_id,
            analysis_completed_at=finding_orm.analysis_completed_at,
        )

        return Finding(
            id=finding_orm.id,
            finding_ref=finding_orm.finding_ref,
            description=finding_orm.description,
            finding_source=finding_orm.finding_source,
            department=finding_orm.department,
            deficiency_severity=finding_orm.deficiency_severity,
            status=finding_orm.status,
            root_cause_analysis=root_cause_analysis,
            created_at=finding_orm.created_at,
            updated_at=finding_orm.updated_at,
        )
