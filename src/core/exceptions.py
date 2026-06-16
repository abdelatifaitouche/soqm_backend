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
    def __init__(
        self,
        message: str = "Invalid Credentials",
        *,
        details: dict | None = None,
    ):
        self.message = message
        super().__init__(
            message=message,
            code="AUTH_INVALID_CREDENTIALS",
            status_code=401,
            details=details,
        )


class TokenExpiredError(AppException):
    def __init__(
        self,
        message: str = "Token Expired",
        *,
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            code="AUTH_TOKEN_EXPIRED",
            status_code=401,
            details=details,
        )


class TokenInvalidError(AppException):
    def __init__(
        self,
        message: str = "Invalid Token",
        *,
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            code="AUTH_TOKEN_INVALID",
            status_code=401,
            details=details,
        )


class AccessDenied(AppException):
    def __init__(
        self,
        message: str = "Access Denied",
        *,
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            code="AUTH_FORBIDDEN",
            status_code=403,
            details=details,
        )


class UserNotFoundError(AppException):
    def __init__(
        self,
        message: str = "Invalid Token",
        *,
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            code="AUTH_USER_NOT_FOUND",
            status_code=403,
            details=details,
        )


class RefreshTokenMissingError(AppException):
    def __init__(
        self,
        message: str = "Invalid Token",
        *,
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            code="AUTH_TOKEN_INVALID",
            status_code=403,
            details=details,
        )
