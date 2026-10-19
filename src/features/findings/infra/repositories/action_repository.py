from src.features.findings.application.ports import IActionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.findings.domain.entities import Action
from uuid import UUID
from src.features.findings.infra.models import Action as ActionDB
from sqlalchemy.dialects.postgresql import insert
from dataclasses import asdict
from sqlalchemy import select


class ActionRepository(IActionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, action: Action) -> None:
        values = asdict(action)

        excluded_columns = {"created_at", "id"}

        insert_stmt = (
            insert(ActionDB)
            .values(**values)
            .on_conflict_do_update(
                index_elements=[ActionDB.id],
                set_={k: v for k, v in values.items() if k not in excluded_columns},
            )
        )
        await self.session.execute(insert_stmt)

    async def get(self, action_id: UUID) -> Action | None:
        stmt = select(ActionDB).where(ActionDB.id == action_id)

        action = (await self.session.execute(stmt)).scalar_one_or_none()

        if not action:
            return None

        return Action(
            id=action.id,
            title=action.title,
            status=action.status,
            estimated_completion_date=action.estimated_completion_date,
            completion_date=action.completion_date,
            finding_id=action.finding_id,
            created_at=action.created_at,
            updated_at=action.updated_at,
        )
