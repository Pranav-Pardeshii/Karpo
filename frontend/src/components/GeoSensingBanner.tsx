import React, { useState, useEffect, useCallback, useRef } from "react";
import { MapPin, CloudSun, Loader2, AlertCircle, RefreshCw } from "lucide-react";
import { api } from "../api/client";
import { GeoSensingResponse } from "../types/api";

interface GeoSensingBannerProps {
  onAutoFill: (data: {
    temperature?: number;
    humidity?: number;
    rainfall?: number;
    ph?: number;
    state?: string;
  }) => void;
}

const AGRO_HUBS = [
  { label: "Maharashtra — Pune / Western", lat: 18.5204, lon: 73.8567 },
  { label: "Maharashtra — Nashik (Onion/Grapes)", lat: 19.9975, lon: 73.7898 },
  { label: "Maharashtra — Chh. Sambhajinagar (Marathwada)", lat: 19.8762, lon: 75.3433 },
  { label: "Maharashtra — Amravati / Vidarbha (Cotton)", lat: 20.9374, lon: 77.7796 },
  { label: "Maharashtra — Kolhapur (Sugarcane)", lat: 16.7050, lon: 74.2433 },
  { label: "Gujarat — Rajkot / Saurashtra (Groundnut/Cotton)", lat: 22.3039, lon: 70.8022 },
  { label: "Madhya Pradesh — Indore / Malwa (Soybean)", lat: 22.7196, lon: 75.8577 },
  { label: "Punjab — Ludhiana (Wheat/Rice)", lat: 30.9010, lon: 75.8573 },
  { label: "Haryana — Karnal (Basmati Rice)", lat: 29.6857, lon: 76.9905 },
  { label: "Karnataka — Dharwad / Belagavi", lat: 15.4589, lon: 75.0078 },
  { label: "Uttar Pradesh — Varanasi / Alluvial", lat: 25.3176, lon: 82.9739 },
  { label: "Telangana — Warangal (Cotton/Chilli)", lat: 17.9784, lon: 79.5941 },
  { label: "Andhra Pradesh — Guntur (Chilli/Tobacco)", lat: 16.3067, lon: 80.4365 },
  { label: "Rajasthan — Kota (Soybean/Mustard)", lat: 25.2138, lon: 75.8648 },
];

const CACHE_STORAGE_KEY = "karpo_geo_sensing_cache";
const CACHE_TTL_MS = 2 * 60 * 60 * 1000; // 2 hours

