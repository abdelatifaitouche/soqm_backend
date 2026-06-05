from fastapi import FastAPI
from src.api.router import router as api
from src.infra.db import models
from src.api.exceptions_handlers import register_exception_handlers


def create_app() -> FastAPI:

    app = FastAPI(title="SOQM", version="v1")

    register_exception_handlers(app)

    app.include_router(api)

    return app


app: FastAPI = create_app()


@app.get("/health")
def home():
    return "soqm here"
