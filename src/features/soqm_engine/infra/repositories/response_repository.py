from uuid import UUID
from src.features.soqm_engine.domain.entities.response import RiskResponse as Response
from src.features.soqm_engine.infra.models import (
    RiskResponse as ResponseDB,
    RiskResponseAssociation,
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.soqm_engine.application.ports import IResponseRepository
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from dataclasses import asdict


class ResponseRepository(IResponseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, response: Response) -> None:
        values = asdict(response)

        risks = set(values.pop("risks", []))

        immutable_fieds = {"id", "response_ref", "created_at", "created_by"}

        insert_stmt = insert(ResponseDB).values(values)

        update_values = {k: v for k, v in values.items() if k not in immutable_fieds}

        if update_values:
            stmt = insert_stmt.on_conflict_do_update(
                index_elements=[ResponseDB.id],
                set_=update_values,
            )
        else:
            stmt = insert_stmt.on_conflict_do_nothing(index_elements=[ResponseDB.id])

        await self.session.execute(stmt)

        delete_stmt = delete(RiskResponseAssociation).where(
            RiskResponseAssociation.response_id == response.id,
            RiskResponseAssociation.risk_id.not_in(risks),
        )

        if not risks:
            delete_stmt = delete(RiskResponseAssociation).where(
                RiskResponseAssociation.response_id == response.id
            )

        await self.session.execute(delete_stmt)

        if risks:
            association_insert = (
                insert(RiskResponseAssociation)
                .values(
                    [{"response_id": response.id, "risk_id": r_id} for r_id in risks]
                )
                .on_conflict_do_nothing(index_elements=["response_id", "risk_id"])
            )

            await self.session.execute(association_insert)

    async def get(self, response_id: UUID) -> Response | None:
        stmt = select(ResponseDB.__table__).where(ResponseDB.id == response_id)

        res = (await self.session.execute(stmt)).mappings().one_or_none()

        if not res:
            return None

        return Response(**dict(res))

    async def get(self, response_id: UUID) -> Response | None:
        stmt = select(ResponseDB.__table__).where(ResponseDB.id == response_id)
        res = (await self.session.execute(stmt)).mappings().one_or_none()

        if not res:
            return None

        data = {
            k: v
            for k, v in dict(res).items()
            if k not in {"objective_id", "component_order"}
        }

        risks = select(RiskResponseAssociation.risk_id).where(
            RiskResponseAssociation.response_id == response_id
        )

        risks_res = (await self.session.execute(risks)).scalars().all()

        data["risks"] = list(risks_res)

        return Response(**data)

    async def delete(self, response_id: UUID) -> None:
        pass
