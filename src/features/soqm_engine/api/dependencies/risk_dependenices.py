from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps.db_session import get_db
from src.infra.db.unit_of_work import UnitOfWork
from src.features.soqm_engine.infra.repositories import (
    RiskRepository,
    ComponentRepository,
    ObjectiveRepository,
    SequenceRepository,
)
from src.features.soqm_engine.application.usecases import RiskUC


def get_risk_uc(db: AsyncSession = Depends(get_db)) -> RiskUC:
    uow = UnitOfWork(db)
    risk_repo = RiskRepository(db)
    seq_repo = SequenceRepository(db)
    obj_repo = ObjectiveRepository(db)
    comp_repo = ComponentRepository(db)
    return RiskUC(
        uow,
        risk_repo,
        seq_repo,
        comp_repo,
        obj_repo,
    )
