"""
Farm Financial Analysis and Economic Optimization Endpoints.
Calculates production volume, gross revenue, cultivation expenses, net profit, ROI, and break-even metrics.
"""

from fastapi import APIRouter

from crop_advisory.api.v1.schemas import (
    FinancialAnalysisRequest,
    FinancialAnalysisResponse,
)
from crop_advisory.domain.calculations import calculate_farm_financials

router = APIRouter(tags=["Financial Analysis"])


@router.post(
    "/financial-analysis",
    response_model=FinancialAnalysisResponse,
    summary="Compute Farm Economics and Profitability",
    description="Computes gross revenue, comprehensive C2 costs, net profit, ROI %, and break-even yield and price thresholds.",
)
async def analyze_financials(payload: FinancialAnalysisRequest) -> FinancialAnalysisResponse:
    """Executes deterministic farm economic and break-even calculations."""
    results = calculate_farm_financials(
        yield_kg_per_ha=payload.yield_kg_per_ha,
        farm_area=payload.farm_area,
        area_unit=payload.area_unit,
        price_per_quintal=payload.price_per_quintal,
        cost_per_ha=payload.cost_per_ha,
    )
    return FinancialAnalysisResponse(**results)
