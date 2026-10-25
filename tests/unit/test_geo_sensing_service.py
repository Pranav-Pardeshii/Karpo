"""
Unit tests for GeoSensingService.
Validates real data categorization, units, coordinates bounds,
caching, and zero fabricated fallback policy when external APIs are unavailable.
"""

import pytest
from unittest.mock import MagicMock, patch

from crop_advisory.services.geo_sensing_service import (
    GeoSensingResult,
    GeoSensingService,
    LocationMetadata,
    SoilEstimateData,
    WeatherData,
)


def test_invalid_coordinates_raise_value_error():
    service = GeoSensingService()
    with pytest.raises(ValueError, match="Latitude must be between -90 and 90"):
        service.get_geo_sensing_advisory(latitude=95.0, longitude=73.8)

    with pytest.raises(ValueError, match="Longitude must be between -180 and 180"):
        service.get_geo_sensing_advisory(latitude=18.5, longitude=-190.0)


def test_reverse_geocoding_success():
    service = GeoSensingService()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "locality": "Shivajinagar",
        "principalSubdivision": "Maharashtra",
        "countryName": "India",
        "localityInfo": {
            "administrative": [
                {"name": "Pune", "adminLevel": 5}
            ]
        }
    }

    with patch("httpx.Client.get", return_value=mock_resp):
        loc = service.fetch_reverse_geocoding(18.5204, 73.8567)
        assert loc.locality == "Shivajinagar"
        assert loc.state == "Maharashtra"
        assert loc.canonical_state == "Maharashtra"
        assert loc.country == "India"
        assert loc.data_category == "Observed"


def test_weather_fetch_success():
    service = GeoSensingService()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "current": {
            "temperature_2m": 24.8,
            "relative_humidity_2m": 62.0,
            "precipitation": 0.0,
            "time": "2026-10-25T12:00:00Z"
        },
        "daily": {
            "precipitation_sum": [0.0, 1.2, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0]
        }
    }

    with patch("httpx.Client.get", return_value=mock_resp):
        weather = service.fetch_weather(18.5204, 73.8567)
        assert weather.status == "success"
        assert weather.temperature_c == 24.8
        assert weather.humidity_pct == 62.0
        assert weather.two_week_rainfall_mm == 8.2
        assert weather.data_category == "Observed"
        assert "Open-Meteo" in weather.source


def test_soil_grids_unavailable_does_not_fabricate():
    service = GeoSensingService()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "properties": {
            "layers": [
                {
                    "name": "phh2o",
                    "depths": [
                        {"values": {"mean": None}}
                    ]
                }
            ]
        }
    }

    with patch("httpx.Client.get", return_value=mock_resp):
        soil = service.fetch_soil_estimate(18.5204, 73.8567)
        assert soil.ph is None
        assert soil.data_category == "Unavailable"
        assert soil.status == "unavailable"
        assert "certified physical soil test" in soil.caveat.lower()


def test_soil_grids_success_divides_by_ten():
    service = GeoSensingService()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "properties": {
            "layers": [
                {
                    "name": "phh2o",
                    "depths": [
                        {"values": {"mean": 68}}  # 68 corresponds to pH 6.8
                    ]
                }
            ]
        }
    }

    with patch("httpx.Client.get", return_value=mock_resp):
        soil = service.fetch_soil_estimate(18.5204, 73.8567)
        assert soil.ph == 6.8
        assert soil.data_category == "Estimated"
        assert soil.status == "success"


def test_external_service_timeout_handling():
    service = GeoSensingService()
    with patch("httpx.Client.get", side_effect=Exception("Connection timed out")):
        weather = service.fetch_weather(18.5204, 73.8567)
        assert weather.status == "failed"
        assert weather.temperature_c is None
        assert weather.data_category == "Unavailable"
        assert "timed out" in weather.error_message


def test_cache_hits_within_ttl():
    service = GeoSensingService()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "current": {"temperature_2m": 22.0, "relative_humidity_2m": 50.0, "precipitation": 0.0},
        "daily": {"precipitation_sum": [1.0]}
    }

    with patch("httpx.Client.get", return_value=mock_resp) as mock_get:
        w1 = service.fetch_weather(18.5204, 73.8567)
        w2 = service.fetch_weather(18.5204, 73.8567)
        assert w1.temperature_c == 22.0
        assert w2.temperature_c == 22.0
        # Second call must hit memory cache, calling client.get only once
        assert mock_get.call_count == 1
