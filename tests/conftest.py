"""
Pytest configuration and shared fixtures for Smart Crop Advisory System.
"""

import sys
from pathlib import Path

import pytest

# Ensure project root and src are on sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))
sys.path.insert(0, str(BASE_DIR))

from crop_advisory.ml.crop_recommender import CropRecommender
from crop_advisory.ml.yield_predictor import YieldPredictor
from crop_advisory.services.cultivation_cost_service import CultivationCostService
from crop_advisory.services.financial_analysis_service import FinancialAnalysisService
from crop_advisory.services.market_service import MarketPriceService


@pytest.fixture(scope="session")
def sample_soil_climate_params():
    """Standard soil nutrient and climatic test inputs."""
    return {
        "n": 90.0,
        "p": 42.0,
        "k": 43.0,
        "temperature": 21.0,
        "humidity": 82.0,
        "ph": 6.5,
        "rainfall": 202.0,
    }


@pytest.fixture(scope="session")
def sample_yield_params():
    """Standard yield forecasting test inputs."""
    return {
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
        "pesticide": 0.35,
    }


@pytest.fixture(scope="session")
def crop_recommender():
    """Session-scoped CropRecommender instance."""
    return CropRecommender()


@pytest.fixture(scope="session")
def yield_predictor():
    """Session-scoped YieldPredictor instance."""
    return YieldPredictor()


@pytest.fixture(scope="session")
def price_service():
    """Session-scoped MarketPriceService instance."""
    return MarketPriceService()


@pytest.fixture(scope="session")
def cost_service():
    """Session-scoped CultivationCostService instance."""
    return CultivationCostService()


@pytest.fixture(scope="session")
def financial_service(crop_recommender, yield_predictor, price_service, cost_service):
    """Session-scoped FinancialAnalysisService instance."""
    return FinancialAnalysisService(
        recommender=crop_recommender,
        yield_predictor=yield_predictor,
        price_service=price_service,
        cost_service=cost_service,
    )
