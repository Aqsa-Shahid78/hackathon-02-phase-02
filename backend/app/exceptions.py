from fastapi import Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400, details=None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details


class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(code="NOT_FOUND", message=message, status_code=404)


class ConflictError(AppException):
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(code="CONFLICT", message=message, status_code=409)


class AuthenticationError(AppException):
    def __init__(self, message: str = "Not authenticated"):
        super().__init__(code="UNAUTHORIZED", message=message, status_code=401)


class AuthorizationError(AppException):
    def __init__(self, message: str = "Access denied"):
        super().__init__(code="FORBIDDEN", message=message, status_code=403)


class ValidationError(AppException):
    def __init__(self, message: str = "Validation error", details=None):
        super().__init__(
            code="VALIDATION_ERROR", message=message, status_code=422, details=details
        )


class RateLimitError(AppException):
    def __init__(self, message: str = "Too many requests. Please try again later."):
        super().__init__(code="RATE_LIMITED", message=message, status_code=429)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )
