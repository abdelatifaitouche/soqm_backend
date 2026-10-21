from src.features.findings.application.ports import (
    IActionRepository,
    IFindingRepository,
)
from src.features.organizations.application.ports import IEmployeeRepository
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
        emp_repo: IEmployeeRepository,
    ):
        self.repo = repo
        self.uow = uow
        self.finding_repo = finding_repo
        self.emp_repo = emp_repo

    async def _get_owner(self, owner_id: UUID):
        owner = await self.emp_repo.get(owner_id)

        if not owner:
            raise Exception(
                f"Cannot find an employee with ID {owner_id}",
            )

        return owner

    async def _get_finding(self, finding_id: UUID):
        finding = await self.finding_repo.get(finding_id)

        if not finding:
            raise Exception(
                f"No Finding Found with ID {finding_id}",
            )

        return finding

    async def create_action(self, action_data: CreateAction):
        async with self.uow:
            finding = await self._get_finding(action_data.finding_id)
            if not finding.can_accept_new_actions():
                raise Exception(
                    f"Cannot add Actions to this finding {finding.finding_title}",
                )

            owner = self._get_owner(action_data.owner_id)

            action = Action.create(
                finding_id=action_data.finding_id,
                title=action_data.title,
                estimated_completion_date=action_data.estimated_completion_date,
                owner_id=action_data.owner_id,
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

            if action_update.owner_id:
                owner = self._get_owner(action_update.owner_id)

            action.update(
                title=action_update.title,
                estimated_completion_date=action_update.estimated_completion_date,
                finding_id=finding_id,
                owner_id=action_update.owner_id,
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
