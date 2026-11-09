from src.features.findings.application.ports import IActionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.findings.domain.entities import Action, ActionCompletionEvidence
from uuid import UUID
from src.features.findings.infra.models import (
    Action as ActionDB,
    ActionEvidence as ActionEvidenceDB,
)
from sqlalchemy.dialects.postgresql import insert
from dataclasses import asdict
from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete


class ActionRepository(IActionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, action: Action) -> None:
        values = asdict(action)
        action_completion_evidences = values.pop("action_completion_evidences")

        excluded_columns = {"created_at", "id", "action_completion_evidences"}
        set_ = {k: v for k, v in values.items() if k not in excluded_columns}
        insert_stmt = (
            insert(ActionDB)
            .values(**values)
            .on_conflict_do_update(
                index_elements=[ActionDB.id],
                set_=set_,
            )
        )
        await self.session.execute(insert_stmt)

        existing_evs_stmt = select(ActionEvidenceDB.id).where(
            ActionEvidenceDB.action_id == action.id
        )

        existing_evs = set(
            (await self.session.execute(existing_evs_stmt)).scalars().all()
        )

        new_ev_ids = {ev["id"] for ev in action_completion_evidences if "id" in ev}

        ev_to_delete = existing_evs - new_ev_ids

        if ev_to_delete:
            delete_stmt = delete(ActionEvidenceDB).where(
                ActionEvidenceDB.id.in_(ev_to_delete)
            )
            await self.session.execute(delete_stmt)

        if action_completion_evidences:
            insert_ev_stmt = insert(ActionEvidenceDB).values(
                action_completion_evidences
            )

            upsert_evidences = insert_ev_stmt.on_conflict_do_update(
                index_elements=[ActionEvidenceDB.id],
                set_={
                    c.name: insert_ev_stmt.excluded[c.name]
                    for c in ActionEvidenceDB.__table__.columns
                    if c.name != "id"
                },
            )
            await self.session.execute(upsert_evidences)

    async def get(self, action_id: UUID) -> Action | None:
        stmt = (
            select(ActionDB)
            .where(ActionDB.id == action_id)
            .options(selectinload(ActionDB.action_completion_evidences))
        )

        action = (await self.session.execute(stmt)).scalar_one_or_none()

        if not action:
            return None

        action_ev = []

        if action.action_completion_evidences:
            action_ev = [
                ActionCompletionEvidence(
                    id=ev.id,
                    action_id=ev.action_id,
                    title=ev.title,
                    description=ev.description,
                    status=ev.status,
                    created_at=ev.created_at,
                    updated_at=ev.updated_at,
                    accepted_at=ev.accepted_at,
                )
                for ev in action.action_completion_evidences
            ]
        return Action(
            id=action.id,
            title=action.title,
            status=action.status,
            estimated_completion_date=action.estimated_completion_date,
            completion_date=action.completion_date,
            owner_id=action.owner_id,
            finding_id=action.finding_id,
            created_at=action.created_at,
            updated_at=action.updated_at,
            soft_delete=action.soft_delete,
            action_completion_evidences=action_ev,
        )
