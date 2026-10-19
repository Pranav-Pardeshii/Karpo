"""
Backward-compatibility shim for crop_mapping module.
Re-exports canonical crop mapping from crop_advisory.domain.crop_mapping.
"""

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

__all__ = [
    "CROP_METADATA",
    "CROP_ALIASES",
    "normalize_crop_name",
    "get_crop_metadata",
    "get_all_supported_crops",
    "map_rec_crop_to_yield_crop",
    "map_to_price_crop",
    "map_to_cost_crop",
]
