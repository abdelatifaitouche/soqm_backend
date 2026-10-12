from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.findings.infra.models import Finding as FindingDB
from sqlalchemy import select
from src.features.findings.application.dtos.finding_dtos import (
    FindingListItem,
    FindingDetails,
)
from src.features.findings.domain.entities.finding import RootCauseAnalysis


class FindingQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self):
        stmt = select(
            FindingDB.id,
            FindingDB.status,
            FindingDB.finding_ref,
            FindingDB.deficiency_severity,
            FindingDB.finding_source,
        )

        result = (await self.session.execute(stmt)).mappings().all()

        return [FindingListItem(**f) for f in result]

    async def get_finding_details(self, finding_id: UUID):
        stmt = select(FindingDB).where(FindingDB.id == finding_id)

        res = (await self.session.execute(stmt)).scalar_one_or_none()

        if not res:
            return None
        root_cause_analysis = RootCauseAnalysis(
            cause_analysis_status=res.cause_analysis_status,
            analysis=res.analysis,
            category_id=res.category_id,
            indicator_id=res.indicator_id,
            potential_root_cause_id=res.potential_root_cause_id,
            soqm_component_id=res.soqm_component_id,
            analysis_completed_at=res.analysis_completed_at,
        )

        return FindingDetails(
            id=res.id,
            description=res.description,
            deficiency_severity=res.deficiency_severity,
            finding_ref=res.finding_ref,
            finding_source=res.finding_source,
            department=res.department,
            status=res.status,
            root_cause_analysis=root_cause_analysis,
            created_at=res.created_at,
            updated_at=res.updated_at,
        )
