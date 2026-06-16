from sqlalchemy.ext.asyncio import AsyncSession
from src.features.risks.models.risk import Risk as RiskDB
from src.features.risks.domain.risk import Risk as RiskEntity
from src.infra.db.exception_utils import translate_db_errors


class RiskRepository:
    model = RiskDB

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    def _to_orm(self, entity: RiskEntity) -> RiskDB:
        return RiskDB(
            id=entity.id,
            component_id=entity.component_id,
            objective_id=entity.objective_id,
            risk_ref=entity.risk_ref,
            risk_discription=entity.risk_discription,
            score=entity.score,
            occurence=entity.occurence,
            significance=entity.significance,
            status=entity.status,
            date_identified=entity.date_identified,
            date_last_assessed=entity.date_last_assessed,
            next_review_date=entity.next_review_date,
            residual_score=entity.residual_score,
        )

    def _to_domain(self, orm: RiskDB) -> RiskEntity:
        return RiskEntity(
            id=orm.id,
            objective_id=orm.objective_id,
            component_id=orm.component_id,
            risk_ref=orm.risk_ref,
            status=orm.status,
            occurence=orm.occurence,
            significance=orm.significance,
            score=orm.score,
            date_identified=orm.date_identified,
            date_last_assessed=orm.date_last_assessed,
            next_review_date=orm.next_review_date,
            residual_score=orm.residual_score,
            risk_discription=orm.risk_discription,
        )

    async def create(self, entity: RiskEntity) -> RiskEntity:
        print("did we reach here ?????")
        print(f"risk:id : {entity.id}")
        print(f"component:id {entity.component_id}")
        print(f"objective:id {entity.objective_id}")
        print("--------------------CREATING RISK -------------------------")
        try:
            orm: RiskDB = self._to_orm(entity)
            print("passed the _to_orm")
            print("ORM : ")
            print(f"risk:id : {orm.id}")
            print(f"component:id {orm.component_id}")
            print(f"objective:id {orm.objective_id}")
            print("--------------------ORM OBJECT IS READY -------------------------")

            self.db.add(orm)

            print("added to db")
            await self.db.flush()
            print("flushed successed")
            await self.db.refresh(orm)
            print("refreshing successed")
            return self._to_domain(orm)
        except Exception as e:
            raise translate_db_errors(e)

    async def list(self):
        return
