from abc import ABC, abstractmethod
from uuid import UUID
from src.features.soqm_components.application.dtos.component_dto import (
    SOQMComponentDetails,
)


class IComponentQueryService:
    async def get_component_details(
        self, component_id: UUID
    ) -> SOQMComponentDetails | None:
        pass
