"""
Backward-compatibility shim for profit_calculation module.
Re-exports calculations from crop_advisory.domain.calculations.
"""

from crop_advisory.config import ACRES_TO_HA, HA_TO_ACRES, KG_PER_QUINTAL
from crop_advisory.domain.calculations import (
    calculate_farm_financials,
    convert_area_to_acres,
    convert_area_to_ha,
    format_inr,
    format_inr_short,
)

__all__ = [
    "convert_area_to_ha",
    "convert_area_to_acres",
    "format_inr",
    "format_inr_short",
    "calculate_farm_financials",
    "HA_TO_ACRES",
    "ACRES_TO_HA",
    "KG_PER_QUINTAL",
]
