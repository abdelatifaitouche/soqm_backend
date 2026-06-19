from src.features.risks.repositories.risk_response_repository import (
    RiskResponseRepository,
)
from src.features.risks.domain.risk_response import RiskResponse as ResponseEntity
from src.features.risks.schemas.risk_response import CreateRiskResponse, RiskResponse
from src.features.risks.repositories.risk_repository import RiskRepository
from uuid import UUID
from src.core.exceptions import NotFoundError
from src.core.pagination import Pagination


class ResponseService:
    def __init__(
        self,
        repo: RiskResponseRepository,
        risk_repo: RiskRepository,
    ):
        self.repo: RiskResponseRepository = repo
        self.risk_repo: RiskRepository = risk_repo

    async def list(self, risk_id: UUID, pagination: Pagination) -> list[ResponseEntity]:
        """THIS NEEDS TO BE DYNAMIC BASED ON THE USER"""
        return await self.repo.list(risk_id, pagination)

    async def create_response(
        self, risk_id: UUID, user_id: UUID, data: CreateRiskResponse
    ) -> ResponseEntity:

        risk = await self.risk_repo.get_by_id(risk_id)

        if not risk:
            raise NotFoundError(
                message=f"Risk with ID {risk_id} was not found",
            )

        response: ResponseEntity = ResponseEntity.response_create(
            risk_id=risk.id,
            response_description=data.response_description,
            evidence_notes=data.evidence_notes,
            response_type=data.response_type,
            created_by=user_id,
            responsible_employee=data.response_employee,
            date_implementation=data.date_implementation,
            date_monitored_design=data.date_monitored_design,
            date_monitored_operating=data.date_monitored_operating,
        )
        # this will emit an event here to be logged or notify (NOT IMPLEMENTED YET)
        return await self.repo.create(response)

    async def get_by_id(self, entity_id: UUID) -> ResponseEntity:

        response: ResponseEntity | None = await self.repo.get_by_id(entity_id)

        if not response:
            raise NotFoundError(
                message=f"Response with ID {entity_id} was not found",
            )

        return response
