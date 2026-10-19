"""
Configuration and Path Resolution Module for Smart Crop Advisory System.
Provides deterministic, environment-aware filesystem paths, agronomic constants,
and unit conversion ratios.
"""

import os
from pathlib import Path
from typing import List

# Root directory of the repository (3 levels up from this file: src/crop_advisory/config.py -> repo root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Dataset directory configuration
_ENV_DATASETS_DIR = os.getenv("CROP_ADVISORY_DATASETS_DIR")
DATASETS_DIR = Path(_ENV_DATASETS_DIR).resolve() if _ENV_DATASETS_DIR else (BASE_DIR / "datasets")

# Artifacts & Models directories
_ENV_ARTIFACTS_DIR = os.getenv("CROP_ADVISORY_ARTIFACTS_DIR")
ARTIFACTS_DIR = (
    Path(_ENV_ARTIFACTS_DIR).resolve() if _ENV_ARTIFACTS_DIR else (BASE_DIR / "artifacts")
)
MODELS_DIR = BASE_DIR / "models"

# Standard dataset filenames
CROP_REC_DATASET_NAME = "Crop_recommendation.csv"
YIELD_DATASET_NAME = "crop_yield_dataset.csv"
PRICE_DATASET_NAME = "india-crop-prices.csv"
COST_DATASET_NAME = "cost-of-cultivation.csv"

# Standard model filenames
CROP_REC_MODEL_FILENAME = "crop_recommendation_model.pkl"
CROP_REC_PREPROCESSOR_FILENAME = "crop_recommendation_preprocessor.pkl"
YIELD_MODEL_FILENAME = "yield_prediction_model.pkl"
YIELD_PREPROCESSOR_FILENAME = "yield_prediction_preprocessor.pkl"
METRICS_FILENAME = "training_metrics.json"

# Plot filenames
CROP_REC_CONFUSION_MATRIX_FILENAME = "crop_rec_confusion_matrix.png"
CROP_REC_FEATURE_IMPORTANCE_FILENAME = "crop_rec_feature_importance.png"
YIELD_ACTUAL_VS_PRED_FILENAME = "yield_actual_vs_predicted.png"
YIELD_FEATURE_IMPORTANCE_FILENAME = "yield_feature_importance.png"

# Unit Conversion Constants
HA_TO_ACRES: float = 2.47105
ACRES_TO_HA: float = 0.404686
KG_PER_QUINTAL: float = 100.0

# Feature Schemas for Machine Learning
CROP_REC_FEATURES: List[str] = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
CROP_REC_TARGET: str = "label"

YIELD_NUMERICAL_FEATURES: List[str] = [
    "Temperature",
    "Rainfall",
    "Humidity",
    "pH",
    "Nitrogen",
    "Phosphorus",
    "Potassium",
    "Fertilizer",
    "Pesticide",
]
YIELD_CATEGORICAL_FEATURES: List[str] = ["Crop", "Season", "Soil Type", "State"]
YIELD_TARGET: str = "Yield"

# Agronomic Physical Bounds for Feature Validation
FEATURE_BOUNDS = {
    "N": {"min": 0.0, "max": 300.0, "unit": "kg/ha"},
    "P": {"min": 0.0, "max": 300.0, "unit": "kg/ha"},
    "K": {"min": 0.0, "max": 300.0, "unit": "kg/ha"},
    "temperature": {"min": -10.0, "max": 60.0, "unit": "°C"},
    "humidity": {"min": 0.0, "max": 100.0, "unit": "%"},
    "ph": {"min": 1.0, "max": 14.0, "unit": "pH"},
    "rainfall": {"min": 0.0, "max": 3000.0, "unit": "mm"},
    "fertilizer": {"min": 0.0, "max": 500.0, "unit": "kg/ha"},
    "pesticide": {"min": 0.0, "max": 10.0, "unit": "kg/ha"},
}


def get_dataset_path(filename: str) -> Path:
    """
    Deterministically resolves dataset file location.
    Checks DATASETS_DIR, BASE_DIR/datasets, and current working directory.
    """
    candidates = [
        DATASETS_DIR / filename,
        BASE_DIR / "datasets" / filename,
        Path("datasets") / filename,
        Path(filename),
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate.resolve()

    # Return expected location if not found (caller handles FileNotFoundError)
    return (DATASETS_DIR / filename).resolve()


def get_artifact_path(filename: str) -> Path:
    """
    Deterministically resolves artifact file location.
    Checks ARTIFACTS_DIR, MODELS_DIR, and fallback relative paths.
    """
    candidates = [
        ARTIFACTS_DIR / filename,
        MODELS_DIR / filename,
        BASE_DIR / "models" / filename,
        Path("models") / filename,
        Path("artifacts") / filename,
        Path(filename),
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate.resolve()

    # Default to MODELS_DIR if exists, else ARTIFACTS_DIR
    if MODELS_DIR.exists():
        return (MODELS_DIR / filename).resolve()
    return (ARTIFACTS_DIR / filename).resolve()
