"""
Integration tests for end-to-end farm financial advisory workflow.
"""

from crop_advisory.services.financial_analysis_service import (
    CropAdvisoryReport,
    generate_crop_advisory,
)


def test_financial_analysis_service_workflow(financial_service):
    report = financial_service.generate_advisory(
        n=95.0,
        p=45.0,
        k=40.0,
        temperature=24.0,
        humidity=78.0,
        ph=6.8,
        rainfall=210.0,
        state="Uttar Pradesh",
        soil_type="Inceptisols",
        season="Kharif",
        farm_area=3.0,
        area_unit="acre",
    )

    assert isinstance(report, CropAdvisoryReport)
    assert report.recommendation["primary_crop"] is not None
    assert report.yield_prediction["predicted_yield_kg_ha"] > 0
    assert report.market_price["modal_rs_per_quintal"] > 0
    assert report.cultivation_cost["cul_cost_c2_per_ha"] > 0
    assert report.financials["total_revenue"] > 0
    assert report.financials["total_cost"] > 0
    assert report.financials["formatted_profit"] is not None
    assert report.financials["input_area"] == 3.0
    assert report.financials["input_unit"] == "acre"


def test_convenience_function_report():
    report = generate_crop_advisory(
        n=80.0,
        p=40.0,
        k=40.0,
        temperature=25.0,
        humidity=80.0,
        ph=6.5,
        rainfall=180.0,
        state="Maharashtra",
        farm_area=2.0,
        area_unit="hectare",
    )
    d = report.to_dict()
    assert isinstance(d, dict)
    assert "recommendation" in d
    assert "financials" in d
    assert d["financials"]["area_hectares"] == 2.0
