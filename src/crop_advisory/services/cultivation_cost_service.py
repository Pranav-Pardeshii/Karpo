"""
Cost of Cultivation Lookup and Benchmarking Service Module.
Queries CACP Comprehensive C2 and operational cultivation costs from datasets/cost-of-cultivation.csv.
Supports state-level breakdown and national agricultural benchmarks.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from crop_advisory.config import (
    COST_DATASET_NAME,
    HA_TO_ACRES,
    get_dataset_path,
)
from crop_advisory.domain.crop_mapping import (
    get_crop_metadata,
    map_to_cost_crop,
    normalize_crop_name,
)
from crop_advisory.exceptions import DatasetNotFoundError


class CultivationCostService:
    """Service for querying CACP cultivation cost benchmarks and state records."""

    def __init__(self, dataset_path: Optional[Union[str, Path]] = None):
        self.dataset_path = (
            Path(dataset_path) if dataset_path else get_dataset_path(COST_DATASET_NAME)
        )
        self._df: Optional[pd.DataFrame] = None

    def load_dataset(self) -> pd.DataFrame:
        """Loads and caches the cost of cultivation dataset."""
        if self._df is None:
            if not self.dataset_path.exists():
                raise DatasetNotFoundError(
                    f"Cost of cultivation dataset file not found: '{self.dataset_path}'"
                )

            df = pd.read_csv(self.dataset_path)
            df.columns = [c.strip().lower() for c in df.columns]

            num_cols = [
                "cul_cost_c2",
                "prod_cost_c2",
                "opr_cost_seed",
                "opr_cost_fertilizer",
                "opr_cost_hmn_lab_casual",
                "opr_cost_mch_lab_hired",
                "opr_cost",
                "derived_yield",
            ]
            for col in num_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(float)
            self._df = df
        return self._df

    def get_available_states(self) -> List[str]:
        """Returns a sorted list of unique states in the cost dataset."""
        df = self.load_dataset()
        if "state_name" in df.columns:
            return sorted(
                [str(s).strip() for s in df["state_name"].dropna().unique() if str(s).strip()]
            )
        return []

    def get_cultivation_cost(
        self, crop_name: str, state_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Looks up C2 Cost of Cultivation (Rs/Hectare and Rs/Acre) for a crop and optional state.
        """
        df = self.load_dataset()
        canon_key = normalize_crop_name(crop_name)
        target_cost_crop = map_to_cost_crop(canon_key)
        meta = get_crop_metadata(canon_key)

        matched_records = pd.DataFrame()
        applied_state = "National Benchmark"

        # Check in CACP field crops dataset
        if target_cost_crop:
            crop_mask = df["crop_name"].str.contains(target_cost_crop, case=False, na=False)
            matched_records = df[crop_mask]

        if not matched_records.empty:
            if state_name:
                clean_state = state_name.strip().lower()
                state_match = matched_records[
                    matched_records["state_name"].str.strip().str.lower() == clean_state
                ]
                if not state_match.empty:
                    matched_records = state_match
                    applied_state = state_match.iloc[0]["state_name"]

            # Aggregate values
            c2_cost_ha = float(matched_records["cul_cost_c2"].median())
            prod_cost_q = float(matched_records["prod_cost_c2"].median())
            seed_cost = float(matched_records.get("opr_cost_seed", pd.Series([0])).median())
            fert_cost = float(matched_records.get("opr_cost_fertilizer", pd.Series([0])).median())
            lab_cost = float(
                matched_records.get("opr_cost_hmn_lab_casual", pd.Series([0])).median()
            )
            mech_cost = float(
                matched_records.get("opr_cost_mch_lab_hired", pd.Series([0])).median()
            )
            crop_label = target_cost_crop
            source_note = "CACP Comprehensive Survey (cost-of-cultivation.csv)"
        else:
            # Horticultural fallback
            c2_cost_ha = float(meta.get("horticultural_cost_rs_ha", 55000.0))
            prod_cost_q = round(c2_cost_ha / 50.0, 2)
            seed_cost = round(c2_cost_ha * 0.15, 2)
            fert_cost = round(c2_cost_ha * 0.25, 2)
            lab_cost = round(c2_cost_ha * 0.35, 2)
            mech_cost = round(c2_cost_ha * 0.15, 2)
            crop_label = meta.get("display_name", crop_name.title())
            source_note = "NHB / Horticultural Economic Guidelines"

        c2_cost_acre = round(c2_cost_ha / HA_TO_ACRES, 2)

        return {
            "canonical_name": canon_key,
            "matched_cost_crop": crop_label,
            "applied_state": applied_state,
            "cul_cost_c2_per_ha": round(c2_cost_ha, 2),
            "cul_cost_c2_per_acre": c2_cost_acre,
            "prod_cost_c2_per_quintal": round(prod_cost_q, 2),
            "seed_cost_per_ha": round(seed_cost, 2),
            "fertilizer_cost_per_ha": round(fert_cost, 2),
            "labor_cost_per_ha": round(lab_cost, 2),
            "machinery_cost_per_ha": round(mech_cost, 2),
            "source": source_note,
        }


# Global default service instance for backwards compatibility
_default_cost_service = CultivationCostService()


def load_cost_dataset() -> pd.DataFrame:
    """Loads and caches the cost dataset using default service."""
    return _default_cost_service.load_dataset()


def get_available_states() -> List[str]:
    """Returns sorted unique states using default service."""
    return _default_cost_service.get_available_states()


def get_cultivation_cost(crop_name: str, state_name: Optional[str] = None) -> Dict[str, Any]:
    """Looks up C2 cost using default service."""
    return _default_cost_service.get_cultivation_cost(crop_name=crop_name, state_name=state_name)
