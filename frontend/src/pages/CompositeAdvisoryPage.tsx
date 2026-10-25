import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
  ArrowRight,
  Printer,
  Sliders,
  DollarSign,
  TrendingUp,
  Database,
  Sprout,
  ShieldCheck,
} from "lucide-react";
import { api, ApiError } from "../api/client";
import { FullAdvisoryRequest, FullAdvisoryResponse } from "../types/api";
import { Button } from "../components/ui/Button";
import { SignalBadge } from "../components/visual/SignalBadge";
import { MetricCard } from "../components/ui/MetricCard";
import { StatusBanner } from "../components/ui/StatusBanner";
import { GeoSensingBanner } from "../components/GeoSensingBanner";
import { useLanguage } from "../context/LanguageContext";

const SEASONS = ["Kharif", "Rabi", "Whole Year", "Summer", "Autumn", "Winter"];
const SOIL_TYPES = [
  "Vertisols",
  "Inceptisols",
  "Alfisols",
  "Entisols",
  "Aridisols",
  "Mollisols",
];

interface AdvLocationState {
  crop?: string;
  state?: string;
  farm_area?: number;
  area_unit?: "acre" | "hectare" | "bigha";
  fromFinancials?: boolean;
}

export const CompositeAdvisoryPage: React.FC = () => {
  const {
    t,
    getCropName,
    getCategoryName,
    getSeasonName,
    getSoilName,
    getStateName,
    getUnitName,
  } = useLanguage();

  const location = useLocation();
  const locationState = location.state as AdvLocationState | null;

  const [formData, setFormData] = useState<FullAdvisoryRequest>({
    n: 90.0,
    p: 42.0,
    k: 43.0,
    temperature: 21.0,
    humidity: 82.0,
    ph: 6.5,
    rainfall: 202.0,
    state: "Maharashtra",
    soil_type: "Vertisols",
    season: "Kharif",
    farm_area: 3.0,
    area_unit: "acre",
    top_k: 3,
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

    setFormData((prev) => ({
      ...prev,
      state: locationState.state || prev.state,
      farm_area: locationState.farm_area ?? prev.farm_area,
      area_unit: locationState.area_unit ?? prev.area_unit,
    }));
  }, [locationState]);

  const mutation = useMutation<
    FullAdvisoryResponse,
    ApiError,
    FullAdvisoryRequest
  >({
    mutationFn: api.getFullAdvisory,
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

  const handlePrint = () => {
    window.print();
  };

  const report = mutation.data;

  return (
    <div className="space-y-12">
      {/* Title Header */}
      <div className="border-b border-obsidian-750 pb-6 flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="font-display font-black text-3xl sm:text-4xl lg:text-5xl tracking-tight text-chalk-50 uppercase">
            {t("adv_page_title")}
          </h1>
          <p className="font-sans text-xs sm:text-sm text-obsidian-300 mt-1 max-w-2xl leading-relaxed">
            {t("adv_page_desc")}
          </p>
        </div>

        {report && (
          <Button
            type="button"
            variant="secondary"
            onClick={handlePrint}
            className="flex items-center gap-2 shrink-0 print:hidden"
          >
            <Printer className="w-4 h-4" />
            <span>{t("adv_print")}</span>
          </Button>
        )}
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Farm & Environmental Parameters (Left Column, 4 cols) */}
        <form
          onSubmit={handleSubmit}
          className="lg:col-span-4 border border-obsidian-750 bg-obsidian-950 p-6 shadow-brutal space-y-5 print:hidden"
        >
          <div className="flex items-center justify-between border-b border-obsidian-800 pb-3">
            <span className="font-mono text-xs font-bold uppercase tracking-technical text-chalk-100 flex items-center gap-2">
              <Sliders className="w-3.5 h-3.5 text-signal-red" />
              {t("comprehensive_inputs")}
            </span>
          </div>

          <GeoSensingBanner onAutoFill={handleGeoAutoFill} />

          {/* Retention Notification */}
          {locationState?.fromFinancials && (
            <div className="p-3 bg-obsidian-900 border border-signal-red/60 text-xs font-mono text-chalk-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2 shadow-brutal-sm">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-signal-red shrink-0 animate-pulse" />
                <span>
                  {t("retained_from_fin")}:{" "}
                  <strong className="text-white">{formData.farm_area} {getUnitName(formData.area_unit || "acre")}</strong> ({getStateName(formData.state || "Maharashtra")})
                </span>
              </div>
            </div>
          )}

          {/* Regional Settings */}
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  {t("yield_state_label")}
                </label>
                <select
                  name="state"
                  value={formData.state}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-2.5 py-1.5 font-mono text-xs focus:border-signal-red focus:outline-none uppercase"
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
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-2.5 py-1.5 font-mono text-xs focus:border-signal-red focus:outline-none uppercase"
                >
                  {SEASONS.map((s) => (
                    <option key={s} value={s}>
                      {getSeasonName(s) || s}
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
                className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-2.5 py-1.5 font-mono text-xs focus:border-signal-red focus:outline-none uppercase"
              >
                {SOIL_TYPES.map((st) => (
                  <option key={st} value={st}>
                    {getSoilName(st) || st}
                  </option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                  {t("fin_farm_area")}
                </label>
                <input
                  type="number"
                  step="0.5"
                  min="0.5"
                  name="farm_area"
                  value={formData.farm_area}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-2.5 py-1.5 font-mono text-xs focus:border-signal-red focus:outline-none"
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
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-2.5 py-1.5 font-mono text-xs focus:border-signal-red focus:outline-none uppercase"
                >
                  <option value="acre">{getUnitName("acre")}</option>
                  <option value="hectare">{getUnitName("hectare")}</option>
                  <option value="bigha">{getUnitName("bigha")}</option>
                </select>
              </div>
            </div>
          </div>

          {/* Soil Chemistry (NPK) */}
          <div className="space-y-3 pt-3 border-t border-obsidian-800">
            <span className="font-mono text-[10px] text-obsidian-400 font-semibold tracking-technical uppercase block">
              {t("soil_chemistry_title")}
            </span>

            <div className="grid grid-cols-3 gap-2">
              <div>
                <label className="block font-mono text-[9px] uppercase text-obsidian-400 mb-1">
                  {t("nitrogen_label")}
                </label>
                <input
                  type="number"
                  name="n"
                  value={formData.n}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-2 py-1 font-mono text-xs focus:border-signal-red focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block font-mono text-[9px] uppercase text-obsidian-400 mb-1">
                  {t("phosphorus_label")}
                </label>
                <input
                  type="number"
                  name="p"
                  value={formData.p}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-2 py-1 font-mono text-xs focus:border-signal-red focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block font-mono text-[9px] uppercase text-obsidian-400 mb-1">
                  {t("potassium_label")}
                </label>
                <input
                  type="number"
                  name="k"
                  value={formData.k}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-2 py-1 font-mono text-xs focus:border-signal-red focus:outline-none"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block font-mono text-[10px] uppercase text-obsidian-300 mb-1">
                {t("soil_reaction")}
              </label>
              <input
                type="number"
                step="0.1"
                name="ph"
                value={formData.ph}
                onChange={handleInputChange}
                className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-2.5 py-1.5 font-mono text-xs focus:border-signal-red focus:outline-none"
                required
              />
            </div>
          </div>

          {/* Microclimate */}
          <div className="space-y-3 pt-3 border-t border-obsidian-800">
            <span className="font-mono text-[10px] text-obsidian-400 font-semibold tracking-technical uppercase block">
              {t("climatic_metrics")}
            </span>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block font-mono text-[9px] uppercase text-obsidian-400 mb-1">
                  {t("temp_label")}
                </label>
                <input
                  type="number"
                  step="0.5"
                  name="temperature"
                  value={formData.temperature}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-2 py-1 font-mono text-xs focus:border-signal-red focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block font-mono text-[9px] uppercase text-obsidian-400 mb-1">
                  {t("rainfall_label")}
                </label>
                <input
                  type="number"
                  step="10"
                  name="rainfall"
                  value={formData.rainfall}
                  onChange={handleInputChange}
                  className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 px-2 py-1 font-mono text-xs focus:border-signal-red focus:outline-none"
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
            <span>{t("adv_btn")}</span>
            <ArrowRight className="w-4 h-4" />
          </Button>
        </form>

        {/* Advisory Dossier (Right Column, 8 cols) */}
        <div className="lg:col-span-8 space-y-6">
          {mutation.isError && (
            <StatusBanner
              type="error"
              title={t("adv_failed")}
              message={mutation.error.message}
              requestId={mutation.error.requestId}
              onRetry={() => mutation.mutate(formData)}
            />
          )}

          {report ? (
            <div className="space-y-6">
              {/* Section 1: Recommended Primary Crop */}
              <div className="border border-obsidian-750 bg-obsidian-950 p-6 shadow-brutal">
                <div className="flex items-center justify-between border-b border-obsidian-800 pb-3 mb-4">
                  <div className="flex items-center gap-2">
                    <Sprout className="w-4 h-4 text-signal-red" />
                    <span className="font-mono text-xs font-bold uppercase tracking-technical text-signal-red">
                      {t("crop_recommendation_tag")}
                    </span>
                  </div>
                  <SignalBadge
                    label={`${report.recommendation.confidence_percent.toFixed(1)}% ${t("match_badge")}`}
                    variant="signal"
                    size="sm"
                  />
                </div>

                <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2">
                  <div>
                    <span className="font-mono text-xs text-obsidian-400 uppercase tracking-widest block">
                      {getCategoryName(report.recommendation.category)}
                    </span>
                    <h2 className="font-display font-black text-3xl sm:text-4xl lg:text-5xl text-chalk-50 tracking-tight uppercase">
                      {getCropName(report.recommendation.display_name) || report.recommendation.display_name}
                    </h2>
                  </div>
                </div>

                <p className="font-sans text-xs sm:text-sm text-obsidian-300 mt-2 leading-relaxed">
                  {report.recommendation.description}
                </p>
              </div>

              {/* Section 2 & 3: Yield Projection & Mandi Intelligence Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {/* Yield Forecast */}
                <div className="border border-obsidian-750 bg-obsidian-950 p-5 shadow-brutal space-y-3">
                  <div className="flex items-center justify-between border-b border-obsidian-800 pb-2">
                    <div className="flex items-center gap-1.5 font-mono text-xs font-bold text-chalk-100 uppercase">
                      <TrendingUp className="w-3.5 h-3.5 text-signal-red" />
                      <span>{t("projected_yield_title")}</span>
                    </div>
                  </div>

                  <div className="space-y-1">
                    <span className="font-mono text-[10px] text-obsidian-400 uppercase">
                      {t("metric_density")}
                    </span>
                    <div className="font-display font-black text-2xl text-chalk-100 tabular-nums">
                      {report.yield_prediction.predicted_yield_kg_ha.toLocaleString()}{" "}
                      <span className="text-xs font-mono text-obsidian-400">KG/HA</span>
                    </div>
                  </div>

                  <div className="pt-2 border-t border-obsidian-800 text-xs font-mono text-obsidian-300">
                    <span>{t("farm_standard")} </span>
                    <strong className="text-chalk-100">
                      {report.yield_prediction.predicted_yield_quintals_acre.toFixed(2)} Q/{getUnitName("acre")}
                    </strong>
                  </div>
                </div>

                {/* Mandi Price */}
                <div className="border border-obsidian-750 bg-obsidian-950 p-5 shadow-brutal space-y-3">
                  <div className="flex items-center justify-between border-b border-obsidian-800 pb-2">
                    <div className="flex items-center gap-1.5 font-mono text-xs font-bold text-chalk-100 uppercase">
                      <Database className="w-3.5 h-3.5 text-signal-red" />
                      <span>{t("mandi_wholesale_price")}</span>
                    </div>
                  </div>

                  <div className="space-y-1">
                    <span className="font-mono text-[10px] text-obsidian-400 uppercase">
                      {t("modal_wholesale_rate")}
                    </span>
                    <div className="font-display font-black text-2xl text-chalk-100 tabular-nums">
                      ₹{report.market_price.modal_rs_per_quintal.toLocaleString()}{" "}
                      <span className="text-xs font-mono text-obsidian-400">/ Q</span>
                    </div>
                  </div>

                  <div className="pt-2 border-t border-obsidian-800 text-xs font-mono flex items-center justify-between">
                    <span className="text-obsidian-400">₹{report.market_price.price_per_kg.toFixed(2)} / kg</span>
                    {report.market_price.msp_rs_per_quintal && (
                      <span className="inline-flex items-center gap-1 text-emerald-400 text-[10px]">
                        <ShieldCheck className="w-3 h-3" />
                        {t("msp_label")} ₹{report.market_price.msp_rs_per_quintal.toLocaleString()}
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* Section 4: Comprehensive C2 Cultivation Cost Breakdown */}
              <div className="border border-obsidian-750 bg-obsidian-950 p-5 shadow-brutal space-y-3">
                <div className="flex items-center justify-between border-b border-obsidian-800 pb-2">
                  <div className="flex items-center gap-1.5 font-mono text-xs font-bold text-chalk-100 uppercase">
                    <DollarSign className="w-3.5 h-3.5 text-signal-red" />
                    <span>{t("cultivation_expenditure_breakdown")}</span>
                  </div>
                  <span className="font-mono text-[10px] text-obsidian-400">
                    {t("state_applied")} {getStateName(report.cultivation_cost.applied_state) || report.cultivation_cost.applied_state}
                  </span>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 font-mono text-xs">
                  <div className="p-2.5 bg-obsidian-900 border border-obsidian-800">
                    <span className="text-[10px] text-obsidian-400 uppercase block mb-0.5">{t("cost_seed")}</span>
                    <span className="font-bold text-chalk-200">₹{Math.round(report.cultivation_cost.seed_cost_per_ha).toLocaleString()}</span>
                  </div>
                  <div className="p-2.5 bg-obsidian-900 border border-obsidian-800">
                    <span className="text-[10px] text-obsidian-400 uppercase block mb-0.5">{t("cost_fertilizer")}</span>
                    <span className="font-bold text-chalk-200">₹{Math.round(report.cultivation_cost.fertilizer_cost_per_ha).toLocaleString()}</span>
                  </div>
                  <div className="p-2.5 bg-obsidian-900 border border-obsidian-800">
                    <span className="text-[10px] text-obsidian-400 uppercase block mb-0.5">{t("cost_labor")}</span>
                    <span className="font-bold text-chalk-200">₹{Math.round(report.cultivation_cost.labor_cost_per_ha).toLocaleString()}</span>
                  </div>
                  <div className="p-2.5 bg-obsidian-900 border border-obsidian-800">
                    <span className="text-[10px] text-obsidian-400 uppercase block mb-0.5">{t("cost_machinery")}</span>
                    <span className="font-bold text-chalk-200">₹{Math.round(report.cultivation_cost.machinery_cost_per_ha).toLocaleString()}</span>
                  </div>
                </div>

                <div className="pt-2 border-t border-obsidian-800 flex items-center justify-between font-mono text-xs text-obsidian-300">
                  <span>{t("total_cost_per_ha")}</span>
                  <strong className="text-chalk-100 font-display font-black text-sm">
                    ₹{report.cultivation_cost.cul_cost_c2_per_ha.toLocaleString()} / ha
                  </strong>
                </div>
              </div>

              {/* Section 5: Farm Financial Feasibility Summary */}
              <div className="border border-obsidian-750 bg-obsidian-950 p-6 shadow-brutal space-y-4">
                <div className="flex items-center justify-between border-b border-obsidian-800 pb-3">
                  <span className="font-mono text-xs font-bold uppercase tracking-technical text-chalk-100">
                    {t("farm_profitability_roi")}
                  </span>
                  <SignalBadge
                    label={`${report.financials.roi_percent.toFixed(1)}% ROI`}
                    variant={report.financials.roi_percent >= 0 ? "success" : "signal"}
                    size="sm"
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <MetricCard
                    label={t("fin_gross_revenue")}
                    value={report.financials.formatted_revenue}
                    secondary={`${t("total_harvest_label")} ${report.financials.total_production_quintals.toFixed(1)} Q`}
                    variant="dark"
                  />
                  <MetricCard
                    label={t("fin_total_cost")}
                    value={report.financials.formatted_cost}
                    secondary={`${t("acre_cost_label")} ₹${Math.round(report.financials.cost_per_acre).toLocaleString()}`}
                    variant="dark"
                  />
                  <MetricCard
                    label={t("fin_net_profit")}
                    value={report.financials.formatted_profit}
                    secondary={`${t("profit_label")} ${report.financials.formatted_profit_per_acre} / ${getUnitName("acre")}`}
                    variant={report.financials.net_profit >= 0 ? "dark" : "signal"}
                  />
                </div>
              </div>
            </div>
          ) : (
            <div className="border border-dashed border-obsidian-750 p-12 text-center space-y-3 bg-obsidian-950">
              <h2 className="font-display font-bold text-lg sm:text-xl text-chalk-100 uppercase">
                {t("awaiting_adv_title")}
              </h2>
              <p className="font-sans text-xs text-obsidian-400 max-w-md mx-auto">
                {t("awaiting_adv_desc")}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
