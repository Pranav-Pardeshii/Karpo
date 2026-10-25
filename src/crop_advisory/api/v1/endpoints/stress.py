"""
Climate & Market Stress Simulator Endpoints for Karpo API v1.
Enables real-time sensitivity analysis under rainfall deficit/surplus,
wholesale price drops, and statutory PMFBY insurance coverage.
"""

from fastapi import APIRouter, Depends, status

from crop_advisory.api.dependencies import get_stress_simulation_service
from crop_advisory.api.v1.schemas import (
    ScenarioComparisonResponse,
    StressSimulationRequest,
)
from crop_advisory.services.stress_simulation_service import StressSimulationService

router = APIRouter(prefix="/stress", tags=["Stress Simulation"])


@router.post(
    "/simulate",
    response_model=ScenarioComparisonResponse,
    status_code=status.HTTP_200_OK,
    summary="Simulate agricultural yield and financial sensitivity under climate and market shocks",
    description=(
        "Evaluates the impact of user-selected rainfall shocks and Mandi price fluctuations "
        "on farm yield, gross revenue, net profit, and PMFBY crop insurance payout eligibility. "
        "Uses trained XGBoost regression models for simulated yield rather than linear estimates."
    ),
)
def simulate_stress_scenario(
    request: StressSimulationRequest,
    service: StressSimulationService = Depends(get_stress_simulation_service),
) -> ScenarioComparisonResponse:
    """Executes dual-scenario climate and market stress simulation."""
    result = service.simulate_stress(
        crop=request.crop,
        season=request.season,
        soil_type=request.soil_type,
        state=request.state,
        farm_area=request.farm_area,
        area_unit=request.area_unit,
        base_rainfall_mm=request.base_rainfall_mm,
        base_temperature_c=request.base_temperature_c,
        base_humidity_pct=request.base_humidity_pct,
        base_ph=request.base_ph,
        base_nitrogen=request.base_nitrogen,
        base_phosphorus=request.base_phosphorus,
        base_potassium=request.base_potassium,
        base_fertilizer=request.base_fertilizer,
        base_pesticide=request.base_pesticide,
        base_price_per_quintal=request.base_price_per_quintal,
        base_cost_per_ha=request.base_cost_per_ha,
        rainfall_shock_percent=request.rainfall_shock_percent,
        price_shock_percent=request.price_shock_percent,
        cost_shock_percent=request.cost_shock_percent,
        pmfby_indemnity_level=request.pmfby_indemnity_level,
    )
    return ScenarioComparisonResponse(**result.to_dict())
