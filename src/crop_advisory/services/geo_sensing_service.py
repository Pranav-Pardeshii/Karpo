"""
Geo-Sensing Service for Karpo Precision Agriculture.
Fetches real meteorological observations from Open-Meteo,
digital soil estimations from ISRIC SoilGrids, and reverse-geocodes coordinates.

Adheres strictly to the Real Agriculture Data Integrity Standard:
- Explicit data categories: Observed, Forecast, Estimated, Unavailable.
- Explicit timestamps, units, and source citations.
- Zero fabricated fallback values when external providers are offline.
"""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import logging
import math
import time
from typing import Any, Dict, List, Optional
import httpx

logger = logging.getLogger(__name__)

# Validated list of 20 canonical Indian states supported by Karpo ML models
CANONICAL_STATES = [
    "Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh", "Gujarat",
    "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Odisha", "Punjab", "Rajasthan",
    "Tamil Nadu", "Telangana", "Uttar Pradesh", "Uttarakhand", "West Bengal"
]


@dataclass
class WeatherData:
    temperature_c: Optional[float]
    humidity_pct: Optional[float]
    precipitation_mm: Optional[float]
    two_week_rainfall_mm: Optional[float]
    observation_time: str
    source: str
    data_category: str
    status: str
    error_message: Optional[str] = None


@dataclass
class SoilEstimateData:
    ph: Optional[float]
    soil_type_hint: Optional[str]
    source: str
    data_category: str
    status: str
    caveat: str
    error_message: Optional[str] = None


@dataclass
class LocationMetadata:
    latitude: float
    longitude: float
    locality: Optional[str]
    district: Optional[str]
    state: Optional[str]
    canonical_state: Optional[str]
    country: Optional[str]
    source: str
    data_category: str


