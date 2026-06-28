# custom errors for our app so we can return nice json messages
from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    # base error class
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN)


class ConflictException(AppException):
    def __init__(self, message: str = "Conflict — resource already exists"):
        super().__init__(message, status_code=status.HTTP_409_CONFLICT)


class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)


class ExternalServiceException(AppException):
    # when tmdb api fails
    def __init__(self, message: str = "External service error"):
        super().__init__(message, status_code=status.HTTP_502_BAD_GATEWAY)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


def register_exception_handlers(app):
    app.add_exception_handler(AppException, app_exception_handler)