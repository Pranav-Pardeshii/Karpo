import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { useMutation, useQuery } from "@tanstack/react-query";
import { ArrowRight, BarChart2, Compass, ArrowUpRight } from "lucide-react";
import { api, ApiError } from "../api/client";
import { YieldPredictionRequest, YieldPredictionResponse } from "../types/api";
import { Button } from "../components/ui/Button";
import { SignalBadge } from "../components/visual/SignalBadge";
import { MetricCard } from "../components/ui/MetricCard";
import { StatusBanner } from "../components/ui/StatusBanner";
import { GeoSensingBanner } from "../components/GeoSensingBanner";
import { FarmDigitalTwin } from "../components/FarmDigitalTwin";
import { useLanguage } from "../context/LanguageContext";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Cell,
} from "recharts";

const SEASONS = ["Kharif", "Rabi", "Whole Year", "Summer", "Autumn", "Winter"];
const SOIL_TYPES = [
  "Vertisols",
  "Inceptisols",
  "Alfisols",
  "Entisols",
  "Aridisols",
  "Mollisols",
];

interface LocationState {
  crop?: string;
  season?: string;
  state?: string;
  soil_type?: string;
  temperature?: number;
  rainfall?: number;
  humidity?: number;
  ph?: number;
  nitrogen?: number;
  phosphorus?: number;
  potassium?: number;
  fromRecommendation?: boolean;
}

