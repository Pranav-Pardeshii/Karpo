"""
Unit tests for CropRotationService.
Verifies multi-season sequence generation, cereal/legume alternation, and ICAR intercropping data.
"""

import pytest
from crop_advisory.services.rotation_service import CropRotationService


@pytest.fixture
def rotation_service():
    return CropRotationService()


def test_cotton_intercropping_options(rotation_service):
    options = rotation_service.get_intercropping_options("cotton")
    assert len(options) >= 2
    crops = [opt["intercrop_crop"] for opt in options]
    assert "pigeonpeas" in crops
    assert "blackgram" in crops
    assert "1.18 - 1.32" in options[0]["literature_ler_range"]
    assert "CICR" in options[0]["source"]


def test_soybean_intercropping_options(rotation_service):
    options = rotation_service.get_intercropping_options("soybean")
    assert len(options) >= 2
    crops = [opt["intercrop_crop"] for opt in options]
    assert "pigeonpeas" in crops
    assert "IISR" in options[0]["source"]


def test_unsupported_crop_intercropping_returns_empty(rotation_service):
    options = rotation_service.get_intercropping_options("unknown_crop_xyz")
    assert options == []


def test_two_year_rotation_cotton(rotation_service):
    plan = rotation_service.plan_multi_year_rotation(
        current_crop="cotton",
        soil_type="Vertisols",
        irrigation_available=True,
        state="Maharashtra",
        years=2,
    )
    assert plan["current_crop"] == "cotton"
    assert plan["plan_years"] == 2
    assert len(plan["yearly_plans"]) == 2
    assert plan["data_category"] == "Estimated"
    assert "ICAR" in plan["data_provenance"]

    # Year 1: Cotton (Kharif) -> Chickpea (Rabi) -> Mungbean (Zaid)
    y1 = plan["yearly_plans"][0]
    assert y1["year_number"] == 1
    assert y1["kharif"]["crop"] == "cotton"
    assert y1["rabi"]["crop"] == "chickpea"
    assert "mungbean" in y1["zaid"]["crop"]

    # Year 2: Alternation to Soybean
    y2 = plan["yearly_plans"][1]
    assert y2["year_number"] == 2
    assert y2["kharif"]["crop"] == "soybean"


def test_rainfed_rotation_zaid_fallow(rotation_service):
    plan = rotation_service.plan_multi_year_rotation(
        current_crop="maize",
        soil_type="Vertisols",
        irrigation_available=False,
        state="Maharashtra",
        years=1,
    )
    y1 = plan["yearly_plans"][0]
    # Without irrigation, zaid should recommend summer fallow/tillage
    assert "Fallow" in y1["zaid"]["crop"] or "Tillage" in y1["zaid"]["crop"]
