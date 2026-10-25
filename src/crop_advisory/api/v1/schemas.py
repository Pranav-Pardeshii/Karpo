"""
Pydantic v2 Request and Response Schemas for API v1.
Provides strict validation, descriptive field metadata, units, and clear response models.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

# =========================================================================
# 1. HEALTH & DIAGNOSTICS SCHEMAS
# =========================================================================


class LivenessResponse(BaseModel):
    """Liveness probe response payload."""

    status: str = Field("alive", description="Process liveness state")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="Timestamp in ISO 8601 UTC"
    )


class ReadinessResponse(BaseModel):
    """Readiness probe reporting resource initialization states."""

    status: str = Field("ready", description="Overall readiness state: ready or not_ready")
    models_loaded: bool = Field(..., description="Whether required ML models are loaded in memory")
    datasets_loaded: bool = Field(..., description="Whether reference datasets are accessible")
    details: Dict[str, Any] = Field(..., description="Component-level diagnostic statuses")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="Timestamp in ISO 8601 UTC"
    )


# =========================================================================
# 2. CROP RECOMMENDATION SCHEMAS
# =========================================================================


class CropRecommendationRequest(BaseModel):
    """Input payload for multi-class crop recommendation."""

    model_config = ConfigDict(extra="forbid")

    n: float = Field(
        ..., ge=0.0, le=300.0, description="Soil Nitrogen content ratio (kg/ha)", examples=[90.0]
    )
    p: float = Field(
        ..., ge=0.0, le=300.0, description="Soil Phosphorus content ratio (kg/ha)", examples=[42.0]
    )
    k: float = Field(
        ..., ge=0.0, le=300.0, description="Soil Potassium content ratio (kg/ha)", examples=[43.0]
    )
    temperature: float = Field(
        ...,
        ge=-10.0,
        le=60.0,
        description="Average ambient temperature in Celsius (°C)",
        examples=[24.5],
    )
    humidity: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Relative ambient humidity percentage (%)",
        examples=[75.0],
    )
    ph: float = Field(
        ..., ge=1.0, le=14.0, description="Soil pH measurement (1.0 - 14.0)", examples=[6.8]
    )
    rainfall: float = Field(
        ...,
        ge=0.0,
        le=3000.0,
        description="Annual or seasonal rainfall in millimeters (mm)",
        examples=[180.0],
    )
    top_k: int = Field(
        3,
        ge=1,
        le=22,
        description="Number of candidate crop recommendations to return",
        examples=[3],
    )


class CandidateCropResponse(BaseModel):
    """Ranked crop candidate with probabilistic confidence score."""

    crop: str = Field(..., description="Canonical crop slug (e.g. 'rice')")
    display_name: str = Field(..., description="Human-readable title (e.g. 'Rice')")
    category: str = Field(..., description="Agronomic category (e.g. 'Cereal', 'Pulse')")
    confidence_score: float = Field(..., description="Predicted percentage score [0.0 - 100.0]")
    probability: float = Field(..., description="Normalized class probability [0.0 - 1.0]")
    description: str = Field(..., description="Agronomic description and climatic requirements")


class CropRecommendationResponse(BaseModel):
    """Result of crop recommendation classification."""

    primary_crop: str = Field(..., description="Top recommended canonical crop slug")
    display_name: str = Field(..., description="Display title of top recommendation")
    confidence_percent: float = Field(..., description="Confidence percentage of primary crop")
    category: str = Field(..., description="Agronomic category")
    description: str = Field(..., description="Crop profile description")
    recommendations: List[CandidateCropResponse] = Field(
        ..., description="Ranked list of top-k crops"
    )
    soil_advisory_notes: List[str] = Field(
        ..., description="Actionable soil diagnostics and nutrient notes"
    )
    model_used: str = Field(..., description="Model identifier used for inference")


class SupportedCropResponse(BaseModel):
    """Metadata record for a supported crop."""

    canonical_name: str = Field(..., description="Canonical key")
    display_name: str = Field(..., description="Display title")
    category: str = Field(..., description="Agronomic grouping")
    yield_crop: Optional[str] = Field(None, description="Mapped name in historical yield dataset")
    price_crop: Optional[str] = Field(None, description="Mapped name in mandi pricing dataset")
    cost_crop: Optional[str] = Field(None, description="Mapped name in cultivation cost dataset")
    default_season: str = Field(..., description="Primary growing season")
    default_soil: str = Field(..., description="Preferred soil classification")
    default_fertilizer: float = Field(..., description="Standard fertilizer recommendation (kg/ha)")
    default_pesticide: float = Field(..., description="Standard pesticide recommendation (kg/ha)")
    description: str = Field(..., description="Agronomic description")


# =========================================================================
# 3. YIELD PREDICTION SCHEMAS
# =========================================================================


class YieldPredictionRequest(BaseModel):
    """Input payload for agricultural yield forecasting."""

    model_config = ConfigDict(extra="forbid")

    crop: str = Field(
        ..., description="Target crop name (e.g. 'Rice', 'Wheat', 'Maize')", examples=["Rice"]
    )
    season: str = Field(
        "Kharif",
        description="Cropping season ('Kharif', 'Rabi', 'Whole Year')",
        examples=["Kharif"],
    )
    soil_type: str = Field(
        "Vertisols",
        description="Soil classification ('Vertisols', 'Inceptisols', etc.)",
        examples=["Vertisols"],
    )
    state: str = Field("Maharashtra", description="Indian State name", examples=["Maharashtra"])
    temperature: float = Field(
        26.0, ge=-10.0, le=60.0, description="Ambient temperature (°C)", examples=[26.0]
    )
    rainfall: float = Field(800.0, ge=0.0, le=3000.0, description="Rainfall (mm)", examples=[800.0])
    humidity: float = Field(
        65.0, ge=0.0, le=100.0, description="Relative humidity (%)", examples=[65.0]
    )
    ph: float = Field(6.8, ge=1.0, le=14.0, description="Soil pH", examples=[6.8])
    nitrogen: float = Field(
        60.0, ge=0.0, le=300.0, description="Nitrogen nutrient ratio (kg/ha)", examples=[60.0]
    )
    phosphorus: float = Field(
        35.0, ge=0.0, le=300.0, description="Phosphorus nutrient ratio (kg/ha)", examples=[35.0]
    )
    potassium: float = Field(
        40.0, ge=0.0, le=300.0, description="Potassium nutrient ratio (kg/ha)", examples=[40.0]
    )
    fertilizer: float = Field(
        75.0, ge=0.0, le=1000.0, description="Fertilizer application rate (kg/ha)", examples=[75.0]
    )
    pesticide: float = Field(
        0.35, ge=0.0, le=50.0, description="Pesticide application rate (kg/ha)", examples=[0.35]
    )


class YieldPredictionResponse(BaseModel):
    """Predicted yield result with unit conversions and benchmarks."""

    crop: str = Field(..., description="Input crop queried")
    mapped_yield_crop: str = Field(..., description="Resolved dataset crop or proxy identifier")
    prediction_method: str = Field(
        ..., description="Predictor method: Trained ML Regressor or Agronomic Calibration"
    )
    predicted_yield_kg_ha: float = Field(
        ..., description="Forecasted yield in kilograms per hectare (kg/ha)"
    )
    predicted_yield_quintals_ha: float = Field(
        ..., description="Forecasted yield in Quintals per hectare (Q/ha)"
    )
    predicted_yield_kg_acre: float = Field(
        ..., description="Forecasted yield in kilograms per acre (kg/acre)"
    )
    predicted_yield_quintals_acre: float = Field(
        ..., description="Forecasted yield in Quintals per acre (Q/acre)"
    )
    historical_min_kg_ha: float = Field(
        ..., description="Historical minimum benchmark yield (kg/ha)"
    )
    historical_median_kg_ha: float = Field(
        ..., description="Historical median benchmark yield (kg/ha)"
    )
    historical_max_kg_ha: float = Field(
        ..., description="Historical maximum benchmark yield (kg/ha)"
    )


class YieldBenchmarkResponse(BaseModel):
    """Benchmark typical agricultural yields for a crop."""

    crop: str = Field(..., description="Crop title")
    min_kg_ha: float = Field(..., description="Historical lower bound (kg/ha)")
    median_kg_ha: float = Field(..., description="Historical median (kg/ha)")
    max_kg_ha: float = Field(..., description="Historical upper bound (kg/ha)")


# =========================================================================
# 4. MANDI MARKET PRICING SCHEMAS
# =========================================================================


class PriceInfoResponse(BaseModel):
    """Official APMC Mandi commodity market rate details."""

    canonical_name: str = Field(..., description="Canonical crop slug")
    matched_crop_name: str = Field(..., description="Market record commodity name")
    modal_rs_per_quintal: float = Field(..., description="Modal wholesale price per Quintal (₹/Q)")
    min_rs_per_quintal: float = Field(..., description="Minimum recorded price per Quintal (₹/Q)")
    max_rs_per_quintal: float = Field(..., description="Maximum recorded price per Quintal (₹/Q)")
    msp_rs_per_quintal: Optional[float] = Field(
        None, description="Government Minimum Support Price (₹/Q)"
    )
    price_per_kg: float = Field(..., description="Equivalent modal price per kilogram (₹/kg)")
    source: str = Field(..., description="Reference data authority")


class MarketPriceListResponse(BaseModel):
    """Paginated or filtered list of Mandi commodity rates."""

    total_records: int = Field(..., description="Number of matching commodity price records")
    prices: List[PriceInfoResponse] = Field(..., description="List of price records")


# =========================================================================
# 5. CULTIVATION COST SCHEMAS
# =========================================================================


class CultivationCostRequest(BaseModel):
    """Payload to look up CACP cultivation cost benchmarks."""

    model_config = ConfigDict(extra="forbid")

    crop_name: str = Field(
        ..., description="Crop title or key (e.g. 'Rice', 'Cotton')", examples=["Rice"]
    )
    state_name: Optional[str] = Field(
        None, description="Optional Indian State name (e.g. 'Punjab')", examples=["Punjab"]
    )


class CultivationCostResponse(BaseModel):
    """CACP Comprehensive C2 Cost of Cultivation benchmark details."""

    canonical_name: str = Field(..., description="Canonical crop slug")
    matched_cost_crop: str = Field(..., description="Matched CACP survey crop name")
    applied_state: str = Field(
        ..., description="State applied (specific state or 'National Benchmark')"
    )
    cul_cost_c2_per_ha: float = Field(
        ..., description="Comprehensive C2 cultivation cost per hectare (₹/ha)"
    )
    cul_cost_c2_per_acre: float = Field(
        ..., description="Comprehensive C2 cultivation cost per acre (₹/acre)"
    )
    prod_cost_c2_per_quintal: float = Field(
        ..., description="Estimated cost of production per Quintal (₹/Q)"
    )
    seed_cost_per_ha: float = Field(..., description="Operational seed and planting cost (₹/ha)")
    fertilizer_cost_per_ha: float = Field(
        ..., description="Operational fertilizer and nutrient cost (₹/ha)"
    )
    labor_cost_per_ha: float = Field(..., description="Human labor cost (₹/ha)")
    machinery_cost_per_ha: float = Field(..., description="Machine and fuel cost (₹/ha)")
    source: str = Field(..., description="Reference data standard")


class StatesListResponse(BaseModel):
    """List of available states in the CACP dataset."""

    states: List[str] = Field(..., description="Sorted list of Indian states with cost survey data")


# =========================================================================
# 6. FARM FINANCIAL ANALYSIS SCHEMAS
# =========================================================================


class FinancialAnalysisRequest(BaseModel):
    """Payload for farm economics, profitability, ROI, and break-even analysis."""

    model_config = ConfigDict(extra="forbid")

    yield_kg_per_ha: float = Field(
        ...,
        gt=0.0,
        description="Expected crop yield in kilograms per hectare (kg/ha)",
        examples=[2000.0],
    )
    farm_area: float = Field(
        ..., gt=0.0, description="Farm landholding operational size", examples=[2.5]
    )
    area_unit: str = Field(
        "acre",
        description="Area measurement unit: 'acre', 'hectare', or 'bigha'",
        examples=["acre"],
    )
    price_per_quintal: float = Field(
        3000.0,
        gt=0.0,
        description="Wholesale market sale price per Quintal (₹/Q)",
        examples=[3000.0],
    )
    cost_per_ha: float = Field(
        35000.0,
        gt=0.0,
        description="Comprehensive C2 cultivation cost per hectare (₹/ha)",
        examples=[35000.0],
    )


class FinancialAnalysisResponse(BaseModel):
    """Detailed farm economic profitability analysis."""

    input_area: float = Field(..., description="User input area value")
    input_unit: str = Field(..., description="User input area unit")
    area_hectares: float = Field(..., description="Standardized area in Hectares")
    area_acres: float = Field(..., description="Standardized area in Acres")

    yield_kg_per_ha: float = Field(..., description="Yield in kg/ha")
    yield_quintals_per_ha: float = Field(..., description="Yield in Quintals/ha")
    yield_kg_per_acre: float = Field(..., description="Yield in kg/acre")
    yield_quintals_per_acre: float = Field(..., description="Yield in Quintals/acre")
    total_production_kg: float = Field(..., description="Total harvest volume in kg")
    total_production_quintals: float = Field(..., description="Total harvest volume in Quintals")

    price_per_quintal: float = Field(..., description="Sale price (₹/Q)")
    price_per_kg: float = Field(..., description="Sale price (₹/kg)")
    cost_per_ha: float = Field(..., description="Cultivation cost (₹/ha)")
    cost_per_acre: float = Field(..., description="Cultivation cost (₹/acre)")

    total_revenue: float = Field(..., description="Gross market revenue (₹)")
    total_cost: float = Field(..., description="Total farm production cost (₹)")
    net_profit: float = Field(..., description="Net farm profit (₹)")
    profit_per_acre: float = Field(..., description="Net profit per acre (₹/acre)")
    profit_per_ha: float = Field(..., description="Net profit per hectare (₹/ha)")
    roi_percent: float = Field(..., description="Return on Investment percentage (%)")
    profit_margin_percent: float = Field(..., description="Profit margin percentage (%)")

    breakeven_yield_kg_per_ha: float = Field(
        ..., description="Break-even harvest yield threshold (kg/ha)"
    )
    breakeven_price_per_quintal: float = Field(
        ..., description="Break-even market price threshold (₹/Q)"
    )

    formatted_revenue: str = Field(
        ..., description="Indian Rupee formatted revenue (e.g. '₹60,000')"
    )
    formatted_cost: str = Field(..., description="Indian Rupee formatted cost (e.g. '₹35,000')")
    formatted_profit: str = Field(..., description="Indian Rupee formatted net profit")
    formatted_profit_per_acre: str = Field(
        ..., description="Indian Rupee formatted profit per acre"
    )
    formatted_profit_per_ha: str = Field(
        ..., description="Indian Rupee formatted profit per hectare"
    )
    formatted_revenue_short: str = Field(
        ..., description="Short formatted revenue (e.g. '₹60.0 K')"
    )
    formatted_cost_short: str = Field(..., description="Short formatted cost")
    formatted_profit_short: str = Field(..., description="Short formatted profit")


# =========================================================================
# 7. INTEGRATED ADVISORY SCHEMAS
# =========================================================================


class FullAdvisoryRequest(BaseModel):
    """End-to-end advisory request combining soil, climate, location, and farm area."""

    model_config = ConfigDict(extra="forbid")

    n: float = Field(..., ge=0.0, le=300.0, description="Soil Nitrogen (kg/ha)", examples=[90.0])
    p: float = Field(..., ge=0.0, le=300.0, description="Soil Phosphorus (kg/ha)", examples=[42.0])
    k: float = Field(..., ge=0.0, le=300.0, description="Soil Potassium (kg/ha)", examples=[43.0])
    temperature: float = Field(
        ..., ge=-10.0, le=60.0, description="Temperature (°C)", examples=[24.5]
    )
    humidity: float = Field(
        ..., ge=0.0, le=100.0, description="Relative Humidity (%)", examples=[75.0]
    )
    ph: float = Field(..., ge=1.0, le=14.0, description="Soil pH", examples=[6.8])
    rainfall: float = Field(..., ge=0.0, le=3000.0, description="Rainfall (mm)", examples=[180.0])

    state: str = Field("Maharashtra", description="Indian State name", examples=["Maharashtra"])
    soil_type: str = Field("Vertisols", description="Soil classification", examples=["Vertisols"])
    season: str = Field("Kharif", description="Cropping season", examples=["Kharif"])
    farm_area: float = Field(2.5, gt=0.0, description="Farm operational area", examples=[2.5])
    area_unit: str = Field(
        "acre", description="Area unit ('acre', 'hectare', 'bigha')", examples=["acre"]
    )
    top_k: int = Field(3, ge=1, le=22, description="Top crop recommendations count", examples=[3])


class FullAdvisoryResponse(BaseModel):
    """Complete integrated agricultural decision support report."""

    recommendation: CropRecommendationResponse
    yield_prediction: YieldPredictionResponse
    market_price: PriceInfoResponse
    cultivation_cost: CultivationCostResponse
    financials: FinancialAnalysisResponse
    metadata: Dict[str, Any]


# =========================================================================
# 8. ERROR RESPONSE SCHEMA
# =========================================================================


class ErrorResponse(BaseModel):
    """Standardized API error envelope."""

    error_code: str = Field(
        ..., description="Machine-readable error category", examples=["VALIDATION_ERROR"]
    )
    message: str = Field(
        ...,
        description="Human-readable safe explanation",
        examples=["Invalid input feature value."],
    )
    request_id: str = Field(
        ..., description="Unique request correlation identifier", examples=["req_a1b2c3d4"]
    )
    details: Optional[Any] = Field(
        None, description="Structured contextual diagnostics if applicable"
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="Timestamp in ISO 8601 UTC"
    )


# =========================================================================
# 9. GEO-SENSING SCHEMAS
# =========================================================================


class LocationMetadataResponse(BaseModel):
    """Geographic and administrative hierarchy."""

    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude coordinate")
    locality: Optional[str] = Field(None, description="Local village or city name")
    district: Optional[str] = Field(None, description="District administrative entity")
    state: Optional[str] = Field(None, description="State administrative division")
    canonical_state: Optional[str] = Field(None, description="Mapped canonical Karpo state")
    country: Optional[str] = Field(None, description="Country name")
    source: str = Field(..., description="Geocoding provider identity")
    data_category: str = Field(..., description="Observed or Unavailable")


class WeatherDataResponse(BaseModel):
    """Meteorological observations and forecasts."""

    temperature_c: Optional[float] = Field(None, description="Current ambient temperature (°C)")
    humidity_pct: Optional[float] = Field(None, description="Current relative humidity percentage (%)")
    precipitation_mm: Optional[float] = Field(None, description="Current precipitation rate (mm)")
    two_week_rainfall_mm: Optional[float] = Field(None, description="14-day cumulative rainfall (mm)")
    observation_time: str = Field(..., description="Observation timestamp in ISO 8601")
    source: str = Field(..., description="Meteorological provider name")
    data_category: str = Field(..., description="Observed, Forecast, or Unavailable")
    status: str = Field(..., description="success or failed")
    error_message: Optional[str] = Field(None, description="Safe error explanation if failed")


class SoilEstimateDataResponse(BaseModel):
    """Digital soil mapping estimates."""

    ph: Optional[float] = Field(None, description="Estimated topsoil pH in H2O")
    soil_type_hint: Optional[str] = Field(None, description="Indicative soil order if resolved")
    source: str = Field(..., description="Digital soil mapping provider name")
    data_category: str = Field(..., description="Estimated or Unavailable")
    status: str = Field(..., description="success, unavailable, or failed")
    caveat: str = Field(..., description="Scientific limitations and laboratory recommendation")
    error_message: Optional[str] = Field(None, description="Safe error explanation if unavailable")


class GeoSensingResponse(BaseModel):
    """Integrated geo-sensing package for automated form enrichment."""

    location: LocationMetadataResponse
    weather: WeatherDataResponse
    soil: SoilEstimateDataResponse
    timestamp: str = Field(..., description="Response generation timestamp in UTC")
    overall_status: str = Field(..., description="success, partial, or failed")


# =========================================================================
# 10. CLIMATE & MARKET STRESS SIMULATION SCHEMAS
# =========================================================================


class StressSimulationRequest(BaseModel):
    """Input payload for climate and market scenario analysis."""

    model_config = ConfigDict(extra="forbid")

    crop: str = Field(..., description="Canonical crop slug (e.g. 'rice', 'wheat')", examples=["rice"])
    season: str = Field("Kharif", description="Cropping season ('Kharif', 'Rabi', 'Whole Year')", examples=["Kharif"])
    soil_type: str = Field("Vertisols", description="Soil classification", examples=["Vertisols"])
    state: str = Field("Maharashtra", description="Indian State name", examples=["Maharashtra"])
    farm_area: float = Field(2.5, gt=0.0, description="Farm operational area", examples=[2.5])
    area_unit: str = Field("acre", description="Area unit ('acre', 'hectare', 'bigha')", examples=["acre"])

    base_rainfall_mm: float = Field(800.0, ge=0.0, le=4000.0, description="Baseline seasonal rainfall (mm)", examples=[800.0])
    base_temperature_c: float = Field(26.0, ge=-10.0, le=60.0, description="Baseline ambient temperature (°C)", examples=[26.0])
    base_humidity_pct: float = Field(65.0, ge=0.0, le=100.0, description="Baseline relative humidity (%)", examples=[65.0])
    base_ph: float = Field(6.8, ge=1.0, le=14.0, description="Baseline soil pH", examples=[6.8])
    base_nitrogen: float = Field(60.0, ge=0.0, le=300.0, description="Baseline Nitrogen ratio (kg/ha)", examples=[60.0])
    base_phosphorus: float = Field(35.0, ge=0.0, le=300.0, description="Baseline Phosphorus ratio (kg/ha)", examples=[35.0])
    base_potassium: float = Field(40.0, ge=0.0, le=300.0, description="Baseline Potassium ratio (kg/ha)", examples=[40.0])
    base_fertilizer: float = Field(75.0, ge=0.0, le=1000.0, description="Baseline fertilizer application (kg/ha)", examples=[75.0])
    base_pesticide: float = Field(0.35, ge=0.0, le=50.0, description="Baseline pesticide application (kg/ha)", examples=[0.35])

    base_price_per_quintal: float = Field(3000.0, gt=0.0, description="Baseline Mandi wholesale price (₹/quintal)", examples=[3000.0])
    base_cost_per_ha: float = Field(35000.0, gt=0.0, description="Baseline CACP cultivation cost (₹/ha)", examples=[35000.0])

    rainfall_shock_percent: float = Field(
        0.0, ge=-60.0, le=60.0, description="Simulated rainfall deficit or surplus percentage (-60% to +60%)", examples=[-30.0]
    )
    price_shock_percent: float = Field(
        0.0, ge=-60.0, le=60.0, description="Simulated market wholesale price shock percentage (-60% to +60%)", examples=[-20.0]
    )
    cost_shock_percent: float = Field(
        0.0, ge=-30.0, le=60.0, description="Simulated input cost inflation percentage (-30% to +60%)", examples=[10.0]
    )
    pmfby_indemnity_level: float = Field(
        0.80, description="PMFBY insurance indemnity level (0.70, 0.80, or 0.90)", examples=[0.80]
    )


class PMFBYSimulationResponse(BaseModel):
    """Pradhan Mantri Fasal Bima Yojana (PMFBY) insurance payout model."""

    indemnity_level: float = Field(..., description="Insurance indemnity level (0.70, 0.80, 0.90)")
    threshold_yield_kg_ha: float = Field(..., description="Government threshold yield benchmark (kg/ha)")
    actual_simulated_yield_kg_ha: float = Field(..., description="Yield predicted under climate shock (kg/ha)")
    is_claim_triggered: bool = Field(..., description="Whether simulated yield fell below threshold")
    shortfall_ratio: float = Field(..., description="Indemnity shortfall proportion [0.0 - 1.0]")
    sum_insured_inr: float = Field(..., description="Scale of Finance total sum insured (₹)")
    farmer_premium_rate_percent: float = Field(..., description="Statutory farmer premium rate (%)")
    farmer_premium_inr: float = Field(..., description="Farmer premium payable (₹)")
    estimated_claim_inr: float = Field(..., description="Projected insurance claim payout (₹)")
    net_position_with_insurance_inr: float = Field(..., description="Simulated net profit after premium & claim (₹)")
    formatted_claim_inr: str = Field(..., description="Formatted claim amount in ₹")
    formatted_premium_inr: str = Field(..., description="Formatted premium amount in ₹")
    formatted_net_position_inr: str = Field(..., description="Formatted net position in ₹")
    guideline_reference: str = Field(..., description="Official government scheme citation")
    caveat: str = Field(..., description="Limitation note on CCE area-yield determination")


class ScenarioComparisonResponse(BaseModel):
    """Comparative scenario analysis response."""

    base_rainfall_mm: float
    simulated_rainfall_mm: float
    rainfall_shock_percent: float

    base_price_per_quintal: float
    simulated_price_per_quintal: float
    price_shock_percent: float

    base_yield_kg_ha: float
    simulated_yield_kg_ha: float
    yield_delta_kg_ha: float
    yield_delta_percent: float

    base_total_revenue: float
    simulated_total_revenue: float
    revenue_delta: float

    base_total_cost: float
    simulated_total_cost: float

    base_net_profit: float
    simulated_net_profit: float
    profit_delta: float
    profit_delta_percent: float

    base_roi_percent: float
    simulated_roi_percent: float

    pmfby_insurance: PMFBYSimulationResponse
    data_category: str = Field("Simulated", description="Explicit classification per data integrity contract")
