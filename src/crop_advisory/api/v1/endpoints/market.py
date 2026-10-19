"""
Mandi Market Pricing Endpoints.
Exposes APMC Mandi commodity rates, modal prices, price intervals, and MSP data.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query

from crop_advisory.api.dependencies import get_price_service, require_readiness
from crop_advisory.api.v1.schemas import MarketPriceListResponse, PriceInfoResponse
from crop_advisory.services.market_service import MarketPriceService

router = APIRouter(prefix="/market", tags=["Market Pricing"])


@router.get(
    "/prices",
    response_model=MarketPriceListResponse,
    summary="Query Mandi Commodity Prices",
    description="Queries wholesale Mandi market rates with optional crop name filtering and pagination.",
    dependencies=[Depends(require_readiness)],
)
async def list_market_prices(
    query: Optional[str] = Query(None, description="Filter commodities by name substring"),
    limit: int = Query(50, ge=1, le=200, description="Maximum records to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    price_service: MarketPriceService = Depends(get_price_service),
) -> MarketPriceListResponse:
    """Lists Mandi commodity market prices with filtering and pagination."""
    df = price_service.load_dataset()

    if query:
        filtered_df = df[df["crop"].str.contains(query.strip(), case=False, na=False)]
    else:
        filtered_df = df

    total_records = len(filtered_df)
    paginated_df = filtered_df.iloc[offset : offset + limit]

    prices = []
    for _, row in paginated_df.iterrows():
        crop_title = str(row["crop"])
        modal_price = float(row["modal_rs_per_quintal"])
        min_p = float(row["min"]) if row["min"] > 0 else modal_price * 0.85
        max_p = float(row["max"]) if row["max"] > 0 else modal_price * 1.15
        msp_val = float(row["msp"]) if "msp" in row and row["msp"] > 0 else None

        prices.append(
            PriceInfoResponse(
                canonical_name=crop_title.lower(),
                matched_crop_name=crop_title,
                modal_rs_per_quintal=modal_price,
                min_rs_per_quintal=min_p,
                max_rs_per_quintal=max_p,
                msp_rs_per_quintal=msp_val,
                price_per_kg=round(modal_price / 100.0, 2),
                source="Agmarknet Mandi Price Reference (india-crop-prices.csv)",
            )
        )

    return MarketPriceListResponse(total_records=total_records, prices=prices)


@router.get(
    "/prices/{crop_name}",
    response_model=PriceInfoResponse,
    summary="Get Mandi Price for a Specific Crop",
    description="Retrieves modal price, price ranges, and MSP for a specific crop name or alias.",
    dependencies=[Depends(require_readiness)],
)
async def get_single_crop_price(
    crop_name: str, price_service: MarketPriceService = Depends(get_price_service)
) -> PriceInfoResponse:
    """Looks up official APMC Mandi market price for a single crop."""
    info = price_service.get_crop_price(crop_name)
    return PriceInfoResponse(**info)
