from src.features.soqm_engine.application.ports.iobjective_repo import (
    IObjectiveRepository,
)


class ObjectiveUC:
    def __init__(self, objective_repo: IObjectiveRepository):
        self.objective_repo = objective_repo

    async def create_objective(self):
        return
