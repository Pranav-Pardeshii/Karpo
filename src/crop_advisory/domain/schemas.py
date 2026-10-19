"""
Data Schemas and Transfer Objects for Smart Crop Advisory System.
Uses typed dataclasses for input validation and structured prediction payloads.
"""

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

import numpy as np


@dataclass(frozen=True)
class SoilClimateInput:
    """Input payload for Crop Recommendation Model."""

    n: float
    p: float
    k: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float
    top_k: int = 3

    def to_features_list(self) -> List[float]:
        """Returns ordered feature list matching training schema."""
        return [self.n, self.p, self.k, self.temperature, self.humidity, self.ph, self.rainfall]

    def to_numpy(self) -> np.ndarray:
        """Returns 2D numpy array for scikit-learn transformers."""
        return np.array([self.to_features_list()], dtype=float)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class YieldInput:
    """Input payload for Crop Yield Prediction Model."""

    crop: str
    season: str = "Kharif"
    soil_type: str = "Vertisols"
    state: str = "Maharashtra"
    temperature: float = 26.0
    rainfall: float = 800.0
    humidity: float = 65.0
    ph: float = 6.8
    nitrogen: float = 60.0
    phosphorus: float = 35.0
    potassium: float = 40.0
    fertilizer: float = 75.0
    pesticide: float = 0.35

    def to_model_input_dict(self, yield_crop_name: str) -> Dict[str, Any]:
        """Returns dictionary formatted for DataFrame inference."""
        return {
            "Crop": yield_crop_name,
            "Season": self.season,
            "Soil Type": self.soil_type,
            "State": self.state,
            "Temperature": self.temperature,
            "Rainfall": self.rainfall,
            "Humidity": self.humidity,
            "pH": self.ph,
            "Nitrogen": self.nitrogen,
            "Phosphorus": self.phosphorus,
            "Potassium": self.potassium,
            "Fertilizer": self.fertilizer,
            "Pesticide": self.pesticide,
        }

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FarmFinancialInput:
    """Input payload for farm economics calculation."""

    yield_kg_per_ha: float
    farm_area: float
    area_unit: str = "acre"
    price_per_quintal: float = 3000.0
    cost_per_ha: float = 35000.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CropRecommendationItem:
    """Individual candidate crop in recommendation ranking."""

    crop: str
    display_name: str
    category: str
    confidence_score: float
    probability: float
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CropRecommendationResult:
    """Full recommendation payload with top picks and agronomic diagnosis."""

    primary_crop: str
    display_name: str
    confidence_percent: float
    category: str
    description: str
    recommendations: List[Dict[str, Any]]
    soil_advisory_notes: List[str]
    model_used: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class YieldPredictionResult:
    """Full yield forecast payload with multi-unit conversions and benchmarks."""

    crop: str
    mapped_yield_crop: str
    prediction_method: str
    predicted_yield_kg_ha: float
    predicted_yield_quintals_ha: float
    predicted_yield_kg_acre: float
    predicted_yield_quintals_acre: float
    historical_min_kg_ha: float
    historical_median_kg_ha: float
    historical_max_kg_ha: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PriceInfoResult:
    """Official APMC Mandi market price information."""

    canonical_name: str
    matched_crop_name: str
    modal_rs_per_quintal: float
    min_rs_per_quintal: float
    max_rs_per_quintal: float
    msp_rs_per_quintal: Optional[float]
    price_per_kg: float
    source: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CostInfoResult:
    """CACP Cost of Cultivation benchmark details."""

    canonical_name: str
    matched_cost_crop: str
    applied_state: str
    cul_cost_c2_per_ha: float
    cul_cost_c2_per_acre: float
    prod_cost_c2_per_quintal: float
    seed_cost_per_ha: float
    fertilizer_cost_per_ha: float
    labor_cost_per_ha: float
    machinery_cost_per_ha: float
    source: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FarmFinancialResult:
    """Comprehensive farm profitability, revenue, cost, and break-even result."""

    input_area: float
    input_unit: str
    area_hectares: float
    area_acres: float

    yield_kg_per_ha: float
    yield_quintals_per_ha: float
    yield_kg_per_acre: float
    yield_quintals_per_acre: float
    total_production_kg: float
    total_production_quintals: float

    price_per_quintal: float
    price_per_kg: float
    cost_per_ha: float
    cost_per_acre: float

    total_revenue: float
    total_cost: float
    net_profit: float
    profit_per_acre: float
    profit_per_ha: float
    roi_percent: float
    profit_margin_percent: float

    breakeven_yield_kg_per_ha: float
    breakeven_price_per_quintal: float

    formatted_revenue: str
    formatted_cost: str
    formatted_profit: str
    formatted_profit_per_acre: str
    formatted_profit_per_ha: str
    formatted_revenue_short: str
    formatted_cost_short: str
    formatted_profit_short: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
