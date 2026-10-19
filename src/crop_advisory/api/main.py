"""
FastAPI Application Factory and ASGI Entry Point.
Assembles lifespan resource management, middleware, routers, error handlers, and OpenAPI docs.
"""

from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from crop_advisory.api.config import APISettings, api_settings
from crop_advisory.api.errors import register_error_handlers
from crop_advisory.api.lifespan import lifespan
from crop_advisory.api.middleware import CorrelationIdMiddleware
from crop_advisory.api.v1.router import api_v1_router

# OpenAPI Documentation Tags Metadata
OPENAPI_TAGS = [
    {
        "name": "Health & Diagnostics",
        "description": "Liveness and readiness probes for infrastructure monitoring and container orchestration.",
    },
    {
        "name": "Crop Recommendation",
        "description": "Multi-class ensemble classification of soil chemistry (NPK, pH) and microclimate indicators.",
    },
    {
        "name": "Yield Prediction",
        "description": "Continuous gradient boosted regression forecasting agricultural yields across states and soil types.",
    },
    {
        "name": "Market Pricing",
        "description": "Wholesale APMC Mandi commodity rates, modal prices, and minimum support prices (MSP).",
    },
    {
        "name": "Cultivation Costs",
        "description": "Official CACP comprehensive C2 cost benchmarks and operational input breakdowns.",
    },
    {
        "name": "Financial Analysis",
        "description": "Deterministic farm economic modeling, revenue projections, net profit, ROI %, and break-even thresholds.",
    },
    {
        "name": "Integrated Advisory",
        "description": "Full-lifecycle agronomic intelligence synthesizing ML predictions with market economics.",
    },
]


def create_app(settings: Optional[APISettings] = None) -> FastAPI:
    """
    Application factory for the Smart Crop Advisory REST service.
    Configures lifespan, middleware stack, exception handlers, and versioned routes.
    """
    cfg = settings or api_settings

    app = FastAPI(
        title=cfg.app_name,
        version=cfg.app_version,
        description=(
            "Production-ready asynchronous REST API for the Smart Crop Advisory ML System. "
            "Delivers ML-powered crop recommendation, agricultural yield forecasting, Mandi price intelligence, "
            "CACP cultivation costs, and farm profitability optimization."
        ),
        openapi_tags=OPENAPI_TAGS,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
        debug=cfg.debug,
    )

    # 1. Custom Middleware
    app.add_middleware(CorrelationIdMiddleware)

    # 2. CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cfg.allowed_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Process-Time"],
    )

    # 3. Trusted Host Middleware (if hosts are explicitly constrained)
    if cfg.allowed_hosts and cfg.allowed_hosts != ["*"]:
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=cfg.allowed_hosts)

    # 4. Global Exception Handlers
    register_error_handlers(app)

    # 5. Versioned API Routers
    app.include_router(api_v1_router, prefix=cfg.api_v1_prefix)

    # 6. Service Root Information Endpoint
    @app.get(
        "/",
        tags=["Health & Diagnostics"],
        summary="Service Metadata and Root Discovery",
        description="Provides general service metadata and documentation links.",
    )
    async def root_info() -> JSONResponse:
        return JSONResponse(
            content={
                "name": cfg.app_name,
                "version": cfg.app_version,
                "environment": cfg.app_env,
                "status": "operational",
                "docs_url": "/docs",
                "redoc_url": "/redoc",
                "api_v1_prefix": cfg.api_v1_prefix,
                "endpoints": {
                    "health_live": f"{cfg.api_v1_prefix}/health/live",
                    "health_ready": f"{cfg.api_v1_prefix}/health/ready",
                    "crop_recommendation": f"{cfg.api_v1_prefix}/crops/recommend",
                    "yield_prediction": f"{cfg.api_v1_prefix}/yield/predict",
                    "market_prices": f"{cfg.api_v1_prefix}/market/prices",
                    "cultivation_costs": f"{cfg.api_v1_prefix}/cultivation-costs/estimate",
                    "financial_analysis": f"{cfg.api_v1_prefix}/financial-analysis",
                    "full_advisory": f"{cfg.api_v1_prefix}/advisory/full",
                },
            }
        )

    return app


# Default module-level application instance for ASGI servers (e.g. uvicorn)
app = create_app()
