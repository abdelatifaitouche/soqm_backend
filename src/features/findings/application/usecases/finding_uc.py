from src.core.shared.interfaces.unit_of_work import IUnitOfWork
from src.features.findings.application.dtos.finding_dtos import CreateFinding
from src.features.findings.domain.entities.finding import Finding
from src.features.findings.application.ports import (
    IFindingDeptSeqRepository,
    IFindingRepository,
)
from src.features.organizations.repositories.department_repository import (
    DepartmentRepository,
)
from uuid import UUID


class FindingUC:
    def __init__(
        self,
        uow: IUnitOfWork,
        repo: IFindingRepository,
        seq_repo: IFindingDeptSeqRepository,
        dept_repo: DepartmentRepository,
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
            dept = await self.dept_repo.get_by_id(finding_data.department)

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
            )

            await self.finding_repo.save(finding)
