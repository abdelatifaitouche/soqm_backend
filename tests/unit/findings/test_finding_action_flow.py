import pytest
from src.features.findings.domain.entities.action import (
    ActionCompletionEvidence,
    ActionState,
    Action,
)
from src.features.findings.domain.entities.action_completion_evidence import (
    ActionCompletionEvidence,
)
from uuid import uuid4
from datetime import datetime


@pytest.fixture()
def action():
    new_action = Action.create(
        finding_id=uuid4(),
        title="action_title",
        owner_id=uuid4(),
        estimated_completion_date=datetime(2027, 2, 2),
    )
    return new_action


class TestFindingActionFlow:
    def test_action_creation(self):
        action = Action.create(
            finding_id=uuid4(),
            title="action_title",
            owner_id=uuid4(),
            estimated_completion_date=datetime(2027, 2, 2),
        )

        assert action.title == "action_title"
        assert action.estimated_completion_date > datetime.now()
        assert action.status == ActionState.DRAFT
        assert action.completion_date == None

    def test_should_transition_action_draft_to_inprogress(self, action: Action):
        action.start()

        assert action.status == ActionState.IN_PROGRESS

    def test_add_new_evidence_to_action(self, action: Action):

        ev = ActionCompletionEvidence.create(
            action.id, title="new_ev", description="new_ev"
        )

        action.start()

        action.submit_new_evidence(
            evidence_title="new_ev", evidence_description="some desc"
        )

        assert len(action.action_completion_evidences) > 0
        assert action.action_completion_evidences[0].title == "new_ev"

    def test_accept_actions_evidence(self, action: Action):
        action.start()

        ev_id = action.submit_new_evidence(
            evidence_title="new_ev", evidence_description="new_ev_desc"
        )

        action.accept_action_evidence(ev_id)
