from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from src.core.exceptions import AppException
from src.core.config import settings
from src.core.request_context import get_request_id
import logging

logger = logging.getLogger(__name__)


def get_client_ip(request: Request):
    """
    ADDED THIS BUT UPDATED LATER FOR THE REVERSE PROXY CASE

    X-FORWARDED ....

    """
    return request.client.host if request.client else "Unknown"


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):

        ip = get_client_ip(request)
        logger.warning(
            "APP ERROR request_id=%s code=%s message=%s",
            get_request_id(),
            exc.code,
            exc.message,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.message,
                "code": exc.code,
                "details": exc.details if settings.DEBUG else {},
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):

        ip = get_client_ip(request)
        logger.warning(
            "HTTP ERROR request_id=%s status=%s detail=%s",
            get_request_id(),
            exc.status_code,
            exc.detail,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):

        logger.warning(
            "VALIDATION_ERROR request_id=%s path=%s errors=%s",
            get_request_id(),
            request.url.path,
            exc.errors(),
        )

        return JSONResponse(
            status_code=422,
            content={
                "message": "Validation error",
                "request_id": get_request_id(),
                "errors": exc.errors(),
            },
        )
