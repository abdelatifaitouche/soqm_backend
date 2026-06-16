import logging
from logging.config import dictConfig
from src.core.request_context import get_request_id


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id() or "-"
        return True


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_id": {
            "()": RequestIdFilter,
        }
    },
    "formatters": {
        "default": {
            "format": "%(asctime)s | %(levelname)s | %(request_id)s | %(name)s | %(message)s",
        }
    },
    "handlers": {
        # Console output
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["request_id"],
            "formatter": "default",
            "level": "DEBUG",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}


def setup_logging():
    dictConfig(LOGGING_CONFIG)
