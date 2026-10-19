from src.features.findings.application.ports import IRcaTrackerRepository
from src.features.findings.domain.entities import RootCauseCategory
from src.core.shared.interfaces.unit_of_work import IUnitOfWork


class RcaTrackerUC:
    def __init__(self, uow: IUnitOfWork, repo: IRcaTrackerRepository):
        self.repo = repo
        self.uow = uow

    async def inject_data(self, categories: list[RootCauseCategory]):
        async with self.uow:
            await self.repo.bulk_insert(categories)
