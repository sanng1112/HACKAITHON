"""Global exception handler and custom exception classes."""
import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from src.utils.response import error_response

logger = logging.getLogger("govone.api")


class AppException(Exception):
    """Base application exception with structured error info."""

    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message


class NotFoundException(AppException):
    def __init__(self, entity: str = "Resource"):
        super().__init__(404, "NOT_FOUND", f"{entity} không tồn tại")


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Không có quyền truy cập"):
        super().__init__(401, "UNAUTHORIZED", message)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Không đủ quyền thực hiện hành động này"):
        super().__init__(403, "FORBIDDEN", message)


class ConflictException(AppException):
    def __init__(self, code: str = "CONFLICT", message: str = "Xung đột dữ liệu"):
        super().__init__(409, code, message)


class BusinessRuleException(AppException):
    def __init__(self, message: str = "Vi phạm quy tắc nghiệp vụ"):
        super().__init__(422, "BUSINESS_RULE_VIOLATION", message)


def setup_error_handlers(app):
    """Register all exception handlers on the FastAPI app."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(code=exc.code, message=exc.message),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content=error_response(code="INTERNAL_ERROR", message="Lỗi hệ thống"),
        )
