from fastapi import APIRouter, Depends
from uuid import UUID
from src.features.findings.api.dependencies.finding_deps import (
    get_finding_uc,
    get_finding_queries,
)
from src.features.findings.api.commands.finding_write import CreateFindingRequest
from src.features.findings.application.dtos.finding_dtos import CreateFinding
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
            description=data.description,
            finding_source=data.finding_source,
            department=data.department,
            deficiency_severity=data.deficiency_severity,
        ),
    )


@router.get("")
async def list_findings(
    queries: FindingQueryService = Depends(get_finding_queries),
):
    return await queries.list()


@router.get("/{finding_id}")
async def get_finding_details(
    finding_id: UUID,
    queries: FindingQueryService = Depends(get_finding_queries),
):
    return await queries.get_finding_details(finding_id)


@router.post("/{finding_id}/root_cause_analyses")
async def start_root_cause_analyses():
    return
