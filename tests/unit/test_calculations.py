"""
Unit tests for domain calculations and unit conversion logic.
"""

from crop_advisory.config import HA_TO_ACRES
from crop_advisory.domain.calculations import (
    calculate_farm_financials,
    convert_area_to_acres,
    convert_area_to_ha,
    format_inr,
    format_inr_short,
)


def test_area_conversion_ha_to_acres():
    assert round(convert_area_to_acres(1.0, "ha"), 2) == round(HA_TO_ACRES, 2)
    assert round(convert_area_to_acres(1.0, "hectare"), 2) == round(HA_TO_ACRES, 2)
    assert convert_area_to_acres(2.5, "acre") == 2.5


def test_area_conversion_acres_to_ha():
    assert round(convert_area_to_ha(2.47105, "acre"), 2) == 1.0
    assert convert_area_to_ha(1.0, "ha") == 1.0
    assert convert_area_to_ha(4.0, "bigha") == 1.0


def test_inr_formatting_basic():
    assert format_inr(0) == "₹0"
    assert format_inr(None) == "₹0"
    assert format_inr(1000) == "₹1,000"
    assert format_inr(1000, include_paise=True) == "₹1,000.00"
    assert format_inr(125000) == "₹1,25,000"
    assert format_inr(15000000) == "₹1,50,00,000"
    assert format_inr(-5000) == "-₹5,000"


def test_inr_short_formatting():
    assert format_inr_short(0) == "₹0"
    assert format_inr_short(None) == "₹0"
    assert format_inr_short(500) == "₹500"
    assert format_inr_short(2500) == "₹2.5 K"
    assert "Lakh" in format_inr_short(250000)
    assert "Cr" in format_inr_short(15000000)
    assert format_inr_short(-250000) == "-₹2.50 Lakh"


def test_farm_financials_positive_roi():
    fin = calculate_farm_financials(
        yield_kg_per_ha=2000.0,
        farm_area=1.0,
        area_unit="hectare",
        price_per_quintal=3000.0,
        cost_per_ha=40000.0,
    )
    assert fin["total_production_quintals"] == 20.0
    assert fin["total_production_kg"] == 2000.0
    assert fin["total_revenue"] == 60000.0
    assert fin["total_cost"] == 40000.0
    assert fin["net_profit"] == 20000.0
    assert fin["roi_percent"] == 50.0
    assert fin["profit_margin_percent"] == round((20000.0 / 60000.0) * 100.0, 2)
    assert fin["breakeven_yield_kg_per_ha"] == round(40000.0 / 30.0, 2)
    assert fin["breakeven_price_per_quintal"] == 2000.0


def test_farm_financials_negative_roi():
    fin = calculate_farm_financials(
        yield_kg_per_ha=500.0,
        farm_area=2.0,
        area_unit="hectare",
        price_per_quintal=2000.0,
        cost_per_ha=30000.0,
    )
    # Total harvest: 1000 kg = 10 quintals. Revenue: 20,000. Cost: 60,000. Net profit: -40,000
    assert fin["total_revenue"] == 20000.0
    assert fin["total_cost"] == 60000.0
    assert fin["net_profit"] == -40000.0
    assert fin["roi_percent"] < 0
    assert fin["formatted_profit"].startswith("-₹")
