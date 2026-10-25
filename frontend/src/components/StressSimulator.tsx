import React, { useState, useEffect } from "react";
import { Sliders, TrendingDown, TrendingUp, ShieldCheck, AlertCircle, RefreshCw } from "lucide-react";
import { api } from "../api/client";
import { ScenarioComparisonResponse } from "../types/api";

interface StressSimulatorProps {
  crop: string;
  season?: string;
  soil_type?: string;
  state?: string;
  farm_area: number;
  area_unit?: "acre" | "hectare" | "bigha";
  base_rainfall_mm: number;
  base_price_per_quintal: number;
  base_cost_per_ha: number;
}

export const StressSimulator: React.FC<StressSimulatorProps> = ({
  crop,
  season = "Kharif",
  soil_type = "Vertisols",
  state = "Maharashtra",
  farm_area,
  area_unit = "acre",
  base_rainfall_mm,
  base_price_per_quintal,
  base_cost_per_ha,
}) => {
  const [rainfallShock, setRainfallShock] = useState<number>(-25);
  const [priceShock, setPriceShock] = useState<number>(-15);
  const [costShock, setCostShock] = useState<number>(5);
  const [indemnityLevel, setIndemnityLevel] = useState<number>(0.8);

  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<ScenarioComparisonResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const runSimulation = async (rShock: number, pShock: number, cShock: number, ind: number) => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.simulateStress({
        crop,
        season,
        soil_type,
        state,
        farm_area: farm_area > 0 ? farm_area : 2.5,
        area_unit,
        base_rainfall_mm: base_rainfall_mm > 0 ? base_rainfall_mm : 800.0,
        base_price_per_quintal: base_price_per_quintal > 0 ? base_price_per_quintal : 3000.0,
        base_cost_per_ha: base_cost_per_ha > 0 ? base_cost_per_ha : 35000.0,
        rainfall_shock_percent: rShock,
        price_shock_percent: pShock,
        cost_shock_percent: cShock,
        pmfby_indemnity_level: ind,
      });
      setResult(res);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Simulation failed.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      runSimulation(rainfallShock, priceShock, costShock, indemnityLevel);
    }, 250);
    return () => clearTimeout(timer);
  }, [crop, season, soil_type, state, farm_area, area_unit, base_rainfall_mm, base_price_per_quintal, base_cost_per_ha, rainfallShock, priceShock, costShock, indemnityLevel]);

  return (
    <div className="border border-obsidian-750 bg-obsidian-950 p-6 shadow-brutal space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-obsidian-800 gap-3">
        <div>
          <span className="font-mono text-xs font-bold uppercase tracking-technical text-chalk-100 flex items-center gap-2">
            <Sliders className="w-4 h-4 text-signal-red" />
            Climate & Market Risk Simulator
          </span>
          <p className="font-sans text-xs text-obsidian-300 mt-1">
            Simulate farm profitability under rainfall deficits, mandi market price drops, and evaluate PMFBY crop insurance protection.
          </p>
        </div>

        <button
          type="button"
          onClick={() => {
            setRainfallShock(-25);
            setPriceShock(-15);
            setCostShock(5);
            setIndemnityLevel(0.8);
          }}
          disabled={loading}
          className="inline-flex items-center gap-1.5 px-2.5 py-1 text-[11px] font-mono text-obsidian-400 hover:text-chalk-100 border border-obsidian-800 hover:border-obsidian-700 bg-obsidian-900 transition-colors shrink-0 disabled:opacity-50"
        >
          <RefreshCw className={`w-3 h-3 ${loading ? "animate-spin text-signal-red" : ""}`} />
          <span>{loading ? "Simulating..." : "Reset Shocks"}</span>
        </button>
      </div>

      {/* Sliders Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Rainfall Deficit/Surplus Slider */}
        <div className="space-y-2">
          <div className="flex justify-between items-center text-xs font-mono">
            <span className="text-obsidian-300">Rainfall Shock</span>
            <span className={`font-bold ${rainfallShock < 0 ? "text-amber-400" : "text-emerald-400"}`}>
              {rainfallShock > 0 ? `+${rainfallShock}%` : `${rainfallShock}%`}
            </span>
          </div>
          <input
            type="range"
            min="-50"
            max="50"
            step="5"
            value={rainfallShock}
            onChange={(e) => setRainfallShock(parseInt(e.target.value, 10))}
            className="w-full accent-emerald-500 bg-obsidian-850 h-2 rounded cursor-pointer"
          />
          <div className="flex justify-between text-[10px] text-obsidian-500 font-mono">
            <span>-50% Drought</span>
            <span>Normal</span>
            <span>+50% Excess</span>
          </div>
        </div>

        {/* Mandi Wholesale Price Shock Slider */}
        <div className="space-y-2">
          <div className="flex justify-between items-center text-xs font-mono">
            <span className="text-obsidian-300">Mandi Price Shock</span>
            <span className={`font-bold ${priceShock < 0 ? "text-signal-red" : "text-emerald-400"}`}>
              {priceShock > 0 ? `+${priceShock}%` : `${priceShock}%`}
            </span>
          </div>
          <input
            type="range"
            min="-50"
            max="50"
            step="5"
            value={priceShock}
            onChange={(e) => setPriceShock(parseInt(e.target.value, 10))}
            className="w-full accent-signal-red bg-obsidian-850 h-2 rounded cursor-pointer"
          />
          <div className="flex justify-between text-[10px] text-obsidian-500 font-mono">
            <span>-50% Crash</span>
            <span>Baseline Mandi</span>
            <span>+50% Rally</span>
          </div>
        </div>

        {/* PMFBY Indemnity Level Selector */}
        <div className="space-y-2">
          <div className="flex justify-between items-center text-xs font-mono">
            <span className="text-obsidian-300">PMFBY Indemnity</span>
            <span className="font-bold text-chalk-100">{Math.round(indemnityLevel * 100)}%</span>
          </div>
          <div className="grid grid-cols-3 gap-1.5 pt-1">
            {[0.7, 0.8, 0.9].map((lvl) => (
              <button
                key={lvl}
                type="button"
                onClick={() => setIndemnityLevel(lvl)}
                className={`py-1.5 text-xs font-mono text-center border transition-all ${
                  indemnityLevel === lvl
                    ? "border-emerald-500 bg-emerald-950/40 text-emerald-300 font-bold"
                    : "border-obsidian-800 bg-obsidian-900 text-obsidian-400 hover:text-chalk-200"
                }`}
              >
                {Math.round(lvl * 100)}%
              </button>
            ))}
          </div>
          <p className="text-[10px] text-obsidian-500 font-mono">
            Standard govt threshold indemnity level
          </p>
        </div>
      </div>

      {/* Error state */}
      {error && (
        <div className="p-3 bg-signal-red/10 border border-signal-red/30 text-xs text-signal-red flex items-center gap-2 font-mono">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Results Comparison Grid */}
      {result && (
        <div className="space-y-4 pt-2 border-t border-obsidian-800">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono">
            {/* Yield Impact Card */}
            <div className="p-4 bg-obsidian-900/80 border border-obsidian-800 space-y-2">
              <span className="text-[11px] text-obsidian-400 uppercase tracking-technical block">
                Simulated Harvest Yield
              </span>
              <div className="flex items-baseline gap-2">
                <span className="text-2xl font-black text-chalk-50">
                  {Math.round(result.simulated_yield_kg_ha)}
                </span>
                <span className="text-xs text-obsidian-400">kg/ha</span>
              </div>
              <div className="flex items-center gap-1.5 text-xs">
                {result.yield_delta_kg_ha < 0 ? (
                  <>
                    <TrendingDown className="w-3.5 h-3.5 text-amber-400" />
                    <span className="text-amber-400">
                      {result.yield_delta_kg_ha} kg/ha ({result.yield_delta_percent}%)
                    </span>
                  </>
                ) : (
                  <>
                    <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
                    <span className="text-emerald-400">
                      +{result.yield_delta_kg_ha} kg/ha (+{result.yield_delta_percent}%)
                    </span>
                  </>
                )}
                <span className="text-[10px] text-obsidian-500 ml-auto">vs base</span>
              </div>
            </div>

            {/* Net Profit Impact Card */}
            <div className="p-4 bg-obsidian-900/80 border border-obsidian-800 space-y-2">
              <span className="text-[11px] text-obsidian-400 uppercase tracking-technical block">
                Simulated Net Farm Profit
              </span>
              <div className="flex items-baseline gap-2">
                <span className={`text-2xl font-black ${result.simulated_net_profit < 0 ? "text-signal-red" : "text-chalk-50"}`}>
                  ₹{Math.round(result.simulated_net_profit).toLocaleString("en-IN")}
                </span>
              </div>
              <div className="flex items-center gap-1.5 text-xs">
                {result.profit_delta < 0 ? (
                  <>
                    <TrendingDown className="w-3.5 h-3.5 text-signal-red" />
                    <span className="text-signal-red">
                      -₹{Math.abs(Math.round(result.profit_delta)).toLocaleString("en-IN")} ({result.profit_delta_percent}%)
                    </span>
                  </>
                ) : (
                  <>
                    <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
                    <span className="text-emerald-400">
                      +₹{Math.round(result.profit_delta).toLocaleString("en-IN")} (+{result.profit_delta_percent}%)
                    </span>
                  </>
                )}
                <span className="text-[10px] text-obsidian-500 ml-auto">
                  ROI: {Math.round(result.simulated_roi_percent)}%
                </span>
              </div>
            </div>

            {/* PMFBY Protection Card */}
            <div className={`p-4 border space-y-2 ${
              result.pmfby_insurance.is_claim_triggered
                ? "bg-emerald-950/20 border-emerald-500/30"
                : "bg-obsidian-900/80 border-obsidian-800"
            }`}>
              <div className="flex items-center justify-between">
                <span className="text-[11px] text-obsidian-400 uppercase tracking-technical">
                  PMFBY Crop Insurance
                </span>
                {result.pmfby_insurance.is_claim_triggered ? (
                  <span className="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded">
                    <ShieldCheck className="w-3 h-3" />
                    Shortfall Claim Active
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 text-[10px] text-obsidian-400 bg-obsidian-800 px-1.5 py-0.5 rounded">
                    Above Threshold
                  </span>
                )}
              </div>

              <div className="flex items-baseline gap-2">
                <span className="text-2xl font-black text-chalk-50">
                  {result.pmfby_insurance.is_claim_triggered
                    ? result.pmfby_insurance.formatted_claim_inr
                    : "₹0"}
                </span>
                <span className="text-xs text-obsidian-400">
                  {result.pmfby_insurance.is_claim_triggered ? "claim payout" : "no claim"}
                </span>
              </div>

              <div className="text-[11px] text-obsidian-300 space-y-0.5 pt-1 border-t border-obsidian-800/60">
                <div className="flex justify-between">
                  <span className="text-obsidian-500">Threshold Yield:</span>
                  <span>{Math.round(result.pmfby_insurance.threshold_yield_kg_ha)} kg/ha</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-obsidian-500">Farmer Premium:</span>
                  <span>{result.pmfby_insurance.formatted_premium_inr} ({result.pmfby_insurance.farmer_premium_rate_percent}%)</span>
                </div>
                {result.pmfby_insurance.is_claim_triggered && (
                  <div className="flex justify-between font-bold text-emerald-300 pt-0.5">
                    <span>Net with Insurance:</span>
                    <span>{result.pmfby_insurance.formatted_net_position_inr}</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          <p className="text-[11px] text-obsidian-500 italic font-mono pt-1">
            * {result.pmfby_insurance.caveat}
          </p>
        </div>
      )}
    </div>
  );
};
