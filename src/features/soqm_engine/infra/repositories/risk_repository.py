from uuid import UUID
from src.features.soqm_engine.domain.entities.risk import Risk
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.soqm_engine.application.ports import IRiskRepository
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from src.features.soqm_engine.infra.models import (
    Risk as RiskDB,
    RiskObjectiveAssociation,
)
from dataclasses import asdict


class RiskRepository(IRiskRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, risk: Risk) -> None:

        values = asdict(risk)

        objectives = set(values.pop("objectives", []))

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

        delete_stmt = delete(RiskObjectiveAssociation).where(
            RiskObjectiveAssociation.risk_id == risk.id,
            RiskObjectiveAssociation.objective_id.not_in(objectives),
        )

        if not objectives:
            delete_stmt = delete(RiskObjectiveAssociation).where(
                RiskObjectiveAssociation.risk_id == risk.id
            )

        await self.session.execute(delete_stmt)

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

    async def get(self, risk_id: UUID) -> Risk | None:
        stmt = select(RiskDB.__table__).where(RiskDB.id == risk_id)
        res = (await self.session.execute(stmt)).mappings().one_or_none()

        if not res:
            return None

        data = {
            k: v
            for k, v in dict(res).items()
            if k not in {"objective_id", "component_order"}
        }

        objective = select(RiskObjectiveAssociation.objective_id).where(
            RiskObjectiveAssociation.risk_id == risk_id
        )

        obj_res = (await self.session.execute(objective)).scalars().all()

        data["objectives"] = list(obj_res)

        return Risk(**data)

    async def delete(self, risk_id: UUID) -> None:
        pass
