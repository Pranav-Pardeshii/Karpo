"""
Full End-to-End Crop Advisory Orchestration Endpoints.
Coordinates crop recommendation, yield forecasting, market pricing, and farm economics.
"""

import anyio
from fastapi import APIRouter, Depends

from crop_advisory.api.dependencies import (
    get_financial_service_dep,
    get_inference_limiter,
    require_readiness,
)
from crop_advisory.api.v1.schemas import (
    CropRecommendationResponse,
    CultivationCostResponse,
    FinancialAnalysisResponse,
    FullAdvisoryRequest,
    FullAdvisoryResponse,
    PriceInfoResponse,
    YieldPredictionResponse,
)
from crop_advisory.services.financial_analysis_service import FinancialAnalysisService

router = APIRouter(prefix="/advisory", tags=["Integrated Advisory"])


@router.post(
    "/full",
    response_model=FullAdvisoryResponse,
    summary="Generate Complete Crop Advisory Report",
    description="End-to-end agronomic intelligence combining ML recommendation, yield prediction, mandi prices, and financial simulation.",
    dependencies=[Depends(require_readiness)],
)
async def generate_full_advisory(
    payload: FullAdvisoryRequest,
    financial_service: FinancialAnalysisService = Depends(get_financial_service_dep),
    limiter: anyio.CapacityLimiter = Depends(get_inference_limiter),
) -> FullAdvisoryResponse:
    """
    Executes full multi-stage agronomic decision pipeline.
    Offloads synchronous ML inference to an AnyIO worker thread bounded by the concurrency limiter.
    """
    async with limiter:
        report = await anyio.to_thread.run_sync(
            financial_service.generate_advisory,
            payload.n,
            payload.p,
            payload.k,
            payload.temperature,
            payload.humidity,
            payload.ph,
            payload.rainfall,
            payload.state,
            payload.soil_type,
            payload.season,
            payload.farm_area,
            payload.area_unit,
            payload.top_k,
        )

    return FullAdvisoryResponse(
        recommendation=CropRecommendationResponse(**report.recommendation),
        yield_prediction=YieldPredictionResponse(**report.yield_prediction),
        market_price=PriceInfoResponse(**report.market_price),
        cultivation_cost=CultivationCostResponse(**report.cultivation_cost),
        financials=FinancialAnalysisResponse(**report.financials),
        metadata=report.metadata,
    )
