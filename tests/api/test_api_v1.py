"""
Integration tests for the versioned REST API (/api/v1).
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_endpoint(async_client: AsyncClient):
    """Verify root endpoint provides API metadata and links."""
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Smart Crop Advisory API"
    assert "version" in data
    assert data["docs_url"] == "/docs"
    assert data["status"] == "operational"


@pytest.mark.asyncio
async def test_health_live_endpoint(async_client: AsyncClient):
    """Verify liveness probe returns alive status."""
    response = await async_client.get("/api/v1/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_health_ready_endpoint(async_client: AsyncClient):
    """Verify readiness probe returns ready when models and data are loaded."""
    response = await async_client.get("/api/v1/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["models_loaded"] is True
    assert data["datasets_loaded"] is True
    assert "details" in data


@pytest.mark.asyncio
async def test_health_ready_uninitialized(uninitialized_client: AsyncClient):
    """Verify readiness probe returns 503 when models are not loaded."""
    response = await uninitialized_client.get("/api/v1/health/ready")
    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "not_ready"
    assert data["models_loaded"] is False


@pytest.mark.asyncio
async def test_custom_request_id_and_headers(async_client: AsyncClient):
    """Verify correlation ID and processing time headers are returned."""
    custom_id = "test-corr-id-999"
    response = await async_client.get(
        "/api/v1/health/live",
        headers={"X-Request-ID": custom_id},
    )
    assert response.status_code == 200
    assert response.headers.get("x-request-id") == custom_id
    assert "x-process-time" in response.headers


# ==============================================================================
# Crop Recommendation Tests
# ==============================================================================


@pytest.mark.asyncio
async def test_crop_recommendation_success(async_client: AsyncClient, valid_crop_rec_payload):
    """Test successful crop recommendation with valid soil/climate inputs."""
    response = await async_client.post(
        "/api/v1/crops/recommend",
        json=valid_crop_rec_payload,
    )
    assert response.status_code == 200
    data = response.json()
    assert "primary_crop" in data
    assert "recommendations" in data
    assert len(data["recommendations"]) == 3
    assert data["primary_crop"] == data["recommendations"][0]["crop"]
    assert 0.0 <= data["confidence_percent"] <= 100.0
    assert isinstance(data["soil_advisory_notes"], list)


@pytest.mark.asyncio
async def test_crop_recommendation_validation_failure(
    async_client: AsyncClient, invalid_crop_rec_payload
):
    """Test validation failure on out-of-range agricultural inputs."""
    response = await async_client.post(
        "/api/v1/crops/recommend",
        json=invalid_crop_rec_payload,
    )
    assert response.status_code == 422
    data = response.json()
    assert data["error_code"] == "INVALID_REQUEST_PAYLOAD"
    assert "ph" in str(data["details"]).lower()
    assert "request_id" in data


@pytest.mark.asyncio
async def test_get_supported_crops(async_client: AsyncClient):
    """Test listing all 22 supported crops."""
    response = await async_client.get("/api/v1/crops/supported")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 22
    crop_names = [c["canonical_name"] for c in data]
    assert "rice" in crop_names
    assert "cotton" in crop_names
    assert "maize" in crop_names


@pytest.mark.asyncio
async def test_get_crop_details_found(async_client: AsyncClient):
    """Test retrieving details for a known crop."""
    response = await async_client.get("/api/v1/crops/rice")
    assert response.status_code == 200
    data = response.json()
    assert data["canonical_name"] == "rice"
    assert data["category"] == "Cereal"


@pytest.mark.asyncio
async def test_get_crop_details_not_found(async_client: AsyncClient):
    """Test retrieving details for an unknown crop returns 404."""
    response = await async_client.get("/api/v1/crops/nonexistent_crop_xyz")
    assert response.status_code == 404
    data = response.json()
    assert data["error_code"] == "CROP_NOT_FOUND"


# ==============================================================================
# Yield Prediction Tests
# ==============================================================================


@pytest.mark.asyncio
async def test_yield_prediction_success(async_client: AsyncClient, valid_yield_payload):
    """Test yield prediction with XGBoost pipeline."""
    response = await async_client.post(
        "/api/v1/yield/predict",
        json=valid_yield_payload,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["crop"] == "rice"
    assert data["predicted_yield_kg_ha"] > 0
    assert data["predicted_yield_quintals_ha"] > 0
    assert data["predicted_yield_kg_acre"] > 0
    assert data["predicted_yield_quintals_acre"] > 0
    assert data["historical_median_kg_ha"] > 0


@pytest.mark.asyncio
async def test_yield_prediction_invalid_input(async_client: AsyncClient, valid_yield_payload):
    """Test yield prediction validation error when pH is out of bounds."""
    payload = valid_yield_payload.copy()
    payload["ph"] = 15.0  # Must be <= 14.0
    response = await async_client.post(
        "/api/v1/yield/predict",
        json=payload,
    )
    assert response.status_code == 422
    data = response.json()
    assert data["error_code"] == "INVALID_REQUEST_PAYLOAD"


@pytest.mark.asyncio
async def test_yield_benchmarks(async_client: AsyncClient):
    """Test yield benchmarks listing."""
    response = await async_client.get("/api/v1/yield/benchmarks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    crops = [b["crop"] for b in data]
    assert "Rice" in crops


# ==============================================================================
# Mandi Market Prices Tests
# ==============================================================================


@pytest.mark.asyncio
async def test_market_prices_list(async_client: AsyncClient):
    """Test querying market prices with pagination."""
    response = await async_client.get("/api/v1/market/prices?limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert "total_records" in data
    assert data["total_records"] > 100
    assert len(data["prices"]) <= 10


@pytest.mark.asyncio
async def test_market_prices_filter(async_client: AsyncClient):
    """Test searching market prices by crop name query."""
    response = await async_client.get("/api/v1/market/prices?query=wheat")
    assert response.status_code == 200
    data = response.json()
    assert data["total_records"] >= 1
    assert any("wheat" in item["canonical_name"].lower() for item in data["prices"])


@pytest.mark.asyncio
async def test_market_price_single_crop(async_client: AsyncClient):
    """Test looking up price for specific crop."""
    response = await async_client.get("/api/v1/market/prices/rice")
    assert response.status_code == 200
    data = response.json()
    assert data["canonical_name"] == "rice"
    assert data["modal_rs_per_quintal"] > 0


@pytest.mark.asyncio
async def test_market_price_fallback(async_client: AsyncClient):
    """Test looking up price for crop not in CSV uses conservative fallback."""
    response = await async_client.get("/api/v1/market/prices/unknown_fruit_123")
    assert response.status_code == 200
    data = response.json()
    assert "Agmarknet" in data["source"]
    assert data["modal_rs_per_quintal"] > 0


# ==============================================================================
# Cultivation Cost Tests
# ==============================================================================


@pytest.mark.asyncio
async def test_cultivation_cost_estimation(async_client: AsyncClient, valid_cost_payload):
    """Test cost estimation using CACP dataset."""
    response = await async_client.post(
        "/api/v1/cultivation-costs/estimate",
        json=valid_cost_payload,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["canonical_name"] == "rice"
    assert data["applied_state"] == "Maharashtra"
    assert data["cul_cost_c2_per_ha"] > 0
    assert data["cul_cost_c2_per_acre"] > 0


@pytest.mark.asyncio
async def test_cultivation_cost_states(async_client: AsyncClient):
    """Test listing available states with historical cost data."""
    response = await async_client.get("/api/v1/cultivation-costs/states")
    assert response.status_code == 200
    data = response.json()
    assert "states" in data
    assert "Maharashtra" in data["states"]


# ==============================================================================
# Farm Financial Analysis Tests
# ==============================================================================


@pytest.mark.asyncio
async def test_financial_analysis_success(async_client: AsyncClient, valid_financial_payload):
    """Test farm profitability, ROI, and break-even calculations."""
    response = await async_client.post(
        "/api/v1/financial-analysis",
        json=valid_financial_payload,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_revenue"] > 0
    assert data["total_cost"] > 0
    assert "net_profit" in data
    assert "roi_percent" in data
    assert data["breakeven_yield_kg_per_ha"] > 0
    assert data["breakeven_price_per_quintal"] > 0


# ==============================================================================
# Full Advisory Orchestration Tests
# ==============================================================================


@pytest.mark.asyncio
async def test_full_advisory_pipeline(async_client: AsyncClient, valid_advisory_payload):
    """Test integrated end-to-end advisory recommendation flow."""
    response = await async_client.post(
        "/api/v1/advisory/full",
        json=valid_advisory_payload,
    )
    assert response.status_code == 200
    data = response.json()
    assert "recommendation" in data
    assert "yield_prediction" in data
    assert "market_price" in data
    assert "cultivation_cost" in data
    assert "financials" in data
    assert "metadata" in data
    assert data["recommendation"]["primary_crop"] is not None
