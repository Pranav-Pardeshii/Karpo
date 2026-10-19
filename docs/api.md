# Smart Crop Advisory REST API Reference (`v1`)

The Smart Crop Advisory API provides production-grade, asynchronous endpoints for agricultural intelligence, machine learning inference, market price lookup, and farm financial decision support.

- **Base URL Prefix**: `/api/v1`
- **Interactive OpenAPI Documentation (Swagger UI)**: `http://localhost:8000/docs`
- **Machine-Readable OpenAPI Specification**: `http://localhost:8000/openapi.json`
- **Alternative ReDoc UI**: `http://localhost:8000/redoc`

---

## Standard Headers & Observability

Every request processes through centralized correlation and timing middleware:

| Header Name | Type | Description |
|:---|:---|:---|
| `X-Request-ID` | String | Unique request trace ID (e.g. `req_7a8b9c0d1e2f`). If supplied by client, it is preserved; otherwise generated via `uuid4`. |
| `X-Process-Time` | String | Execution duration in milliseconds (e.g. `4.25ms`). |

---

## Error Response Format

All error responses return a uniform JSON schema across 4xx and 5xx status codes:

```json
{
  "error_code": "INVALID_REQUEST_PAYLOAD",
  "message": "One or more fields failed schema validation.",
  "request_id": "req_8f1b2c3d4e5a",
  "details": [
    {
      "field": "ph",
      "message": "Input should be less than or equal to 14",
      "type": "less_than_equal"
    }
  ],
  "timestamp": "2026-10-18T15:00:00.000000Z"
}
```

### Standard Error Codes

| Status Code | Error Code | Meaning |
|:---|:---|:---|
| `404 Not Found` | `CROP_NOT_FOUND` | Specified crop slug or alias is not in the canonical agronomic taxonomy. |
| `422 Unprocessable Content` | `INVALID_REQUEST_PAYLOAD` | Request body failed Pydantic schema validation or bound constraints. |
| `422 Unprocessable Content` | `VALIDATION_ERROR` | Domain-level feature validation failed (e.g. negative NPK). |
| `503 Service Unavailable` | `SERVICE_NOT_READY` | Application startup has not completed or model artifacts are uninitialized. |
| `503 Service Unavailable` | `MODEL_NOT_FOUND` | Mandatory ML model pipeline file missing from disk. |
| `503 Service Unavailable` | `DATASET_UNAVAILABLE` | Reference CSV dataset (prices or CACP costs) missing. |
| `500 Internal Server Error` | `INFERENCE_FAILURE` | Exception occurred during model inference. |
| `500 Internal Server Error` | `INTERNAL_SERVER_ERROR` | Unhandled internal exception; safe generic error returned to client. |

---

## 1. System Health & Diagnostics

### `GET /api/v1/health/live`
Confirms the ASGI application process is alive and receiving traffic.

- **Status Code**: `200 OK`
- **Response**:
```json
{
  "status": "alive",
  "timestamp": "2026-10-18T15:10:00.123456Z"
}
```

### `GET /api/v1/health/ready`
Confirms that all machine learning models (Random Forest, XGBoost) and reference agricultural datasets (Agmarknet prices, CACP costs) are preloaded in memory and ready for inference.

- **Status Code**: `200 OK` (when ready) / `503 Service Unavailable` (when uninitialized or corrupted)
- **Response**:
```json
{
  "status": "ready",
  "models_loaded": true,
  "datasets_loaded": true,
  "details": {
    "models": "Loaded successfully",
    "datasets": {
      "prices_count": 122,
      "cost_records_count": 3880
    }
  },
  "timestamp": "2026-10-18T15:10:00.123456Z"
}
```

---

## 2. Crop Recommendation

### `POST /api/v1/crops/recommend`
Recommends top candidate crops based on soil chemistry (Nitrogen, Phosphorus, Potassium, pH) and ambient climatic factors (temperature, humidity, rainfall). Inference is offloaded to a non-blocking thread pool bounded by AnyIO capacity limiter.

- **Request Body**:
```json
{
  "n": 90.0,
  "p": 42.0,
  "k": 43.0,
  "temperature": 20.87,
  "humidity": 82.0,
  "ph": 6.5,
  "rainfall": 202.93,
  "top_k": 3
}
```

