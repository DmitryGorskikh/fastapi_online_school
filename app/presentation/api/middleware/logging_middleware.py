import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger('app.http')


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        logger.info(
            '%s %s -> %s (%sms)',
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            extra={
                'method': request.method,
                'path': request.url.path,
                'status_code': response.status_code,
                'duration_ms': duration_ms,
            },
        )
        return response
