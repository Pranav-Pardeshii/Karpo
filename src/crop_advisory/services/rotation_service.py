"""
Crop Rotation and Intercropping Optimizer Service.
Generates multi-season agronomic rotation plans (Kharif -> Rabi -> Zaid) and
validated intercropping combinations based on ICAR agronomic principles:
- Cereal to legume alternation for biological nitrogen fixation
- Deep-rooted to shallow-rooted alternation for nutrient horizon balance
- Pest and weed lifecycle disruption
- Literature-backed Land Equivalent Ratios (LER) with explicit data caveats.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from crop_advisory.domain.crop_mapping import (
    CROP_METADATA,
    get_crop_metadata,
    normalize_crop_name,
)

logger = logging.getLogger(__name__)

# Validated intercropping systems from ICAR All India Coordinated Research Projects (AICRP)
ICAR_INTERCROPPING_SYSTEMS: Dict[str, List[Dict[str, Any]]] = {
    "cotton": [
        {
            "intercrop_crop": "pigeonpeas",
            "display_name": "Pigeonpea (Tur / Arhar)",
            "row_ratio": "6:1 or 8:2",
            "agronomic_benefit": "Deep-root canopy complementation. Pigeonpea fixes atmospheric nitrogen and acts as an economic buffer if cotton bollworm strikes.",
            "water_competition": "Moderate; both crops are drought-hardy, but peak moisture demands differ by 40-50 days.",
            "literature_ler_range": "1.18 - 1.32",
            "source": "ICAR - Central Institute for Cotton Research (CICR) Bulletin No. 42",
        },
        {
            "intercrop_crop": "blackgram",
            "display_name": "Blackgram (Urad)",
            "row_ratio": "1:1 or 1:2",
            "agronomic_benefit": "Early maturing short-duration legume (65-70 days) provides quick green ground cover, suppressing weeds before cotton canopy closes.",
            "water_competition": "Low; harvested well before peak cotton reproductive stage.",
            "literature_ler_range": "1.12 - 1.25",
            "source": "ICAR - AICRP on Dryland Agriculture (AICRPDA)",
        },
    ],
    "soybean": [
        {
            "intercrop_crop": "pigeonpeas",
            "display_name": "Pigeonpea (Tur / Arhar)",
            "row_ratio": "4:2 or 2:1",
            "agronomic_benefit": "Standard recommendation for Vertisols in Central India. Soybean is harvested in 90-100 days; pigeonpea continues into Rabi utilizing subsoil moisture.",
            "water_competition": "Low in early season; distinct maturity durations eliminate moisture competition.",
            "literature_ler_range": "1.25 - 1.40",
            "source": "ICAR - Indian Institute of Soybean Research (IISR) Technical Bulletin 28",
        },
        {
            "intercrop_crop": "maize",
            "display_name": "Maize",
            "row_ratio": "2:2 or 4:2",
            "agronomic_benefit": "Cereal-legume synergy. Tall maize canopy optimizes solar radiation capture while soybean provides soil nitrogen fixation.",
            "water_competition": "Moderate; requires adequate monsoon rainfall (>750 mm).",
            "literature_ler_range": "1.15 - 1.28",
            "source": "ICAR - Directorate of Maize Research",
        },
    ],
    "maize": [
        {
            "intercrop_crop": "mungbean",
            "display_name": "Green Gram (Moong)",
            "row_ratio": "1:2 or 2:2",
            "agronomic_benefit": "Short-stature legume provides living mulch, reducing soil erosion during heavy downpours and replenishing root-zone nitrogen.",
            "water_competition": "Low; fast maturity (60 days) ensures no competition during maize tasseling.",
            "literature_ler_range": "1.20 - 1.35",
            "source": "ICAR - Indian Institute of Maize Research (IIMR)",
        },
        {
            "intercrop_crop": "pigeonpeas",
            "display_name": "Pigeonpea (Arhar)",
            "row_ratio": "2:1 or 1:1",
            "agronomic_benefit": "Complementary root depth and maturity timings; enhances overall biomass productivity per unit land.",
            "water_competition": "Moderate; well suited for rainfed loamy soils.",
            "literature_ler_range": "1.18 - 1.30",
            "source": "ICAR - IIMR Agronomy Compendium",
        },
    ],
    "rice": [
        {
            "intercrop_crop": "mungbean",
            "display_name": "Relay Green Gram (Utera / Paira cropping)",
            "row_ratio": "Broadcast into standing crop 10-15 days before harvest",
            "agronomic_benefit": "Utilizes residual paddy soil moisture to establish a nitrogen-fixing pulse without tillage costs.",
            "water_competition": "Zero; seeded at physiological maturity of paddy.",
            "literature_ler_range": "1.20 - 1.30",
            "source": "ICAR - National Rice Research Institute (NRRI) Cuttack",
        },
    ],
    "groundnut": [
        {
            "intercrop_crop": "pigeonpeas",
            "display_name": "Pigeonpea (Red Gram)",
            "row_ratio": "7:1 or 5:1",
            "agronomic_benefit": "Groundnut forms a dense low ground cover while pigeonpea provides scattered shade and deep nutrient recycling.",
            "water_competition": "Low to moderate; excellent risk mitigation in semi-arid zones.",
            "literature_ler_range": "1.15 - 1.28",
            "source": "ICAR - Directorate of Groundnut Research (DGR) Junagadh",
        },
    ],
}


class CropRotationService:
    """Multi-season rotation and intercropping planning service based on ICAR agronomic rules."""

    def get_intercropping_options(self, crop: str) -> List[Dict[str, Any]]:
        """Returns verified ICAR intercropping systems for the given crop."""
        canon = normalize_crop_name(crop)
        return ICAR_INTERCROPPING_SYSTEMS.get(canon, [])

    def plan_multi_year_rotation(
        self,
        current_crop: str,
        soil_type: str = "Vertisols",
        irrigation_available: bool = True,
        state: str = "Maharashtra",
        years: int = 2,
    ) -> Dict[str, Any]:
        """
        Synthesizes an evidence-based multi-year cropping rotation sequence.
        Rotates exhaustive cereals with restorative legumes across Kharif, Rabi, and Zaid seasons.
        """
        canon_crop = normalize_crop_name(current_crop)
        meta = get_crop_metadata(canon_crop)
        category = meta.get("category", "Cereal")

        # Cap plan duration between 1 and 3 years
        plan_years = max(1, min(3, years))

        yearly_plans = []

        for yr in range(1, plan_years + 1):
            if yr == 1:
                # Year 1 starts with farmer's current or selected crop
                kharif_crop = canon_crop
                kharif_rationale = (
                    f"Baseline primary crop ({meta.get('display_name', kharif_crop.capitalize())}) "
                    f"adapted to {soil_type} in {state}."
                )

                # Rabi selection: alternate cereal/exhaustive crop <-> restorative legume
                is_exhaustive = any(k in category for k in ["Cereal", "Fiber", "Cash"]) or canon_crop in ["cotton", "rice", "maize"]
                if is_exhaustive:
                    # After cereal/cotton, plant a nitrogen-fixing restorative legume
                    rabi_crop = "chickpea"
                    rabi_rationale = (
                        "Restorative Legume Rotation: Chickpea replenishes soil nitrogen fixed from the atmosphere, "
                        "reversing nutrient depletion from the previous Kharif crop."
                    )
                else:
                    # After pulse/oilseed, plant a high-value cereal
                    rabi_crop = "wheat" if irrigation_available else "chickpea"
                    rabi_rationale = (
                        "Cereal Rotation: Taking advantage of legume-enriched residual nitrogen to achieve optimal grain yields."
                        if irrigation_available
                        else "Dryland Legume: Soil moisture conservation rotation suitable for rainfed fields."
                    )

                # Zaid (Summer) selection
                if irrigation_available:
                    zaid_crop = "mungbean"
                    zaid_rationale = (
                        "Catch Crop: 60-day short-duration green gram adds green manure biomass and "
                        "prevents summer soil erosion before the next monsoon."
                    )
                else:
                    zaid_crop = "Summer Fallow / Deep Tillage"
                    zaid_rationale = (
                        "Summer Conservation Fallow: Solarization and deep summer plowing to eliminate pest pupae and weed seeds."
                    )

            elif yr == 2:
                # Year 2: Switch crop family completely to prevent soil pathogen accumulation
                if canon_crop in ["rice", "maize"]:
                    kharif_crop = "soybean"
                    kharif_rationale = (
                        "Family Shift: Rotating from grass cereals to oilseed legume breaks monoculture pest cycles "
                        "and enhances topsoil microbial biodiversity."
                    )
                    rabi_crop = "wheat" if irrigation_available else "chickpea"
                    rabi_rationale = "High-efficiency post-soybean cereal crop utilizing loosened soil structure."
                elif canon_crop in ["cotton"]:
                    kharif_crop = "soybean"
                    kharif_rationale = (
                        "Nutrient Balancing: Sowing soybean after cotton prevents deep subsoil exhaustion and "
                        "fixes nitrogen in the upper 30 cm soil layer."
                    )
                    rabi_crop = "chickpea"
                    rabi_rationale = "Double-pulse restorative cycle to completely rebuild organic matter."
                else:
                    kharif_crop = "maize"
                    kharif_rationale = (
                        "Biomass Maximization: Sowing maize to incorporate organic carbon and deep root channels."
                    )
                    rabi_crop = "chickpea"
                    rabi_rationale = "Nitrogen replenishment pulse."

                if irrigation_available:
                    zaid_crop = "mungbean"
                    zaid_rationale = "Nitrogen fixation and short-duration cash generation."
                else:
                    zaid_crop = "Summer Fallow / Deep Tillage"
                    zaid_rationale = "Soil solarization and weed root desiccation."

            else:  # Year 3
                kharif_crop = "cotton" if soil_type == "Vertisols" else "maize"
                kharif_rationale = "Deep taproot rotation to extract nutrients from lower horizons."
                rabi_crop = "chickpea"
                rabi_rationale = "Leguminous restoration."
                zaid_crop = "mungbean" if irrigation_available else "Summer Fallow"
                zaid_rationale = "Summer soil health management."

            yearly_plans.append({
                "year_number": yr,
                "kharif": {
                    "crop": kharif_crop,
                    "display_name": get_crop_metadata(kharif_crop).get("display_name", kharif_crop.capitalize()),
                    "season": "Kharif (Monsoon)",
                    "agronomic_role": kharif_rationale,
                },
                "rabi": {
                    "crop": rabi_crop,
                    "display_name": get_crop_metadata(rabi_crop).get("display_name", rabi_crop.capitalize()) if rabi_crop != "chickpea" else "Chickpea (Gram)",
                    "season": "Rabi (Winter)",
                    "agronomic_role": rabi_rationale,
                },
                "zaid": {
                    "crop": zaid_crop,
                    "display_name": "Mungbean (Moong)" if "mungbean" in zaid_crop else zaid_crop,
                    "season": "Zaid (Summer)",
                    "agronomic_role": zaid_rationale,
                },
            })

        intercropping = self.get_intercropping_options(canon_crop)

        return {
            "current_crop": canon_crop,
            "soil_type": soil_type,
            "state": state,
            "irrigation_available": irrigation_available,
            "plan_years": plan_years,
            "yearly_plans": yearly_plans,
            "intercropping_options": intercropping,
            "agronomic_principles": [
                "Cereal -> Legume alternation for biological Rhizobium nitrogen fixation.",
                "Alternation of root architectures (deep taproots vs shallow fibrous) to balance nutrient extraction across soil horizons.",
                "Pest and soil-borne fungal lifecycle break via botanical family changes.",
            ],
            "data_category": "Estimated",
            "data_provenance": "ICAR Cropping Systems Research & Agronomic Principles",
            "caveat": (
                "Crop rotation plans provide evidence-based agronomic guidelines based on Indian agro-climatic principles. "
                "Local groundwater reserves, canal schedules, and market economics should be verified prior to sowing."
            ),
        }
