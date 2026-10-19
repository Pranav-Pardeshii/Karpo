"""
Cultivation Cost Benchmarking Endpoints.
Exposes CACP comprehensive C2 cultivation and operational cost estimates.
"""

from fastapi import APIRouter, Depends

from crop_advisory.api.dependencies import get_cost_service, require_readiness
from crop_advisory.api.v1.schemas import (
    CultivationCostRequest,
    CultivationCostResponse,
    StatesListResponse,
)
from crop_advisory.services.cultivation_cost_service import CultivationCostService

router = APIRouter(prefix="/cultivation-costs", tags=["Cultivation Costs"])


@router.post(
    "/estimate",
    response_model=CultivationCostResponse,
    summary="Estimate C2 Cost of Cultivation",
    description="Calculates comprehensive C2 cultivation cost per hectare/acre and operational input breakdown.",
    dependencies=[Depends(require_readiness)],
)
async def estimate_cultivation_cost(
    payload: CultivationCostRequest,
    cost_service: CultivationCostService = Depends(get_cost_service),
) -> CultivationCostResponse:
    """Retrieves CACP cultivation cost standards for a crop and optional state."""
    raw_cost = cost_service.get_cultivation_cost(
        crop_name=payload.crop_name, state_name=payload.state_name
    )
    return CultivationCostResponse(**raw_cost)


@router.get(
    "/states",
    response_model=StatesListResponse,
    summary="List Surveyed Indian States",
    description="Retrieves a list of all Indian states with CACP cultivation cost survey data.",
)
async def list_cost_states(
    cost_service: CultivationCostService = Depends(get_cost_service),
) -> StatesListResponse:
    """Returns available states in the CACP cost dataset."""
    states = cost_service.get_available_states()
    return StatesListResponse(states=states)
