"""
FastAPI Dependency Injection Providers.
Provides service singletons, AnyIO concurrency limiters, and readiness checks.
"""

import anyio
from fastapi import HTTPException, Request, status

from crop_advisory.ml.crop_recommender import CropRecommender
from crop_advisory.ml.yield_predictor import YieldPredictor
from crop_advisory.services.cultivation_cost_service import CultivationCostService
from crop_advisory.services.financial_analysis_service import (
    FinancialAnalysisService,
    get_financial_service,
)
from crop_advisory.services.geo_sensing_service import GeoSensingService
from crop_advisory.services.lens_service import KarpoLensService
from crop_advisory.services.market_service import MarketPriceService
from crop_advisory.services.rotation_service import CropRotationService
from crop_advisory.services.stress_simulation_service import StressSimulationService
from crop_advisory.services.voice_copilot_service import VoiceCopilotService

# Service singletons
_recommender_singleton: CropRecommender = None
_yield_predictor_singleton: YieldPredictor = None
_price_service_singleton: MarketPriceService = None
_cost_service_singleton: CultivationCostService = None
_geo_sensing_service_singleton: GeoSensingService = None
_stress_simulation_service_singleton: StressSimulationService = None
_voice_copilot_service_singleton: VoiceCopilotService = None
_lens_service_singleton: KarpoLensService = None
_rotation_service_singleton: CropRotationService = None


def get_crop_recommender() -> CropRecommender:
    """Dependency provider for CropRecommender instance."""
    global _recommender_singleton
    if _recommender_singleton is None:
        _recommender_singleton = CropRecommender()
    return _recommender_singleton


def get_yield_predictor() -> YieldPredictor:
    """Dependency provider for YieldPredictor instance."""
    global _yield_predictor_singleton
    if _yield_predictor_singleton is None:
        _yield_predictor_singleton = YieldPredictor()
    return _yield_predictor_singleton


def get_price_service() -> MarketPriceService:
    """Dependency provider for MarketPriceService instance."""
    global _price_service_singleton
    if _price_service_singleton is None:
        _price_service_singleton = MarketPriceService()
    return _price_service_singleton


def get_cost_service() -> CultivationCostService:
    """Dependency provider for CultivationCostService instance."""
    global _cost_service_singleton
    if _cost_service_singleton is None:
        _cost_service_singleton = CultivationCostService()
    return _cost_service_singleton


def get_financial_service_dep() -> FinancialAnalysisService:
    """Dependency provider for FinancialAnalysisService orchestrator."""
    return get_financial_service()


def get_geo_sensing_service() -> GeoSensingService:
    """Dependency provider for GeoSensingService singleton."""
    global _geo_sensing_service_singleton
    if _geo_sensing_service_singleton is None:
        _geo_sensing_service_singleton = GeoSensingService()
    return _geo_sensing_service_singleton


def get_stress_simulation_service() -> StressSimulationService:
    """Dependency provider for StressSimulationService singleton."""
    global _stress_simulation_service_singleton
    if _stress_simulation_service_singleton is None:
        _stress_simulation_service_singleton = StressSimulationService()
    return _stress_simulation_service_singleton


def get_inference_limiter(request: Request) -> anyio.CapacityLimiter:
    """Dependency provider for application AnyIO concurrency limiter."""
    limiter = getattr(request.app.state, "inference_limiter", None)
    if limiter is None:
        # Fallback if accessed outside standard lifespan
        limiter = anyio.CapacityLimiter(10)
        request.app.state.inference_limiter = limiter
    return limiter


def require_readiness(request: Request) -> None:
    """Dependency enforcing that backend models and datasets are loaded and ready."""
    is_ready = getattr(request.app.state, "is_ready", False)
    if not is_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Application models or datasets are not fully initialized.",
        )


def get_voice_copilot_service() -> VoiceCopilotService:
    """Dependency provider for Kisan Voice Copilot service."""
    global _voice_copilot_service_singleton
    if _voice_copilot_service_singleton is None:
        _voice_copilot_service_singleton = VoiceCopilotService(
            market_price_service=get_price_service(),
            cost_service=get_cost_service(),
        )
    return _voice_copilot_service_singleton


def get_lens_service() -> KarpoLensService:
    """Dependency provider for Karpo Lens crop disease inspection service."""
    global _lens_service_singleton
    if _lens_service_singleton is None:
        _lens_service_singleton = KarpoLensService()
    return _lens_service_singleton


def get_rotation_service() -> CropRotationService:
    """Dependency provider for CropRotationService singleton."""
    global _rotation_service_singleton
    if _rotation_service_singleton is None:
        _rotation_service_singleton = CropRotationService()
    return _rotation_service_singleton


