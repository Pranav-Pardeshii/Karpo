"""
Model and Preprocessor Artifact Loader Module.
Provides thread-safe caching and descriptive error handling when loading
serialized scikit-learn and XGBoost pipelines from disk.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

import joblib

from crop_advisory.config import (
    CROP_REC_MODEL_FILENAME,
    CROP_REC_PREPROCESSOR_FILENAME,
    METRICS_FILENAME,
    YIELD_MODEL_FILENAME,
    YIELD_PREPROCESSOR_FILENAME,
    get_artifact_path,
)
from crop_advisory.exceptions import ModelNotFoundError


class ModelLoader:
    """Thread-safe caching loader for machine learning artifacts."""

    def __init__(self, artifacts_dir: Optional[Path] = None):
        self.artifacts_dir = artifacts_dir
        self._cache: Dict[str, Any] = {}

    def _resolve_path(self, filename: str) -> Path:
        if self.artifacts_dir:
            path = self.artifacts_dir / filename
            if path.exists():
                return path.resolve()
        return get_artifact_path(filename)

    def load_crop_recommendation_model(self) -> Any:
        """Loads fitted crop recommendation classifier (Random Forest / XGBoost)."""
        key = "crop_rec_model"
        if key not in self._cache:
            path = self._resolve_path(CROP_REC_MODEL_FILENAME)
            if not path.exists():
                raise ModelNotFoundError(
                    f"Crop recommendation model artifact not found at '{path}'. "
                    "Ensure models are trained by running 'python scripts/train_models.py'."
                )
            self._cache[key] = joblib.load(path)
        return self._cache[key]

    def load_crop_recommendation_preprocessor(self) -> Dict[str, Any]:
        """Loads preprocessing dictionary containing StandardScaler, LabelEncoder, and classes."""
        key = "crop_rec_preprocessor"
        if key not in self._cache:
            path = self._resolve_path(CROP_REC_PREPROCESSOR_FILENAME)
            if not path.exists():
                raise ModelNotFoundError(
                    f"Crop recommendation preprocessor artifact not found at '{path}'. "
                    "Ensure models are trained by running 'python scripts/train_models.py'."
                )
            self._cache[key] = joblib.load(path)
        return self._cache[key]

    def load_yield_prediction_model(self) -> Any:
        """Loads fitted crop yield regressor."""
        key = "yield_pred_model"
        if key not in self._cache:
            path = self._resolve_path(YIELD_MODEL_FILENAME)
            if not path.exists():
                raise ModelNotFoundError(
                    f"Yield prediction model artifact not found at '{path}'. "
                    "Ensure models are trained by running 'python scripts/train_models.py'."
                )
            self._cache[key] = joblib.load(path)
        return self._cache[key]

    def load_yield_prediction_preprocessor(self) -> Dict[str, Any]:
        """Loads yield preprocessor bundle containing ColumnTransformer and metadata."""
        key = "yield_pred_preprocessor"
        if key not in self._cache:
            path = self._resolve_path(YIELD_PREPROCESSOR_FILENAME)
            if not path.exists():
                raise ModelNotFoundError(
                    f"Yield prediction preprocessor artifact not found at '{path}'. "
                    "Ensure models are trained by running 'python scripts/train_models.py'."
                )
            self._cache[key] = joblib.load(path)
        return self._cache[key]

    def load_training_metrics(self) -> Optional[Dict[str, Any]]:
        """Loads JSON summary metrics from disk, returning None if file is absent."""
        key = "training_metrics"
        if key not in self._cache:
            path = self._resolve_path(METRICS_FILENAME)
            if not path.exists():
                return None
            with open(path, "r", encoding="utf-8") as f:
                self._cache[key] = json.load(f)
        return self._cache[key]

    def clear_cache(self) -> None:
        """Clears memory cache to force re-reading from disk."""
        self._cache.clear()


# Default singleton instance
default_model_loader = ModelLoader()
