from dataclasses import asdict
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.soqm_engine.application.ports import IRiskRepository
from src.features.soqm_engine.domain.entities.risk import Risk
from src.features.soqm_engine.infra.models import (
    Risk as RiskDB,
)
from src.features.soqm_engine.infra.models import (
    RiskObjectiveAssociation,
    RiskResponseAssociation,
)


class RiskRepository(IRiskRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, risk: Risk) -> None:

        values = asdict(risk)

        closure_reason = values.pop("closure_reason", None)

        if closure_reason:
            values["closure_code"] = closure_reason.get("closure_code")
            values["closure_title"] = closure_reason.get("closure_title")
            values["closure_reason_comment"] = closure_reason.get(
                "closure_reason_comment"
            )

        objectives = set(values.pop("objectives", []))
        responses = set(values.pop("responses", []))
        immutable_fields = {
            "id",
            "created_by",
            "created_at",
            "risk_ref",
            "sequence",
        }

        insert_stmt = insert(RiskDB).values(values)

        update_values = {k: v for k, v in values.items() if k not in immutable_fields}

        if update_values:
            stmt = insert_stmt.on_conflict_do_update(
                index_elements=[RiskDB.id], set_=update_values
            )
        else:
            stmt = insert_stmt.on_conflict_do_nothing(index_elements=[RiskDB.id])

        await self.session.execute(stmt)

        delete_obj_stmt = delete(RiskObjectiveAssociation).where(
            RiskObjectiveAssociation.risk_id == risk.id,
            RiskObjectiveAssociation.objective_id.not_in(objectives),
        )

        if not objectives:
            delete_obj_stmt = delete(RiskObjectiveAssociation).where(
                RiskObjectiveAssociation.risk_id == risk.id
            )

        await self.session.execute(delete_obj_stmt)

        if objectives:
            rows = [
                {"risk_id": risk.id, "objective_id": obj_id} for obj_id in objectives
            ]

            association_insert = (
                insert(RiskObjectiveAssociation)
                .values(rows)
                .on_conflict_do_nothing(
                    index_elements=["risk_id", "objective_id"],
                )
            )

            await self.session.execute(association_insert)

        delete_resp_stmt = delete(RiskResponseAssociation).where(
            RiskResponseAssociation.risk_id == risk.id,
            RiskResponseAssociation.response_id.not_in(responses),
        )

        if not responses:
            delete_resp_stmt = delete(RiskResponseAssociation).where(
                RiskResponseAssociation.risk_id == risk.id
            )

        await self.session.execute(delete_resp_stmt)

        if responses:
            rows = [
                {"risk_id": risk.id, "response_id": resp_id} for resp_id in responses
            ]

            resp_association_insert = (
                insert(RiskResponseAssociation)
                .values(rows)
                .on_conflict_do_nothing(
                    index_elements=["risk_id", "response_id"],
                )
            )

            await self.session.execute(resp_association_insert)

    async def _sync_risk_associations(
        self, risk_id: UUID, sync_column, association_table, new_data
    ):

        new_data_set = set(new_data) if new_data else set()

        column = getattr(association_table, sync_column)
        risk_id_column = getattr(association_table, "risk_id")

        delete_stmt = delete(association_table).where(
            risk_id_column == risk_id,
            column.not_in(new_data),
        )

        if not new_data:
            delete_obj_stmt = delete(association_table).where(risk_id_column == risk_id)

        await self.session.execute(delete_stmt)

        if new_data:
            rows = [{"risk_id": risk_id, sync_column: id} for id in new_data]

            association_insert = (
                insert(association_table)
                .values(rows)
                .on_conflict_do_nothing(
                    index_elements=["risk_id", sync_column],
                )
            )

            await self.session.execute(association_insert)

    async def get(self, risk_id: UUID) -> Risk | None:
        stmt = select(RiskDB.__table__).where(RiskDB.id == risk_id)
        res = (await self.session.execute(stmt)).mappings().one_or_none()

        if not res:
            return None

        closure_reason = {
            "closure_code": res.get("closure_code", None),
            "closure_title": res.get("closure_title", None),
            "closure_reason_comment": res.get("closure_reason_comment", None),
        }

        exculeded = {*closure_reason.keys(), "objective_id", "component_order"}

        data = {k: v for k, v in dict(res).items() if k not in exculeded}

        objective = select(RiskObjectiveAssociation.objective_id).where(
            RiskObjectiveAssociation.risk_id == risk_id
        )

        obj_res = (await self.session.execute(objective)).scalars().all()

        responses = select(RiskResponseAssociation.response_id).where(
            RiskResponseAssociation.risk_id == risk_id
        )

        resp_data = (await self.session.execute(responses)).scalars().all()

        data["objectives"] = list(obj_res)
        data["responses"] = list(resp_data)
        data["closure_reason"] = closure_reason
        return Risk(**data)

    async def delete(self, risk_id: UUID) -> None:
        pass
