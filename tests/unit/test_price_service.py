"""
Unit tests for Mandi Market Price service.
"""

from crop_advisory.services.market_service import get_crop_price


def test_price_lookup_wheat(price_service):
    price_info = price_service.get_crop_price("Wheat")
    assert price_info["modal_rs_per_quintal"] > 0
    assert price_info["price_per_kg"] == round(price_info["modal_rs_per_quintal"] / 100.0, 2)
    assert price_info["min_rs_per_quintal"] <= price_info["max_rs_per_quintal"]


def test_price_lookup_rice():
    price_info = get_crop_price("rice")
    assert price_info["modal_rs_per_quintal"] > 0
    assert "Rice" in price_info["matched_crop_name"]


def test_price_lookup_fallback(price_service):
    price_info = price_service.get_crop_price("UnknownCropX")
    assert price_info["modal_rs_per_quintal"] > 0
    assert price_info["price_per_kg"] > 0
    assert "Agmarknet" in price_info["source"]