export const YieldPredictionPage: React.FC = () => {
  const { t, getCropName, getCategoryName, getSeasonName, getSoilName, getStateName } = useLanguage();
  const location = useLocation();
  const locationState = location.state as LocationState | null;

  const [formData, setFormData] = useState<YieldPredictionRequest>({
    crop: "rice",
    season: "Kharif",
    soil_type: "Vertisols",
    state: "Maharashtra",
    temperature: 25.0,
    rainfall: 900.0,
    humidity: 70.0,
    ph: 6.5,
    nitrogen: 90.0,
    phosphorus: 40.0,
    potassium: 40.0,
    fertilizer: 100.0,
    pesticide: 0.35,
  });

  const { data: supportedCrops = [] } = useQuery({
    queryKey: ["supportedCrops"],
    queryFn: api.getSupportedCrops,
  });

  const { data: statesData } = useQuery({
    queryKey: ["cultivationStates"],
    queryFn: api.getCultivationStates,
  });

  const states = statesData?.states || [
    "Maharashtra",
    "Punjab",
    "Uttar Pradesh",
    "Gujarat",
    "Karnataka",
    "Tamil Nadu",
  ];

  useEffect(() => {
    if (!locationState) return;

    setFormData((prev) => {
      const next = { ...prev };
      if (locationState.crop) next.crop = locationState.crop.toLowerCase().trim();
      if (locationState.temperature != null) next.temperature = locationState.temperature;
      if (locationState.rainfall != null) next.rainfall = locationState.rainfall;
      if (locationState.humidity != null) next.humidity = locationState.humidity;
      if (locationState.ph != null) next.ph = locationState.ph;
      if (locationState.nitrogen != null) next.nitrogen = locationState.nitrogen;
      if (locationState.phosphorus != null) next.phosphorus = locationState.phosphorus;
      if (locationState.potassium != null) next.potassium = locationState.potassium;
      if (locationState.season) next.season = locationState.season;
      if (locationState.state) next.state = locationState.state;
      if (locationState.soil_type) next.soil_type = locationState.soil_type;

      const cropMeta = supportedCrops.find(
        (c) => c.canonical_name.toLowerCase() === (locationState.crop || "").toLowerCase()
      );
      if (cropMeta) {
        if (!locationState.season && cropMeta.default_season) next.season = cropMeta.default_season;
        if (!locationState.soil_type && cropMeta.default_soil) next.soil_type = cropMeta.default_soil;
        if (cropMeta.default_fertilizer) next.fertilizer = cropMeta.default_fertilizer;
        if (cropMeta.default_pesticide) next.pesticide = cropMeta.default_pesticide;
      }
      return next;
    });
  }, [locationState, supportedCrops]);

  const mutation = useMutation<
    YieldPredictionResponse,
    ApiError,
    YieldPredictionRequest
  >({
    mutationFn: api.predictYield,
  });

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "number" ? parseFloat(value) || 0 : value,
    }));
  };

  const handleGeoAutoFill = (detected: {
    temperature?: number;
    humidity?: number;
    rainfall?: number;
    ph?: number;
    state?: string;
  }) => {
    setFormData((prev) => ({
      ...prev,
      ...(detected.temperature !== undefined && { temperature: detected.temperature }),
      ...(detected.humidity !== undefined && { humidity: detected.humidity }),
      ...(detected.rainfall !== undefined && { rainfall: detected.rainfall }),
      ...(detected.ph !== undefined && { ph: detected.ph }),
      ...(detected.state && { state: detected.state }),
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate(formData);
  };

  const result = mutation.data;

  // Comparison plot data
  const comparisonData = result
    ? [
        {
          metric: "Historical Min",
          value: Math.round(result.historical_min_kg_ha),
          fill: "#262C3A",
        },
        {
          metric: "Historical Median",
          value: Math.round(result.historical_median_kg_ha),
          fill: "#414A60",
        },
        {
          metric: "Predicted Yield",
          value: Math.round(result.predicted_yield_kg_ha),
          fill: "#FF2A2A",
        },
        {
          metric: "Historical Max",
          value: Math.round(result.historical_max_kg_ha),
          fill: "#262C3A",
        },
      ]
    : [];

  return (
    <div className="space-y-12">
      {/* Title Ribbon */}
      <div className="border-b border-obsidian-750 pb-6 flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="font-display font-black text-3xl sm:text-4xl lg:text-5xl tracking-tight text-chalk-50 uppercase">
            {t("yield_page_title")}
          </h1>
          <p className="font-sans text-xs sm:text-sm text-obsidian-300 mt-1 max-w-2xl leading-relaxed">
            {t("yield_page_desc")}
          </p>
        </div>
      </div>

      {/* Main Two-Column Workflow */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Parameters Form (Left Column, 5 cols) */}
        <form
          onSubmit={handleSubmit}
          className="lg:col-span-5 border border-obsidian-750 bg-obsidian-950 p-6 shadow-brutal space-y-6"
        >
          <div className="flex items-center justify-between border-b border-obsidian-800 pb-3">
            <span className="font-mono text-xs font-bold uppercase tracking-technical text-chalk-100 flex items-center gap-2">
              <Compass className="w-4 h-4 text-signal-red" />
              {t("soil_env_inputs")}
            </span>
          </div>

          <GeoSensingBanner onAutoFill={handleGeoAutoFill} />

          {/* Retention Notification */}
          {locationState?.fromRecommendation && (
            <div className="p-3 bg-obsidian-900 border border-signal-red/60 text-xs font-mono text-chalk-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2 shadow-brutal-sm">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-signal-red shrink-0 animate-pulse" />
                <span>
                  {t("retained_from_rec")}:{" "}
                  <strong className="text-white uppercase">{getCropName(formData.crop)}</strong>
                </span>
              </div>
              <span className="text-[10px] text-obsidian-400">
                NPK: {formData.nitrogen}-{formData.phosphorus}-{formData.potassium} &bull; pH {formData.ph} &bull; {formData.temperature}°C &bull; {formData.rainfall}mm
              </span>
            </div>
          )}

          {/* Regional & Taxonomic Settings */}
          <div className="space-y-3">
            <div>
              <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                {t("yield_crop_label")}
              </label>
              <select
                name="crop"
                value={formData.crop}
                onChange={handleInputChange}
                className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none uppercase"
              >
                {supportedCrops.length > 0 ? (
                  supportedCrops.map((c) => (
                    <option key={c.canonical_name} value={c.canonical_name}>
                      {getCropName(c.display_name)} ({getCategoryName(c.category)})
                    </option>
                  ))
                ) : (
                  <option value="rice">{getCropName("Rice")}</option>
                )}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  {t("yield_state_label")}
                </label>
                <select
                  name="state"
                  value={formData.state}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none uppercase"
                >
                  {states.map((st) => (
                    <option key={st} value={st}>
                      {getStateName(st) || st}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  {t("yield_season_label")}
                </label>
                <select
                  name="season"
                  value={formData.season}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none uppercase"
                >
                  {SEASONS.map((s) => (
                    <option key={s} value={s}>
                      {getSeasonName(s)}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                {t("yield_soil_label")}
              </label>
              <select
                name="soil_type"
                value={formData.soil_type}
                onChange={handleInputChange}
                className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none uppercase"
              >
                {SOIL_TYPES.map((st) => (
                  <option key={st} value={st}>
                    {getSoilName(st)}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Environmental Conditions */}
          <div className="space-y-3 pt-4 border-t border-obsidian-800">
            <span className="font-mono text-[11px] text-obsidian-400 font-semibold tracking-technical uppercase block">
              {t("climatic_metrics")}
            </span>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  {t("temp_label")}
                </label>
                <input
                  type="number"
                  step="0.5"
                  name="temperature"
                  value={formData.temperature}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  {t("rainfall_label")}
                </label>
                <input
                  type="number"
                  step="10"
                  name="rainfall"
                  value={formData.rainfall}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none"
                  required
                />
              </div>
            </div>
          </div>

          {/* Agricultural Inputs (Fertilizer & Pesticide) */}
          <div className="space-y-3 pt-4 border-t border-obsidian-800">
            <span className="font-mono text-[11px] text-obsidian-400 font-semibold tracking-technical uppercase block">
              {t("yield_fertilizer_label")} &amp; {t("yield_pesticide_label")}
            </span>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  {t("yield_fertilizer_label")}
                </label>
                <input
                  type="number"
                  step="1"
                  name="fertilizer"
                  value={formData.fertilizer}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  {t("yield_pesticide_label")}
                </label>
                <input
                  type="number"
                  step="0.05"
                  name="pesticide"
                  value={formData.pesticide}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none"
                  required
                />
              </div>
            </div>
          </div>

          <Button
            type="submit"
            isLoading={mutation.isPending}
            className="w-full py-3.5 flex items-center justify-center gap-2"
          >
            <span>{mutation.isPending ? t("yield_computing") : t("yield_btn")}</span>
            <ArrowRight className="w-4 h-4" />
          </Button>
        </form>

        {/* Results Panel (Right Column, 7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          {mutation.isError && (
            <StatusBanner
              type="error"
              title="YIELD FORECAST FAILED"
              message={mutation.error.message}
              requestId={mutation.error.requestId}
              onRetry={() => mutation.mutate(formData)}
            />
          )}

          {result ? (
            <div className="space-y-6">
              {/* Primary Massive Forecast Display */}
              <div className="border border-obsidian-750 bg-obsidian-950 p-6 shadow-brutal">
                <div className="flex items-center justify-between border-b border-obsidian-800 pb-3 mb-6">
                  <div>
                    <span className="font-mono text-xs text-obsidian-400 uppercase tracking-widest block mb-0.5">
                      {getCropName(result.crop)} &bull; {formData.state}
                    </span>
                    <h2 className="font-display font-black text-2xl sm:text-3xl text-chalk-50 uppercase tracking-tight">
                      {t("yield_predicted_label")}
                    </h2>
                  </div>
                  <SignalBadge label="HARVEST FORECAST" variant="signal" size="sm" />
                </div>

                {/* 2x2 Metric Grid */}
                <div className="grid grid-cols-2 gap-4">
                  <MetricCard
                    label="METRIC YIELD DENSITY"
                    value={result.predicted_yield_kg_ha.toLocaleString()}
                    unit="KG / HA"
                    secondary="Standardized metric hectare yield"
                    variant="dark"
                  />
                  <MetricCard
                    label="FARM SCALE YIELD"
                    value={result.predicted_yield_quintals_acre.toFixed(2)}
                    unit="Q / ACRE"
                    secondary="Standard farm quintals per acre"
                    variant="signal"
                  />
                  <MetricCard
                    label="HECTARE PRODUCTION"
                    value={result.predicted_yield_quintals_ha.toFixed(2)}
                    unit="Q / HA"
                    secondary="Quintals harvest volume per hectare"
                    variant="dark"
                  />
                  <MetricCard
                    label="ACRE MASS"
                    value={result.predicted_yield_kg_acre.toLocaleString(undefined, {
                      maximumFractionDigits: 1,
                    })}
                    unit="KG / ACRE"
                    secondary="Kilograms per acre"
                    variant="dark"
                  />
                </div>
              </div>

              {/* Scientific Benchmark Comparison Plot */}
              <div className="border border-obsidian-750 bg-obsidian-950 p-6 shadow-brutal space-y-4">
                <div className="flex items-center justify-between border-b border-obsidian-800 pb-3">
                  <div className="flex items-center gap-2 font-mono text-xs font-bold uppercase tracking-technical text-chalk-100">
                    <BarChart2 className="w-4 h-4 text-signal-red" />
                    <span>Historical Spread &amp; Predicted Realization</span>
                  </div>
                </div>

                <div className="h-44 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={comparisonData}
                      margin={{ top: 10, right: 20, left: -10, bottom: 20 }}
                    >
                      <CartesianGrid strokeDasharray="2 2" stroke="#1D222E" vertical={false} />
                      <XAxis
                        dataKey="metric"
                        stroke="#414A60"
                        tick={{ fontFamily: "JetBrains Mono", fontSize: 10, fill: "#AEBAD1" }}
                      />
                      <YAxis
                        stroke="#414A60"
                        tick={{ fontFamily: "JetBrains Mono", fontSize: 10, fill: "#8694B0" }}
                        unit=" kg"
                      />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: "#060709",
                          color: "#F5F4EF",
                          border: "1px solid #31384A",
                          borderRadius: 0,
                          fontFamily: "JetBrains Mono",
                          fontSize: 12,
                        }}
                      />
                      <Bar dataKey="value" name="Yield (kg/ha)">
                        {comparisonData.map((entry, index) => (
                          <Cell
                            key={`cell-${index}`}
                            fill={entry.fill}
                            stroke={entry.fill === "#FF2A2A" ? "#FF2A2A" : "#31384A"}
                          />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                <div className="grid grid-cols-3 gap-3 font-mono text-xs pt-2">
                  <div className="p-2.5 bg-obsidian-900 border border-obsidian-800">
                    <span className="text-[10px] text-obsidian-400 uppercase block mb-0.5">
                      Historical Min
                    </span>
                    <span className="font-bold text-sm text-chalk-200 tabular-nums">
                      {Math.round(result.historical_min_kg_ha).toLocaleString()}
                    </span>
                    <span className="text-[10px] text-obsidian-400 ml-1">kg/ha</span>
                  </div>

                  <div className="p-2.5 bg-obsidian-900 border border-obsidian-800">
                    <span className="text-[10px] text-obsidian-400 uppercase block mb-0.5">
                      Historical Median
                    </span>
                    <span className="font-bold text-sm text-chalk-200 tabular-nums">
                      {Math.round(result.historical_median_kg_ha).toLocaleString()}
                    </span>
                    <span className="text-[10px] text-obsidian-400 ml-1">kg/ha</span>
                  </div>

                  <div className="p-2.5 bg-obsidian-900 border border-obsidian-800">
                    <span className="text-[10px] text-obsidian-400 uppercase block mb-0.5">
                      Historical Max
                    </span>
                    <span className="font-bold text-sm text-chalk-200 tabular-nums">
                      {Math.round(result.historical_max_kg_ha).toLocaleString()}
                    </span>
                    <span className="text-[10px] text-obsidian-400 ml-1">kg/ha</span>
                  </div>
                </div>

                <div className="pt-3 border-t border-obsidian-800 flex items-center justify-between text-[11px] font-mono text-obsidian-400">
                  <span>DES HISTORICAL BASELINE</span>
                  <Link
                    to="/financials"
                    state={{
                      crop: result.crop,
                      yield_kg_per_ha: result.predicted_yield_kg_ha,
                      state: formData.state,
                      fromYieldForecast: true,
                    }}
                    className="text-signal-red font-bold hover:underline flex items-center gap-1"
                  >
                    {t("yield_proceed_fin")} <ArrowUpRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            </div>
          ) : (
            <div className="border border-dashed border-obsidian-750 p-12 text-center space-y-3 bg-obsidian-950">
              <h2 className="font-display font-bold text-lg sm:text-xl text-chalk-100 uppercase">
                {t("awaiting_yield_title")}
              </h2>
              <p className="font-sans text-xs text-obsidian-400 max-w-md mx-auto">
                {t("awaiting_yield_desc")}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Feature 7: Interactive Farm Digital Twin Visualizer */}
      <div className="mt-8">
        <FarmDigitalTwin
          crop={result?.crop || formData.crop}
          soilType={formData.soil_type}
          rainfallMm={formData.rainfall}
          temperatureC={formData.temperature}
        />
      </div>
    </div>
  );
};
