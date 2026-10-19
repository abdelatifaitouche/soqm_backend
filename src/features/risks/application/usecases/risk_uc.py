from src.core.shared.interfaces.unit_of_work import IUnitOfWork
from src.features.risks.application.dtos.risk_dtos import CreateRisk as CreateRiskDTO
from src.features.risks.application.ports.irisk_repo import IRiskRepository
from src.features.risks.domain.entities.risk import Risk


class RiskUC:
    def __init__(self, uow: IUnitOfWork, risk_repo: IRiskRepository):
        self.risk_repo = risk_repo
        self.uow = uow

    async def create_risk(self, data: CreateRiskDTO):

        async with self.uow:
            risk = Risk.create()

            await self.risk_repo.save(risk)

            pass
