class AppException(Exception):
    status_code: int = 400

    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)


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
