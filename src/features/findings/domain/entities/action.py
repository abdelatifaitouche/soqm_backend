from dataclasses import dataclass, field
from uuid import uuid4, UUID
from datetime import datetime
from src.features.findings.domain.enums import ActionState
from .action_completion_evidence import ActionCompletionEvidence
from enum import StrEnum


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
    owner_id: UUID | None = None

    action_completion_evidences: list[ActionCompletionEvidence] = field(
        default_factory=list
    )

    @classmethod
    def create(
        cls,
        *,
        finding_id: UUID,
        title: str,
        estimated_completion_date: datetime,
        owner_id: UUID,
    ) -> "Action":
        if estimated_completion_date <= datetime.now():
            raise Exception("Invalid time")

        action = cls(
            id=uuid4(),
            title=title,
            finding_id=finding_id,
            estimated_completion_date=estimated_completion_date,
            status=ActionState.DRAFT,
            owner_id=owner_id,
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
        owner_id: UUID | None = None,
    ):

        if self.soft_delete:
            raise Exception("Invalid Action State : Deleted")

        if title and title.strip() != "":
            self.title = title

        if estimated_completion_date and estimated_completion_date > datetime.now():
            self.estimated_completion_date = estimated_completion_date

        if finding_id:
            self.finding_id = finding_id

        if owner_id:
            self.owner_id = owner_id

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

        if (
            not self.action_completion_evidences
            or len(self.action_completion_evidences) == 0
        ):
            raise Exception(
                "Cannot complete an action without evidences",
            )
        self.status = ActionState.COMPLETED
        self.completion_date = datetime.now()
        self.updated_at = datetime.now()

    def mark_as_deleted(self):
        if self.status != ActionState.DRAFT or self.soft_delete:
            raise Exception("Cannot delete non draft actions")
        self.soft_delete = True
        self.updated_at = datetime.now()

    def submit_new_evidence(self, evidence_title: str, evidence_description: str):
        if self.status != ActionState.IN_PROGRESS:
            raise Exception(
                "Cannot add evidence to a completed action",
            )
        new_evidence = ActionCompletionEvidence.create(
            action_id=self.id,
            title=evidence_title,
            description=evidence_description,
        )
        self.action_completion_evidences.append(new_evidence)

        return new_evidence.id

    def accept_action_evidence(self, evidence_id: UUID):
        if self.status != ActionState.IN_PROGRESS:
            raise Exception("Cannot accept action to a completed action")

        if not self.action_completion_evidences:
            raise

        evidence = next(
            (ev for ev in self.action_completion_evidences if ev.id == evidence_id),
            None,
        )

        if not evidence:
            raise Exception("No matching evidence for this action")

        evidence.accept_evidence()

    def review_action_completion_evidence(
        self,
        evidence_id: UUID,
        decision: bool,
        comment: str,
    ):
        return
