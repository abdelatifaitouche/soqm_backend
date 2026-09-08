from src.features.soqm_engine.application.ports.irisk_repo import IRiskRepository


class RiskUC:
    def __init__(self, risk_repository: IRiskRepository):
        self.risk_repository = risk_repository
