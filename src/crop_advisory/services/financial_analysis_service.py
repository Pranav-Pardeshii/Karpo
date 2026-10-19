"""
Financial Analysis and Advisory Orchestration Service.
Coordinates ML recommendations, yield forecasts, mandi pricing, and CACP cultivation costs
into unified agronomic decision reports independent of any web framework.
"""

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

from crop_advisory.domain.calculations import calculate_farm_financials
from crop_advisory.domain.crop_mapping import get_crop_metadata
from crop_advisory.ml.crop_recommender import CropRecommender
from crop_advisory.ml.yield_predictor import YieldPredictor
from crop_advisory.services.cultivation_cost_service import (
    CultivationCostService,
)
from crop_advisory.services.market_service import MarketPriceService


@dataclass
class CropAdvisoryReport:
    """Comprehensive end-to-end agronomic advisory report."""

    recommendation: Dict[str, Any]
    yield_prediction: Dict[str, Any]
    market_price: Dict[str, Any]
    cultivation_cost: Dict[str, Any]
    financials: Dict[str, Any]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class FinancialAnalysisService:
    """
    High-level orchestrator for full-pipeline agronomic and financial advisory.
    Integrates ML inference with economic models.
    """

    def __init__(
        self,
        recommender: Optional[CropRecommender] = None,
        yield_predictor: Optional[YieldPredictor] = None,
        price_service: Optional[MarketPriceService] = None,
        cost_service: Optional[CultivationCostService] = None,
    ):
        self.recommender = recommender or CropRecommender()
        self.yield_predictor = yield_predictor or YieldPredictor()
        self.price_service = price_service or MarketPriceService()
        self.cost_service = cost_service or CultivationCostService()

    def generate_advisory(
        self,
        n: float,
        p: float,
        k: float,
        temperature: float,
        humidity: float,
        ph: float,
        rainfall: float,
        state: str = "Maharashtra",
        soil_type: str = "Vertisols",
        season: str = "Kharif",
        farm_area: float = 2.5,
        area_unit: str = "acre",
        top_k: int = 3,
    ) -> CropAdvisoryReport:
        """
        Executes complete advisory pipeline:
        1. Multi-class crop recommendation
        2. Continuous yield forecasting
        3. APMC mandi price lookup
        4. CACP C2 cost of cultivation estimation
        5. Farm financial, ROI, and break-even simulation
        """
        # 1. Recommendation
        rec_result = self.recommender.predict(
            n=n,
            p=p,
            k=k,
            temperature=temperature,
            humidity=humidity,
            ph=ph,
            rainfall=rainfall,
            top_k=top_k,
        )
        recommended_crop = rec_result["primary_crop"]
        crop_meta = get_crop_metadata(recommended_crop)

        # 2. Yield Prediction
        yield_result = self.yield_predictor.predict(
            crop=recommended_crop,
            season=season,
            soil_type=soil_type,
            state=state,
            temperature=temperature,
            rainfall=rainfall,
            humidity=humidity,
            ph=ph,
            nitrogen=n,
            phosphorus=p,
            potassium=k,
            fertilizer=float(crop_meta.get("default_fertilizer", 75.0)),
            pesticide=float(crop_meta.get("default_pesticide", 0.35)),
        )
        predicted_yield_ha = yield_result["predicted_yield_kg_ha"]

        # 3. Mandi Market Price
        price_data = self.price_service.get_crop_price(recommended_crop)
        modal_price = price_data["modal_rs_per_quintal"]

        # 4. Cultivation Cost
        cost_data = self.cost_service.get_cultivation_cost(recommended_crop, state_name=state)
        c2_cost_ha = cost_data["cul_cost_c2_per_ha"]

        # 5. Farm Financials
        financials = calculate_farm_financials(
            yield_kg_per_ha=predicted_yield_ha,
            farm_area=farm_area,
            area_unit=area_unit,
            price_per_quintal=modal_price,
            cost_per_ha=c2_cost_ha,
        )

        return CropAdvisoryReport(
            recommendation=rec_result,
            yield_prediction=yield_result,
            market_price=price_data,
            cultivation_cost=cost_data,
            financials=financials,
            metadata=crop_meta,
        )


# Global default service instance
_default_financial_service: Optional[FinancialAnalysisService] = None


def get_financial_service() -> FinancialAnalysisService:
    """Lazy loader for default financial analysis service singleton."""
    global _default_financial_service
    if _default_financial_service is None:
        _default_financial_service = FinancialAnalysisService()
    return _default_financial_service


def generate_crop_advisory(**kwargs) -> CropAdvisoryReport:
    """Convenience functional wrapper for advisory report generation."""
    return get_financial_service().generate_advisory(**kwargs)
