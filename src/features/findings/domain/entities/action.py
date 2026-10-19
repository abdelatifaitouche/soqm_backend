from dataclasses import dataclass
from uuid import uuid4, UUID
from datetime import datetime
from src.features.findings.domain.enums import ActionState


@dataclass
class Action:
    id: UUID
    finding_id: UUID
    title: str
    status: ActionState
    estimated_completion_date: datetime
    created_at: datetime
    updated_at: datetime

    completion_date: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        finding_id: UUID,
        title: str,
        estimated_completion_date: datetime,
    ) -> "Action":
        if estimated_completion_date <= datetime.now():
            raise Exception("Invalid time")

        action = cls(
            id=uuid4(),
            title=title,
            finding_id=finding_id,
            estimated_completion_date=estimated_completion_date,
            status=ActionState.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return action

    def update(
        self,
        title: str | None,
        estimated_completion_date: datetime | None,
        finding_id: UUID | None,
    ):

        if self.status == ActionState.COMPLETED:
            raise Exception(
                "Cannot Update a completed action",
            )

        if title and title.strip() != "":
            self.title = title

        if estimated_completion_date and estimated_completion_date > datetime.now():
            self.estimated_completion_date = estimated_completion_date

        if finding_id:
            self.finding_id = finding_id

    def start(self):
        if self.status != ActionState.DRAFT:
            raise Exception("Invalid Action state")

        self.status = ActionState.IN_PROGRESS
        self.updated_at = datetime.now()

    def complete(self):
        if self.status != ActionState.IN_PROGRESS:
            raise Exception("Invalid Action State")
        self.status = ActionState.COMPLETED
        self.completion_date = datetime.now()
        self.updated_at = datetime.now()
