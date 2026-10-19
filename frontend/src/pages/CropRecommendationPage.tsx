import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { ArrowRight, ArrowUpRight, Sprout } from "lucide-react";
import { api, ApiError } from "../api/client";
import { CropRecommendationRequest, CropRecommendationResponse } from "../types/api";
import { Button } from "../components/ui/Button";
import { SignalBadge } from "../components/visual/SignalBadge";
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

export const CropRecommendationPage: React.FC = () => {
  const [formData, setFormData] = useState<CropRecommendationRequest>({
    n: 90.0,
    p: 42.0,
    k: 43.0,
    temperature: 20.87,
    humidity: 82.0,
    ph: 6.5,
    rainfall: 202.93,
    top_k: 3,
  });

  const mutation = useMutation<
    CropRecommendationResponse,
    ApiError,
    CropRecommendationRequest
  >({
    mutationFn: api.recommendCrops,
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: parseFloat(value) || 0,
    }));
  };

  const handlePreset = (preset: Partial<CropRecommendationRequest>) => {
    setFormData((prev) => ({ ...prev, ...preset }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate(formData);
  };

  const result = mutation.data;

  // Chart data for candidates
  const candidateChartData =
    result?.recommendations.map((rec) => ({
      crop: rec.display_name,
      confidence: parseFloat(rec.confidence_score.toFixed(1)),
      probability: rec.probability,
    })) || [];

  return (
    <div className="space-y-12">
      {/* Page Title Ribbon */}
      <div className="border-b border-obsidian-750 pb-6 flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="font-display font-black text-3xl sm:text-4xl lg:text-5xl tracking-tight text-chalk-50 uppercase">
            Crop Suitability Recommendation
          </h1>
          <p className="font-sans text-xs sm:text-sm text-obsidian-300 mt-1 max-w-2xl leading-relaxed">
            Input soil macronutrient levels (NPK), chemical reaction (pH), and local weather conditions to identify the optimal crops for your land.
          </p>
        </div>

        {/* Rapid Preset Selector */}
        <div className="flex flex-wrap items-center gap-2 font-mono text-xs shrink-0">
          <span className="text-obsidian-400 uppercase text-[10px]">SOIL PRESETS:</span>
          <button
            type="button"
            onClick={() =>
              handlePreset({
                n: 90,
                p: 42,
                k: 43,
                temperature: 20.87,
                humidity: 82.0,
                ph: 6.5,
                rainfall: 202.93,
              })
            }
            className="px-2.5 py-1 bg-obsidian-850 hover:bg-obsidian-800 border border-obsidian-700 text-obsidian-300 hover:text-white text-[11px] uppercase tracking-technical transition-colors"
          >
            Alluvial Paddy
          </button>
          <button
            type="button"
            onClick={() =>
              handlePreset({
                n: 110,
                p: 50,
                k: 20,
                temperature: 24.0,
                humidity: 60.0,
                ph: 7.2,
                rainfall: 80.0,
              })
            }
            className="px-2.5 py-1 bg-obsidian-850 hover:bg-obsidian-800 border border-obsidian-700 text-obsidian-300 hover:text-white text-[11px] uppercase tracking-technical transition-colors"
          >
            Black Cotton
          </button>
          <button
            type="button"
            onClick={() =>
              handlePreset({
                n: 20,
                p: 70,
                k: 80,
                temperature: 18.0,
                humidity: 55.0,
                ph: 6.8,
                rainfall: 75.0,
              })
            }
            className="px-2.5 py-1 bg-obsidian-850 hover:bg-obsidian-800 border border-obsidian-700 text-obsidian-300 hover:text-white text-[11px] uppercase tracking-technical transition-colors"
          >
            Winter Chickpea
          </button>
        </div>
      </div>

      {/* Main Two-Column Layout: Form & Results */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Input Parameters Form (Left Column, 5 cols) */}
        <form
          onSubmit={handleSubmit}
          className="lg:col-span-5 border border-obsidian-750 bg-obsidian-950 p-6 shadow-brutal space-y-6"
        >
          <div className="flex items-center justify-between border-b border-obsidian-800 pb-3">
            <span className="font-mono text-xs font-bold uppercase tracking-technical text-chalk-100 flex items-center gap-2">
              <Sprout className="w-4 h-4 text-signal-red" />
              Soil &amp; Environmental Inputs
            </span>
          </div>

          {/* Macronutrients (NPK) */}
          <div className="space-y-3">
            <span className="font-mono text-[11px] text-obsidian-400 font-semibold tracking-technical uppercase block">
              Soil Macronutrients (kg/ha)
            </span>

            <div className="grid grid-cols-3 gap-2">
              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  Nitrogen (N)
                </label>
                <input
                  type="number"
                  step="1"
                  name="n"
                  value={formData.n}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  Phosphorus (P)
                </label>
                <input
                  type="number"
                  step="1"
                  name="p"
                  value={formData.p}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  Potassium (K)
                </label>
                <input
                  type="number"
                  step="1"
                  name="k"
                  value={formData.k}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                Soil Reaction (pH Value: 3.5 – 9.5)
              </label>
              <input
                type="number"
                step="0.1"
                min="3.0"
                max="10.0"
                name="ph"
                value={formData.ph}
                onChange={handleInputChange}
                className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none"
                required
              />
            </div>
          </div>

          {/* Climatic Factors */}
          <div className="space-y-3 pt-4 border-t border-obsidian-800">
            <span className="font-mono text-[11px] text-obsidian-400 font-semibold tracking-technical uppercase block">
              Atmospheric Conditions
            </span>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  Temperature (°C)
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="temperature"
                  value={formData.temperature}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  Relative Humidity (%)
                </label>
                <input
                  type="number"
                  step="1"
                  name="humidity"
                  value={formData.humidity}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                Seasonal Rainfall (mm)
              </label>
              <input
                type="number"
                step="1"
                name="rainfall"
                value={formData.rainfall}
                onChange={handleInputChange}
                className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none"
                required
              />
            </div>

            <div>
              <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                Candidate Rankings
              </label>
              <select
                name="top_k"
                value={formData.top_k}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    top_k: parseInt(e.target.value) || 3,
                  }))
                }
                className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none uppercase"
              >
                <option value={1}>Top 1 Crop</option>
                <option value={3}>Top 3 Ranked Crops</option>
                <option value={5}>Top 5 Ranked Crops</option>
              </select>
            </div>
          </div>

          <Button
            type="submit"
            isLoading={mutation.isPending}
            className="w-full py-3.5 flex items-center justify-center gap-2"
          >
            <span>Analyze Crop Suitability</span>
            <ArrowRight className="w-4 h-4" />
          </Button>
        </form>

        {/* Results Panel (Right Column, 7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          {mutation.isError && (
            <StatusBanner
              type="error"
              title="SUITABILITY ANALYSIS FAILED"
              message={mutation.error.message}
              requestId={mutation.error.requestId}
              onRetry={() => mutation.mutate(formData)}
            />
          )}

          {result ? (
            <div className="space-y-6">
              {/* Primary Recommended Crop Card */}
              <div className="border border-obsidian-750 bg-obsidian-950 p-6 sm:p-8 shadow-brutal relative overflow-hidden">
                <div className="flex items-center justify-between border-b border-obsidian-800 pb-3 mb-6">
                  <span className="font-mono text-xs tracking-technical uppercase text-signal-red font-bold">
                    RECOMMENDED PRIMARY CROP
                  </span>
                  <SignalBadge
                    label={`${result.confidence_percent.toFixed(1)}% MATCH`}
                    variant="signal"
                    size="sm"
                  />
                </div>

                <div className="space-y-2">
                  <span className="font-mono text-xs text-obsidian-400 uppercase tracking-widest block">
                    {result.category}
                  </span>
                  <h2 className="font-display font-black text-4xl sm:text-5xl lg:text-6xl text-chalk-50 tracking-tight uppercase">
                    {result.display_name}
                  </h2>
                  <p className="font-sans text-xs sm:text-sm text-obsidian-200 leading-relaxed max-w-xl pt-2">
                    {result.description}
                  </p>
                </div>

                {/* Soil Advisory Notes */}
                {result.soil_advisory_notes && result.soil_advisory_notes.length > 0 && (
                  <div className="mt-6 pt-4 border-t border-obsidian-800 space-y-2">
                    <span className="font-mono text-[11px] uppercase text-obsidian-400 tracking-wider font-semibold block">
                      Agronomic Soil Advisory:
                    </span>
                    <div className="space-y-1.5 font-sans text-xs text-obsidian-300">
                      {result.soil_advisory_notes.map((note, idx) => (
                        <div key={idx} className="flex items-start gap-2">
                          <span className="text-signal-red font-bold select-none">&bull;</span>
                          <span>{note}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="mt-8 pt-4 border-t border-obsidian-800 flex flex-wrap items-center justify-between gap-4 font-mono text-[11px] text-obsidian-400">
                  <span>SUITABLE FOR ENTERED SOIL CONDITIONS</span>
                  <Link
                    to="/yield"
                    className="text-signal-red font-bold hover:underline flex items-center gap-1"
                  >
                    Proceed to Yield Forecast <ArrowUpRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>

              {/* Ranked Candidates Probability Distribution Chart */}
              <div className="border border-obsidian-750 bg-obsidian-950 p-6 shadow-brutal">
                <div className="flex items-center justify-between border-b border-obsidian-800 pb-4 mb-6">
                  <div>
                    <h3 className="font-display font-bold text-base sm:text-lg text-chalk-100 uppercase tracking-tight">
                      Candidate Probability Distribution
                    </h3>
                    <p className="font-sans text-xs text-obsidian-400">
                      Ranked suitability scores across top {result.recommendations.length} evaluated crops
                    </p>
                  </div>
                </div>

                <div className="h-44 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={candidateChartData}
                      layout="vertical"
                      margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
                    >
                      <CartesianGrid strokeDasharray="2 2" stroke="#1D222E" horizontal={false} />
                      <XAxis
                        type="number"
                        domain={[0, 100]}
                        stroke="#414A60"
                        tick={{ fontFamily: "JetBrains Mono", fontSize: 11, fill: "#8694B0" }}
                        unit="%"
                      />
                      <YAxis
                        type="category"
                        dataKey="crop"
                        stroke="#414A60"
                        tick={{ fontFamily: "JetBrains Mono", fontSize: 11, fill: "#AEBAD1" }}
                        width={90}
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
                      <Bar dataKey="confidence" name="Suitability Score (%)">
                        {candidateChartData.map((_, index) => (
                          <Cell
                            key={`cell-${index}`}
                            fill={index === 0 ? "#FF2A2A" : "#2E3648"}
                          />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          ) : (
            <div className="border border-dashed border-obsidian-750 p-12 text-center space-y-3 bg-obsidian-950">
              <h2 className="font-display font-bold text-lg sm:text-xl text-chalk-100 uppercase">
                Awaiting Soil Parameters
              </h2>
              <p className="font-sans text-xs text-obsidian-400 max-w-md mx-auto">
                Adjust soil macronutrients or pick a preset on the left, then click "Analyze Crop Suitability" to evaluate crop compatibility.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
