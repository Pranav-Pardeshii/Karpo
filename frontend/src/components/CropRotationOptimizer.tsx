import React, { useState, useEffect } from "react";
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
    // Automatically load plan on initial mount
    handleFetchPlan();
  }, [crop, soilType, irrigationAvailable, years]);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-800 gap-2">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xl">🔄</span>
            <h3 className="text-lg font-semibold text-slate-100">
              Crop Rotation & Intercropping Optimizer
            </h3>
            <span className="text-xs px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-400 border border-emerald-800 font-medium">
              ICAR Validated
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Multi-season sequencing alternating restorative legumes and exhaustive cereals to protect soil organic carbon.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <label className="text-xs text-slate-400">Plan Duration:</label>
          <select
            value={years}
            onChange={(e) => setYears(Number(e.target.value))}
            className="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded px-2.5 py-1 focus:outline-none focus:border-emerald-500"
          >
            <option value={1}>1 Year (3 Seasons)</option>
            <option value={2}>2 Years (6 Seasons)</option>
            <option value={3}>3 Years (9 Seasons)</option>
          </select>
        </div>
      </div>

      {/* Control Strip */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 my-4 bg-slate-950/50 p-3 rounded-lg border border-slate-800/80 text-xs">
        <div>
          <label className="block text-slate-400 mb-1">Primary Baseline Crop</label>
          <select
            value={crop}
            onChange={(e) => setCrop(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 text-slate-200 rounded px-2 py-1.5 focus:outline-none focus:border-emerald-500 capitalize"
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
          <label className="block text-slate-400 mb-1">Soil Classification</label>
          <select
            value={soilType}
            onChange={(e) => setSoilType(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 text-slate-200 rounded px-2 py-1.5 focus:outline-none focus:border-emerald-500"
          >
            <option value="Vertisols">Vertisols (Black Cotton Soil)</option>
            <option value="Inceptisols">Inceptisols (Alluvial / Loamy)</option>
            <option value="Alfisols">Alfisols (Red Sandy / Loam)</option>
            <option value="Entisols">Entisols (Riverine / Shallow)</option>
          </select>
        </div>

        <div>
          <label className="block text-slate-400 mb-1">State Context</label>
          <select
            value={state}
            onChange={(e) => setState(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 text-slate-200 rounded px-2 py-1.5 focus:outline-none focus:border-emerald-500"
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
          <label className="flex items-center gap-2 cursor-pointer text-slate-300 py-1.5">
            <input
              type="checkbox"
              checked={irrigationAvailable}
              onChange={(e) => setIrrigationAvailable(e.target.checked)}
              className="rounded bg-slate-800 border-slate-700 text-emerald-500 focus:ring-emerald-500 w-4 h-4"
            />
            <span>Assured Irrigation</span>
          </label>
        </div>
      </div>

      {error && (
        <div className="p-3 mb-4 rounded bg-red-950/40 border border-red-800 text-xs text-red-300">
          {error}
        </div>
      )}

      {loading && !rotationPlan && (
        <div className="py-8 text-center text-xs text-slate-500">
          Synthesizing multi-season agronomic crop rotation plan...
        </div>
      )}

      {rotationPlan && (
        <div className="space-y-5">
          {/* Timeline Cards */}
          <div className="space-y-3">
            <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
              Multi-Season Cropping Calendar
            </h4>

            <div className="grid grid-cols-1 gap-3">
              {rotationPlan.yearly_plans.map((year) => (
                <div
                  key={year.year_number}
                  className="bg-slate-950/40 border border-slate-800/90 rounded-lg p-3.5"
                >
                  <div className="flex items-center justify-between mb-2.5 pb-1.5 border-b border-slate-800/60">
                    <span className="text-xs font-bold text-emerald-400">
                      YEAR {year.year_number} SEQUENCE
                    </span>
                    <span className="text-[11px] text-slate-500">
                      3-Season Agro Cycle
                    </span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {/* Kharif */}
                    <div className="bg-slate-900/90 border border-slate-800 rounded p-2.5">
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] uppercase font-bold text-amber-400 bg-amber-950/50 px-1.5 py-0.5 rounded border border-amber-900/50">
                          Kharif (Monsoon)
                        </span>
                      </div>
                      <div className="text-sm font-semibold text-slate-100 mt-1.5">
                        {year.kharif.display_name}
                      </div>
                      <p className="text-[11px] text-slate-400 mt-1 leading-relaxed">
                        {year.kharif.agronomic_role}
                      </p>
                    </div>

                    {/* Rabi */}
                    <div className="bg-slate-900/90 border border-slate-800 rounded p-2.5">
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] uppercase font-bold text-sky-400 bg-sky-950/50 px-1.5 py-0.5 rounded border border-sky-900/50">
                          Rabi (Winter)
                        </span>
                      </div>
                      <div className="text-sm font-semibold text-slate-100 mt-1.5">
                        {year.rabi.display_name}
                      </div>
                      <p className="text-[11px] text-slate-400 mt-1 leading-relaxed">
                        {year.rabi.agronomic_role}
                      </p>
                    </div>

                    {/* Zaid */}
                    <div className="bg-slate-900/90 border border-slate-800 rounded p-2.5">
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] uppercase font-bold text-emerald-400 bg-emerald-950/50 px-1.5 py-0.5 rounded border border-emerald-900/50">
                          Zaid (Summer)
                        </span>
                      </div>
                      <div className="text-sm font-semibold text-slate-100 mt-1.5">
                        {year.zaid.display_name}
                      </div>
                      <p className="text-[11px] text-slate-400 mt-1 leading-relaxed">
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
            <div className="pt-2 border-t border-slate-800">
              <div className="flex items-center justify-between mb-2.5">
                <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                  Validated Companion Intercropping Systems for {rotationPlan.current_crop.toUpperCase()}
                </h4>
                <span className="text-[11px] text-slate-400">
                  Land Equivalent Ratio (LER) &gt; 1.0 represents land efficiency gain
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {rotationPlan.intercropping_options.map((option, idx) => (
                  <div
                    key={idx}
                    className="bg-slate-950/60 border border-slate-800 rounded-lg p-3 text-xs"
                  >
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="font-semibold text-slate-100">
                        + {option.display_name}
                      </span>
                      <span className="px-2 py-0.5 bg-emerald-950 text-emerald-300 border border-emerald-800 rounded font-mono font-bold text-[11px]">
                        LER: {option.literature_ler_range}
                      </span>
                    </div>

                    <div className="text-[11px] text-slate-400 mb-1">
                      <strong className="text-slate-300">Spatial Configuration:</strong> {option.row_ratio}
                    </div>

                    <p className="text-[11px] text-slate-300 mb-2 leading-relaxed">
                      {option.agronomic_benefit}
                    </p>

                    <div className="pt-1.5 border-t border-slate-800/80 flex items-center justify-between text-[10px] text-slate-500">
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
          <div className="pt-3 border-t border-slate-800/80 flex flex-col sm:flex-row items-start sm:items-center justify-between text-[11px] text-slate-500 gap-2">
            <div className="flex items-center gap-2">
              <span className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[10px]">
                Category: {rotationPlan.data_category}
              </span>
              <span>{rotationPlan.data_provenance}</span>
            </div>
            <p className="text-[10px] text-slate-500 italic max-w-xl">
              {rotationPlan.caveat}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
