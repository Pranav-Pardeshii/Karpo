"""
Backward-compatibility shim for cost_lookup module.
Re-exports cultivation cost functions from crop_advisory.services.cultivation_cost_service.
"""

from crop_advisory.config import HA_TO_ACRES
from crop_advisory.services.cultivation_cost_service import (
    get_available_states,
    get_cultivation_cost,
    load_cost_dataset,
)

# HA_TO_ACRE alias for backwards compatibility
HA_TO_ACRE = HA_TO_ACRES

__all__ = [
    "HA_TO_ACRE",
    "load_cost_dataset",
    "get_available_states",
    "get_cultivation_cost",
]
