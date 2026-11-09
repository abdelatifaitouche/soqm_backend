from dataclasses import dataclass
from uuid import UUID, uuid4
from src.features.findings.domain.enums import ActionEvidenceState
from datetime import datetime


@dataclass
class ActionCompletionEvidence:
    id: UUID
    action_id: UUID
    title: str
    description: str
    status: ActionEvidenceState

    created_at: datetime
    updated_at: datetime
    accepted_at: datetime | None = None

    @classmethod
    def create(cls, action_id, title, description):
        evidence = cls(
            id=uuid4(),
            action_id=action_id,
            title=title,
            description=description,
            status=ActionEvidenceState.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        return evidence

    def mark_for_validation(self):
        return

    def accept_evidence(self):
        if self.status != ActionEvidenceState.DRAFT:
            raise Exception("Cannot accept non draft evidence")

        self.status = ActionEvidenceState.ACCEPTED
        self.accepted_at = datetime.now()

    def reject_evidence(self):
        return
