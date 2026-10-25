"""
Karpo Lens: Crop Disease Assistance Endpoints.
Provides multipart image upload validation and disease diagnosis assistance with honest status reporting.
"""

import logging
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from crop_advisory.api.dependencies import get_lens_service, require_readiness
from crop_advisory.api.v1.schemas import LensInspectionResponse
from crop_advisory.services.lens_service import KarpoLensService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/lens", tags=["Karpo Lens Disease Assistance"])


@router.post(
    "/inspect",
    response_model=LensInspectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Inspect crop image for plant disease symptoms",
    description="Validates image decoding and dimensions. Returns honest diagnosis status and authoritative ICAR symptom guides.",
    dependencies=[Depends(require_readiness)],
)
async def inspect_crop_image(
    image: UploadFile = File(..., description="Crop leaf photo (JPEG, PNG, WEBP)"),
    crop: Optional[str] = Form(None, description="Optional crop species (rice, cotton, soybean, wheat, maize)"),
    lens_service: KarpoLensService = Depends(get_lens_service),
) -> LensInspectionResponse:
    """Validates uploaded leaf image and returns verified diagnostic report."""
    try:
        content = await image.read()
        filename = image.filename or "upload.jpg"
        result = lens_service.validate_and_inspect_image(
            image_bytes=content,
            filename=filename,
            crop_name=crop,
        )
        return LensInspectionResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error inspecting crop image: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error processing image inspection.",
        )
