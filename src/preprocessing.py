"""
Backward-compatibility shim for preprocessing module.
Re-exports preprocessing from crop_advisory.ml.preprocessing.
"""

from crop_advisory.config import (
    CROP_REC_FEATURES,
    CROP_REC_TARGET,
    YIELD_CATEGORICAL_FEATURES,
    YIELD_NUMERICAL_FEATURES,
    YIELD_TARGET,
    get_dataset_path,
)
from crop_advisory.ml.preprocessing import (
    build_yield_preprocessor,
    extract_state_from_region,
    get_crop_rec_splits,
    get_yield_splits,
    load_and_clean_crop_rec_data,
    load_and_clean_yield_data,
)

__all__ = [
    "CROP_REC_FEATURES",
    "CROP_REC_TARGET",
    "YIELD_NUMERICAL_FEATURES",
    "YIELD_CATEGORICAL_FEATURES",
    "YIELD_TARGET",
    "get_dataset_path",
    "load_and_clean_crop_rec_data",
    "get_crop_rec_splits",
    "extract_state_from_region",
    "load_and_clean_yield_data",
    "build_yield_preprocessor",
    "get_yield_splits",
]
