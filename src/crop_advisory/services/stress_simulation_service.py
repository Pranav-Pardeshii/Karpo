"""
Climate & Market Stress Scenario Simulation Service for Karpo.
Enables farmers and agronomists to model the financial resilience of their crop plan:
- Rainfall shocks (drought / deficit vs excess rainfall) evaluated via real ML YieldPredictor.
- Mandi commodity market price crashes / surges.
- Input cost fluctuations (fertilizer, diesel, labor).
- Pradhan Mantri Fasal Bima Yojana (PMFBY) insurance payout simulation based on Area-Yield Index scheme rules.

Strictly adheres to the Real Agriculture Data Integrity Standard:
- All scenario outputs are explicitly classified as 'Simulated'.
- Uses actual trained ML models for yield sensitivity rather than fabricated formulas.
- Clearly states PMFBY assumptions and caveats without claiming guaranteed payouts.
"""

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

from crop_advisory.domain.calculations import (
    calculate_farm_financials,
    convert_area_to_ha,
    format_inr,
    format_inr_short,
)
from crop_advisory.exceptions import ValidationError
from crop_advisory.ml.yield_predictor import YieldPredictor


@dataclass
class PMFBYSimulationResult:
    indemnity_level: float
    threshold_yield_kg_ha: float
    actual_simulated_yield_kg_ha: float
    is_claim_triggered: bool
    shortfall_ratio: float
    sum_insured_inr: float
    farmer_premium_rate_percent: float
    farmer_premium_inr: float
    estimated_claim_inr: float
    net_position_with_insurance_inr: float
    formatted_claim_inr: str
    formatted_premium_inr: str
    formatted_net_position_inr: str
    guideline_reference: str
    caveat: str