- **Validation Rules**:
  - `n`, `p`, `k`: Float [0.0 - 300.0] kg/ha
  - `temperature`: Float [-10.0 - 60.0] °C
  - `humidity`: Float [0.0 - 100.0] %
  - `ph`: Float [1.0 - 14.0]
  - `rainfall`: Float [0.0 - 3000.0] mm
  - `top_k`: Integer [1 - 22], default `3`

- **Response** (`200 OK`):
```json
{
  "primary_crop": "rice",
  "display_name": "Rice",
  "confidence_percent": 90.16,
  "category": "Cereal",
  "description": "Paddy is a primary staple cereal requiring high water availability and warm humid climates.",
  "recommendations": [
    {
      "crop": "rice",
      "display_name": "Rice",
      "category": "Cereal",
      "confidence_score": 90.16,
      "probability": 0.9016,
      "description": "Paddy is a primary staple cereal..."
    },
    {
      "crop": "jute",
      "display_name": "Jute",
      "category": "Fiber",
      "confidence_score": 6.24,
      "probability": 0.0624,
      "description": "Golden fiber crop suitable for warm humid alluvial floodplains."
    },
    {
      "crop": "coffee",
      "display_name": "Coffee",
      "category": "Cash Crop",
      "confidence_score": 1.82,
      "probability": 0.0182,
      "description": "Perennial plantation crop requiring hilly shade and moderate temperatures."
    }
  ],
  "soil_advisory_notes": [],
  "model_used": "RandomForestClassifier(n_estimators=100)"
}
```

### `GET /api/v1/crops/supported`
Returns canonical agronomic metadata for all 22 supported crops.

- **Response** (`200 OK`):
```json
[
  {
    "canonical_name": "rice",
    "display_name": "Rice",
    "category": "Cereal",
    "yield_crop": "Rice",
    "price_crop": "Rice",
    "cost_crop": "PADDY",
    "default_season": "Kharif",
    "default_soil": "Clayey / Alluvial",
    "default_fertilizer": 120.0,
    "default_pesticide": 0.5,
    "description": "Paddy is a primary staple cereal requiring high water availability and warm humid climates."
  }
]
```

### `GET /api/v1/crops/{crop_name}`
Retrieves canonical metadata for a single crop, resolving synonyms and vernacular variations (e.g. `paddy` -> `rice`, `groundnut` -> `peanut`).

---

## 3. Agricultural Yield Prediction

### `POST /api/v1/yield/predict`
Predicts crop yield in both metric (`kg/ha`, `Q/ha`) and imperial farm units (`kg/acre`, `Q/acre`) using trained XGBoost regressors or agronomic calibrated models.

- **Request Body**:
```json
{
  "crop": "rice",
  "season": "Kharif",
  "soil_type": "Vertisols",
  "state": "Maharashtra",
  "temperature": 25.0,
  "rainfall": 900.0,
  "humidity": 70.0,
  "ph": 6.5,
  "nitrogen": 90.0,
  "phosphorus": 40.0,
  "potassium": 40.0,
  "fertilizer": 100.0,
  "pesticide": 0.35
}
```

- **Response** (`200 OK`):
```json
{
  "crop": "rice",
  "mapped_yield_crop": "Rice",
  "prediction_method": "Trained ML Regressor (XGBoost)",
  "predicted_yield_kg_ha": 3524.81,
  "predicted_yield_quintals_ha": 35.25,
  "predicted_yield_kg_acre": 1426.44,
  "predicted_yield_quintals_acre": 14.26,
  "historical_min_kg_ha": 1500.0,
  "historical_median_kg_ha": 3500.0,
  "historical_max_kg_ha": 6500.0
}
```

### `GET /api/v1/yield/benchmarks`
Retrieves historical yield reference benchmarks across major Indian crops.

---

## 4. Mandi Market Prices

### `GET /api/v1/market/prices`
Paginated search and listing of official APMC Mandi wholesale commodity prices.

- **Query Parameters**:
  - `query` (optional string): Filter by crop name (e.g. `?query=wheat`)
  - `limit` (optional integer): Records per page (1 - 200, default `50`)
  - `offset` (optional integer): Record offset for pagination (default `0`)

