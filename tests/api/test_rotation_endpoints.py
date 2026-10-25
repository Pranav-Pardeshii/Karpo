"""
API tests for Crop Rotation & Intercropping endpoints:
- POST /api/v1/rotation/plan
- GET /api/v1/rotation/intercropping/{crop}
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_rotation_plan_endpoint(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/rotation/plan",
        json={
            "current_crop": "cotton",
            "soil_type": "Vertisols",
            "irrigation_available": True,
            "state": "Maharashtra",
            "years": 2,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["current_crop"] == "cotton"
    assert data["plan_years"] == 2
    assert len(data["yearly_plans"]) == 2
    assert data["data_category"] == "Estimated"
    assert "ICAR" in data["data_provenance"]
    assert len(data["intercropping_options"]) > 0


@pytest.mark.asyncio
async def test_intercropping_endpoint_cotton(async_client: AsyncClient):
    response = await async_client.get("/api/v1/rotation/intercropping/cotton")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    crops = [item["intercrop_crop"] for item in data]
    assert "pigeonpeas" in crops


@pytest.mark.asyncio
async def test_intercropping_endpoint_unknown_crop(async_client: AsyncClient):
    response = await async_client.get("/api/v1/rotation/intercropping/xyz_crop")
    assert response.status_code == 200
    data = response.json()
    assert data == []


@pytest.mark.asyncio
async def test_rotation_plan_invalid_years(async_client: AsyncClient):
    # years=5 violates ge=1, le=3
    response = await async_client.post(
        "/api/v1/rotation/plan",
        json={
            "current_crop": "cotton",
            "years": 5,
        },
    )
    assert response.status_code == 422
