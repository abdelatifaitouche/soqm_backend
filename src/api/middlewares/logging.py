import uuid
import time
import logging
from fastapi import Request
from src.core.request_context import set_request_id

logger = logging.getLogger("app.request")


async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    set_request_id(request_id)

    ip = request.client.host if request.client else "unknown"
    start = time.perf_counter()

    logger.info(
        "START method=%s path=%s ip=%s",
        request.method,
        request.url.path,
        ip,
    )

    try:
        response = await call_next(request)

        duration = (time.perf_counter() - start) * 1000

        logger.info(
            "END method=%s path=%s status=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        response.headers["X-Request-ID"] = request_id
        return response

    except Exception:
        duration = (time.perf_counter() - start) * 1000

        logger.exception(
            "FAILED method=%s path=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            duration,
        )
        raise
