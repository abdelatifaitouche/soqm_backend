from src.core.shared.interfaces.unit_of_work import IUnitOfWork
from src.features.findings.application.ports.ifinding_repository import (
    IFindingRepository,
)
from src.features.findings.application.dtos.finding_dtos import CreateFinding
from src.features.findings.domain.entities.finding import Finding


class FindingUC:
    def __init__(self, uow: IUnitOfWork, repo: IFindingRepository):
        self.uow = uow
        self.repo = repo

    async def identify_finding(self, finding_data: CreateFinding):
        async with self.uow:
            finding = Finding.create(
                finding_ref="",
                description=finding_data.description,
                finding_source=finding_data.finding_source,
                department=finding_data.department,
                deficiency_severity=finding_data.deficiency_severity,
            )

            await self.repo.save(finding)
