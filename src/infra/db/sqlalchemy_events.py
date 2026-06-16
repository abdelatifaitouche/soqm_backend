import logging
from sqlalchemy import event

logger = logging.getLogger("app.sql")


def setup_sqlalchemy_logging(engine):

    @event.listens_for(engine, "before_cursor_execute")
    def before_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        conn.info.setdefault("query_start_time", []).append(__import__("time").time())

        logger.debug("SQL START: %s", statement)

    @event.listens_for(engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        start = conn.info["query_start_time"].pop()
        duration = (__import__("time").time() - start) * 1000

        logger.debug(
            "SQL END duration_ms=%.2f statement=%s",
            duration,
            statement,
        )
