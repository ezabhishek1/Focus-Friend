"""
Focus Friend - Global Exception Handlers.
Guarantees consistent, predictable error responses across all REST API endpoints.
Translates domain exceptions, Pydantic validation errors, and network faults into standard JSON envelopes.
"""

from datetime import datetime, timezone
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from backend.exceptions import (
    FocusFriendError,
    InputValidationError,
    OllamaConnectionError,
    InferenceTimeoutError,
    ModelNotFoundError,
    DistillationParsingError,
)
from backend.utils.logger import logger


def format_error_response(error: str, code: str, detail: str, status_code: int) -> JSONResponse:
    """Helper to generate consistent JSON error structures."""
    content = {
        "error": error,
        "code": code,
        "detail": detail,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    return JSONResponse(status_code=status_code, content=content)


def register_exception_handlers(app: FastAPI) -> None:
    """Registers domain and framework exception handlers on the FastAPI app."""

    @app.exception_handler(InputValidationError)
    async def handle_input_validation_error(request: Request, exc: InputValidationError):
        logger.warning(f"Input validation error on {request.url.path}: {exc.message}")
        return format_error_response(
            error="Invalid Request Input",
            code=exc.code,
            detail=exc.message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @app.exception_handler(ModelNotFoundError)
    async def handle_model_not_found(request: Request, exc: ModelNotFoundError):
        logger.warning(f"Model not found on {request.url.path}: {exc.message}")
        return format_error_response(
            error="Model Not Found",
            code=exc.code,
            detail=exc.message,
            status_code=status.HTTP_404_NOT_FOUND,
        )

    @app.exception_handler(InferenceTimeoutError)
    async def handle_inference_timeout(request: Request, exc: InferenceTimeoutError):
        logger.error(f"Inference timeout on {request.url.path}: {exc.message}")
        return format_error_response(
            error="Inference Timeout",
            code=exc.code,
            detail=exc.message,
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        )

    @app.exception_handler(OllamaConnectionError)
    async def handle_ollama_connection(request: Request, exc: OllamaConnectionError):
        logger.warning(f"Ollama connection error on {request.url.path}: {exc.message}")
        return format_error_response(
            error="Local Inference Engine Unavailable",
            code=exc.code,
            detail=exc.message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    @app.exception_handler(DistillationParsingError)
    async def handle_parsing_error(request: Request, exc: DistillationParsingError):
        logger.error(f"Distillation parsing error on {request.url.path}: {exc.message}")
        return format_error_response(
            error="Distillation Parsing Failure",
            code=exc.code,
            detail=exc.message,
            status_code=status.HTTP_502_BAD_GATEWAY,
        )

    @app.exception_handler(FocusFriendError)
    async def handle_generic_domain_error(request: Request, exc: FocusFriendError):
        logger.error(f"Domain error on {request.url.path}: {exc.message}")
        return format_error_response(
            error="Application Error",
            code=exc.code,
            detail=exc.message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_pydantic_validation(request: Request, exc: RequestValidationError):
        first_error = exc.errors()[0] if exc.errors() else {}
        loc = " -> ".join(str(l) for l in first_error.get("loc", []))
        msg = first_error.get("msg", "Invalid field format.")
        detail = f"Field validation failed at '{loc}': {msg}"
        logger.warning(f"Request validation error on {request.url.path}: {detail}")
        
        # RFC 9110 standard HTTP 422 Unprocessable Content
        status_code = getattr(status, "HTTP_422_UNPROCESSABLE_CONTENT", 422)
        return format_error_response(
            error="Validation Error",
            code="SCHEMA_VALIDATION_ERROR",
            detail=detail,
            status_code=status_code,
        )

    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException):
        detail = str(exc.detail) if exc.detail else "HTTP error encountered."
        logger.warning(f"HTTPException on {request.url.path} [{exc.status_code}]: {detail}")
        return format_error_response(
            error="HTTP Error",
            code=f"HTTP_{exc.status_code}",
            detail=detail,
            status_code=exc.status_code,
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(request: Request, exc: Exception):
        logger.critical(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
        return format_error_response(
            error="Internal Server Error",
            code="UNHANDLED_EXCEPTION",
            detail="An unexpected error occurred while processing the request. Check server logs.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
