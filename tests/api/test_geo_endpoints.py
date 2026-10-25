"""
Integration tests for Geo-Sensing REST API endpoints (/api/v1/geo).
"""

import pytest
from httpx import AsyncClient
from unittest.mock import MagicMock, patch

from crop_advisory.services.geo_sensing_service import (
    GeoSensingResult,
    LocationMetadata,
    SoilEstimateData,
    WeatherData,
)


@pytest.mark.asyncio
async def test_geo_climate_soil_endpoint_success(async_client: AsyncClient):
    mock_result = GeoSensingResult(
        location=LocationMetadata(
            latitude=18.5204,
            longitude=73.8567,
            locality="Pune",
            district="Pune",
            state="Maharashtra",
            canonical_state="Maharashtra",
            country="India",
            source="BigDataCloud Client Reverse Geocode",
            data_category="Observed",
        ),
        weather=WeatherData(
            temperature_c=25.5,
            humidity_pct=65.0,
            precipitation_mm=0.0,
            two_week_rainfall_mm=12.5,
            observation_time="2026-10-25T12:00:00Z",
            source="Open-Meteo Atmospheric Model (ECMWF/GFS)",
            data_category="Observed",
            status="success",
        ),
        soil=SoilEstimateData(
            ph=6.8,
            soil_type_hint=None,
            source="ISRIC SoilGrids 250m v2.0",
            data_category="Estimated",
            status="success",
            caveat="Digital soil mapping estimate.",
        ),
        timestamp="2026-10-25T12:00:00Z",
        overall_status="success",
    )

    with patch(
        "crop_advisory.services.geo_sensing_service.GeoSensingService.get_geo_sensing_advisory",
        return_value=mock_result,
    ):
        response = await async_client.get(
            "/api/v1/geo/climate-soil",
            params={"latitude": 18.5204, "longitude": 73.8567},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["overall_status"] == "success"
        assert data["location"]["canonical_state"] == "Maharashtra"
        assert data["weather"]["temperature_c"] == 25.5
        assert data["weather"]["humidity_pct"] == 65.0
        assert data["soil"]["ph"] == 6.8
        assert data["soil"]["data_category"] == "Estimated"


@pytest.mark.asyncio
async def test_geo_climate_soil_invalid_latitude(async_client: AsyncClient):
    response = await async_client.get(
        "/api/v1/geo/climate-soil",
        params={"latitude": 120.0, "longitude": 73.8567},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_geo_climate_soil_missing_params(async_client: AsyncClient):
    response = await async_client.get("/api/v1/geo/climate-soil")
    assert response.status_code == 422
