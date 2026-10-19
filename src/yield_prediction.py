"""
Backward-compatibility shim for yield_prediction module.
Re-exports yield predictor and benchmarks from crop_advisory.ml.yield_predictor.
"""

from crop_advisory.config import (
    MODELS_DIR,
    YIELD_MODEL_FILENAME,
    YIELD_PREPROCESSOR_FILENAME,
)
from crop_advisory.ml.yield_predictor import (
    HISTORICAL_YIELD_BENCHMARKS,
    YieldPredictor,
    train_and_evaluate_yield_models,
)

MODEL_DIR = str(MODELS_DIR)
MODEL_PATH = str(MODELS_DIR / YIELD_MODEL_FILENAME)
PREPROCESSOR_PATH = str(MODELS_DIR / YIELD_PREPROCESSOR_FILENAME)

__all__ = [
    "HISTORICAL_YIELD_BENCHMARKS",
    "YieldPredictor",
    "train_and_evaluate_yield_models",
    "MODEL_DIR",
    "MODEL_PATH",
    "PREPROCESSOR_PATH",
]
