import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { ArrowRight, BarChart3, CheckCircle2 } from "lucide-react";
import { api } from "../api/client";
import { MetricCard } from "../components/ui/MetricCard";
import { AgroSystemVisual } from "../components/visual/AgroSystemVisual";
import { KarpoLens } from "../components/KarpoLens";
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

export const OverviewPage: React.FC = () => {
  const { t, getCropName, getCategoryName, getSeasonName } = useLanguage();
  const [selectedCropCategory, setSelectedCropCategory] = useState<string>("ALL");

  const { data: health } = useQuery({
    queryKey: ["healthReady"],
    queryFn: api.getHealthReady,
  });

  const { data: supportedCrops = [] } = useQuery({
    queryKey: ["supportedCrops"],
    queryFn: api.getSupportedCrops,
  });

  const { data: yieldBenchmarks = [] } = useQuery({
    queryKey: ["yieldBenchmarks"],
    queryFn: api.getYieldBenchmarks,
  });

  const categories = [
    "ALL",
    ...Array.from(new Set(supportedCrops.map((c) => c.category))),
  ];

  const filteredCrops =
    selectedCropCategory === "ALL"
      ? supportedCrops
      : supportedCrops.filter((c) => c.category === selectedCropCategory);

  const [selectedBenchmarkCategory, setSelectedBenchmarkCategory] = useState<string>("Cereals & Grains");
  const [selectedYieldUnit, setSelectedYieldUnit] = useState<"kg/ha" | "Q/ha">("kg/ha");

  const benchmarkCropMetadata: Record<string, { category: string; isBiomass?: boolean; notes?: string }> = {
    "Rice": { category: "Cereals & Grains" },
    "Wheat": { category: "Cereals & Grains" },
    "Maize": { category: "Cereals & Grains" },
    "Barley": { category: "Cereals & Grains" },
    "Pearl Millet": { category: "Cereals & Grains" },
    "Sorghum (Kharif)": { category: "Cereals & Grains" },
    "Chickpea": { category: "Pulses & Legumes" },
    "Pigeonpea": { category: "Pulses & Legumes" },
    "Minor Pulses": { category: "Pulses & Legumes" },
    "Groundnut": { category: "Oilseeds" },
    "Soybean": { category: "Oilseeds" },
    "Sunflower": { category: "Oilseeds" },
    "Sesamum": { category: "Oilseeds" },
    "Cotton": { category: "Commercial & Fibre", notes: "Seed cotton / lint yield" },
    "Sugarcane": { category: "Commercial & Fibre", isBiomass: true, notes: "Fresh millable stalk biomass (~55 t/ha)" },
  };

  const benchmarkCategories = [
    "Cereals & Grains",
    "Pulses & Legumes",
    "Oilseeds",
    "Commercial & Fibre",
    "All Crops",
  ];

  const filteredBenchmarks = yieldBenchmarks.filter((b) => {
    if (selectedBenchmarkCategory === "All Crops") return true;
    const meta = benchmarkCropMetadata[b.crop];
    return meta?.category === selectedBenchmarkCategory;
  });

  const isQha = selectedYieldUnit === "Q/ha";

  const benchmarkChartData = filteredBenchmarks.map((b) => {
    const meta = benchmarkCropMetadata[b.crop];
    const shortName = b.crop === "Sorghum (Kharif)" ? "Sorghum" : b.crop;
    const medianVal = isQha
      ? Math.round(b.median_kg_ha * 0.01 * 10) / 10
      : Math.round(b.median_kg_ha);
    const minVal = isQha
      ? Math.round(b.min_kg_ha * 0.01 * 10) / 10
      : Math.round(b.min_kg_ha);
    const maxVal = isQha
      ? Math.round(b.max_kg_ha * 0.01 * 10) / 10
      : Math.round(b.max_kg_ha);

    return {
      name: shortName,
      fullName: b.crop,
      localizedName: getCropName(b.crop),
      median: medianVal,
      min: minVal,
      max: maxVal,
      rawMedianKg: Math.round(b.median_kg_ha),
      category: meta?.category ?? "Field Crop",
      isBiomass: meta?.isBiomass ?? false,
      notes: meta?.notes,
    };
  });

  const maxBenchmark = Math.max(...benchmarkChartData.map((d) => d.median), 0);
  const containsBiomass = benchmarkChartData.some((d) => d.isBiomass);

  return (
    <div className="space-y-16">
      {/* 1. Concise Editorial Hero */}
      <section className="border-b border-obsidian-750 pb-12 sm:pb-16">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
          {/* Left Column (7 cols): Clean Headline, Concise Text, Actions */}
          <div className="lg:col-span-7 space-y-6">
            <div className="space-y-3">
              <span className="font-mono text-xs text-signal-red uppercase font-semibold tracking-technical">
                {t("brand_sub")}
              </span>

              {/* Memorable Headline */}
              <h1 className="font-display font-black text-3xl sm:text-5xl lg:text-6xl tracking-tight text-chalk-50 leading-[0.98] uppercase">
                {t("hero_headline")}
              </h1>

              {/* Concise Supporting Copy */}
              <p className="font-sans text-sm sm:text-base text-obsidian-300 leading-relaxed max-w-xl">
                {t("hero_subheadline")}
              </p>
            </div>

            {/* Clear Product Actions */}
            <div className="flex flex-col sm:flex-row gap-3 pt-2">
              <Link
                to="/recommend"
                className="px-6 py-3.5 bg-signal-red text-white hover:bg-signal-darkred border border-signal-red shadow-brutal flex items-center justify-center gap-3 font-mono text-xs font-bold tracking-technical uppercase transition-all duration-150 group"
              >
                <span>{t("explore_crop_rec")}</span>
                <ArrowRight className="w-4 h-4 shrink-0 group-hover:translate-x-1 transition-transform" />
              </Link>

              <Link
                to="/advisory"
                className="px-6 py-3.5 bg-obsidian-850 text-chalk-100 hover:bg-obsidian-800 hover:text-white border border-obsidian-700 shadow-brutal flex items-center justify-center gap-3 font-mono text-xs font-bold tracking-technical uppercase transition-all duration-150"
              >
                <span>{t("view_full_advisory")}</span>
              </Link>
            </div>
          </div>

          {/* Right Column (5 cols): Defined Topographic Scientific Visual */}
          <div className="lg:col-span-5">
            <AgroSystemVisual />
          </div>
        </div>
      </section>

      {/* 2. Core Agricultural Data Metrics */}
      <section className="space-y-4">
        <div className="flex items-center justify-between border-b border-obsidian-800 pb-2 font-mono text-xs text-obsidian-400">
          <span className="font-bold uppercase tracking-technical text-chalk-200">
            {t("system_inventory")}
          </span>
          <span className="text-[11px] text-obsidian-400">
            {t("official_datasets")}
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            label={t("supported_crops")}
            value={supportedCrops.length > 0 ? supportedCrops.length : 22}
            unit={t("species_unit")}
            secondary={t("across_categories")}
            variant="dark"
          />
          <MetricCard
            label={t("mandi_coverage")}
            value={health?.details?.datasets?.prices_count ?? 122}
            unit={t("commodities_unit")}
            secondary={t("mandi_sub")}
            variant="dark"
          />
          <MetricCard
            label={t("cost_benchmarks")}
            value={health?.details?.datasets?.cost_records_count ?? 3880}
            unit={t("records_unit")}
            secondary={t("cacp_sub")}
            variant="dark"
          />
          <MetricCard
            label={t("historical_harvests")}
            value="198,369"
            unit={t("surveys_unit")}
            secondary={t("yield_sub")}
            variant="dark"
          />
        </div>
      </section>

      {/* 3. Scientific Yield Reference & Core Capabilities */}
      <section className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column (7 cols): Historical Yield Reference Chart */}
        <div className="lg:col-span-7 border border-obsidian-750 bg-obsidian-950 p-6 shadow-brutal flex flex-col justify-between">
          <div>
            <div className="flex flex-col gap-3 border-b border-obsidian-800 pb-4 mb-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <BarChart3 className="w-4 h-4 text-signal-red" />
                    <h2 className="font-display font-bold text-lg text-chalk-100 uppercase tracking-tight">
                      {t("benchmarks_heading")}
                    </h2>
                  </div>
                  <p className="font-mono text-xs text-obsidian-400">
                    {t("benchmarks_sub")} ({selectedYieldUnit})
                  </p>
                </div>

                {/* Unit Switcher */}
                <div className="flex items-center border border-obsidian-750 bg-obsidian-900 p-0.5 self-start sm:self-auto shrink-0">
                  <button
                    type="button"
                    onClick={() => setSelectedYieldUnit("kg/ha")}
                    className={`px-2 py-1 font-mono text-[10px] uppercase tracking-technical transition-colors ${
                      selectedYieldUnit === "kg/ha"
                        ? "bg-signal-red text-white font-bold"
                        : "text-obsidian-400 hover:text-chalk-100"
                    }`}
                  >
                    kg / ha
                  </button>
                  <button
                    type="button"
                    onClick={() => setSelectedYieldUnit("Q/ha")}
                    className={`px-2 py-1 font-mono text-[10px] uppercase tracking-technical transition-colors ${
                      selectedYieldUnit === "Q/ha"
                        ? "bg-signal-red text-white font-bold"
                        : "text-obsidian-400 hover:text-chalk-100"
                    }`}
                  >
                    Q / ha
                  </button>
                </div>
              </div>

              {/* Category Segment Tabs */}
              <div className="flex flex-wrap gap-1 pt-1">
                {benchmarkCategories.map((cat) => (
                  <button
                    key={cat}
                    type="button"
                    onClick={() => setSelectedBenchmarkCategory(cat)}
                    className={`px-2.5 py-1 font-mono text-[10px] sm:text-[11px] uppercase tracking-technical border transition-colors ${
                      selectedBenchmarkCategory === cat
                        ? "bg-signal-red text-white border-signal-red font-bold"
                        : "bg-obsidian-900 text-obsidian-400 border-obsidian-750 hover:bg-obsidian-850 hover:text-chalk-100"
                    }`}
                  >
                    {getCategoryName(cat)}
                  </button>
                ))}
              </div>
            </div>

            <div className="h-64 sm:h-72 w-full">
              {benchmarkChartData.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={benchmarkChartData}
                    margin={{ top: 15, right: 15, left: 10, bottom: 40 }}
                  >
                    <CartesianGrid strokeDasharray="2 2" stroke="#1D222E" vertical={false} />
                    <XAxis
                      dataKey="name"
                      stroke="#414A60"
                      tick={{ fontFamily: "JetBrains Mono", fontSize: 11, fill: "#AEBAD1" }}
                      interval={0}
                      angle={-20}
                      textAnchor="end"
                      height={45}
                      tickFormatter={(val) => getCropName(val)}
                    />
                    <YAxis
                      stroke="#414A60"
                      width={65}
                      tick={{ fontFamily: "JetBrains Mono", fontSize: 11, fill: "#8694B0" }}
                      tickFormatter={(v) => {
                        if (selectedYieldUnit === "Q/ha") {
                          return `${v} Q`;
                        }
                        return v >= 1000 ? `${Math.round(v / 1000)}k kg` : `${v} kg`;
                      }}
                    />
                    <Tooltip
                      cursor={{ fill: "rgba(255, 42, 42, 0.05)" }}
                      content={({ active, payload }) => {
                        if (!active || !payload || !payload.length) return null;
                        const item = payload[0].payload;
                        return (
                          <div className="bg-obsidian-950 border border-obsidian-700 p-3 shadow-brutal font-mono text-xs space-y-1.5 min-w-[210px]">
                            <div className="font-bold text-chalk-100 flex items-center justify-between border-b border-obsidian-800 pb-1">
                              <span>{item.localizedName ?? item.name}</span>
                              <span className="text-[10px] text-signal-red uppercase font-semibold">
                                {getCategoryName(item.category)}
                              </span>
                            </div>
                            <div className="text-chalk-200 flex justify-between">
                              <span className="text-obsidian-400">{t("median_harvest")}</span>
                              <span className="font-bold text-signal-red">
                                {item.median.toLocaleString()} {selectedYieldUnit}
                              </span>
                            </div>
                            <div className="text-obsidian-300 text-[11px] flex justify-between">
                              <span className="text-obsidian-400">{t("historical_range")}</span>
                              <span>
                                {item.min.toLocaleString()} – {item.max.toLocaleString()} {selectedYieldUnit}
                              </span>
                            </div>
                            {item.notes && (
                              <div className="text-[10px] text-signal-red border-t border-obsidian-800 pt-1 mt-1 leading-snug">
                                * {item.notes}
                              </div>
                            )}
                          </div>
                        );
                      }}
                    />
                    <Bar dataKey="median" name="Median Yield">
                      {benchmarkChartData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={entry.median === maxBenchmark ? "#FF2A2A" : "#262C3A"}
                          stroke={entry.median === maxBenchmark ? "#FF2A2A" : "#414A60"}
                          className="transition-colors duration-150 hover:opacity-85"
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex items-center justify-center font-mono text-xs text-obsidian-400">
                  No benchmarks available for this category.
                </div>
              )}
            </div>

            {containsBiomass && (
              <div className="mt-3 px-3 py-2 bg-obsidian-900 border-l-2 border-signal-red text-[11px] font-mono text-obsidian-300 leading-snug">
                <span className="text-signal-red font-bold mr-1">AGRONOMIC NOTE:</span>
                Sugarcane yields reflect fresh wet millable stalk biomass (~55,000 kg/ha or 550 Q/ha), whereas grain, pulse, and oilseed crops reflect dry harvest (0.5–2 tonnes/ha).
              </div>
            )}
          </div>

          <div className="mt-4 pt-3 border-t border-obsidian-800 flex flex-wrap items-center justify-between gap-3 text-[11px] font-mono text-obsidian-400">
            <span>{t("source_des")}</span>
            <Link
              to="/yield"
              className="text-signal-red font-semibold hover:underline flex items-center gap-1 uppercase"
            >
              {t("forecast_yield_btn")} <ArrowRight className="w-3 h-3" />
            </Link>
          </div>
        </div>

        {/* Right Column (5 cols): Agricultural Capabilities */}
        <div className="lg:col-span-5 border border-obsidian-750 bg-obsidian-850 p-6 divide-y divide-obsidian-800">
          <div className="pb-4">
            <h2 className="font-display font-bold text-lg text-chalk-100 uppercase tracking-tight mb-1">
              {t("core_capabilities")}
            </h2>
            <p className="font-sans text-xs text-obsidian-300">
              {t("integrated_tools")}
            </p>
          </div>

          <div className="py-4 space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="font-mono font-bold text-xs uppercase text-chalk-100">
                {t("suitability_title")}
              </span>
              <Link to="/recommend" className="text-signal-red font-mono text-[11px] hover:underline">
                {t("explore_arrow")}
              </Link>
            </div>
            <p className="font-sans text-xs text-obsidian-300 leading-relaxed">
              {t("suitability_desc")}
            </p>
          </div>

          <div className="py-4 space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="font-mono font-bold text-xs uppercase text-chalk-100">
                {t("yield_forecasting_title")}
              </span>
              <Link to="/yield" className="text-signal-red font-mono text-[11px] hover:underline">
                {t("explore_arrow")}
              </Link>
            </div>
            <p className="font-sans text-xs text-obsidian-300 leading-relaxed">
              {t("yield_forecasting_desc")}
            </p>
          </div>

          <div className="py-4 space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="font-mono font-bold text-xs uppercase text-chalk-100">
                {t("mandi_intel_title")}
              </span>
              <Link to="/market" className="text-signal-red font-mono text-[11px] hover:underline">
                {t("explore_arrow")}
              </Link>
            </div>
            <p className="font-sans text-xs text-obsidian-300 leading-relaxed">
              {t("mandi_intel_desc")}
            </p>
          </div>

          <div className="pt-4 space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="font-mono font-bold text-xs uppercase text-chalk-100">
                {t("farm_econ_title")}
              </span>
              <Link to="/financials" className="text-signal-red font-mono text-[11px] hover:underline">
                {t("explore_arrow")}
              </Link>
            </div>
            <p className="font-sans text-xs text-obsidian-300 leading-relaxed">
              {t("farm_econ_desc")}
            </p>
          </div>
        </div>
      </section>

      {/* 4. Karpo Lens: Field Crop Disease Assistance */}
      <KarpoLens />

      {/* 5. Supported Agronomic Taxonomy */}
      <section className="border border-obsidian-750 bg-obsidian-950 p-6 shadow-brutal">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-obsidian-800 pb-4 mb-6">
          <div>
            <h2 className="font-display font-bold text-xl text-chalk-100 uppercase tracking-tight">
              {t("supported_crops_heading")}
            </h2>
            <p className="font-sans text-xs text-obsidian-400 mt-0.5">
              {t("supported_crops_sub")}
            </p>
          </div>

          {/* Category Filter Tabs */}
          <div className="flex flex-wrap gap-1">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCropCategory(cat)}
                className={`px-2.5 py-1 font-mono text-[11px] uppercase tracking-technical border transition-colors ${
                  selectedCropCategory === cat
                    ? "bg-signal-red text-white border-signal-red font-bold"
                    : "bg-obsidian-900 text-obsidian-400 border-obsidian-750 hover:bg-obsidian-850 hover:text-chalk-100"
                }`}
              >
                {getCategoryName(cat)}
              </button>
            ))}
          </div>
        </div>

        {/* Crops Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
          {filteredCrops.map((crop) => (
            <Link
              key={crop.canonical_name}
              to="/yield"
              state={{ crop: crop.canonical_name }}
              className="p-3 border border-obsidian-800 bg-obsidian-900 hover:border-signal-red hover:bg-obsidian-850 transition-all duration-150 flex flex-col justify-between group cursor-pointer"
            >
              <div>
                <span className="font-mono text-[9px] text-obsidian-400 uppercase tracking-widest block mb-1">
                  {getCategoryName(crop.category)}
                </span>
                <div className="font-display font-bold text-sm text-chalk-100 group-hover:text-white uppercase tracking-tight">
                  {getCropName(crop.display_name)}
                </div>
              </div>

              <div className="mt-3 pt-2 border-t border-obsidian-800 flex items-center justify-between font-mono text-[10px] text-obsidian-400">
                <span>{getSeasonName(crop.default_season)}</span>
                <CheckCircle2 className="w-3 h-3 text-signal-green shrink-0" />
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
};
