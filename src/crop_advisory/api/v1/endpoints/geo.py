"""
Geo-Sensing Endpoints for Karpo API v1.
Provides real-time meteorological observations, reverse geocoding,
and digital soil properties with strict provenance and data categorization.
"""

from fastapi import APIRouter, Depends, Query, Request, status

from crop_advisory.api.dependencies import get_geo_sensing_service
from crop_advisory.api.v1.schemas import GeoSensingResponse
from crop_advisory.services.geo_sensing_service import GeoSensingService

router = APIRouter(prefix="/geo", tags=["Geo-Sensing"])


@router.get(
    "/climate-soil",
    response_model=GeoSensingResponse,
    status_code=status.HTTP_200_OK,
    summary="Fetch live agro-climatic conditions and soil properties",
    description=(
        "Retrieves real meteorological observations from Open-Meteo, "
        "reverse geocoding hierarchy, and digital soil pH estimates from ISRIC SoilGrids. "
        "Returns explicit provenance and data categorization for each field."
    ),
)
def get_climate_and_soil(
    latitude: float = Query(
        ...,
        ge=-90.0,
        le=90.0,
        description="Geographic latitude in decimal degrees",
        examples=[18.5204],
    ),
    longitude: float = Query(
        ...,
        ge=-180.0,
        le=180.0,
        description="Geographic longitude in decimal degrees",
        examples=[73.8567],
    ),
    service: GeoSensingService = Depends(get_geo_sensing_service),
) -> GeoSensingResponse:
    """Fetches real weather and soil conditions for specified coordinates."""
    result = service.get_geo_sensing_advisory(latitude, longitude)
    return GeoSensingResponse(**result.to_dict())


@router.get(
    "/auto-detect",
    response_model=GeoSensingResponse,
    status_code=status.HTTP_200_OK,
    summary="Auto-detect field climate and soil via IP geolocation",
    description="Resolves approximate farm coordinates from network/IP location and queries live meteorological and soil services.",
)
def auto_detect_climate_and_soil(
    request: Request,
    service: GeoSensingService = Depends(get_geo_sensing_service),
) -> GeoSensingResponse:
    """Automatically detects coordinates from network IP and fetches real weather and soil data."""
    client_ip = request.client.host if request.client else None
    geo_info = service.detect_coordinates_from_ip(client_ip)
    if not geo_info:
        # Default to Maharashtra central agricultural coordinate baseline
        lat, lon = 18.5204, 73.8567
    else:
        lat = geo_info["latitude"]
        lon = geo_info["longitude"]

    result = service.get_geo_sensing_advisory(lat, lon)
    return GeoSensingResponse(**result.to_dict())

