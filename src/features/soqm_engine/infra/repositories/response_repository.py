from uuid import UUID
from src.features.soqm_engine.domain.entities.reponse import Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.soqm_engine.application.ports import IResponseRepository


class ResponseRepository(IResponseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, response: Response) -> None:
        pass

    async def get(self, response_id: UUID) -> Response | None:
        pass

    async def delete(self, response_id: UUID) -> None:
        pass
