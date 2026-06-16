from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import router as api
from src.infra.db import models
from src.api.exceptions_handlers import register_exception_handlers
from src.core.logging import setup_logging
from src.api.middlewares.logging import request_logging_middleware


def create_app() -> FastAPI:
    """
    ENTRY FACTORY,might change things later
    """
    origins = [
        "http://localhost:5173",
        "http://localhost",
    ]

    setup_logging()

    app = FastAPI(title="SOQM", version="v1")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.middleware("http")(request_logging_middleware)

    register_exception_handlers(app)

    app.include_router(api)
    return app


app: FastAPI = create_app()


@app.get("/health")
def home():
    return "soqm here"
