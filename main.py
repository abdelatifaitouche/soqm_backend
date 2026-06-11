from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import router as api
from src.infra.db import models
from src.api.exceptions_handlers import register_exception_handlers


def create_app() -> FastAPI:

    origins = [
        "http://localhost:5173",
        "http://localhost",
    ]

    app = FastAPI(title="SOQM", version="v1")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    app.include_router(api)

    return app


app: FastAPI = create_app()


@app.get("/health")
def home():
    return "soqm here"