- **Response** (`200 OK`):
```json
{
  "total_records": 122,
  "prices": [
    {
      "canonical_name": "wheat",
      "matched_crop_name": "Wheat",
      "modal_rs_per_quintal": 2275.0,
      "min_rs_per_quintal": 2125.0,
      "max_rs_per_quintal": 2450.0,
      "msp_rs_per_quintal": 2275.0,
      "price_per_kg": 22.75,
      "source": "Agmarknet Mandi Price Reference (india-crop-prices.csv)"
    }
  ]
}
```

### `GET /api/v1/market/prices/{crop_name}`
Looks up the wholesale rate for a specific crop. Automatically applies conservative fallback benchmarks if the crop is not surveyed in APMC wholesale reports.

---

## 5. Cultivation Cost Estimation

### `POST /api/v1/cultivation-costs/estimate`
Calculates comprehensive CACP C2 Cost of Cultivation benchmarks including seed, fertilizer, labor, machinery, and land rental estimates.

- **Request Body**:
```json
{
  "crop_name": "rice",
  "state_name": "Maharashtra"
}
```

- **Response** (`200 OK`):
```json
{
  "canonical_name": "rice",
  "matched_cost_crop": "PADDY",
  "applied_state": "Maharashtra",
  "cul_cost_c2_per_ha": 42560.0,
  "cul_cost_c2_per_acre": 17223.48,
  "prod_cost_c2_per_quintal": 1450.0,
  "seed_cost_per_ha": 2500.0,
  "fertilizer_cost_per_ha": 6200.0,
  "labor_cost_per_ha": 18400.0,
  "machinery_cost_per_ha": 8500.0,
  "source": "CACP Comprehensive Scheme (cost_of_cultivation.csv)"
}
```

### `GET /api/v1/cultivation-costs/states`
Returns all Indian states with empirical CACP cost survey records.

---

## 6. Farm Economics & Financial Feasibility

### `POST /api/v1/financial-analysis`
Computes gross revenue, total cultivation expenditure, net farm income, profit per acre/hectare, Return on Investment (ROI %), and critical break-even yield and price thresholds.

- **Request Body**:
```json
{
  "yield_kg_per_ha": 3500.0,
  "farm_area": 2.5,
  "area_unit": "acre",
  "price_per_quintal": 2250.0,
  "cost_per_ha": 35000.0
}
```

- **Response** (`200 OK`):
```json
{
  "input_area": 2.5,
  "input_unit": "acre",
  "area_hectares": 1.0117,
  "area_acres": 2.5,
  "yield_kg_per_ha": 3500.0,
  "yield_quintals_per_ha": 35.0,
  "yield_kg_acre": 1416.4,
  "yield_quintals_per_acre": 14.16,
  "total_production_kg": 3541.0,
  "total_production_quintals": 35.41,
  "price_per_quintal": 2250.0,
  "price_per_kg": 22.5,
  "cost_per_ha": 35000.0,
  "cost_per_acre": 14163.99,
  "total_revenue": 79672.5,
  "total_cost": 35410.0,
  "net_profit": 44262.5,
  "profit_per_acre": 17705.0,
  "profit_per_ha": 43750.0,
  "roi_percent": 125.0,
  "profit_margin_percent": 55.56,
  "breakeven_yield_kg_per_ha": 1555.56,
  "breakeven_price_per_quintal": 1000.0,
  "formatted_revenue": "₹79,672",
  "formatted_cost": "₹35,410",
  "formatted_profit": "₹44,262",
  "formatted_profit_per_acre": "₹17,705",
  "formatted_profit_per_ha": "₹43,750",
  "formatted_revenue_short": "₹79.7 K",
  "formatted_cost_short": "₹35.4 K",
  "formatted_profit_short": "₹44.3 K"
}
```

---

## 7. Integrated Full Agricultural Advisory

### `POST /api/v1/advisory/full`
Orchestrates the entire agricultural advisory pipeline in a single unified API call:
1. Recommends the optimal crop given soil chemistry and climate.
2. Predicts expected yield for the recommended crop in the farmer's state, season, and soil.
3. Retrieves current APMC mandi market wholesale rate and MSP.
4. Estimates CACP C2 cultivation expenditure.
5. Computes complete financial profitability, net profit, ROI, and break-even targets.

- **Request Body**:
```json
{
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
  "top_k": 3
}
```

- **Response** (`200 OK`):
Returns a complete composite report containing `recommendation`, `yield_prediction`, `market_price`, `cultivation_cost`, `financials`, and operational metadata with execution timestamps.