@dataclass
class ScenarioComparisonResult:
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

    pmfby_insurance: PMFBYSimulationResult
    data_category: str = "Simulated"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class StressSimulationService:
    """Evaluates agricultural financial and yield resilience under climate and market shocks."""

    def __init__(self, yield_predictor: Optional[YieldPredictor] = None):
        self.yield_predictor = yield_predictor or YieldPredictor()

    def simulate_stress(
        self,
        crop: str,
        season: str = "Kharif",
        soil_type: str = "Vertisols",
        state: str = "Maharashtra",
        farm_area: float = 2.5,
        area_unit: str = "acre",
        base_rainfall_mm: float = 800.0,
        base_temperature_c: float = 26.0,
        base_humidity_pct: float = 65.0,
        base_ph: float = 6.8,
        base_nitrogen: float = 60.0,
        base_phosphorus: float = 35.0,
        base_potassium: float = 40.0,
        base_fertilizer: float = 75.0,
        base_pesticide: float = 0.35,
        base_price_per_quintal: float = 3000.0,
        base_cost_per_ha: float = 35000.0,
        rainfall_shock_percent: float = 0.0,
        price_shock_percent: float = 0.0,
        cost_shock_percent: float = 0.0,
        pmfby_indemnity_level: float = 0.80,
    ) -> ScenarioComparisonResult:
        """
        Executes a dual-scenario evaluation comparing baseline against user-selected climate & market shocks.
        """
        # Validate shock bounds
        if not (-60.0 <= rainfall_shock_percent <= 60.0):
            raise ValidationError(
                f"Rainfall shock {rainfall_shock_percent}% outside defensible bounds [-60, +60]."
            )
        if not (-60.0 <= price_shock_percent <= 60.0):
            raise ValidationError(
                f"Price shock {price_shock_percent}% outside defensible bounds [-60, +60]."
            )
        if not (-30.0 <= cost_shock_percent <= 60.0):
            raise ValidationError(
                f"Cost shock {cost_shock_percent}% outside defensible bounds [-30, +60]."
            )
        if pmfby_indemnity_level not in (0.70, 0.80, 0.90):
            raise ValidationError(
                f"PMFBY indemnity level must be 0.70, 0.80, or 0.90, received {pmfby_indemnity_level}."
            )
        if farm_area <= 0.0:
            raise ValidationError("Farm area must be greater than zero.")

        # 1. Base yield via trained ML YieldPredictor
        base_yield_res = self.yield_predictor.predict(
            crop=crop,
            season=season,
            soil_type=soil_type,
            state=state,
            temperature=base_temperature_c,
            rainfall=base_rainfall_mm,
            humidity=base_humidity_pct,
            ph=base_ph,
            nitrogen=base_nitrogen,
            phosphorus=base_phosphorus,
            potassium=base_potassium,
            fertilizer=base_fertilizer,
            pesticide=base_pesticide,
        )
        base_yield_kg_ha = base_yield_res["predicted_yield_kg_ha"]

        # 2. Base financials
        base_fin = calculate_farm_financials(
            yield_kg_per_ha=base_yield_kg_ha,
            farm_area=farm_area,
            area_unit=area_unit,
            price_per_quintal=base_price_per_quintal,
            cost_per_ha=base_cost_per_ha,
        )

        # 3. Apply shocks
        sim_rainfall_mm = max(0.0, round(base_rainfall_mm * (1.0 + rainfall_shock_percent / 100.0), 1))
        sim_price_per_quintal = max(0.0, round(base_price_per_quintal * (1.0 + price_shock_percent / 100.0), 2))
        sim_cost_per_ha = max(0.0, round(base_cost_per_ha * (1.0 + cost_shock_percent / 100.0), 2))

        # 4. Stressed yield via trained ML YieldPredictor
        sim_yield_res = self.yield_predictor.predict(
            crop=crop,
            season=season,
            soil_type=soil_type,
            state=state,
            temperature=base_temperature_c,
            rainfall=sim_rainfall_mm,
            humidity=base_humidity_pct,
            ph=base_ph,
            nitrogen=base_nitrogen,
            phosphorus=base_phosphorus,
            potassium=base_potassium,
            fertilizer=base_fertilizer,
            pesticide=base_pesticide,
        )
        sim_yield_kg_ha = sim_yield_res["predicted_yield_kg_ha"]

        # 5. Stressed financials
        sim_fin = calculate_farm_financials(
            yield_kg_per_ha=sim_yield_kg_ha,
            farm_area=farm_area,
            area_unit=area_unit,
            price_per_quintal=sim_price_per_quintal,
            cost_per_ha=sim_cost_per_ha,
        )

        # 6. Differentials
        yield_delta = round(sim_yield_kg_ha - base_yield_kg_ha, 2)
        yield_delta_pct = (
            round((yield_delta / base_yield_kg_ha) * 100.0, 2) if base_yield_kg_ha > 0 else 0.0
        )
        revenue_delta = round(sim_fin["total_revenue"] - base_fin["total_revenue"], 2)
        profit_delta = round(sim_fin["net_profit"] - base_fin["net_profit"], 2)
        profit_delta_pct = (
            round((profit_delta / abs(base_fin["net_profit"])) * 100.0, 2)
            if base_fin["net_profit"] != 0
            else 0.0
        )

        # 7. PMFBY Insurance Model
        # Reference Benchmark: Historical median yield for this crop
        ref_yield_kg_ha = base_yield_res.get("historical_median_kg_ha") or base_yield_kg_ha
        threshold_yield = round(ref_yield_kg_ha * pmfby_indemnity_level, 2)
        area_ha = convert_area_to_ha(farm_area, area_unit)

        # Sum Insured pegged to baseline CACP cost of cultivation (Scale of Finance)
        sum_insured_inr = round(area_ha * base_cost_per_ha, 2)

        # Farmer premium rate (PMFBY guidelines: 2% Kharif foodgrains/oilseeds, 1.5% Rabi)
        is_kharif = "kharif" in season.lower()
        premium_rate = 2.0 if is_kharif else 1.5
        farmer_premium = round(sum_insured_inr * (premium_rate / 100.0), 2)

        is_claim_triggered = sim_yield_kg_ha < threshold_yield
        if is_claim_triggered and threshold_yield > 0:
            shortfall_ratio = round((threshold_yield - sim_yield_kg_ha) / threshold_yield, 4)
            estimated_claim = round(shortfall_ratio * sum_insured_inr, 2)
        else:
            shortfall_ratio = 0.0
            estimated_claim = 0.0

        net_with_ins = round(sim_fin["net_profit"] + estimated_claim - farmer_premium, 2)

        pmfby_res = PMFBYSimulationResult(
            indemnity_level=pmfby_indemnity_level,
            threshold_yield_kg_ha=threshold_yield,
            actual_simulated_yield_kg_ha=sim_yield_kg_ha,
            is_claim_triggered=is_claim_triggered,
            shortfall_ratio=shortfall_ratio,
            sum_insured_inr=sum_insured_inr,
            farmer_premium_rate_percent=premium_rate,
            farmer_premium_inr=farmer_premium,
            estimated_claim_inr=estimated_claim,
            net_position_with_insurance_inr=net_with_ins,
            formatted_claim_inr=format_inr(estimated_claim),
            formatted_premium_inr=format_inr(farmer_premium),
            formatted_net_position_inr=format_inr(net_with_ins),
            guideline_reference="PMFBY Operational Guidelines (DAC&FW, Ministry of Agriculture & Farmers Welfare)",
            caveat=(
                "Simulated estimate based on Area-Yield Index methodology. Actual indemnities are settled based on "
                "notified Insurance Unit (Gram Panchayat/Block) Crop Cutting Experiments (CCEs)."
            ),
        )

        return ScenarioComparisonResult(
            base_rainfall_mm=base_rainfall_mm,
            simulated_rainfall_mm=sim_rainfall_mm,
            rainfall_shock_percent=rainfall_shock_percent,
            base_price_per_quintal=base_price_per_quintal,
            simulated_price_per_quintal=sim_price_per_quintal,
            price_shock_percent=price_shock_percent,
            base_yield_kg_ha=base_yield_kg_ha,
            simulated_yield_kg_ha=sim_yield_kg_ha,
            yield_delta_kg_ha=yield_delta,
            yield_delta_percent=yield_delta_pct,
            base_total_revenue=base_fin["total_revenue"],
            simulated_total_revenue=sim_fin["total_revenue"],
            revenue_delta=revenue_delta,
            base_total_cost=base_fin["total_cost"],
            simulated_total_cost=sim_fin["total_cost"],
            base_net_profit=base_fin["net_profit"],
            simulated_net_profit=sim_fin["net_profit"],
            profit_delta=profit_delta,
            profit_delta_percent=profit_delta_pct,
            base_roi_percent=base_fin["roi_percent"],
            simulated_roi_percent=sim_fin["roi_percent"],
            pmfby_insurance=pmfby_res,
            data_category="Simulated",
        )
