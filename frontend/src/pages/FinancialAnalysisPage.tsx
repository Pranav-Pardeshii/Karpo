import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { useMutation, useQuery } from "@tanstack/react-query";
import { ArrowRight, DollarSign, Sliders, Zap, ArrowUpRight } from "lucide-react";
import { api, ApiError } from "../api/client";
import {
  FinancialAnalysisRequest,
  FinancialAnalysisResponse,
} from "../types/api";
import { Button } from "../components/ui/Button";
import { SignalBadge } from "../components/visual/SignalBadge";
import { MetricCard } from "../components/ui/MetricCard";
import { StatusBanner } from "../components/ui/StatusBanner";
import { StressSimulator } from "../components/StressSimulator";
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
import { useLanguage } from "../context/LanguageContext";

interface FinLocationState {
  crop?: string;
  yield_kg_per_ha?: number;
  state?: string;
  farm_area?: number;
  area_unit?: "acre" | "hectare" | "bigha";
  fromYieldForecast?: boolean;
}

export const FinancialAnalysisPage: React.FC = () => {
  const { t, getCropName, getStateName, getUnitName } = useLanguage();
  const location = useLocation();
  const locationState = location.state as FinLocationState | null;

  const [formData, setFormData] = useState<FinancialAnalysisRequest>({
    yield_kg_per_ha: 3500.0,
    farm_area: 2.5,
    area_unit: "acre",
    price_per_quintal: 2250.0,
    cost_per_ha: 38000.0,
  });

  const [lookupCrop, setLookupCrop] = useState<string>("rice");
  const [lookupState, setLookupState] = useState<string>("Maharashtra");

  const { data: supportedCrops = [] } = useQuery({
    queryKey: ["supportedCrops"],
    queryFn: api.getSupportedCrops,
  });

  const { data: statesData } = useQuery({
    queryKey: ["cultivationStates"],
    queryFn: api.getCultivationStates,
  });

  const states = statesData?.states || ["Maharashtra", "Punjab", "Uttar Pradesh", "Gujarat"];

  const costLookupMutation = useMutation({
    mutationFn: api.estimateCultivationCosts,
    onSuccess: (data) => {
      setFormData((prev) => ({
        ...prev,
        cost_per_ha: data.cul_cost_c2_per_ha,
      }));
    },
  });

  const priceLookupMutation = useMutation({
    mutationFn: api.getMarketPriceForCrop,
    onSuccess: (data) => {
      setFormData((prev) => ({
        ...prev,
        price_per_quintal: data.modal_rs_per_quintal,
      }));
    },
  });

  useEffect(() => {
    if (!locationState?.state) {
      try {
        const raw = sessionStorage.getItem("karpo_geo_sensing_cache");
        if (raw) {
          const cached = JSON.parse(raw);
          if (cached?.data?.location?.canonical_state) {
            setLookupState(cached.data.location.canonical_state);
          }
        }
      } catch {
        // Ignore cache parse error
      }
    }

    if (!locationState) return;

    if (locationState.crop) {
      setLookupCrop(locationState.crop.toLowerCase().trim());
    }
    if (locationState.state) {
      setLookupState(locationState.state);
    }
    if (locationState.yield_kg_per_ha != null) {
      setFormData((prev) => ({
        ...prev,
        yield_kg_per_ha: Math.round(locationState.yield_kg_per_ha!),
        farm_area: locationState.farm_area ?? prev.farm_area,
        area_unit: locationState.area_unit ?? prev.area_unit,
      }));
    }

    const cropToLookup = locationState.crop || lookupCrop;
    const stateToLookup = locationState.state || lookupState;
    costLookupMutation.mutate({ crop_name: cropToLookup, state_name: stateToLookup });
    priceLookupMutation.mutate(cropToLookup);
  }, [locationState]);

  const mutation = useMutation<
    FinancialAnalysisResponse,
    ApiError,
    FinancialAnalysisRequest
  >({
    mutationFn: api.calculateFinancials,
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

  const handleAutofillBenchmarks = () => {
    costLookupMutation.mutate({ crop_name: lookupCrop, state_name: lookupState });
    priceLookupMutation.mutate(lookupCrop);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate(formData);
  };

  const result = mutation.data;

  // Chart data for revenue vs expenditure vs profit
  const financialChartData = result
    ? [
        { name: t("fin_gross_revenue"), amount: result.total_revenue, fill: "#244B35" },
        { name: t("fin_total_cost"), amount: result.total_cost, fill: "#A66B18" },
        {
          name: t("fin_net_profit"),
          amount: Math.max(0, result.net_profit),
          fill: result.net_profit >= 0 ? "#357A4A" : "#B54747",
        },
      ]
    : [];

  return (
    <div className="space-y-12">
      {/* Title Header */}
      <div className="border-b border-obsidian-750 pb-6 flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="font-display font-black text-3xl sm:text-4xl lg:text-5xl tracking-tight text-chalk-50 uppercase">
            {t("fin_page_title")}
          </h1>
          <p className="font-sans text-xs sm:text-sm text-obsidian-300 mt-1 max-w-2xl leading-relaxed">
            {t("fin_page_desc")}
          </p>
        </div>

        {/* Quick Benchmark Sync Widget */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 p-3 border border-obsidian-800 bg-white shrink-0">
          <div className="flex items-center gap-1.5 font-mono text-xs">
            <select
              value={lookupCrop}
              onChange={(e) => setLookupCrop(e.target.value)}
              className="bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-2 py-1 uppercase text-[11px] focus:outline-none"
            >
              {supportedCrops.map((c) => (
                <option key={c.canonical_name} value={c.canonical_name}>
                  {getCropName(c.canonical_name) || c.display_name}
                </option>
              ))}
            </select>

            <select
              value={lookupState}
              onChange={(e) => setLookupState(e.target.value)}
              className="bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-2 py-1 uppercase text-[11px] focus:outline-none"
            >
              {states.map((st) => (
                <option key={st} value={st}>
                  {getStateName(st) || st}
                </option>
              ))}
            </select>
          </div>

          <button
            type="button"
            onClick={handleAutofillBenchmarks}
            disabled={costLookupMutation.isPending || priceLookupMutation.isPending}
            className="px-3 py-1 bg-obsidian-850 hover:bg-signal-red hover:text-white border border-obsidian-700 text-chalk-200 font-mono text-[10px] uppercase tracking-technical flex items-center justify-center gap-1.5 transition-colors disabled:opacity-40"
          >
            <Zap className="w-3 h-3 text-signal-red" />
            <span>{t("sync_benchmarks")}</span>
          </button>
        </div>
      </div>

      {/* Main Two-Column Workflow */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Parameters Form (Left Column, 5 cols) */}
        <form
          onSubmit={handleSubmit}
          className="lg:col-span-5 border border-obsidian-800 bg-white p-6 shadow-brutal space-y-6"
        >
          <div className="flex items-center justify-between border-b border-obsidian-800 pb-3">
            <span className="font-mono text-xs font-bold uppercase tracking-technical text-chalk-100 flex items-center gap-2">
              <DollarSign className="w-4 h-4 text-signal-red" />
              {t("econ_sim_inputs")}
            </span>
          </div>

          {/* Retention Notification */}
          {locationState?.fromYieldForecast && (
            <div className="p-3 bg-obsidian-900 border border-signal-red/60 text-xs font-mono text-chalk-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2 shadow-brutal-sm">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-signal-red shrink-0 animate-pulse" />
                <span>
                  {t("retained_from_yield")}:{" "}
                  <strong className="text-chalk-50 uppercase">{getCropName(lookupCrop)}</strong> ({Math.round(formData.yield_kg_per_ha).toLocaleString()} kg/ha &bull; {getStateName(lookupState)})
                </span>
              </div>
            </div>
          )}

          {/* Land Scale & Area */}
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  {t("fin_farm_area")}
                </label>
                <input
                  type="number"
                  step="0.1"
                  min="0.1"
                  name="farm_area"
                  value={formData.farm_area}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  {t("fin_area_unit")}
                </label>
                <select
                  name="area_unit"
                  value={formData.area_unit}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none uppercase"
                >
                  <option value="acre">{getUnitName("acre")}</option>
                  <option value="hectare">{getUnitName("hectare")}</option>
                  <option value="bigha">{getUnitName("bigha")}</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                {t("fin_yield")}
              </label>
              <input
                type="number"
                step="50"
                name="yield_kg_per_ha"
                value={formData.yield_kg_per_ha}
                onChange={handleInputChange}
                className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none"
                required
              />
            </div>
          </div>

          {/* Pricing & Cost Structures */}
          <div className="space-y-3 pt-4 border-t border-obsidian-800">
            <span className="font-mono text-[11px] text-obsidian-400 font-semibold tracking-technical uppercase block">
              {t("market_rate_standards")}
            </span>

            <div>
              <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                {t("fin_price")}
              </label>
              <input
                type="number"
                step="25"
                name="price_per_quintal"
                value={formData.price_per_quintal}
                onChange={handleInputChange}
                className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none"
                required
              />
            </div>

            <div>
              <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                {t("fin_cost")}
              </label>
              <input
                type="number"
                step="500"
                name="cost_per_ha"
                value={formData.cost_per_ha}
                onChange={handleInputChange}
                className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-3 py-2 font-mono text-xs focus:border-signal-red focus:outline-none"
                required
              />
            </div>
          </div>

          <Button
            type="submit"
            isLoading={mutation.isPending}
            className="w-full py-3.5 flex items-center justify-center gap-2"
          >
            <span>{t("fin_btn")}</span>
            <ArrowRight className="w-4 h-4" />
          </Button>
        </form>

        {/* Results Panel (Right Column, 7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          {mutation.isError && (
            <StatusBanner
              type="error"
              title={t("fin_failed")}
              message={mutation.error.message}
              requestId={mutation.error.requestId}
              onRetry={() => mutation.mutate(formData)}
            />
          )}

          {result ? (
            <div className="space-y-6">
              {/* Primary Profitability Hero Card */}
              <div className="border border-obsidian-800 bg-white p-6 shadow-brutal">
                <div className="flex items-center justify-between border-b border-obsidian-800 pb-3 mb-6">
                  <div>
                    <span className="font-mono text-xs text-obsidian-400 uppercase tracking-widest block mb-0.5">
                      {t("feasibility_summary")} &bull; {result.input_area} {getUnitName(result.input_unit).toUpperCase()}
                    </span>
                    <h2 className="font-display font-black text-2xl sm:text-3xl text-chalk-50 uppercase tracking-tight">
                      {t("net_farm_profit")}
                    </h2>
                  </div>
                  <SignalBadge
                    label={`${result.roi_percent.toFixed(1)}% ROI`}
                    variant={result.roi_percent >= 0 ? "success" : "signal"}
                    size="md"
                  />
                </div>

                {/* Core Financial Hierarchy Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-6">
                  <div className="p-4 bg-obsidian-900 border border-obsidian-800">
                    <span className="font-mono text-[10px] text-obsidian-400 uppercase tracking-technical block mb-1">
                      {t("fin_gross_revenue")}
                    </span>
                    <div className="font-display font-black text-2xl text-chalk-100 tabular-nums">
                      {result.formatted_revenue}
                    </div>
                    <span className="font-mono text-[10px] text-obsidian-400 block mt-1">
                      {result.total_production_quintals.toFixed(1)} {t("q_harvest")}
                    </span>
                  </div>

                  <div className="p-4 bg-obsidian-900 border border-obsidian-800">
                    <span className="font-mono text-[10px] text-obsidian-400 uppercase tracking-technical block mb-1">
                      {t("fin_total_cost")}
                    </span>
                    <div className="font-display font-black text-2xl text-obsidian-300 tabular-nums">
                      {result.formatted_cost}
                    </div>
                    <span className="font-mono text-[10px] text-obsidian-400 block mt-1">
                      {t("comprehensive_c2")}
                    </span>
                  </div>

                  <div className="p-4 bg-obsidian-900 border border-obsidian-800">
                    <span className="font-mono text-[10px] text-obsidian-400 uppercase tracking-technical block mb-1">
                      {t("fin_net_profit")}
                    </span>
                    <div
                      className={`font-display font-black text-2xl tabular-nums ${
                        result.net_profit >= 0 ? "text-signal-green" : "text-signal-error"
                      }`}
                    >
                      {result.formatted_profit}
                    </div>
                    <span className="font-mono text-[10px] text-obsidian-400 block mt-1">
                      {t("margin")}: {result.profit_margin_percent.toFixed(1)}%
                    </span>
                  </div>
                </div>

                {/* Per-Unit Metrics */}
                <div className="grid grid-cols-2 gap-3 pt-4 border-t border-obsidian-800">
                  <MetricCard
                    label={t("profit_per_acre")}
                    value={result.formatted_profit_per_acre}
                    secondary={t("normalized_acreage_income")}
                    variant="dark"
                  />
                  <MetricCard
                    label={t("profit_per_ha")}
                    value={result.formatted_profit_per_ha}
                    secondary={t("standard_metric_realization")}
                    variant="dark"
                  />
                </div>
              </div>

              {/* Revenue vs Cost Comparison Chart */}
              <div className="border border-obsidian-800 bg-white p-6 shadow-brutal space-y-4">
                <div className="flex items-center justify-between border-b border-obsidian-800 pb-3">
                  <h3 className="font-display font-bold text-base sm:text-lg text-chalk-100 uppercase tracking-tight">
                    {t("rev_vs_exp_breakdown")}
                  </h3>
                </div>

                <div className="h-40 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={financialChartData}
                      layout="vertical"
                      margin={{ top: 5, right: 30, left: 50, bottom: 5 }}
                    >
                      <CartesianGrid strokeDasharray="2 2" stroke="#E3E6DF" horizontal={false} />
                      <XAxis
                        type="number"
                        stroke="#E3E6DF"
                        tick={{ fontFamily: "JetBrains Mono", fontSize: 10, fill: "#647568" }}
                        tickFormatter={(val) => `₹${(val / 1000).toFixed(0)}k`}
                      />
                      <YAxis
                        type="category"
                        dataKey="name"
                        stroke="#E3E6DF"
                        tick={{ fontFamily: "JetBrains Mono", fontSize: 11, fill: "#647568" }}
                        width={130}
                      />
                      <Tooltip
                        formatter={(val: number) => [`₹${val.toLocaleString()}`, t("amount_label")]}
                        contentStyle={{
                          backgroundColor: "#FFFFFF",
                          color: "#202820",
                          border: "1px solid #E3E6DF",
                          borderRadius: 0,
                          fontFamily: "JetBrains Mono",
                          fontSize: 12,
                        }}
                      />
                      <Bar dataKey="amount" name={`${t("amount_label")} (₹)`}>
                        {financialChartData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.fill} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Break-Even Critical Risk Boundaries */}
              <div className="border border-obsidian-800 bg-white p-6 shadow-brutal space-y-4">
                <div className="flex items-center justify-between border-b border-obsidian-800 pb-3">
                  <div className="font-mono text-xs font-bold uppercase tracking-technical text-chalk-100 flex items-center gap-2">
                    <Sliders className="w-4 h-4 text-signal-red" />
                    <span>{t("critical_breakeven_thresholds")}</span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 font-mono text-xs">
                  <div className="p-3 bg-obsidian-900 border border-obsidian-800">
                    <span className="text-[10px] text-obsidian-400 uppercase tracking-widest block mb-1">
                      {t("fin_breakeven_yield")} (kg/ha)
                    </span>
                    <div className="font-display font-black text-2xl text-chalk-100 tabular-nums">
                      {Math.round(result.breakeven_yield_kg_per_ha).toLocaleString()}
                    </div>
                    <span className="text-[10px] text-obsidian-400 block mt-1">
                      {t("min_harvest_operational_costs")}
                    </span>
                  </div>

                  <div className="p-3 bg-obsidian-900 border border-obsidian-800">
                    <span className="text-[10px] text-obsidian-400 uppercase tracking-widest block mb-1">
                      {t("fin_breakeven_price")} (₹/Q)
                    </span>
                    <div className="font-display font-black text-2xl text-chalk-100 tabular-nums">
                      ₹{Math.round(result.breakeven_price_per_quintal).toLocaleString()}
                    </div>
                    <span className="text-[10px] text-obsidian-400 block mt-1">
                      {t("floor_market_price")}
                    </span>
                  </div>
                </div>

                <div className="pt-3 border-t border-obsidian-800 flex items-center justify-between text-[11px] font-mono text-obsidian-400">
                  <span>{t("cacp_methodology_standards")}</span>
                  <Link
                    to="/advisory"
                    state={{
                      crop: lookupCrop,
                      state: lookupState,
                      farm_area: formData.farm_area,
                      area_unit: formData.area_unit,
                      fromFinancials: true,
                    }}
                    className="text-signal-red font-bold hover:underline flex items-center gap-1 uppercase"
                  >
                    {t("generate_full_advisory_link")} <ArrowUpRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            </div>
          ) : (
            <div className="border border-dashed border-obsidian-750 p-12 text-center space-y-3 bg-white">
              <h2 className="font-display font-bold text-lg sm:text-xl text-chalk-100 uppercase">
                {t("awaiting_fin_title")}
              </h2>
              <p className="font-sans text-xs text-obsidian-400 max-w-md mx-auto">
                {t("awaiting_fin_desc")}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Stress & Risk Sensitivity Analysis */}
      <StressSimulator
        crop={lookupCrop}
        state={lookupState}
        farm_area={formData.farm_area}
        area_unit={formData.area_unit}
        base_rainfall_mm={800}
        base_price_per_quintal={formData.price_per_quintal ?? 2250}
        base_cost_per_ha={formData.cost_per_ha ?? 38000}
      />
    </div>
  );
};
