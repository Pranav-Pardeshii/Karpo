import React, { useState, useEffect } from "react";
import { RotateCcw, Calendar } from "lucide-react";
import { api } from "../api/client";
import { CropRotationResponse } from "../types/api";

interface CropRotationOptimizerProps {
  initialCrop?: string;
  initialSoil?: string;
  initialState?: string;
}

export const CropRotationOptimizer: React.FC<CropRotationOptimizerProps> = ({
  initialCrop = "cotton",
  initialSoil = "Vertisols",
  initialState = "Maharashtra",
}) => {
  const [crop, setCrop] = useState(initialCrop);
  const [soilType, setSoilType] = useState(initialSoil);
  const [state, setState] = useState(initialState);
  const [irrigationAvailable, setIrrigationAvailable] = useState(true);
  const [years, setYears] = useState(2);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [rotationPlan, setRotationPlan] = useState<CropRotationResponse | null>(null);

  useEffect(() => {
    if (initialCrop) {
      setCrop(initialCrop.toLowerCase());
    }
  }, [initialCrop]);

  const handleFetchPlan = async () => {
    setLoading(true);
    setError(null);
    try {
      const plan = await api.getRotationPlan({
        current_crop: crop,
        soil_type: soilType,
        irrigation_available: irrigationAvailable,
        state: state,
        years: years,
      });
      setRotationPlan(plan);
    } catch (err: any) {
      setError(err?.message || "Unable to compute crop rotation plan.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleFetchPlan();
  }, [crop, soilType, irrigationAvailable, years]);

  return (
    <div className="border border-obsidian-800 bg-white p-6 shadow-sm space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-obsidian-800 gap-3">
        <div>
          <div className="flex items-center gap-2">
            <div className="p-1.5 bg-[#EAF0E6] border border-[#789477]/40 text-[#244B35]">
              <RotateCcw className="w-4 h-4" />
            </div>
            <h3 className="font-mono text-sm font-bold uppercase tracking-technical text-chalk-100">
              Crop Rotation & Intercropping Optimizer
            </h3>
            <span className="text-[10px] uppercase font-mono font-bold tracking-wider px-2 py-0.5 bg-[#EAF0E6] text-[#357A4A] border border-[#357A4A]/30">
              ICAR Validated
            </span>
          </div>
          <p className="font-sans text-xs text-obsidian-300 mt-1 max-w-2xl leading-relaxed">
            Multi-season sequencing alternating restorative legumes and exhaustive cereals to protect soil organic carbon.
          </p>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs shrink-0">
          <label className="text-obsidian-400 uppercase text-[10px]">Plan Duration:</label>
          <select
            value={years}
            onChange={(e) => setYears(Number(e.target.value))}
            className="bg-white border border-obsidian-800 text-chalk-100 text-xs px-2.5 py-1.5 focus:border-signal-red focus:outline-none"
          >
            <option value={1}>1 Year (3 Seasons)</option>
            <option value={2}>2 Years (6 Seasons)</option>
            <option value={3}>3 Years (9 Seasons)</option>
          </select>
        </div>
      </div>

      {/* Control Strip */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 bg-[#F7F5EF] border border-obsidian-800 p-3.5 font-mono text-xs">
        <div>
          <label className="block text-obsidian-400 uppercase text-[10px] mb-1">
            Primary Baseline Crop
          </label>
          <select
            value={crop}
            onChange={(e) => setCrop(e.target.value)}
            className="w-full bg-white border border-obsidian-800 text-chalk-100 px-3 py-1.5 font-mono text-xs focus:border-signal-red focus:outline-none capitalize"
          >
            <option value="cotton">Cotton (Kharif)</option>
            <option value="soybean">Soybean (Kharif)</option>
            <option value="maize">Maize (Kharif)</option>
            <option value="rice">Rice / Paddy (Kharif)</option>
            <option value="groundnut">Groundnut (Kharif)</option>
            <option value="chickpea">Chickpea (Rabi)</option>
            <option value="wheat">Wheat (Rabi)</option>
            <option value="pigeonpeas">Pigeonpea / Arhar</option>
          </select>
        </div>

        <div>
          <label className="block text-obsidian-400 uppercase text-[10px] mb-1">
            Soil Classification
          </label>
          <select
            value={soilType}
            onChange={(e) => setSoilType(e.target.value)}
            className="w-full bg-obsidian-850 border border-obsidian-700 text-chalk-100 px-3 py-1.5 font-mono text-xs focus:border-signal-red focus:outline-none"
          >
            <option value="Vertisols">Vertisols (Black Cotton Soil)</option>
            <option value="Inceptisols">Inceptisols (Alluvial / Loamy)</option>
            <option value="Alfisols">Alfisols (Red Sandy / Loam)</option>
            <option value="Entisols">Entisols (Riverine / Shallow)</option>
          </select>
        </div>

        <div>
          <label className="block text-obsidian-400 uppercase text-[10px] mb-1">
            State Context
          </label>
          <select
            value={state}
            onChange={(e) => setState(e.target.value)}
            className="w-full bg-obsidian-850 border border-obsidian-700 text-chalk-100 px-3 py-1.5 font-mono text-xs focus:border-signal-red focus:outline-none"
          >
            <option value="Maharashtra">Maharashtra</option>
            <option value="Madhya Pradesh">Madhya Pradesh</option>
            <option value="Gujarat">Gujarat</option>
            <option value="Punjab">Punjab</option>
            <option value="Karnataka">Karnataka</option>
            <option value="Uttar Pradesh">Uttar Pradesh</option>
          </select>
        </div>

        <div className="flex flex-col justify-end">
          <label className="flex items-center gap-2 cursor-pointer text-chalk-200 py-1.5 select-none font-mono text-xs">
            <input
              type="checkbox"
              checked={irrigationAvailable}
              onChange={(e) => setIrrigationAvailable(e.target.checked)}
              className="accent-[#244B35] bg-obsidian-850 border-obsidian-700 w-4 h-4 cursor-pointer"
            />
            <span>Assured Irrigation</span>
          </label>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-signal-red/10 border border-signal-red/40 text-xs text-chalk-200 font-mono">
          {error}
        </div>
      )}

      {loading && !rotationPlan && (
        <div className="py-8 text-center text-xs font-mono text-obsidian-400">
          Synthesizing multi-season agronomic crop rotation plan...
        </div>
      )}

      {rotationPlan && (
        <div className="space-y-6">
          {/* Timeline Cards */}
          <div className="space-y-3">
            <h4 className="font-mono text-xs font-bold text-obsidian-300 uppercase tracking-technical">
              Multi-Season Cropping Calendar
            </h4>

            <div className="grid grid-cols-1 gap-3">
              {rotationPlan.yearly_plans.map((year) => (
                <div
                  key={year.year_number}
                  className="bg-white border border-obsidian-800 p-4 space-y-3 shadow-sm"
                >
                  <div className="flex items-center justify-between pb-2 border-b border-obsidian-800">
                    <span className="font-mono text-xs font-bold text-signal-red uppercase tracking-technical flex items-center gap-1.5">
                      <Calendar className="w-3.5 h-3.5 text-signal-red" />
                      YEAR {year.year_number} SEQUENCE
                    </span>
                    <span className="font-mono text-[10px] text-obsidian-400 uppercase tracking-wider">
                      3-Season Agro Cycle
                    </span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {/* Kharif */}
                    <div className="bg-[#F7F5EF] border border-obsidian-800 p-3 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] uppercase font-mono font-bold text-signal-amber bg-[#FDF8F0] border border-signal-amber/40 px-2 py-0.5">
                          Kharif (Monsoon)
                        </span>
                      </div>
                      <div className="text-sm font-semibold text-chalk-100 font-display">
                        {year.kharif.display_name}
                      </div>
                      <p className="text-xs text-obsidian-300 leading-relaxed font-sans">
                        {year.kharif.agronomic_role}
                      </p>
                    </div>

                    {/* Rabi */}
                    <div className="bg-[#F7F5EF] border border-obsidian-800 p-3 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] uppercase font-mono font-bold text-[#244B35] bg-[#EAF0E6] border border-[#244B35]/40 px-2 py-0.5">
                          Rabi (Winter)
                        </span>
                      </div>
                      <div className="text-sm font-semibold text-chalk-100 font-display">
                        {year.rabi.display_name}
                      </div>
                      <p className="text-xs text-obsidian-300 leading-relaxed font-sans">
                        {year.rabi.agronomic_role}
                      </p>
                    </div>

                    {/* Zaid */}
                    <div className="bg-[#F7F5EF] border border-obsidian-800 p-3 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] uppercase font-mono font-bold text-[#357A4A] bg-[#EAF0E6] border border-[#357A4A]/40 px-2 py-0.5">
                          Zaid (Summer)
                        </span>
                      </div>
                      <div className="text-sm font-semibold text-chalk-100 font-display">
                        {year.zaid.display_name}
                      </div>
                      <p className="text-xs text-obsidian-300 leading-relaxed font-sans">
                        {year.zaid.agronomic_role}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Intercropping Section */}
          {rotationPlan.intercropping_options.length > 0 && (
            <div className="pt-2 border-t border-obsidian-800 space-y-3">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <h4 className="font-mono text-xs font-bold text-obsidian-300 uppercase tracking-technical">
                  Validated Companion Intercropping Systems for {rotationPlan.current_crop.toUpperCase()}
                </h4>
                <span className="font-mono text-[10px] text-obsidian-400">
                  Land Equivalent Ratio (LER) &gt; 1.0 represents efficiency gain
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {rotationPlan.intercropping_options.map((option, idx) => (
                  <div
                    key={idx}
                    className="bg-white border border-obsidian-800 p-3.5 space-y-2 shadow-sm"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-chalk-100 font-display text-xs">
                        + {option.display_name}
                      </span>
                      <span className="px-2 py-0.5 bg-[#EAF0E6] text-[#357A4A] border border-[#357A4A]/40 font-mono font-bold text-[11px]">
                        LER: {option.literature_ler_range}
                      </span>
                    </div>

                    <div className="font-mono text-[11px] text-obsidian-400">
                      <strong className="text-chalk-300">Spatial Configuration:</strong> {option.row_ratio}
                    </div>

                    <p className="font-sans text-xs text-obsidian-300 leading-relaxed">
                      {option.agronomic_benefit}
                    </p>

                    <div className="pt-2 border-t border-obsidian-800/80 flex items-center justify-between font-mono text-[10px] text-obsidian-500">
                      <span>Competition: {option.water_competition}</span>
                      <span className="truncate max-w-[200px]" title={option.source}>
                        Source: {option.source}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Agronomic Principles & Provenance Footer */}
          <div className="pt-3 border-t border-obsidian-800 flex flex-col sm:flex-row items-start sm:items-center justify-between font-mono text-[11px] text-obsidian-400 gap-2">
            <div className="flex items-center gap-2">
              <span className="px-1.5 py-0.5 bg-obsidian-900 border border-obsidian-750 text-chalk-300 text-[10px] uppercase">
                Category: {rotationPlan.data_category}
              </span>
              <span>{rotationPlan.data_provenance}</span>
            </div>
            <p className="text-[10px] text-obsidian-400 italic max-w-xl">
              {rotationPlan.caveat}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
