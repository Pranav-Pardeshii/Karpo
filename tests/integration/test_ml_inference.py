"""
Integration tests for ML model inference and validation.
"""

import pytest

from crop_advisory.exceptions import ValidationError


def test_crop_recommender_inference(crop_recommender, sample_soil_climate_params):
    out = crop_recommender.predict(**sample_soil_climate_params)
    assert "primary_crop" in out
    assert "display_name" in out
    assert out["confidence_percent"] > 0
    assert len(out["recommendations"]) == 3
    assert out["recommendations"][0]["crop"] == out["primary_crop"]


def test_crop_recommender_validation_failure(crop_recommender):
    with pytest.raises(ValidationError):
        # Negative pH is impossible
        crop_recommender.predict(
            n=90.0, p=42.0, k=43.0, temperature=21.0, humidity=82.0, ph=-1.0, rainfall=202.0
        )


def test_yield_predictor_inference(yield_predictor, sample_yield_params):
    out = yield_predictor.predict(**sample_yield_params)
    assert out["predicted_yield_kg_ha"] > 100.0
    assert out["predicted_yield_quintals_ha"] == round(out["predicted_yield_kg_ha"] / 100.0, 2)
    assert out["predicted_yield_kg_acre"] > 0
    assert out["predicted_yield_quintals_acre"] == round(out["predicted_yield_kg_acre"] / 100.0, 2)
    assert "historical_median_kg_ha" in out


def test_yield_predictor_horticultural_fallback(yield_predictor):
    # Banana is a horticultural crop without records in crop_yield_dataset.csv
    out = yield_predictor.predict(
        crop="banana",
        season="Whole Year",
        soil_type="Inceptisols",
        state="Tamil Nadu",
        temperature=28.0,
        rainfall=1200.0,
        humidity=80.0,
        ph=6.5,
        nitrogen=100.0,
        phosphorus=50.0,
        potassium=60.0,
        fertilizer=150.0,
        pesticide=0.4,
    )
    assert out["predicted_yield_kg_ha"] > 5000.0
    assert "Horticultural" in out["prediction_method"]
