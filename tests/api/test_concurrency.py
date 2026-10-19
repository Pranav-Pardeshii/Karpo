"""
Tests for concurrent asynchronous execution and thread-pool capacity limiting.
"""

import asyncio

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_concurrent_crop_recommendations(async_client: AsyncClient, valid_crop_rec_payload):
    """
    Test running 20 concurrent crop recommendations.
    Ensures AnyIO CapacityLimiter bounds inference threads without deadlocks or crashes.
    """
    tasks = [
        async_client.post("/api/v1/crops/recommend", json=valid_crop_rec_payload) for _ in range(20)
    ]
    responses = await asyncio.gather(*tasks)

    assert len(responses) == 20
    for res in responses:
        assert res.status_code == 200
        data = res.json()
        assert "primary_crop" in data
        assert len(data["recommendations"]) == 3


@pytest.mark.asyncio
async def test_concurrent_yield_predictions(async_client: AsyncClient, valid_yield_payload):
    """
    Test running 20 concurrent yield predictions.
    Ensures XGBoost pipeline safely handles simultaneous inference calls.
    """
    tasks = [
        async_client.post("/api/v1/yield/predict", json=valid_yield_payload) for _ in range(20)
    ]
    responses = await asyncio.gather(*tasks)

    assert len(responses) == 20
    for res in responses:
        assert res.status_code == 200
        data = res.json()
        assert data["crop"] == "rice"
        assert data["predicted_yield_kg_ha"] > 0


@pytest.mark.asyncio
async def test_mixed_concurrent_workload(
    async_client: AsyncClient,
    valid_crop_rec_payload,
    valid_yield_payload,
    valid_financial_payload,
):
    """
    Test mixed concurrent requests: recommendations, yield predictions,
    financial calculations, and market price queries simultaneously.
    """
    tasks = []
    # 5 recommendations
    tasks.extend(
        async_client.post("/api/v1/crops/recommend", json=valid_crop_rec_payload) for _ in range(5)
    )
    # 5 yield predictions
    tasks.extend(
        async_client.post("/api/v1/yield/predict", json=valid_yield_payload) for _ in range(5)
    )
    # 5 financial analyses
    tasks.extend(
        async_client.post("/api/v1/financial-analysis", json=valid_financial_payload)
        for _ in range(5)
    )
    # 5 market queries
    tasks.extend(async_client.get("/api/v1/market/prices/rice") for _ in range(5))

    responses = await asyncio.gather(*tasks)
    assert len(responses) == 20
    for res in responses:
        assert res.status_code == 200
