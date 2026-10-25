import React, { useState } from "react";
import { MapPin, CloudSun, Loader2, CheckCircle2, AlertCircle } from "lucide-react";
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

export const GeoSensingBanner: React.FC<GeoSensingBannerProps> = ({ onAutoFill }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<GeoSensingResponse | null>(null);

  const handleDetect = () => {
    if (!navigator.geolocation) {
      setError("Location services are not supported by your browser. Please enter values manually.");
      return;
    }

    setLoading(true);
    setError(null);

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        try {
          const lat = pos.coords.latitude;
          const lon = pos.coords.longitude;
          const res = await api.getGeoSensing(lat, lon);
          setData(res);

          // Prepare clean autofill payload
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
            // If two-week rainfall is available, extrapolate roughly or use direct value
            fillPayload.rainfall = Math.round(res.weather.two_week_rainfall_mm);
          }
          if (res.soil.ph !== null && res.soil.ph !== undefined) {
            fillPayload.ph = res.soil.ph;
          }
          if (res.location.canonical_state) {
            fillPayload.state = res.location.canonical_state;
          }

          onAutoFill(fillPayload);
        } catch (err: unknown) {
          const msg = err instanceof Error ? err.message : "Unable to reach weather services.";
          setError(msg);
        } finally {
          setLoading(false);
        }
      },
      (geoErr) => {
        setLoading(false);
        if (geoErr.code === geoErr.PERMISSION_DENIED) {
          setError("Location permission was not granted. Please input your field data manually.");
        } else {
          setError("Location request timed out. You can still enter your values manually below.");
        }
      },
      { timeout: 10000, enableHighAccuracy: true }
    );
  };

  return (
    <div className="mb-6 rounded-xl border border-emerald-500/20 bg-emerald-950/20 p-4 transition-all">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-start gap-3">
          <div className="rounded-lg bg-emerald-500/10 p-2 text-emerald-400 mt-0.5">
            <CloudSun className="w-5 h-5" />
          </div>
          <div>
            <h4 className="text-sm font-semibold text-emerald-300">
              Auto-Detect Field Climate & Soil
            </h4>
            <p className="text-xs text-zinc-400 mt-0.5">
              Pull live temperature, humidity, and rainfall from Open-Meteo satellite observations.
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={handleDetect}
          disabled={loading}
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 px-3.5 py-2 text-xs font-medium text-white transition-colors disabled:opacity-50 shadow-sm shrink-0"
        >
          {loading ? (
            <>
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
              <span>Detecting Field...</span>
            </>
          ) : (
            <>
              <MapPin className="w-3.5 h-3.5" />
              <span>Use My Location</span>
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="mt-3 flex items-center gap-2 text-xs text-amber-400/90 bg-amber-950/30 border border-amber-500/20 rounded-lg p-2.5">
          <AlertCircle className="w-4 h-4 shrink-0 text-amber-400" />
          <span>{error}</span>
        </div>
      )}

      {data && !error && (
        <div className="mt-3.5 pt-3 border-t border-emerald-500/20 text-xs flex flex-wrap items-center gap-x-4 gap-y-2 text-zinc-300">
          <span className="inline-flex items-center gap-1.5 text-emerald-400 font-medium">
            <CheckCircle2 className="w-3.5 h-3.5" />
            {data.location.locality || data.location.district || "Field location detected"}
            {data.location.canonical_state ? `, ${data.location.canonical_state}` : ""}
          </span>
          {data.weather.temperature_c !== null && data.weather.temperature_c !== undefined && (
            <span className="text-zinc-400">
              Temp: <strong className="text-zinc-200">{data.weather.temperature_c}°C</strong>
            </span>
          )}
          {data.weather.humidity_pct !== null && data.weather.humidity_pct !== undefined && (
            <span className="text-zinc-400">
              Humidity: <strong className="text-zinc-200">{data.weather.humidity_pct}%</strong>
            </span>
          )}
          {data.soil.ph !== null && data.soil.ph !== undefined ? (
            <span className="text-zinc-400">
              Est. pH: <strong className="text-zinc-200">{data.soil.ph}</strong>
            </span>
          ) : (
            <span className="text-amber-300/80 italic">
              Soil pH: laboratory test recommended
            </span>
          )}
          <span className="ml-auto text-[10px] text-zinc-500">
            Source: Open-Meteo & ISRIC SoilGrids
          </span>
        </div>
      )}
    </div>
  );
};
