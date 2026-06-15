from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    InterfaceError,
    ProgrammingError,
    OperationalError,
)

from src.core.exceptions import ValidationError, DatabaseError


def translate_db_errors(e: Exception) -> Exception:

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
