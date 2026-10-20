from src.features.findings.application.ports import (
    IActionRepository,
    IFindingRepository,
)
from src.core.shared.interfaces.unit_of_work import IUnitOfWork
from src.features.findings.application.dtos import CreateAction, UpdateAction
from src.features.findings.domain.entities import Action
from uuid import UUID


class ActionUC:
    def __init__(
        self,
        uow: IUnitOfWork,
        repo: IActionRepository,
        finding_repo: IFindingRepository,
    ):
        self.repo = repo
        self.uow = uow
        self.finding_repo = finding_repo

    async def create_action(self, action_data: CreateAction):
        async with self.uow:
            finding = await self.finding_repo.get(action_data.finding_id)

            if not finding:
                raise Exception(
                    f"No Finding Found with ID {action_data.finding_id}",
                )

            if not finding.can_accept_new_actions():
                raise Exception(
                    f"Cannot add Actions to this finding {action_data.finding_id}",
                )

            action = Action.create(
                finding_id=action_data.finding_id,
                title=action_data.title,
                estimated_completion_date=action_data.estimated_completion_date,
            )

            await self.repo.save(action)

        return action

    async def update_action(self, action_id: UUID, action_update: UpdateAction):
        async with self.uow:
            action = await self.get(action_id)

            finding_id = action_update.finding_id

            if finding_id:
                finding = await self.finding_repo.get(finding_id)

                if not finding:
                    raise Exception(
                        f"Finding Not Found with ID {action_update.finding_id}"
                    )

            action.update(
                title=action_update.title,
                estimated_completion_date=action_update.estimated_completion_date,
                finding_id=finding_id,
            )
            await self.repo.save(action)
        return action

    async def get(self, action_id: UUID) -> Action:
        action = await self.repo.get(action_id)

        if not action:
            raise Exception(
                f"Action with ID {action_id}",
            )

        if action.soft_delete:
            raise Exception(
                f"Action was deleted",
            )

        return action

    async def start_action(self, action_id: UUID):
        async with self.uow:
            action = await self.get(action_id)

            action.start()

            await self.repo.save(action)

    async def complete_action(self, action_id: UUID):
        async with self.uow:
            action = await self.get(action_id)

            action.complete()

            await self.repo.save(action)

    async def mark_as_delete(self, action_id: UUID):
        async with self.uow:
            action = await self.get(action_id)

            action.mark_as_deleted()

            await self.repo.save(action)

    async def mark_as_draft(self, action_id: UUID):
        async with self.uow:
            action = await self.get(action_id)

            action.mark_as_draft()

            await self.repo.save(action)
