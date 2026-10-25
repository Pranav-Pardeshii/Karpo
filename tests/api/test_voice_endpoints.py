"""
API tests for Kisan Voice Copilot endpoint /api/v1/voice/query.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_voice_query_success_marathi(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/voice/query",
        json={
            "query_text": "सोयाबीनचा भाव सांगा",
            "language": "mr",
            "state": "Maharashtra",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["matched_crop"] == "soybean"
    assert data["intent"] == "market_price"
    assert data["data_category"] == "Observed"
    assert "spoken_text" in data
    assert "display_text" in data
    assert "modal_rs_per_quintal" in data["structured_data"]


@pytest.mark.asyncio
async def test_voice_query_success_english(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/voice/query",
        json={
            "query_text": "What is the cost of cotton cultivation in Gujarat?",
            "language": "en",
            "state": "Gujarat",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["matched_crop"] == "cotton"
    assert data["intent"] == "cultivation_cost"
    assert data["data_category"] == "Historical"


@pytest.mark.asyncio
async def test_voice_query_validation_error(async_client: AsyncClient):
    # Empty query text violates min_length=1
    response = await async_client.post(
        "/api/v1/voice/query",
        json={
            "query_text": "",
            "language": "en",
        },
    )
    assert response.status_code == 422
