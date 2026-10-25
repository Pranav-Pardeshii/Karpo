"""
Integration tests for Climate & Market Stress Simulation API (/api/v1/stress).
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_simulate_stress_endpoint_success(async_client: AsyncClient):
    payload = {
        "crop": "rice",
        "season": "Kharif",
        "soil_type": "Vertisols",
        "state": "Maharashtra",
        "farm_area": 2.5,
        "area_unit": "acre",
        "base_rainfall_mm": 850.0,
        "base_temperature_c": 26.0,
        "base_humidity_pct": 70.0,
        "base_ph": 6.8,
        "base_nitrogen": 70.0,
        "base_phosphorus": 35.0,
        "base_potassium": 40.0,
        "base_fertilizer": 80.0,
        "base_pesticide": 0.35,
        "base_price_per_quintal": 2800.0,
        "base_cost_per_ha": 32000.0,
        "rainfall_shock_percent": -25.0,
        "price_shock_percent": -15.0,
        "cost_shock_percent": 5.0,
        "pmfby_indemnity_level": 0.80,
    }

    response = await async_client.post("/api/v1/stress/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["data_category"] == "Simulated"
    assert data["rainfall_shock_percent"] == -25.0
    assert data["price_shock_percent"] == -15.0
    assert "pmfby_insurance" in data
    assert "threshold_yield_kg_ha" in data["pmfby_insurance"]
    assert "estimated_claim_inr" in data["pmfby_insurance"]


@pytest.mark.asyncio
async def test_simulate_stress_endpoint_validation_error(async_client: AsyncClient):
    # Shock outside allowed bounds (-99%)
    payload = {
        "crop": "rice",
        "rainfall_shock_percent": -99.0,
    }
    response = await async_client.post("/api/v1/stress/simulate", json=payload)
    assert response.status_code == 422
