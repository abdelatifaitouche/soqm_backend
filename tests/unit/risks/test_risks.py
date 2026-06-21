import pytest
from src.features.risks.domain.events.risk_events import RiskCreatedEvent
from src.features.risks.domain.risk import Risk
import uuid
from datetime import date


@pytest.fixture
def risk() -> Risk:
    return Risk.create(
        objective_id=uuid.uuid4(),
        component_id=uuid.uuid4(),
        created_by=uuid.uuid4(),
        risk_ref="test risk creation",
        risk_discription="test risk discreption",
        occurence=3,
        significance=3,
        next_review_date=date(2026, 9, 30),
    )


class TestRisk:
    def test_risk_creation(self, risk: Risk):
        assert risk.score == 9
        assert risk.score == risk.occurence * risk.significance

    def test_risk_event(self, risk: Risk):
        assert len(risk.get_events()) > 0

        events = risk.get_events()

        assert isinstance(events[0], RiskCreatedEvent)

        creation_event = events[0]

        assert creation_event.score == risk.score
        assert creation_event.occurence == risk.occurence
        assert creation_event.significance == risk.significance
