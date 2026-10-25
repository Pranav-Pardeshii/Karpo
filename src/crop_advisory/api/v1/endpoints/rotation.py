"""
Crop Rotation & Intercropping API Endpoints.
Provides multi-season crop sequencing and ICAR-validated companion cropping systems.
"""

import logging
from typing import List
from fastapi import APIRouter, Depends, status

from crop_advisory.api.dependencies import get_rotation_service, require_readiness
from crop_advisory.api.v1.schemas import (
    CropRotationResponse,
    IntercropOptionItem,
    RotationPlanRequest,
)
from crop_advisory.services.rotation_service import CropRotationService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/rotation", tags=["Crop Rotation & Intercropping"])


@router.post(
    "/plan",
    response_model=CropRotationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate multi-season crop rotation plan",
    description="Synthesizes an evidence-based multi-year cropping sequence (Kharif, Rabi, Zaid) alternating cereals and legumes.",
    dependencies=[Depends(require_readiness)],
)
async def generate_rotation_plan(
    request: RotationPlanRequest,
    rotation_service: CropRotationService = Depends(get_rotation_service),
) -> CropRotationResponse:
    """Generates an evidence-based multi-season rotation and companion cropping plan."""
    plan = rotation_service.plan_multi_year_rotation(
        current_crop=request.current_crop,
        soil_type=request.soil_type,
        irrigation_available=request.irrigation_available,
        state=request.state,
        years=request.years,
    )
    return CropRotationResponse(**plan)


@router.get(
    "/intercropping/{crop}",
    response_model=List[IntercropOptionItem],
    status_code=status.HTTP_200_OK,
    summary="Get verified ICAR intercropping options",
    description="Returns research-backed companion intercrops with row ratios and Land Equivalent Ratios (LER).",
    dependencies=[Depends(require_readiness)],
)
async def get_intercropping_systems(
    crop: str,
    rotation_service: CropRotationService = Depends(get_rotation_service),
) -> List[IntercropOptionItem]:
    """Retrieves validated ICAR intercropping systems for the specified crop."""
    options = rotation_service.get_intercropping_options(crop)
    return [IntercropOptionItem(**opt) for opt in options]
