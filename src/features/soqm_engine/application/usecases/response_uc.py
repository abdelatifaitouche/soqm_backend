from src.features.soqm_engine.application.ports.iresponse_repo import (
    IResponseRepository,
)


class ResponseUC:
    def __init__(self, response_repo: IResponseRepository):
        self.response_repo = response_repo
