"""
Feature Validation Module for Machine Learning Pipelines.
Ensures input features strictly adhere to physical agronomic bounds
and exact ordering expected by fitted estimators and transformers.
"""

from typing import List

from crop_advisory.config import (
    CROP_REC_FEATURES,
    FEATURE_BOUNDS,
)
from crop_advisory.exceptions import ValidationError


def validate_soil_climate_input(
    n: float, p: float, k: float, temperature: float, humidity: float, ph: float, rainfall: float
) -> None:
    """
    Validates physical feasibility of soil chemistry and environmental parameters.
    Raises ValidationError if any parameter violates biological/agronomic limits.
    """
    params = {
        "N": n,
        "P": p,
        "K": k,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall,
    }

    for name, val in params.items():
        if val is None:
            raise ValidationError(f"Parameter '{name}' cannot be None.")
        bounds = FEATURE_BOUNDS.get(name)
        if bounds:
            if val < bounds["min"] or val > bounds["max"]:
                raise ValidationError(
                    f"Parameter '{name}' value {val} is outside valid agronomic range "
                    f"[{bounds['min']}, {bounds['max']}] {bounds['unit']}."
                )


def validate_crop_rec_feature_ordering(features: List[str]) -> None:
    """Verifies that feature ordering strictly matches training schema."""
    if features != CROP_REC_FEATURES:
        raise ValidationError(
            f"Feature ordering mismatch for Crop Recommendation. "
            f"Expected {CROP_REC_FEATURES}, got {features}."
        )


def validate_yield_input(
    crop: str,
    season: str,
    soil_type: str,
    state: str,
    temperature: float,
    rainfall: float,
    humidity: float,
    ph: float,
    nitrogen: float,
    phosphorus: float,
    potassium: float,
    fertilizer: float,
    pesticide: float,
) -> None:
    """Validates inputs for Yield Prediction regression model."""
    if not crop or not isinstance(crop, str):
        raise ValidationError("Crop name must be a non-empty string.")
    if not season or not isinstance(season, str):
        raise ValidationError("Season must be a non-empty string.")
    if not soil_type or not isinstance(soil_type, str):
        raise ValidationError("Soil Type must be a non-empty string.")
    if not state or not isinstance(state, str):
        raise ValidationError("State must be a non-empty string.")

    validate_soil_climate_input(
        n=nitrogen,
        p=phosphorus,
        k=potassium,
        temperature=temperature,
        humidity=humidity,
        ph=ph,
        rainfall=rainfall,
    )

    if fertilizer < 0.0 or fertilizer > 1000.0:
        raise ValidationError(
            f"Fertilizer value {fertilizer} kg/ha is outside reasonable agronomic range [0, 1000]."
        )
    if pesticide < 0.0 or pesticide > 50.0:
        raise ValidationError(
            f"Pesticide value {pesticide} kg/ha is outside reasonable agronomic range [0, 50]."
        )
