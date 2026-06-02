from fastapi import FastAPI


def create_app() -> FastAPI:

    app = FastAPI(title="SOQM", version="v1")

    return app


create_app()
