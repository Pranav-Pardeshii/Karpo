"""
Domain package for Smart Crop Advisory System.
Encapsulates entity schemas, canonical agronomic crop mappings, and financial math.
"""

from crop_advisory.domain.calculations import (
    calculate_farm_financials,
    convert_area_to_acres,
    convert_area_to_ha,
    format_inr,
    format_inr_short,
)
from crop_advisory.domain.crop_mapping import (
    CROP_ALIASES,
    CROP_METADATA,
    get_all_supported_crops,
    get_crop_metadata,
    map_rec_crop_to_yield_crop,
    map_to_cost_crop,
    map_to_price_crop,
    normalize_crop_name,
)
from crop_advisory.domain.schemas import (
    CostInfoResult,
    CropRecommendationItem,
    CropRecommendationResult,
    FarmFinancialInput,
    FarmFinancialResult,
    PriceInfoResult,
    SoilClimateInput,
    YieldInput,
    YieldPredictionResult,
)

__all__ = [
    "CROP_METADATA",
    "CROP_ALIASES",
    "normalize_crop_name",
    "get_crop_metadata",
    "get_all_supported_crops",
    "map_rec_crop_to_yield_crop",
    "map_to_price_crop",
    "map_to_cost_crop",
    "convert_area_to_ha",
    "convert_area_to_acres",
    "format_inr",
    "format_inr_short",
    "calculate_farm_financials",
    "SoilClimateInput",
    "YieldInput",
    "FarmFinancialInput",
    "CropRecommendationItem",
    "CropRecommendationResult",
    "YieldPredictionResult",
    "PriceInfoResult",
    "CostInfoResult",
    "FarmFinancialResult",
]
