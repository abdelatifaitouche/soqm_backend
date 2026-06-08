from src.features.soqm_components.repositories.components_repository import (
    ComponentRepository,
)
from src.features.soqm_components.domain.component import SOQMComponent


class ComponentService:
    def __init__(self, repo: ComponentRepository):
        self.repo: ComponentRepository = repo

    async def list(self) -> list[SOQMComponent]:
        return await self.repo.list()
