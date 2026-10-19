"""
Shared fixtures and test configuration for FastAPI API tests.
"""

from typing import Any, AsyncGenerator, Dict

import pytest
from httpx import ASGITransport, AsyncClient

from crop_advisory.api.main import create_app


@pytest.fixture
def test_app():
    """Create a FastAPI application instance configured for testing."""
    return create_app()


@pytest.fixture
async def async_client(test_app) -> AsyncGenerator[AsyncClient, None]:
    """
    Async HTTPX client with application lifespan active (models and datasets preloaded).
    """
    async with test_app.router.lifespan_context(test_app):
        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client


@pytest.fixture
async def uninitialized_client(test_app) -> AsyncGenerator[AsyncClient, None]:
    """
    Async HTTPX client WITHOUT entering lifespan context (to test unready / 503 state).
    """
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def valid_crop_rec_payload() -> Dict[str, Any]:
    """Valid payload for crop recommendation."""
    return {
        "n": 90.0,
        "p": 42.0,
        "k": 43.0,
        "temperature": 21.0,
        "humidity": 82.0,
        "ph": 6.5,
        "rainfall": 202.0,
        "top_k": 3,
    }


@pytest.fixture
def invalid_crop_rec_payload() -> Dict[str, Any]:
    """Invalid payload for crop recommendation (pH > 14)."""
    return {
        "n": 90.0,
        "p": 42.0,
        "k": 43.0,
        "temperature": 21.0,
        "humidity": 82.0,
        "ph": 15.5,  # Invalid: max allowed is 14.0
        "rainfall": 202.0,
        "top_k": 3,
    }


@pytest.fixture
def valid_yield_payload() -> Dict[str, Any]:
    """Valid payload for yield prediction."""
    return {
        "crop": "rice",
        "season": "Kharif",
        "state": "Maharashtra",
        "soil_type": "Vertisols",
        "temperature": 25.0,
        "rainfall": 900.0,
        "humidity": 70.0,
        "ph": 6.5,
        "nitrogen": 90.0,
        "phosphorus": 40.0,
        "potassium": 40.0,
        "fertilizer": 100.0,
        "pesticide": 0.35,
    }


@pytest.fixture
def valid_cost_payload() -> Dict[str, Any]:
    """Valid payload for cultivation cost estimation."""
    return {
        "crop_name": "rice",
        "state_name": "Maharashtra",
    }


@pytest.fixture
def valid_financial_payload() -> Dict[str, Any]:
    """Valid payload for farm financial analysis."""
    return {
        "yield_kg_per_ha": 3500.0,
        "farm_area": 2.5,
        "area_unit": "acre",
        "price_per_quintal": 2250.0,
        "cost_per_ha": 35000.0,
    }


@pytest.fixture
def valid_advisory_payload() -> Dict[str, Any]:
    """Valid payload for end-to-end full agricultural advisory."""
    return {
        "n": 90.0,
        "p": 42.0,
        "k": 43.0,
        "temperature": 21.0,
        "humidity": 82.0,
        "ph": 6.5,
        "rainfall": 202.0,
        "state": "Maharashtra",
        "soil_type": "Vertisols",
        "season": "Kharif",
        "farm_area": 3.0,
        "area_unit": "acre",
        "top_k": 3,
    }
