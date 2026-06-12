class AppException(Exception):
    def __init__(
        self,
        message: str,
        *,
        code: str,
        status_code: int,
        details: dict | None = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class DatabaseError(AppException):
    def __init__(self, message: str = "Database error", *, details: dict | None = None):
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            status_code=500,
            details=details,
        )


class ValidationError(AppException):
    def __init__(
        self,
        message: str = "Validation error",
        *,
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=400,
            details=details,
        )


class NotFoundError(AppException):
    def __init__(
        self,
        message: str = "Resource not found",
        *,
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=404,
            details=details,
        )


class InvalidStateTransition(AppException):
    def __init__(
        self,
        message: str = "Invalid Transition",
        *,
        details: dict | None = None,
    ):
        super().__init__(
            message=message, code="TRANSITION_ERROR", status_code=400, details=details
        )


class WrongCredentialsError(AppException):
    status_code: int = 403


class TokenExpiredError(AppException):
    status_code: int = 401


class TokenInvalidError(AppException):
    status_code: int = 401


class AccessDenied(AppException):
    status_code: int = 403


class UserNotFoundError(AppException):
    status_code: int = 400


class RefreshTokenMissingError(AppException):
    status_code: int = 403
