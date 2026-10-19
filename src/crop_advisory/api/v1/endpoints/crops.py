"""
Crop Recommendation and Taxonomy Endpoints.
Exposes multi-class Random Forest/XGBoost classification and canonical crop metadata.
"""

from typing import List

import anyio
from fastapi import APIRouter, Depends

from crop_advisory.api.dependencies import (
    get_crop_recommender,
    get_inference_limiter,
    require_readiness,
)
from crop_advisory.api.v1.schemas import (
    CropRecommendationRequest,
    CropRecommendationResponse,
    SupportedCropResponse,
)
from crop_advisory.domain.crop_mapping import (
    CROP_METADATA,
    get_all_supported_crops,
    get_crop_metadata,
    normalize_crop_name,
)
from crop_advisory.exceptions import CropNotFoundError
from crop_advisory.ml.crop_recommender import CropRecommender

router = APIRouter(prefix="/crops", tags=["Crop Recommendation"])


@router.post(
    "/recommend",
    response_model=CropRecommendationResponse,
    summary="Recommend Optimal Crops",
    description="Classifies soil chemistry (NPK, pH) and climatic indicators to recommend top candidate crops.",
    dependencies=[Depends(require_readiness)],
)
async def recommend_crops(
    payload: CropRecommendationRequest,
    recommender: CropRecommender = Depends(get_crop_recommender),
    limiter: anyio.CapacityLimiter = Depends(get_inference_limiter),
) -> CropRecommendationResponse:
    """
    Executes multi-class crop recommendation.
    Offloads CPU-bound tree inference to an AnyIO worker thread bounded by the concurrency limiter.
    """
    async with limiter:
        raw_result = await anyio.to_thread.run_sync(
            recommender.predict,
            payload.n,
            payload.p,
            payload.k,
            payload.temperature,
            payload.humidity,
            payload.ph,
            payload.rainfall,
            payload.top_k,
        )
    return CropRecommendationResponse(**raw_result)


@router.get(
    "/supported",
    response_model=List[SupportedCropResponse],
    summary="List Supported Crops",
    description="Retrieves canonical agronomic profiles and cross-dataset identifiers for all 22 supported crops.",
)
async def list_supported_crops() -> List[SupportedCropResponse]:
    """Returns metadata for all 22 canonical agricultural crops."""
    crops = get_all_supported_crops()
    return [SupportedCropResponse(**c) for c in crops]


@router.get(
    "/{crop_name}",
    response_model=SupportedCropResponse,
    summary="Get Crop Metadata by Name",
    description="Looks up canonical metadata for a crop by name, common alias, or vernacular name.",
)
async def get_crop_by_name(crop_name: str) -> SupportedCropResponse:
    """Retrieves canonical metadata for a single crop."""
    canon = normalize_crop_name(crop_name)
    if canon not in CROP_METADATA:
        raise CropNotFoundError(
            f"Crop '{crop_name}' is not in the canonical supported crops directory."
        )
    meta = get_crop_metadata(canon)
    return SupportedCropResponse(**meta)
