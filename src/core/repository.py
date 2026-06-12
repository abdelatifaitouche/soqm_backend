from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    OperationalError,
    ProgrammingError,
    InterfaceError,
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.exceptions import ValidationError, DatabaseError
from typing import Any


class BaseRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    def _to_orm(self, entity: Any) -> Any:
        """
        Child class implements this _to_orm to transform from domain entity to db model
        """
        pass

    def _to_domain(self, orm: Any) -> Any:
        """
        Child class Impements this to transform from db model to domain entity
        """
        pass

    def _apply_filters(self, *args, **kwargs):
        pass

    def _apply_pagination(self, *args, **kwargs):
        pass

    """
    async def save(self, entity: Any):
        try:
            orm = self._to_orm(entity)
            self.db.add(orm)
            await self.db.flush()
            await self.db.refresh(orm)
            return self._to_domain(orm)
        except Exception as e:
            raise self._translate_db_errors(e)
    """

    def _translate_db_errors(self, e: Exception) -> Exception:

        details = {"error_type": type(e).__name__, "error": str(e)}

        match e:
            case IntegrityError():
                return ValidationError(
                    "Constraint vioalation",
                    details=details,
                )

            case DataError():
                return ValidationError(
                    "Invalid data format",
                    details=details,
                )

            case OperationalError():
                return DatabaseError(
                    "Database unvailable",
                    details=details,
                )

            case ProgrammingError():
                return DatabaseError(
                    "Query Error / schema mismatch",
                    details=details,
                )

            case InterfaceError():
                return DatabaseError(
                    "Database session error",
                    details=details,
                )

            case _:
                return DatabaseError(
                    "Unknow database error",
                    details=details,
                )
