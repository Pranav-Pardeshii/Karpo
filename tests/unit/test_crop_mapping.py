"""
Unit tests for canonical crop metadata and cross-dataset normalization.
"""

from crop_advisory.domain.crop_mapping import (
    get_all_supported_crops,
    get_crop_metadata,
    map_rec_crop_to_yield_crop,
    map_to_cost_crop,
    map_to_price_crop,
    normalize_crop_name,
)


def test_crop_normalization_canonical():
    assert normalize_crop_name("Rice") == "rice"
    assert normalize_crop_name("  PADDY  ") == "rice"
    assert normalize_crop_name("chana") == "chickpea"
    assert normalize_crop_name("Gram (Chana)") == "chickpea"
    assert normalize_crop_name("Pigeon Peas") == "pigeonpeas"
    assert normalize_crop_name("tur") == "pigeonpeas"
    assert normalize_crop_name("cotton") == "cotton"
    assert normalize_crop_name("Kapas") == "cotton"
    assert normalize_crop_name("Moong") == "mungbean"
    assert normalize_crop_name("Urad") == "blackgram"
    assert normalize_crop_name("Corn") == "maize"


def test_all_supported_crops():
    crops = get_all_supported_crops()
    assert len(crops) == 22
    for c in crops:
        assert "canonical_name" in c
        assert "display_name" in c
        assert "category" in c
        assert "default_season" in c


def test_cross_dataset_mappings():
    assert map_rec_crop_to_yield_crop("rice") == "Rice"
    assert map_rec_crop_to_yield_crop("maize") == "Maize"
    assert map_rec_crop_to_yield_crop("chickpea") == "Chickpea"
    assert map_rec_crop_to_yield_crop("blackgram") == "Minor Pulses"
    assert map_rec_crop_to_yield_crop("cotton") == "Cotton"

    assert map_to_price_crop("rice") == "Rice (Paddy)"
    assert map_to_price_crop("wheat") == "Wheat"
    assert map_to_price_crop("maize") == "Maize (Corn)"
    assert map_to_price_crop("chickpea") == "Gram (Chana)"

    assert map_to_cost_crop("rice") == "Paddy"
    assert map_to_cost_crop("chickpea") == "Gram"
    assert map_to_cost_crop("cotton") == "Cotton"


def test_unknown_crop_metadata_fallback():
    meta = get_crop_metadata("unknown_exotic_crop")
    assert meta["canonical_name"] == "unknown exotic crop"
    assert meta["category"] == "Field Crop"
    assert "default_fertilizer" in meta
