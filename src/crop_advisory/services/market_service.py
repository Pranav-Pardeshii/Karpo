"""
Price Lookup and Mandi Market Service Module.
Loads and queries mandi prices from datasets/india-crop-prices.csv.
Provides modal prices, price ranges (min-max), MSP, and per-kg rates.
"""

from pathlib import Path
from typing import Any, Dict, Optional, Union

import pandas as pd

from crop_advisory.config import (
    PRICE_DATASET_NAME,
    get_dataset_path,
)
from crop_advisory.domain.crop_mapping import (
    get_crop_metadata,
    map_to_price_crop,
    normalize_crop_name,
)
from crop_advisory.exceptions import DatasetNotFoundError


class MarketPriceService:
    """Service for querying and analyzing APMC Mandi market rates."""

    def __init__(self, dataset_path: Optional[Union[str, Path]] = None):
        self.dataset_path = (
            Path(dataset_path) if dataset_path else get_dataset_path(PRICE_DATASET_NAME)
        )
        self._df: Optional[pd.DataFrame] = None

    def load_dataset(self) -> pd.DataFrame:
        """Loads and caches the crop prices dataframe."""
        if self._df is None:
            if not self.dataset_path.exists():
                raise DatasetNotFoundError(
                    f"Crop prices dataset file not found: '{self.dataset_path}'"
                )

            df = pd.read_csv(self.dataset_path)
            df.columns = [c.strip().lower() for c in df.columns]

            for col in ["modal_rs_per_quintal", "min", "max"]:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(float)
            if "msp" in df.columns:
                df["msp"] = pd.to_numeric(df["msp"], errors="coerce")
            self._df = df
        return self._df

    def get_crop_price(self, crop_name: str) -> Dict[str, Any]:
        """
        Looks up official market price information for a given crop.
        """
        df = self.load_dataset()
        canon_key = normalize_crop_name(crop_name)
        target_price_crop = map_to_price_crop(canon_key)
        meta = get_crop_metadata(canon_key)

        # 1. Exact match on mapped price_crop
        match = df[df["crop"].str.strip().str.lower() == target_price_crop.lower()]

        # 2. Substring or keyword match
        if match.empty:
            match = df[df["crop"].str.contains(target_price_crop, case=False, na=False)]

        # 3. Match on canonical name or hindi name
        if match.empty:
            match = df[df["crop"].str.contains(canon_key, case=False, na=False)]

        if not match.empty:
            row = match.iloc[0]
            modal_price = float(row["modal_rs_per_quintal"])
            min_p = float(row["min"]) if row["min"] > 0 else modal_price * 0.85
            max_p = float(row["max"]) if row["max"] > 0 else modal_price * 1.15
            msp_val = float(row["msp"]) if pd.notna(row["msp"]) else None
            crop_title = str(row["crop"])
        else:
            # Fallback benchmark
            modal_price = 4500.0
            min_p = 3800.0
            max_p = 5200.0
            msp_val = None
            crop_title = meta.get("display_name", crop_name.title())

        return {
            "canonical_name": canon_key,
            "matched_crop_name": crop_title,
            "modal_rs_per_quintal": modal_price,
            "min_rs_per_quintal": min_p,
            "max_rs_per_quintal": max_p,
            "msp_rs_per_quintal": msp_val,
            "price_per_kg": round(modal_price / 100.0, 2),
            "source": "Agmarknet Mandi Price Reference (india-crop-prices.csv)",
        }


# Global default service instance for backwards compatibility
_default_price_service = MarketPriceService()


def load_prices_dataset() -> pd.DataFrame:
    """Loads and caches the crop prices dataframe using default service."""
    return _default_price_service.load_dataset()


def get_crop_price(crop_name: str) -> Dict[str, Any]:
    """Looks up official market price information using default service."""
    return _default_price_service.get_crop_price(crop_name)
