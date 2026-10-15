from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.soqm_engine.application.dtos.risk_matrix_dto import (
    RiskMatrix,
    RiskMatrixCell,
)
from src.features.soqm_engine.application.filters.risk_filters import RiskFilters
from src.features.soqm_engine.infra.models import Risk as RiskDB


class RiskMatrixQuery:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _apply_filters(self, stmt, filters: RiskFilters):

        if filters.component_id:
            stmt = stmt.where(RiskDB.component_id == filters.component_id)

        return stmt

    async def query(self, filters: RiskFilters) -> RiskMatrix:
        """
        Builds a 3 X 3 risk matrix (fixed by the isqm requirements)

        Returns:
            RiskMatrix object of  RiskMatrixCells, occurence/significance fetched
            calculate the total from the database otherwise set to 0
        """
        significance_range = range(1, 4)  # 1 to 3 values for significance
        occurence_range = range(1, 4)  # 1 to 3 values for occurence
        stmt = (
            select(
                RiskDB.occurence,
                RiskDB.significance,
                func.count(RiskDB.id).label("total"),
            )
            .select_from(RiskDB)
            .group_by(
                RiskDB.occurence,
                RiskDB.significance,
            )
        )

        stmt = self._apply_filters(stmt, filters)

        result = (await self.session.execute(stmt)).mappings().all()

        total: int = sum(r.total for r in result)

        counts = {(r["occurence"], r["significance"]): r["total"] for r in result}

        cells = [
            RiskMatrixCell(
                occurence=occurence,
                significance=significance,
                percent=counts.get((occurence, significance), 0) / total * 100,
            )
            for occurence in range(1, 4)
            for significance in range(1, 4)
        ]

        return RiskMatrix(
            cells=cells,
        )
