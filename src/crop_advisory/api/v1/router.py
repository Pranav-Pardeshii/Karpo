"""
Aggregated API Router for v1 Endpoints.
Mounts all resource subrouters under the /api/v1 prefix.
"""

from fastapi import APIRouter

from crop_advisory.api.v1.endpoints import (
    advisory,
    crops,
    cultivation_costs,
    financial_analysis,
    geo,
    health,
    market,
    yield_prediction,
)

api_v1_router = APIRouter()

# Mount all endpoint routers
api_v1_router.include_router(health.router)
api_v1_router.include_router(crops.router)
api_v1_router.include_router(yield_prediction.router)
api_v1_router.include_router(market.router)
api_v1_router.include_router(cultivation_costs.router)
api_v1_router.include_router(financial_analysis.router)
api_v1_router.include_router(advisory.router)
api_v1_router.include_router(geo.router)
