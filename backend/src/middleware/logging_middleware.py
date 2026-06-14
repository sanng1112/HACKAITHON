"""Middleware to log every incoming request."""
import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("govone.api")


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log method, path, status code, and duration for every request."""

    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        logger.info(
            "%s %s -> %s (%.3fs)",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )
        return response
