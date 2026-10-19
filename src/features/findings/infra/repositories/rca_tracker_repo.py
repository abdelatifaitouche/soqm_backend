from sqlalchemy.ext.asyncio import AsyncSession
from src.features.findings.infra.models import (
    RootCauseCategory as RootCauseCategoryDB,
    RootCauseIndicator as RootCauseIndicatorDB,
    PotentialRootCause as PotentialRootCauseDB,
)
from src.features.findings.domain.entities import RootCauseCategory
from sqlalchemy.dialects.postgresql import insert
from src.features.findings.application.ports import IRcaTrackerRepository


class RcaTrackerRepository(IRcaTrackerRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def bulk_insert(self, categories: list[RootCauseCategory]):

        cat_payload = []
        ind_payload = []
        potential_payload = []

        for category in categories:
            cat_payload.append(
                {"id": category.id, "category": category.category},
            )

            for indicator in category.indicators:
                ind_payload.append(
                    {
                        "id": indicator.id,
                        "indicator": indicator.indicator,
                        "root_cause_category_id": category.id,
                    },
                )

                for potential in indicator.potential_causes:
                    potential_payload.append(
                        {
                            "id": potential.id,
                            "potential_root_cause": potential.potential_root_cause,
                            "root_cause_indicator_id": indicator.id,
                            "component_id": potential.isqm_component,
                        },
                    )

        if cat_payload:
            cat_stmt = insert(RootCauseCategoryDB).values(cat_payload)
            cat_stmt = cat_stmt.on_conflict_do_nothing(index_elements=["id"])
            await self.session.execute(cat_stmt)

        if ind_payload:
            ind_stmt = insert(RootCauseIndicatorDB).values(ind_payload)
            ind_stmt = ind_stmt.on_conflict_do_nothing(index_elements=["id"])
            await self.session.execute(ind_stmt)

        if potential_payload:
            pot_stmt = insert(PotentialRootCauseDB).values(potential_payload)
            pot_stmt = pot_stmt.on_conflict_do_nothing(index_elements=["id"])
            await self.session.execute(pot_stmt)