export const GeoSensingBanner: React.FC<GeoSensingBannerProps> = ({ onAutoFill }) => {
  const [loading, setLoading] = useState(true);
  const [detectSource, setDetectSource] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<GeoSensingResponse | null>(null);
  const [showManualOverride, setShowManualOverride] = useState(false);
  const hasTriggeredInitial = useRef(false);

  const applyAutoFill = useCallback(
    (res: GeoSensingResponse, sourceLabel: string, saveCache: boolean = true) => {
      setData(res);
      setDetectSource(sourceLabel);
      setError(null);

      if (saveCache) {
        try {
          sessionStorage.setItem(
            CACHE_STORAGE_KEY,
            JSON.stringify({ data: res, source: sourceLabel, timestamp: Date.now() })
          );
        } catch {
          // Ignore sessionStorage quota errors
        }
      }

      const fillPayload: {
        temperature?: number;
        humidity?: number;
        rainfall?: number;
        ph?: number;
        state?: string;
      } = {};

      if (res.weather.temperature_c !== null && res.weather.temperature_c !== undefined) {
        fillPayload.temperature = Math.round(res.weather.temperature_c * 10) / 10;
      }
      if (res.weather.humidity_pct !== null && res.weather.humidity_pct !== undefined) {
        fillPayload.humidity = Math.round(res.weather.humidity_pct);
      }
      if (res.weather.two_week_rainfall_mm !== null && res.weather.two_week_rainfall_mm !== undefined) {
        fillPayload.rainfall = Math.round(res.weather.two_week_rainfall_mm);
      }
      if (res.soil.ph !== null && res.soil.ph !== undefined) {
        fillPayload.ph = res.soil.ph;
      }
      if (res.location.canonical_state) {
        fillPayload.state = res.location.canonical_state;
      }

      onAutoFill(fillPayload);
    },
    [onAutoFill]
  );

  const runAutoDetection = useCallback(() => {
    setLoading(true);
    setError(null);

    const tryNetworkIpDetection = async (gpsReason?: string) => {
      try {
        const res = await api.autoDetectGeoSensing();
        applyAutoFill(res, "Network Location (IP)", true);
      } catch (ipErr: unknown) {
        const msg = ipErr instanceof Error ? ipErr.message : "Location services unreachable.";
        setError(
          gpsReason
            ? `${gpsReason} Unable to detect coordinates automatically. You can pick your district manually below.`
            : msg
        );
        setShowManualOverride(true);
      } finally {
        setLoading(false);
      }
    };

    if (!navigator.geolocation) {
      tryNetworkIpDetection("Browser GPS not supported.");
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        try {
          const lat = pos.coords.latitude;
          const lon = pos.coords.longitude;
          const res = await api.getGeoSensing(lat, lon);
          applyAutoFill(res, "Browser GPS", true);
        } catch {
          await tryNetworkIpDetection();
        } finally {
          setLoading(false);
        }
      },
      async () => {
        await tryNetworkIpDetection();
      },
      { timeout: 3500, enableHighAccuracy: false, maximumAge: 300000 }
    );
  }, [applyAutoFill]);

  useEffect(() => {
    if (hasTriggeredInitial.current) return;
    hasTriggeredInitial.current = true;

    try {
      const cachedRaw = sessionStorage.getItem(CACHE_STORAGE_KEY);
      if (cachedRaw) {
        const cached = JSON.parse(cachedRaw);
        if (cached?.data && Date.now() - (cached.timestamp || 0) < CACHE_TTL_MS) {
          setData(cached.data);
          setDetectSource(cached.source);
          applyAutoFill(cached.data, cached.source, false);
          setLoading(false);
          return;
        }
      }
    } catch {
      // Fall through to live detection
    }

    runAutoDetection();
  }, [runAutoDetection, applyAutoFill]);

  const handleHubSelect = async (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    if (!val) return;
    const [latStr, lonStr] = val.split(",");
    const lat = parseFloat(latStr);
    const lon = parseFloat(lonStr);
    if (isNaN(lat) || isNaN(lon)) return;

    setLoading(true);
    setError(null);
    try {
      const res = await api.getGeoSensing(lat, lon);
      applyAutoFill(res, "Selected Agricultural Hub", true);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Unable to reach weather services.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="border border-obsidian-800 bg-white p-4 shadow-sm space-y-3">
      {/* Header Block: Title + Status Badge */}
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2">
          <div className="p-1.5 bg-[#EAF0E6] border border-[#789477]/40 text-[#244B35] shrink-0">
            <CloudSun className="w-4 h-4" />
          </div>
          <div>
            <h4 className="font-mono text-xs font-bold text-chalk-100 uppercase tracking-technical">
              Field Climate & Soil Auto-Sensing
            </h4>
            <p className="font-sans text-[11px] text-obsidian-400 mt-0.5 leading-tight">
              Live weather & soil data synchronized with your farm.
            </p>
          </div>
        </div>

        {/* State Badge */}
        <div className="shrink-0">
          {loading ? (
            <span className="inline-flex items-center gap-1.5 px-2 py-0.5 bg-[#EAF0E6] border border-[#789477]/40 font-mono text-[10px] text-[#244B35]">
              <Loader2 className="w-3 h-3 animate-spin text-[#244B35]" />
              <span>Detecting...</span>
            </span>
          ) : data ? (
            <span className="inline-flex items-center gap-1.5 px-2 py-0.5 bg-[#EAF0E6] border border-[#357A4A]/40 font-mono text-[10px] text-[#357A4A] font-semibold">
              <span className="w-1.5 h-1.5 rounded-full bg-[#357A4A] animate-pulse" />
              <span>Auto-Detected</span>
            </span>
          ) : (
            <button
              type="button"
              onClick={runAutoDetection}
              className="inline-flex items-center gap-1 px-2.5 py-1 bg-signal-red hover:bg-signal-darkred text-white font-mono text-[10px] uppercase font-bold transition-colors shadow-sm"
            >
              <MapPin className="w-3 h-3" />
              <span>Auto-Detect</span>
            </button>
          )}
        </div>
      </div>

      {/* Telemetry Data Grid */}
      {data && (
        <div className="pt-2.5 border-t border-obsidian-800 space-y-2 font-mono text-xs">
          {/* Location Line */}
          <div className="flex items-center justify-between text-[#244B35] font-medium text-[11px]">
            <span className="flex items-center gap-1 truncate">
              <MapPin className="w-3 h-3 shrink-0" />
              <strong className="text-chalk-100">
                {data.location.locality || data.location.district || "Farm Location"}
                {data.location.canonical_state ? `, ${data.location.canonical_state}` : ""}
              </strong>
            </span>
            {detectSource && (
              <span className="text-[10px] text-obsidian-400 font-normal shrink-0">
                ({detectSource})
              </span>
            )}
          </div>

          {/* Metric Pills Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-1.5 text-[11px] text-obsidian-300">
            {data.weather.temperature_c !== null && data.weather.temperature_c !== undefined && (
              <div className="bg-obsidian-850 border border-obsidian-800 px-2 py-1 flex items-center justify-between">
                <span className="text-obsidian-400">Temp</span>
                <span className="text-chalk-100 font-bold">{data.weather.temperature_c}°C</span>
              </div>
            )}

            {data.weather.humidity_pct !== null && data.weather.humidity_pct !== undefined && (
              <div className="bg-obsidian-850 border border-obsidian-800 px-2 py-1 flex items-center justify-between">
                <span className="text-obsidian-400">Humidity</span>
                <span className="text-chalk-100 font-bold">{data.weather.humidity_pct}%</span>
              </div>
            )}

            {data.weather.two_week_rainfall_mm !== null && data.weather.two_week_rainfall_mm !== undefined && (
              <div className="bg-obsidian-850 border border-obsidian-800 px-2 py-1 flex items-center justify-between">
                <span className="text-obsidian-400">Rainfall</span>
                <span className="text-chalk-100 font-bold">{data.weather.two_week_rainfall_mm} mm</span>
              </div>
            )}

            <div className="bg-obsidian-850 border border-obsidian-800 px-2 py-1 flex items-center justify-between">
              <span className="text-obsidian-400">Soil pH</span>
              <span className="text-chalk-100 font-bold">
                {data.soil.ph !== null && data.soil.ph !== undefined ? data.soil.ph : "Test Advised"}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Action Buttons Row */}
      {data && (
        <div className="pt-2 border-t border-obsidian-800 flex items-center justify-between gap-2 font-mono text-[10px]">
          <span className="text-obsidian-500 truncate">
            Live Open-Meteo & ISRIC SoilGrids
          </span>

          <div className="flex items-center gap-1.5 shrink-0">
            <button
              type="button"
              onClick={runAutoDetection}
              title="Refresh live field detection"
              className="inline-flex items-center gap-1 px-2 py-1 bg-obsidian-850 hover:bg-[#DCE6D7] border border-obsidian-800 text-chalk-100 uppercase transition-colors cursor-pointer"
            >
              <RefreshCw className="w-2.5 h-2.5 text-obsidian-400" />
              <span>Refresh</span>
            </button>

            <button
              type="button"
              onClick={() => setShowManualOverride((prev) => !prev)}
              title="Manually override district or state"
              className="inline-flex items-center gap-1 px-2 py-1 bg-obsidian-850 hover:bg-[#DCE6D7] border border-obsidian-800 text-chalk-100 uppercase transition-colors cursor-pointer"
            >
              <span>{showManualOverride ? "Hide" : "Change Region"}</span>
            </button>
          </div>
        </div>
      )}

      {/* Manual Hub Selector (Visible only when requested via Change Region or on error) */}
      {showManualOverride && (
        <div className="pt-2 border-t border-obsidian-800 space-y-1.5 bg-obsidian-850 p-2.5 border border-obsidian-800 font-mono text-xs">
          <label className="block text-[10px] uppercase text-obsidian-400">
            Select Agricultural Hub Override:
          </label>
          <select
            onChange={handleHubSelect}
            defaultValue=""
            className="w-full bg-white border border-obsidian-800 text-xs text-chalk-100 px-2.5 py-1.5 focus:border-signal-red focus:outline-none cursor-pointer"
          >
            <option value="" disabled>
              Select Agricultural Hub...
            </option>
            {AGRO_HUBS.map((hub) => (
              <option key={hub.label} value={`${hub.lat},${hub.lon}`}>
                {hub.label}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="flex items-center gap-2 text-xs text-signal-amber bg-[#FDF8F0] border border-signal-amber/40 p-2 font-mono">
          <AlertCircle className="w-4 h-4 shrink-0 text-signal-amber" />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
};
