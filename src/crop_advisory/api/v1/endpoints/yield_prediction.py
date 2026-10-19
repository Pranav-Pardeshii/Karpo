"""
Agricultural Yield Prediction Endpoints.
Exposes continuous XGBoost regression and agronomic calibration for crop yields.
"""

from typing import List

import anyio
from fastapi import APIRouter, Depends

from crop_advisory.api.dependencies import (
    get_inference_limiter,
    get_yield_predictor,
    require_readiness,
)
from crop_advisory.api.v1.schemas import (
    YieldBenchmarkResponse,
    YieldPredictionRequest,
    YieldPredictionResponse,
)
from crop_advisory.ml.yield_predictor import (
    HISTORICAL_YIELD_BENCHMARKS,
    YieldPredictor,
)

router = APIRouter(prefix="/yield", tags=["Yield Prediction"])


@router.post(
    "/predict",
    response_model=YieldPredictionResponse,
    summary="Predict Agricultural Yield",
    description="Forecasts agricultural harvest yield in kg/ha, quintals/ha, and kg/acre using trained XGBoost regression.",
    dependencies=[Depends(require_readiness)],
)
async def predict_yield(
    payload: YieldPredictionRequest,
    predictor: YieldPredictor = Depends(get_yield_predictor),
    limiter: anyio.CapacityLimiter = Depends(get_inference_limiter),
) -> YieldPredictionResponse:
    """
    Executes yield forecasting regression.
    Offloads CPU-bound gradient boosted tree inference to an AnyIO worker thread bounded by the concurrency limiter.
    """
    async with limiter:
        raw_result = await anyio.to_thread.run_sync(
            predictor.predict,
            payload.crop,
            payload.season,
            payload.soil_type,
            payload.state,
            payload.temperature,
            payload.rainfall,
            payload.humidity,
            payload.ph,
            payload.nitrogen,
            payload.phosphorus,
            payload.potassium,
            payload.fertilizer,
            payload.pesticide,
        )
    return YieldPredictionResponse(**raw_result)


@router.get(
    "/benchmarks",
    response_model=List[YieldBenchmarkResponse],
    summary="List Typical Yield Benchmarks",
    description="Retrieves historical minimum, median, and maximum agricultural yields (kg/ha) across Indian crops.",
)
async def get_yield_benchmarks() -> List[YieldBenchmarkResponse]:
    """Returns baseline agronomic yield reference statistics."""
    benchmarks = []
    for crop_name, stats in HISTORICAL_YIELD_BENCHMARKS.items():
        benchmarks.append(
            YieldBenchmarkResponse(
                crop=crop_name,
                min_kg_ha=stats["min"],
                median_kg_ha=stats["median"],
                max_kg_ha=stats["max"],
            )
        )
    return benchmarks
