"""
Unit tests for StressSimulationService.
Tests climate shock, market price collapse, financial delta calculations,
and PMFBY insurance Area-Yield index claims logic.
"""

import pytest
from unittest.mock import MagicMock

from crop_advisory.exceptions import ValidationError
from crop_advisory.services.stress_simulation_service import (
    PMFBYSimulationResult,
    ScenarioComparisonResult,
    StressSimulationService,
)


def test_stress_simulation_validation_errors():
    service = StressSimulationService()
    # Rainfall shock out of [-60, +60]
    with pytest.raises(ValidationError, match="outside defensible bounds"):
        service.simulate_stress(crop="rice", rainfall_shock_percent=-75.0)

    # Price shock out of [-60, +60]
    with pytest.raises(ValidationError, match="outside defensible bounds"):
        service.simulate_stress(crop="rice", price_shock_percent=80.0)

    # Invalid PMFBY indemnity level
    with pytest.raises(ValidationError, match="PMFBY indemnity level must be"):
        service.simulate_stress(crop="rice", pmfby_indemnity_level=0.50)

    # Area <= 0
    with pytest.raises(ValidationError, match="Farm area must be greater than zero"):
        service.simulate_stress(crop="rice", farm_area=0.0)


def test_stress_simulation_math_and_deltas():
    mock_yp = MagicMock()
    # Base yield returns 2000 kg/ha, drought yield returns 1400 kg/ha
    mock_yp.predict.side_effect = [
        {"predicted_yield_kg_ha": 2000.0, "historical_median_kg_ha": 2000.0},
        {"predicted_yield_kg_ha": 1400.0, "historical_median_kg_ha": 2000.0},
    ]

    service = StressSimulationService(yield_predictor=mock_yp)
    res = service.simulate_stress(
        crop="rice",
        season="Kharif",
        farm_area=1.0,  # 1 hectare
        area_unit="ha",
        base_rainfall_mm=1000.0,
        base_price_per_quintal=2000.0,
        base_cost_per_ha=20000.0,
        rainfall_shock_percent=-30.0,
        price_shock_percent=-10.0,
        pmfby_indemnity_level=0.80,
    )

    assert isinstance(res, ScenarioComparisonResult)
    assert res.base_rainfall_mm == 1000.0
    assert res.simulated_rainfall_mm == 700.0
    assert res.base_yield_kg_ha == 2000.0
    assert res.simulated_yield_kg_ha == 1400.0
    assert res.yield_delta_kg_ha == -600.0
    assert res.yield_delta_percent == -30.0

    # Base: 20 quintals * 2000 = 40,000 revenue. Cost = 20,000. Profit = 20,000
    assert res.base_total_revenue == 40000.0
    assert res.base_total_cost == 20000.0
    assert res.base_net_profit == 20000.0

    # Sim: 14 quintals * 1800 = 25,200 revenue. Cost = 20,000. Profit = 5,200
    assert res.simulated_total_revenue == 25200.0
    assert res.simulated_net_profit == 5200.0
    assert res.profit_delta == -14800.0

    # PMFBY insurance:
    # Threshold = 2000 * 0.8 = 1600 kg/ha. Simulated = 1400 kg/ha (trigger!)
    # Shortfall = (1600 - 1400) / 1600 = 200 / 1600 = 0.125
    # Sum insured = 20000. Claim = 0.125 * 20000 = 2500
    # Kharif premium = 2% of 20000 = 400
    assert res.pmfby_insurance.is_claim_triggered is True
    assert res.pmfby_insurance.threshold_yield_kg_ha == 1600.0
    assert res.pmfby_insurance.shortfall_ratio == 0.125
    assert res.pmfby_insurance.estimated_claim_inr == 2500.0
    assert res.pmfby_insurance.farmer_premium_inr == 400.0
    # Net position with insurance = 5200 + 2500 - 400 = 7300
    assert res.pmfby_insurance.net_position_with_insurance_inr == 7300.0


def test_pmfby_no_claim_when_above_threshold():
    mock_yp = MagicMock()
    mock_yp.predict.side_effect = [
        {"predicted_yield_kg_ha": 2000.0, "historical_median_kg_ha": 2000.0},
        {"predicted_yield_kg_ha": 1800.0, "historical_median_kg_ha": 2000.0},
    ]

    service = StressSimulationService(yield_predictor=mock_yp)
    res = service.simulate_stress(
        crop="rice",
        season="Kharif",
        farm_area=2.47105,
        area_unit="acre",
        base_cost_per_ha=20000.0,
        rainfall_shock_percent=-5.0,
        pmfby_indemnity_level=0.80,  # Threshold = 1600 kg/ha
    )

    # 1800 > 1600 -> no claim triggered
    assert res.pmfby_insurance.is_claim_triggered is False
    assert res.pmfby_insurance.estimated_claim_inr == 0.0
    assert res.pmfby_insurance.shortfall_ratio == 0.0
