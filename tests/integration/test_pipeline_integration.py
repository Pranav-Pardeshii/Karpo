"""
Integration and backward-compatibility tests for legacy src.* interfaces.
Ensures existing notebooks, scripts, and external tools retain 100% compatibility.
"""


def test_legacy_imports_and_interfaces():
    """Verify that importing from legacy src.* paths works identically."""
    from src.cost_lookup import get_cultivation_cost
    from src.crop_mapping import (
        get_all_supported_crops,
        normalize_crop_name,
    )
    from src.crop_recommendation import CropRecommender
    from src.price_lookup import get_crop_price
    from src.profit_calculation import (
        calculate_farm_financials,
    )
    from src.yield_prediction import YieldPredictor

    # 1. Normalization
    assert normalize_crop_name("Paddy") == "rice"
    assert len(get_all_supported_crops()) == 22

    # 2. Recommender
    recommender = CropRecommender()
    rec = recommender.predict(n=90, p=42, k=43, temperature=21, humidity=82, ph=6.5, rainfall=202)
    top_crop = rec["primary_crop"]
    assert top_crop is not None

    # 3. Yield
    predictor = YieldPredictor()
    yd = predictor.predict(crop=top_crop, season="Kharif", state="Maharashtra")
    assert yd["predicted_yield_kg_ha"] > 0

    # 4. Pricing & Cost
    price = get_crop_price(top_crop)
    cost = get_cultivation_cost(top_crop, state_name="Maharashtra")
    assert price["modal_rs_per_quintal"] > 0
    assert cost["cul_cost_c2_per_ha"] > 0

    # 5. Financials
    fin = calculate_farm_financials(
        yield_kg_per_ha=yd["predicted_yield_kg_ha"],
        farm_area=2.5,
        area_unit="acre",
        price_per_quintal=price["modal_rs_per_quintal"],
        cost_per_ha=cost["cul_cost_c2_per_ha"],
    )
    assert fin["total_revenue"] > 0
    assert fin["formatted_profit"] is not None
