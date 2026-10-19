import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useMutation, useQuery } from "@tanstack/react-query";
import { ArrowRight, BarChart2, Compass, ArrowUpRight } from "lucide-react";
import { api, ApiError } from "../api/client";
import { YieldPredictionRequest, YieldPredictionResponse } from "../types/api";
import { Button } from "../components/ui/Button";
import { SignalBadge } from "../components/visual/SignalBadge";
import { MetricCard } from "../components/ui/MetricCard";
import { StatusBanner } from "../components/ui/StatusBanner";
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

export const YieldPredictionPage: React.FC = () => {
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
    "Haryana",
    "Madhya Pradesh",
    "Karnataka",
    "Tamil Nadu",
    "Andhra Pradesh",
    "West Bengal",
  ];

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
            Crop Yield Forecasting
          </h1>
          <p className="font-sans text-xs sm:text-sm text-obsidian-300 mt-1 max-w-2xl leading-relaxed">
            Project expected harvest volume per hectare and acre based on crop choice, regional climate, soil classification, and input applications.
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
              Field &amp; Environmental Settings
            </span>
          </div>

          {/* Regional & Taxonomic Settings */}
          <div className="space-y-3">
            <div>
              <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                Target Crop
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
                      {c.display_name} ({c.category})
                    </option>
                  ))
                ) : (
                  <option value="rice">Rice (Cereal)</option>
                )}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  Agro-Climatic Region
                </label>
                <select
                  name="state"
                  value={formData.state}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none uppercase"
                >
                  {states.map((st) => (
                    <option key={st} value={st}>
                      {st}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  Season
                </label>
                <select
                  name="season"
                  value={formData.season}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none uppercase"
                >
                  {SEASONS.map((s) => (
                    <option key={s} value={s}>
                      {s}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                Soil Order
              </label>
              <select
                name="soil_type"
                value={formData.soil_type}
                onChange={handleInputChange}
                className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none uppercase"
              >
                {SOIL_TYPES.map((st) => (
                  <option key={st} value={st}>
                    {st}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Environmental Conditions */}
          <div className="space-y-3 pt-4 border-t border-obsidian-800">
            <span className="font-mono text-[11px] text-obsidian-400 font-semibold tracking-technical uppercase block">
              Weather &amp; Rain Conditions
            </span>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  Temperature (°C)
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
                  Total Rainfall (mm)
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
              Application Rates
            </span>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  Fertilizer Rate (kg/ha)
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
                  Pesticide Rate (kg/ha)
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
            <span>Project Harvest Yield</span>
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
                      CROP: {result.crop.toUpperCase()} &bull; REGION: {formData.state}
                    </span>
                    <h2 className="font-display font-black text-2xl sm:text-3xl text-chalk-50 uppercase tracking-tight">
                      PROJECTED HARVEST CAPACITY
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
                    className="text-signal-red font-bold hover:underline flex items-center gap-1"
                  >
                    Calculate Farm Economics <ArrowUpRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            </div>
          ) : (
            <div className="border border-dashed border-obsidian-750 p-12 text-center space-y-3 bg-obsidian-950">
              <h2 className="font-display font-bold text-lg sm:text-xl text-chalk-100 uppercase">
                Awaiting Forecast Parameters
              </h2>
              <p className="font-sans text-xs text-obsidian-400 max-w-md mx-auto">
                Specify crop, region, and application rates on the left, then click "Project Harvest Yield" to compute anticipated production.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
