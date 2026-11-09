import pytest
from uuid import uuid4
from sqlalchemy import select

from src.features.findings.domain.entities import Action
from src.features.findings.domain.enums import ActionState
from src.features.findings.infra.models import Action as ActionDB
from src.features.findings.infra.repositories import ActionRepository
from datetime import datetime


@pytest.mark.asyncio
class TestActionRepository:
    async def test_save_new_action(self, db_session):

        new_action = Action.create(
            finding_id=uuid4(),
            title="action_title",
            owner_id=uuid4(),
            estimated_completion_date=datetime(2028, 3, 3),
        )

        repo = ActionRepository(db_session)

        await repo.save(new_action)
        await db_session.commit()

        db_action = await repo.get(new_action.id)
        assert db_action is not None
        assert db_action.title == "action_title"
        assert db_action.action_completion_evidences == []

    async def test_start_action_save(self, db_session):

        new_action = Action.create(
            finding_id=uuid4(),
            title="action_title",
            owner_id=uuid4(),
            estimated_completion_date=datetime(2028, 3, 3),
        )

        repo = ActionRepository(db_session)
        await repo.save(new_action)
        await db_session.commit()
        inserted_action = await repo.get(new_action.id)

        assert inserted_action is not None

        inserted_action.start()

        await repo.save(inserted_action)
        await db_session.commit()
        db_session.expire_all()
        updated_action = await repo.get(inserted_action.id)

        assert updated_action is not None

        assert updated_action.status == ActionState.IN_PROGRESS

    async def test_add_new_evidence_to_action_and_persist(self, db_session):

        action = Action.create(
            finding_id=uuid4(),
            title="action_with_ev",
            owner_id=uuid4(),
            estimated_completion_date=datetime(2027, 8, 8),
        )

        repo = ActionRepository(db_session)

        await repo.save(action)
        await db_session.commit()

        act = await repo.get(action.id)

        assert act is not None
        assert act.action_completion_evidences == []
        act.start()

        await repo.save(act)
        await db_session.commit()

        started_act = await repo.get(act.id)
        assert started_act is not None
        assert started_act.status == ActionState.IN_PROGRESS
        started_act.submit_new_evidence(
            evidence_title="evidence_title",
            evidence_description="evidence_description",
        )
        await repo.save(started_act)
        await db_session.commit()

        db_session.expire_all()

        ev_action = await repo.get(started_act.id)
        assert ev_action is not None
        assert len(ev_action.action_completion_evidences) > 0
