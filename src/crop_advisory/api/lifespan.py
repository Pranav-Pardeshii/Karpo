"""
FastAPI Lifespan Manager for Resource Initialization and Graceful Shutdown.
Preloads ML models, validates reference datasets, manages shared HTTP clients,
and configures AnyIO concurrency limiters for non-blocking inference offloading.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import anyio
import httpx
from fastapi import FastAPI

from crop_advisory.api.config import api_settings
from crop_advisory.ml.model_loader import default_model_loader
from crop_advisory.services.cultivation_cost_service import load_cost_dataset
from crop_advisory.services.market_service import load_prices_dataset

logger = logging.getLogger("crop_advisory.api.lifespan")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan context manager:
    - Preloads and validates machine learning model pipelines
    - Preloads and caches Mandi and CACP datasets
    - Configures bounded concurrency limiter for CPU-bound thread offloading
    - Initializes shared HTTPX client
    - Deterministically closes connections on shutdown
    """
    logger.info("Initializing Smart Crop Advisory API resources...")

    # 1. State tracking initialization
    app.state.is_ready = False
    app.state.models_ready = False
    app.state.datasets_ready = False
    app.state.diagnostics = {}

    # 2. Concurrency Limiter for CPU-bound Model Inference
    # Prevents unbounded thread creation and protects CPU/memory capacity
    app.state.inference_limiter = anyio.CapacityLimiter(api_settings.max_inference_concurrency)
    logger.info(
        f"Inference concurrency limiter initialized with capacity: {api_settings.max_inference_concurrency}"
    )

    # 3. Model Preloading
    try:
        default_model_loader.load_crop_recommendation_model()
        default_model_loader.load_crop_recommendation_preprocessor()
        default_model_loader.load_yield_prediction_model()
        default_model_loader.load_yield_prediction_preprocessor()
        app.state.models_ready = True
        app.state.diagnostics["models"] = "Loaded successfully"
        logger.info("Machine learning models and preprocessors loaded successfully.")
    except Exception as exc:
        app.state.models_ready = False
        app.state.diagnostics["models"] = f"Failed to load: {exc}"
        logger.error(f"Error loading model artifacts during startup: {exc}", exc_info=True)

    # 4. Reference Datasets Preloading
    try:
        prices_df = load_prices_dataset()
        cost_df = load_cost_dataset()
        app.state.datasets_ready = True
        app.state.diagnostics["datasets"] = {
            "prices_count": len(prices_df),
            "cost_records_count": len(cost_df),
        }
        logger.info(
            f"Reference datasets loaded: {len(prices_df)} prices, {len(cost_df)} cultivation records."
        )
    except Exception as exc:
        app.state.datasets_ready = False
        app.state.diagnostics["datasets"] = f"Failed to load: {exc}"
        logger.error(f"Error loading datasets during startup: {exc}", exc_info=True)

    # 5. Shared Async HTTP Client
    app.state.http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(api_settings.request_timeout_seconds),
        limits=httpx.Limits(max_keepalive_connections=20, max_connections=50),
    )

    # Set overall readiness
    app.state.is_ready = app.state.models_ready and app.state.datasets_ready
    logger.info(f"API initialization complete. Readiness status: {app.state.is_ready}")

    try:
        yield
    finally:
        logger.info("Initiating graceful shutdown...")
        app.state.is_ready = False

        # Close shared HTTP client
        if hasattr(app.state, "http_client") and app.state.http_client:
            await app.state.http_client.aclose()
            logger.info("Shared HTTP client closed.")

        logger.info("Smart Crop Advisory API shutdown complete.")