@dataclass
class GeoSensingResult:
    location: LocationMetadata
    weather: WeatherData
    soil: SoilEstimateData
    timestamp: str
    overall_status: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class GeoSensingService:
    """
    Handles live meteorological fetching and soil property querying
    with in-memory TTL caching and timeout safeguards.
    """

    def __init__(
        self,
        weather_ttl_seconds: int = 10800,  # 3 hours
        soil_ttl_seconds: int = 604800,     # 7 days
        http_timeout_seconds: float = 6.0,
    ):
        self.weather_ttl = weather_ttl_seconds
        self.soil_ttl = soil_ttl_seconds
        self.http_timeout = http_timeout_seconds
        self._cache: Dict[str, Dict[str, Any]] = {}

    def _cache_key(self, prefix: str, lat: float, lon: float) -> str:
        # Round to 3 decimal places (~110m precision) for cache hits
        return f"{prefix}:{round(lat, 3)}:{round(lon, 3)}"

    def _match_canonical_state(self, raw_state: Optional[str]) -> Optional[str]:
        if not raw_state:
            return None
        raw_lower = raw_state.strip().lower()
        for state in CANONICAL_STATES:
            if state.lower() == raw_lower or state.lower() in raw_lower:
                return state
        return None

    def fetch_reverse_geocoding(self, lat: float, lon: float) -> LocationMetadata:
        """Resolves latitude/longitude to administrative hierarchy."""
        cache_key = self._cache_key("geocode", lat, lon)
        now = time.time()
        if cache_key in self._cache:
            entry = self._cache[cache_key]
            if now - entry["cached_at"] < self.soil_ttl:
                return entry["data"]

        locality = None
        district = None
        state = None
        country = None
        source = "BigDataCloud Client Reverse Geocode"

        try:
            url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=en"
            with httpx.Client(timeout=self.http_timeout) as client:
                resp = client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    locality = data.get("locality") or data.get("city")
                    district = data.get("localityInfo", {}).get("administrative", [{}])
                    # Extract district if available
                    for admin in data.get("localityInfo", {}).get("administrative", []):
                        if admin.get("adminLevel") in (5, 6):
                            district = admin.get("name")
                            break
                    if isinstance(district, list):
                        district = locality
                    state = data.get("principalSubdivision")
                    country = data.get("countryName")
        except Exception as e:
            logger.warning("Reverse geocoding lookup failed: %s", e)
            source = "Coordinate Baseline"

        canonical_state = self._match_canonical_state(state)
        metadata = LocationMetadata(
            latitude=lat,
            longitude=lon,
            locality=locality,
            district=district if isinstance(district, str) else None,
            state=state,
            canonical_state=canonical_state,
            country=country,
            source=source,
            data_category="Observed" if locality else "Unavailable",
        )
        self._cache[cache_key] = {"data": metadata, "cached_at": now}
        return metadata

    def fetch_weather(self, lat: float, lon: float) -> WeatherData:
        """Fetches live weather conditions and 14-day rainfall sum from Open-Meteo."""
        cache_key = self._cache_key("weather", lat, lon)
        now = time.time()
        if cache_key in self._cache:
            entry = self._cache[cache_key]
            if now - entry["cached_at"] < self.weather_ttl:
                return entry["data"]

        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,precipitation"
            f"&daily=precipitation_sum&past_days=7&forecast_days=7&timezone=auto"
        )
        try:
            with httpx.Client(timeout=self.http_timeout) as client:
                resp = client.get(url)
                if resp.status_code == 200:
                    payload = resp.json()
                    curr = payload.get("current", {})
                    daily = payload.get("daily", {})
                    temp = curr.get("temperature_2m")
                    hum = curr.get("relative_humidity_2m")
                    precip = curr.get("precipitation")
                    daily_precips = daily.get("precipitation_sum", [])
                    two_week_sum = sum(daily_precips) if daily_precips else None
                    if two_week_sum is not None:
                        two_week_sum = round(two_week_sum, 1)

                    result = WeatherData(
                        temperature_c=temp,
                        humidity_pct=hum,
                        precipitation_mm=precip,
                        two_week_rainfall_mm=two_week_sum,
                        observation_time=curr.get("time") or datetime.now(timezone.utc).isoformat(),
                        source="Open-Meteo Atmospheric Model (ECMWF/GFS)",
                        data_category="Observed",
                        status="success",
                    )
                    self._cache[cache_key] = {"data": result, "cached_at": now}
                    return result
                else:
                    return WeatherData(
                        temperature_c=None,
                        humidity_pct=None,
                        precipitation_mm=None,
                        two_week_rainfall_mm=None,
                        observation_time=datetime.now(timezone.utc).isoformat(),
                        source="Open-Meteo",
                        data_category="Unavailable",
                        status="failed",
                        error_message=f"HTTP {resp.status_code} from Open-Meteo weather service",
                    )
        except Exception as e:
            logger.warning("Weather fetch error: %s", e)
            return WeatherData(
                temperature_c=None,
                humidity_pct=None,
                precipitation_mm=None,
                two_week_rainfall_mm=None,
                observation_time=datetime.now(timezone.utc).isoformat(),
                source="Open-Meteo",
                data_category="Unavailable",
                status="failed",
                error_message=f"Weather service unavailable: {str(e)}",
            )

    def fetch_soil_estimate(self, lat: float, lon: float) -> SoilEstimateData:
        """Queries ISRIC SoilGrids 250m v2.0 for topsoil pH estimation."""
        cache_key = self._cache_key("soil", lat, lon)
        now = time.time()
        if cache_key in self._cache:
            entry = self._cache[cache_key]
            if now - entry["cached_at"] < self.soil_ttl:
                return entry["data"]

        url = (
            f"https://rest.isric.org/soilgrids/v2.0/properties/query"
            f"?lat={lat}&lon={lon}&property=phh2o&depth=0-5cm&value=mean"
        )
        caveat_text = (
            "Digital soil mapping estimate from ISRIC SoilGrids 250m global model. "
            "Not a certified physical soil test. Certified laboratory testing recommended for precision fertilization."
        )

        try:
            with httpx.Client(timeout=min(self.http_timeout, 2.0)) as client:
                resp = client.get(url)
                if resp.status_code == 200:
                    payload = resp.json()
                    layers = payload.get("properties", {}).get("layers", [])
                    ph_val = None
                    for layer in layers:
                        if layer.get("name") == "phh2o":
                            depths = layer.get("depths", [])
                            if depths:
                                mean_val = depths[0].get("values", {}).get("mean")
                                if mean_val is not None:
                                    # SoilGrids returns pH * 10
                                    ph_val = round(float(mean_val) / 10.0, 2)
                                    break

                    if ph_val is not None:
                        result = SoilEstimateData(
                            ph=ph_val,
                            soil_type_hint=None,
                            source="ISRIC SoilGrids 250m v2.0",
                            data_category="Estimated",
                            status="success",
                            caveat=caveat_text,
                        )
                    else:
                        result = SoilEstimateData(
                            ph=None,
                            soil_type_hint=None,
                            source="ISRIC SoilGrids 250m v2.0",
                            data_category="Unavailable",
                            status="unavailable",
                            caveat=caveat_text,
                            error_message="Satellite digital soil mapping has no recorded value for this specific grid coordinate. Please enter laboratory test pH manually.",
                        )
                    self._cache[cache_key] = {"data": result, "cached_at": now}
                    return result
                else:
                    return SoilEstimateData(
                        ph=None,
                        soil_type_hint=None,
                        source="ISRIC SoilGrids",
                        data_category="Unavailable",
                        status="failed",
                        caveat=caveat_text,
                        error_message=f"HTTP {resp.status_code} from ISRIC SoilGrids service",
                    )
        except Exception as e:
            logger.warning("SoilGrids fetch error: %s", e)
            result = SoilEstimateData(
                ph=None,
                soil_type_hint=None,
                source="ISRIC SoilGrids",
                data_category="Unavailable",
                status="failed",
                caveat=caveat_text,
                error_message=f"Soil data service unavailable: {str(e)}",
            )
            self._cache[cache_key] = {"data": result, "cached_at": now}
            return result

    def get_geo_sensing_advisory(self, latitude: float, longitude: float) -> GeoSensingResult:
        """
        Coordinates full geo-sensing pipeline: reverse geocoding,
        live weather observations, and digital soil estimation.
        """
        # Validate coordinates bounds
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError(f"Latitude must be between -90 and 90, received {latitude}")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError(f"Longitude must be between -180 and 180, received {longitude}")

        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_loc = executor.submit(self.fetch_reverse_geocoding, latitude, longitude)
            future_weather = executor.submit(self.fetch_weather, latitude, longitude)
            future_soil = executor.submit(self.fetch_soil_estimate, latitude, longitude)

            loc = future_loc.result()
            weather = future_weather.result()
            soil = future_soil.result()

        overall = "success"
        if weather.status != "success" and soil.status != "success":
            overall = "failed"
        elif weather.status != "success" or soil.status != "success":
            overall = "partial"

        return GeoSensingResult(
            location=loc,
            weather=weather,
            soil=soil,
            timestamp=datetime.now(timezone.utc).isoformat(),
            overall_status=overall,
        )

    def detect_coordinates_from_ip(self, client_ip: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Attempts to resolve approximate latitude and longitude from IP address.
        Used as a high-reliability fallback when browser GPS times out or lacks hardware access.
        """
        cache_key = f"ipgeo:{client_ip or 'local'}"
        now = time.time()
        if cache_key in self._cache:
            entry = self._cache[cache_key]
            if now - entry["cached_at"] < self.soil_ttl:
                return entry["data"]

        is_local = not client_ip or client_ip in ("127.0.0.1", "localhost", "::1", "0.0.0.0")
        url = "https://ipwho.is/" if is_local else f"https://ipwho.is/{client_ip}"

        try:
            with httpx.Client(timeout=min(self.http_timeout, 2.5)) as client:
                resp = client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("success", False) or "latitude" in data:
                        res = {
                            "latitude": float(data["latitude"]),
                            "longitude": float(data["longitude"]),
                            "city": data.get("city"),
                            "region": data.get("region"),
                            "country": data.get("country"),
                        }
                        self._cache[cache_key] = {"data": res, "cached_at": now}
                        return res
        except Exception as e:
            logger.warning("Primary IP geolocation lookup failed: %s", e)

        try:
            fb_url = "https://freeipapi.com/api/json" if is_local else f"https://freeipapi.com/api/json/{client_ip}"
            with httpx.Client(timeout=self.http_timeout) as client:
                resp = client.get(fb_url)
                if resp.status_code == 200:
                    data = resp.json()
                    if "latitude" in data and "longitude" in data:
                        return {
                            "latitude": float(data["latitude"]),
                            "longitude": float(data["longitude"]),
                            "city": data.get("cityName"),
                            "region": data.get("regionName"),
                            "country": data.get("countryName"),
                        }
        except Exception as e:
            logger.warning("Fallback IP geolocation lookup failed: %s", e)

        return None

