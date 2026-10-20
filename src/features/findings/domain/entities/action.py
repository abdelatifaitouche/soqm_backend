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
    soft_delete: bool
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
            soft_delete=False,
        )

        return action

    def update(
        self,
        title: str | None,
        estimated_completion_date: datetime | None,
        finding_id: UUID | None,
    ):

        if self.soft_delete:
            raise Exception("Invalid Action State : Deleted")

        if title and title.strip() != "":
            self.title = title

        if estimated_completion_date and estimated_completion_date > datetime.now():
            self.estimated_completion_date = estimated_completion_date

        if finding_id:
            self.finding_id = finding_id

    def start(self):
        if self.status != ActionState.DRAFT or self.soft_delete:
            raise Exception("Invalid Action state")

        self.status = ActionState.IN_PROGRESS
        self.updated_at = datetime.now()

    def mark_as_draft(self):
        if self.status == ActionState.DRAFT or self.soft_delete:
            raise Exception("Invalid Action State")

        self.status = ActionState.DRAFT
        self.updated_at = datetime.now()

    def complete(self):
        if self.status != ActionState.IN_PROGRESS or self.soft_delete:
            raise Exception("Invalid Action State")
        self.status = ActionState.COMPLETED
        self.completion_date = datetime.now()
        self.updated_at = datetime.now()

    def mark_as_deleted(self):
        if self.status != ActionState.DRAFT or self.soft_delete:
            raise Exception("Cannot delete non draft actions")
        self.soft_delete = True
        self.updated_at = datetime.now()
