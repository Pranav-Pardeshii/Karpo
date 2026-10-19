"""
Backward-compatibility shim for price_lookup module.
Re-exports pricing functions from crop_advisory.services.market_service.
"""

from crop_advisory.services.market_service import (
    get_crop_price,
    load_prices_dataset,
)

__all__ = [
    "get_crop_price",
    "load_prices_dataset",
]
