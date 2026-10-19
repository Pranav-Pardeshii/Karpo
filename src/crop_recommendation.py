"""
Backward-compatibility shim for crop_recommendation module.
Re-exports recommender and training logic from crop_advisory.ml.crop_recommender.
"""

from crop_advisory.config import (
    CROP_REC_MODEL_FILENAME,
    CROP_REC_PREPROCESSOR_FILENAME,
    MODELS_DIR,
)
from crop_advisory.ml.crop_recommender import (
    CropRecommender,
    train_and_evaluate_crop_models,
)

MODEL_DIR = str(MODELS_DIR)
MODEL_PATH = str(MODELS_DIR / CROP_REC_MODEL_FILENAME)
PREPROCESSOR_PATH = str(MODELS_DIR / CROP_REC_PREPROCESSOR_FILENAME)

__all__ = [
    "CropRecommender",
    "train_and_evaluate_crop_models",
    "MODEL_DIR",
    "MODEL_PATH",
    "PREPROCESSOR_PATH",
]
