"""
HTTP Middleware for Correlation Tracking, Timing, and Structured Logging.
"""

import logging
import time
import uuid
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("crop_advisory.api.access")


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    Ensures every request has a validated correlation identifier (X-Request-ID)
    and measures processing duration (X-Process-Time).
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.perf_counter()

        # Sanitize or generate correlation ID
        incoming_id = request.headers.get("X-Request-ID")
        if incoming_id and len(incoming_id) <= 64 and incoming_id.replace("-", "").isalnum():
            request_id = incoming_id
        else:
            request_id = f"req_{uuid.uuid4().hex[:12]}"

        # Bind to request state
        request.state.request_id = request_id

        # Proceed through pipeline
        try:
            response = await call_next(request)
        except Exception:
            # Let global exception handlers format the error response with request_id
            raise

        # Calculate execution duration
        duration_ms = (time.perf_counter() - start_time) * 1000.0

        # Inject response headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{duration_ms:.2f}ms"

        # Structured access logging
        client_host = request.client.host if request.client else "unknown"
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} - "
            f"Status: {response.status_code} ({duration_ms:.2f}ms) - Client: {client_host}"
        )

        return response
