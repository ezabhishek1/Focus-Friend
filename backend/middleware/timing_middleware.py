"""
Focus Friend - Timing & Performance Middleware.
Appends execution latency headers and structured access metrics.
"""

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from backend.utils.logger import logger


class TimingMiddleware(BaseHTTPMiddleware):
    """Measures total request processing time and adds X-Process-Time header."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"
        
        # Log API requests cleanly
        if request.url.path.startswith("/api/"):
            logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({process_time:.3f}s)")
            
        return response
