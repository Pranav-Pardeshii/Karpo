"""
Global Exception Handlers and Error Response Formatting.
Translates domain, validation, and infrastructure exceptions into standardized ErrorResponse JSON.
"""

import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from crop_advisory.exceptions import (
    CropNotFoundError,
    DatasetNotFoundError,
    InferenceError,
    ModelNotFoundError,
)
from crop_advisory.exceptions import (
    ValidationError as DomainValidationError,
)

logger = logging.getLogger("crop_advisory.api.errors")


def _get_request_id(request: Request) -> str:
    """Helper to safely retrieve correlation ID from request state."""
    return getattr(request.state, "request_id", "unknown_request")


def _build_error_response(
    status_code: int, error_code: str, message: str, request: Request, details: Any = None
) -> JSONResponse:
    request_id = _get_request_id(request)
    payload = {
        "error_code": error_code,
        "message": message,
        "request_id": request_id,
        "details": details,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return JSONResponse(
        status_code=status_code, content=payload, headers={"X-Request-ID": request_id}
    )


def register_error_handlers(app: FastAPI) -> None:
    """Registers comprehensive exception handlers on the FastAPI application."""

    @app.exception_handler(DomainValidationError)
    async def domain_validation_handler(request: Request, exc: DomainValidationError):
        logger.warning(f"[{_get_request_id(request)}] Domain validation error: {exc}")
        return _build_error_response(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            error_code="VALIDATION_ERROR",
            message=str(exc),
            request=request,
        )

    @app.exception_handler(CropNotFoundError)
    async def crop_not_found_handler(request: Request, exc: CropNotFoundError):
        logger.warning(f"[{_get_request_id(request)}] Crop not found: {exc}")
        return _build_error_response(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="CROP_NOT_FOUND",
            message=str(exc),
            request=request,
        )

    @app.exception_handler(ModelNotFoundError)
    async def model_not_found_handler(request: Request, exc: ModelNotFoundError):
        logger.error(f"[{_get_request_id(request)}] Model unavailable: {exc}", exc_info=True)
        return _build_error_response(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="MODEL_UNAVAILABLE",
            message="Required machine learning model artifact is not ready.",
            request=request,
            details=str(exc) if app.debug else None,
        )

    @app.exception_handler(DatasetNotFoundError)
    async def dataset_not_found_handler(request: Request, exc: DatasetNotFoundError):
        logger.error(f"[{_get_request_id(request)}] Dataset unavailable: {exc}", exc_info=True)
        return _build_error_response(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="DATASET_UNAVAILABLE",
            message="Reference agricultural dataset is not available.",
            request=request,
            details=str(exc) if app.debug else None,
        )

    @app.exception_handler(InferenceError)
    async def inference_error_handler(request: Request, exc: InferenceError):
        logger.error(f"[{_get_request_id(request)}] ML inference failure: {exc}", exc_info=True)
        return _build_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INFERENCE_FAILURE",
            message="Machine learning prediction execution failed.",
            request=request,
            details=str(exc) if app.debug else None,
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(request: Request, exc: RequestValidationError):
        logger.info(
            f"[{_get_request_id(request)}] Pydantic request validation failed: {exc.errors()}"
        )
        formatted_errors = [
            {
                "field": " -> ".join(str(loc) for loc in err["loc"] if loc != "body"),
                "message": err["msg"],
                "type": err["type"],
            }
            for err in exc.errors()
        ]
        return _build_error_response(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            error_code="INVALID_REQUEST_PAYLOAD",
            message="One or more fields failed schema validation.",
            request=request,
            details=formatted_errors,
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.warning(f"[{_get_request_id(request)}] HTTP {exc.status_code}: {exc.detail}")
        return _build_error_response(
            status_code=exc.status_code,
            error_code=f"HTTP_{exc.status_code}",
            message=str(exc.detail),
            request=request,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error(f"[{_get_request_id(request)}] Unhandled server error: {exc}", exc_info=True)
        return _build_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_SERVER_ERROR",
            message="An unexpected internal server error occurred. Please contact system support.",
            request=request,
            details=str(exc) if app.debug else None,
        )
