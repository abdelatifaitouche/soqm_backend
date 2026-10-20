from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.core.pagination import Pagination
from src.features.findings.api.commands.finding_write import (
    UpdateFindingRequest,
    CreateFindingRequest,
    StartRootCauseAnalysisRequest,
)
from src.features.findings.api.dependencies.finding_deps import (
    get_finding_queries,
    get_finding_uc,
)
from src.features.findings.application.dtos.finding_dtos import (
    CreateFinding,
    UpdateFinding,
)
from src.features.findings.application.dtos.root_cause_analysis import (
    CreateRootCauseAnalysis,
)
from src.features.findings.application.filters.finding_filters import FindingFilters
from src.features.findings.application.usecases.finding_uc import FindingUC
from src.features.findings.infra.queries.finding_queries import FindingQueryService

router = APIRouter(prefix="/finding")


@router.post("")
async def identify_finding(
    data: CreateFindingRequest,
    uc: FindingUC = Depends(get_finding_uc),
):
    return await uc.identify_finding(
        finding_data=CreateFinding(
            finding_title=data.finding_title,
            description=data.description,
            finding_source=data.finding_source,
            department=data.department,
            deficiency_severity=data.deficiency_severity,
        ),
    )


@router.get("")
async def list_findings(
    pagination: Pagination = Depends(),
    filters: FindingFilters = Depends(),
    queries: FindingQueryService = Depends(get_finding_queries),
):
    return await queries.list(pagination, filters)


@router.get("/{finding_id}")
async def get_finding_details(
    finding_id: UUID,
    queries: FindingQueryService = Depends(get_finding_queries),
):
    return await queries.get_finding_details(finding_id)


@router.patch("/{finding_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_finding(
    finding_id: UUID,
    data: UpdateFindingRequest,
    uc: FindingUC = Depends(get_finding_uc),
):
    await uc.update(
        finding_id,
        UpdateFinding(
            finding_title=data.finding_title,
            finding_source=data.finding_source,
            description=data.description,
        ),
    )


@router.patch("/{finding_id}/root_cause_analyses")
async def start_root_cause_analyses(
    finding_id: UUID,
    root_cause_analysis: StartRootCauseAnalysisRequest,
    uc: FindingUC = Depends(get_finding_uc),
):
    return await uc.start_root_cause_analysis(
        finding_id=finding_id,
        root_cause_analysis=CreateRootCauseAnalysis(
            analysis=root_cause_analysis.analysis,
            category_id=root_cause_analysis.category_id,
            potential_root_cause_id=root_cause_analysis.potential_root_cause_id,
            indicator_id=root_cause_analysis.indicator_id,
            component_id=root_cause_analysis.component_id,
        ),
    )
