"""
Health and Readiness Probes.
Provides Kubernetes-style /health/live and /health/ready diagnostic endpoints.
"""

from fastapi import APIRouter, Request, Response, status

from crop_advisory.api.v1.schemas import LivenessResponse, ReadinessResponse

router = APIRouter(prefix="/health", tags=["Health & Diagnostics"])


@router.get(
    "/live",
    response_model=LivenessResponse,
    summary="Process Liveness Probe",
    description="Confirms that the application process is running and able to handle HTTP events.",
)
async def check_liveness() -> LivenessResponse:
    """Lightweight liveness probe."""
    return LivenessResponse(status="alive")


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    summary="System Readiness Probe",
    description="Verifies that ML model artifacts and datasets are preloaded and available for inference.",
)
async def check_readiness(request: Request, response: Response) -> ReadinessResponse:
    """
    Readiness probe reporting resource initialization states.
    Returns HTTP 200 if ready, HTTP 503 if models or datasets are uninitialized.
    """
    is_ready = getattr(request.app.state, "is_ready", False)
    models_ready = getattr(request.app.state, "models_ready", False)
    datasets_ready = getattr(request.app.state, "datasets_ready", False)
    details = getattr(request.app.state, "diagnostics", {})

    if not is_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return ReadinessResponse(
        status="ready" if is_ready else "not_ready",
        models_loaded=models_ready,
        datasets_loaded=datasets_ready,
        details=details,
    )
