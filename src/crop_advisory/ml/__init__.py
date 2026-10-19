"""
Machine Learning Subpackage for Smart Crop Advisory System.
Contains feature validators, artifact loaders, preprocessing pipelines,
crop recommendation classifier, and yield prediction regressor.
"""

from crop_advisory.ml.crop_recommender import CropRecommender
from crop_advisory.ml.feature_validation import (
    validate_soil_climate_input,
    validate_yield_input,
)
from crop_advisory.ml.model_loader import ModelLoader
from crop_advisory.ml.yield_predictor import (
    HISTORICAL_YIELD_BENCHMARKS,
    YieldPredictor,
)

__all__ = [
    "CropRecommender",
    "YieldPredictor",
    "ModelLoader",
    "validate_soil_climate_input",
    "validate_yield_input",
    "HISTORICAL_YIELD_BENCHMARKS",
]
