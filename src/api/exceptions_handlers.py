from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from src.core.exceptions import AppException
from src.core.config import settings


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.message,
                "details": exc.details if settings.DEBUG else {},
            },
        )
