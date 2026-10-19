"""
Unit tests for domain transfer schemas and input objects.
"""

import numpy as np

from crop_advisory.domain.schemas import (
    CropRecommendationItem,
    SoilClimateInput,
    YieldInput,
)


def test_soil_climate_input_to_numpy():
    payload = SoilClimateInput(
        n=90.0, p=42.0, k=43.0, temperature=21.0, humidity=82.0, ph=6.5, rainfall=202.0
    )
    arr = payload.to_numpy()
    assert isinstance(arr, np.ndarray)
    assert arr.shape == (1, 7)
    assert arr[0, 0] == 90.0
    assert arr[0, 6] == 202.0


def test_yield_input_to_model_dict():
    payload = YieldInput(crop="rice", season="Kharif", soil_type="Vertisols", state="Maharashtra")
    d = payload.to_model_input_dict(yield_crop_name="Rice")
    assert d["Crop"] == "Rice"
    assert d["Season"] == "Kharif"
    assert d["Soil Type"] == "Vertisols"
    assert d["State"] == "Maharashtra"
    assert "Nitrogen" in d
    assert "Phosphorus" in d


def test_crop_recommendation_item_serialization():
    item = CropRecommendationItem(
        crop="rice",
        display_name="Rice",
        category="Cereal",
        confidence_score=94.5,
        probability=0.945,
        description="Staple cereal",
    )
    d = item.to_dict()
    assert d["crop"] == "rice"
    assert d["confidence_score"] == 94.5
    assert isinstance(d, dict)
