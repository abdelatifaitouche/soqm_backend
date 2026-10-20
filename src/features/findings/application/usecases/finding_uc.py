from uuid import UUID

from src.core.shared.interfaces.unit_of_work import IUnitOfWork
from src.features.findings.application.dtos import (
    UpdateFinding,
    CreateFinding,
    CreateRootCauseAnalysis,
)
from src.features.findings.application.ports import (
    IFindingDeptSeqRepository,
    IFindingRepository,
)
from src.features.findings.domain.entities.finding import Finding, RootCauseAnalysis
from src.features.organizations.application.ports import IDepartmentRepository


class FindingUC:
    def __init__(
        self,
        uow: IUnitOfWork,
        repo: IFindingRepository,
        seq_repo: IFindingDeptSeqRepository,
        dept_repo: IDepartmentRepository,
    ):
        self.uow = uow
        self.finding_repo = repo
        self.seq_repo = seq_repo
        self.dept_repo = dept_repo

    def _generate_finding_ref(self, dept_name: str) -> str:
        words = dept_name.split()

        if len(words) >= 2:
            return "".join(word[0] for word in words[:2]).upper()

        return words[0][:2].upper() if words else ""

    async def identify_finding(self, finding_data: CreateFinding):
        async with self.uow:
            dept = await self.dept_repo.get(finding_data.department)

            if not dept:
                raise Exception("Invalid Department")

            seq_num = await self.seq_repo.inc_get(finding_data.department)

            ref = self._generate_finding_ref(dept.name)

            finding = Finding.create(
                finding_ref=ref + str(seq_num),
                description=finding_data.description,
                finding_source=finding_data.finding_source,
                department=finding_data.department,
                deficiency_severity=finding_data.deficiency_severity,
                finding_title=finding_data.finding_title,
            )

            await self.finding_repo.save(finding)

    async def get(self, finding_id: UUID):

        finding = await self.finding_repo.get(finding_id)

        if not finding:
            raise Exception()

        return finding

    async def update(self, finding_id: UUID, update_data: UpdateFinding):
        async with self.uow:
            finding = await self.get(finding_id)

            finding.update(
                finding_title=update_data.finding_title,
                description=update_data.description,
                finding_source=update_data.finding_source,
            )

            await self.finding_repo.save(finding)

    async def start_root_cause_analysis(
        self, finding_id: UUID, root_cause_analysis: CreateRootCauseAnalysis
    ):
        async with self.uow:
            finding = await self.get(finding_id)

            root_cause = RootCauseAnalysis(
                analysis=root_cause_analysis.analysis,
                category_id=root_cause_analysis.category_id,
                indicator_id=root_cause_analysis.indicator_id,
                potential_root_cause_id=root_cause_analysis.potential_root_cause_id,
                soqm_component_id=root_cause_analysis.component_id,
            )

            finding.start_root_cause_analysis(root_cause)

            await self.finding_repo.save(finding)
