# Operations & Deployment Guide

This guide covers operational execution, environment configuration, containerization, observability, and infrastructure decisions for the Smart Crop Advisory FastAPI backend.

---

## 1. Running the Backend

The project uses [uv](https://github.com/astral-sh/uv) for fast, deterministic dependency resolution and environment management.

### Local Development Server

Run Uvicorn with auto-reload enabled:

```bash
uv run uvicorn crop_advisory.api.main:app --reload --host 127.0.0.1 --port 8000
```

Once running:
- API Index: [http://localhost:8000/](http://localhost:8000/)
- OpenAPI Interactive UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Liveness Probe: [http://localhost:8000/api/v1/health/live](http://localhost:8000/api/v1/health/live)
- Readiness Probe: [http://localhost:8000/api/v1/health/ready](http://localhost:8000/api/v1/health/ready)

### Production ASGI Execution

In a production environment, run Uvicorn with single or multi-worker configuration (or Gunicorn with Uvicorn worker class) without reload:

```bash
uv run uvicorn crop_advisory.api.main:app --host 0.0.0.0 --port 8000 --workers 2 --access-log
```

---

## 2. Environment Configuration

All settings are strongly typed using `pydantic-settings.BaseSettings` in `src/crop_advisory/api/config.py`.
Variables can be passed via system environment variables or a `.env` file in the project root.

| Environment Variable | Type | Default | Description |
|:---|:---|:---|:---|
| `CROP_ADVISORY_ENV` | `str` | `production` | Runtime mode: `development`, `testing`, `production` |
| `CROP_ADVISORY_DEBUG` | `bool` | `false` | Enable detailed debug logs and exception details in responses |
| `CROP_ADVISORY_HOST` | `str` | `0.0.0.0` | Bind host address for the HTTP server |
| `CROP_ADVISORY_PORT` | `int` | `8000` | Bind port for the HTTP server |
| `CROP_ADVISORY_LOG_LEVEL` | `str` | `INFO` | Logger verbosity: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `CROP_ADVISORY_CORS_ORIGINS` | `list[str]` | `["*"]` | Allowed CORS origins for frontend web applications |
| `CROP_ADVISORY_ALLOWED_HOSTS` | `list[str]` | `["*"]` | Trusted host headers for HTTP host header protection |
| `CROP_ADVISORY_MAX_CONCURRENCY` | `int` | `10` | Maximum simultaneous CPU inference threads allowed by AnyIO limiter |
| `CROP_ADVISORY_HTTP_TIMEOUT` | `float` | `10.0` | Default timeout in seconds for external HTTP client calls |
| `CROP_ADVISORY_MODELS_DIR` | `Path` | `models/` | Directory path containing trained joblib/pickle model pipelines |
| `CROP_ADVISORY_DATASETS_DIR` | `Path` | `datasets/` | Directory path containing price and cultivation cost CSV datasets |

A template file `.env.example` is provided in the repository root.

---

## 3. Application Lifecycle & Health Probes

The application uses FastAPI's `lifespan` context manager (`src/crop_advisory/api/lifespan.py`) to manage startup and shutdown deterministically.

```
       Startup (Lifespan Enter)
                  │
  ┌───────────────┴───────────────┐
  ▼                               ▼
Preload ML Models          Preload & Cache Datasets
- RandomForest (rec)       - india-crop-prices.csv
- XGBoost (yield)          - cost_of_cultivation.csv
  │                               │
  └───────────────┬───────────────┘
                  ▼
   Initialize CapacityLimiter (threads=10)
   Initialize Shared httpx.AsyncClient
   Set app.state.is_ready = True
                  │
           Request Handling
                  │
       Shutdown (Lifespan Exit)
                  ▼
   Close httpx.AsyncClient connections
   Release model & dataset references
   Set app.state.is_ready = False
```

### Health Check Semantics

1. **Liveness Probe (`/api/v1/health/live`)**:
   - Purpose: Kubernetes / ECS / Docker container liveness test.
   - Evaluates: Whether the ASGI event loop is active and accepting socket connections.
   - Overhead: Zero I/O, instantaneous execution (< 1ms).
   - Response: `200 OK` always, returning current UTC timestamp.

2. **Readiness Probe (`/api/v1/health/ready`)**:
   - Purpose: Load balancer traffic readiness gating.
   - Evaluates: Whether models and datasets have successfully loaded into memory.
   - Response:
     - `200 OK` when `models_loaded: true` and `datasets_loaded: true`.
     - `503 Service Unavailable` if startup failed or models are missing.

---

## 4. Asynchronous Architecture & CPU-Bound ML Inference

### The Problem
Scikit-learn tree inference (`RandomForestClassifier.predict_proba`) and XGBoost regression (`XGBRegressor.predict`) execute synchronous, CPU-intensive C-extension code. Executing them directly in an `async def` route would freeze Python's single-threaded asyncio event loop, causing all concurrent HTTP requests, health checks, and I/O to queue up.

### The Solution
We use AnyIO's thread-worker bridge bounded by a capacity limiter:

```python
async with limiter:
    raw_result = await anyio.to_thread.run_sync(
        recommender.predict, n, p, k, temperature, humidity, ph, rainfall, top_k
    )
```

**Key Architectural Guarantees**:
1. **Non-blocking Event Loop**: The asyncio event loop remains free to process incoming requests, health probes, and I/O tasks while CPU-bound math executes in a background worker thread.
2. **Strict Concurrency Bound**: The `anyio.CapacityLimiter` (default: 10 concurrent threads) strictly prevents thread-pool explosion, thrashing, and memory saturation under high traffic bursts.
3. **Zero Request Disk I/O**: Models and CSV datasets are preloaded during lifespan startup and held in memory; inference calls never touch the disk.

---

## 5. Architectural Decision: Stateless Design vs Database Persistence

### Decision
**No database (PostgreSQL/SQLAlchemy/Alembic) is added in Phase 2.** The backend remains completely stateless.

### Justification & Product Requirements Analysis
1. **Current Domain Capabilities**:
   - Crop recommendation: Mathematical function of `(N, P, K, pH, climate) -> [Crops]`.
   - Yield prediction: Mathematical function of `(crop, season, state, soil, inputs) -> Yield`.
   - Price intelligence: Read-only in-memory lookup against Agmarknet APMC benchmarks.
   - Cost estimation: Read-only in-memory lookup against CACP survey records.
   - Farm economics: Deterministic algebraic calculations for revenue, cost, profit, and ROI.
2. **No Persistent Entities in Scope**:
   - No user authentication or registration (deferred to a dedicated future phase).
   - No durable farm profiles, land records, or saved farmer history.
   - Agricultural inputs are calculated on-the-fly and returned in the HTTP response.
3. **Operational Simplicity**:
   - Avoids speculative infrastructure (PostgreSQL container, volume provisioning, migration pipelines, connection pool sizing).
   - Allows the backend to scale horizontally across any number of container instances without database locks, connection bottlenecks, or read/write split complexity.

---

## 6. Container Deployment with Docker

A production-ready, multi-stage `Dockerfile` is provided in the repository root.

### Docker Highlights
- **Multi-stage build**: Builder stage uses `ghcr.io/astral-sh/uv` to install dependencies; runner stage uses minimal `python:3.12-slim`.
- **Security**: Runs under a dedicated non-root user `appuser` (UID `10001`).
- **Layer caching**: Dependency metadata (`pyproject.toml`, `uv.lock`) is copied and cached before source code.
- **Built-in Healthcheck**: Tests `http://127.0.0.1:8000/api/v1/health/live` every 30 seconds.

### Build and Run

```bash
# Build the production Docker image
docker build -t smart-crop-advisory-api:latest .

# Run the container
docker run -d \
  --name crop-api \
  -p 8000:8000 \
  -e CROP_ADVISORY_ENV=production \
  -e CROP_ADVISORY_LOG_LEVEL=INFO \
  smart-crop-advisory-api:latest

# Check container status and health
docker ps

# View application logs
docker logs -f crop-api
```

---

## 7. Streamlit Presentation Coexistence

The existing Streamlit application remains fully functional and operates alongside the new FastAPI backend:

```bash
# Run the Streamlit web dashboard
uv run streamlit run src/crop_advisory/presentation/streamlit_app.py --server.port 8501
```

Both the Streamlit UI and the FastAPI backend share identical underlying domain packages (`crop_advisory.ml`, `crop_advisory.services`, `crop_advisory.domain`), ensuring numerical consistency across both interfaces without duplicate business logic.
