import React, { useState } from "react";
import { Printer, Share2, Check, ShieldCheck, Sprout, TrendingUp, DollarSign, Database, MapPin, Calendar, User, FileText } from "lucide-react";
import { FullAdvisoryResponse } from "../types/api";
import { useLanguage } from "../context/LanguageContext";

interface KisanAdvisoryCardProps {
  report: FullAdvisoryResponse;
  state: string;
  season: string;
  soilType: string;
  farmArea: number;
  areaUnit: string;
  soilData: {
    n: number;
    p: number;
    k: number;
    ph: number;
    rainfall: number;
    temperature: number;
    humidity: number;
  };
}

export const KisanAdvisoryCard: React.FC<KisanAdvisoryCardProps> = ({
  report,
  state,
  season,
  soilType,
  farmArea,
  areaUnit,
  soilData,
}) => {
  const { getCropName, getCategoryName, getSeasonName, getSoilName, getStateName, getUnitName } = useLanguage();

  const [farmerName, setFarmerName] = useState<string>("");
  const [fieldId, setFieldId] = useState<string>("");
  const [copied, setCopied] = useState<boolean>(false);

  const generationDate = new Date().toLocaleDateString("en-IN", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  const handlePrint = () => {
    window.print();
  };

  const handleShare = async () => {
    const summaryText = `KARPO KRISHI ADVISORY
Crop: ${report.recommendation.display_name} (${report.recommendation.confidence_percent.toFixed(1)}% match)
Location: ${state} | Area: ${farmArea} ${areaUnit} (${season})
Expected Yield: ${Math.round(report.yield_prediction.predicted_yield_kg_ha)} kg/ha
Mandi Rate: ₹${report.market_price.modal_rs_per_quintal.toLocaleString()}/Q
Net Profit: ₹${Math.round(report.financials.net_profit).toLocaleString()} (${report.financials.roi_percent.toFixed(1)}% ROI)
Generated on Karpo Precision Agriculture Platform`;

    if (navigator.share) {
      try {
        await navigator.share({
          title: `Krishi Advisory - ${report.recommendation.display_name}`,
          text: summaryText,
        });
        return;
      } catch {
        // Fall back to clipboard
      }
    }

    await navigator.clipboard.writeText(summaryText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  // Agronomic soil status analysis
  const getNitrogenStatus = (val: number) => {
    if (val < 50) return { label: "Low", note: "Supplement with organic compost or bio-fertilizer" };
    if (val <= 120) return { label: "Medium", note: "Balanced nitrogen level for vegetative growth" };
    return { label: "High", note: "Adequate foliage support; avoid excessive urea" };
  };

  const getPhStatus = (val: number) => {
    if (val < 6.0) return { label: "Acidic", note: "Apply agricultural lime if pH drops further" };
    if (val <= 7.5) return { label: "Optimal", note: "Ideal nutrient solubility range" };
    return { label: "Alkaline", note: "Gypsum application recommended for sodic soils" };
  };

  const nStatus = getNitrogenStatus(soilData.n);
  const phStatus = getPhStatus(soilData.ph);

  return (
    <div className="space-y-4">
      {/* Action Bar (Hidden in Print) */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 p-4 bg-obsidian-900 border border-obsidian-750 print:hidden">
        <div className="flex items-center gap-3">
          <input
            type="text"
            placeholder="Farmer Name (Optional)"
            value={farmerName}
            onChange={(e) => setFarmerName(e.target.value)}
            className="bg-white border border-obsidian-700 text-chalk-100 px-3 py-1.5 text-xs font-mono focus:border-signal-red focus:outline-none placeholder:text-obsidian-500 w-44"
          />
          <input
            type="text"
            placeholder="Survey/Gat No. (Optional)"
            value={fieldId}
            onChange={(e) => setFieldId(e.target.value)}
            className="bg-white border border-obsidian-700 text-chalk-100 px-3 py-1.5 text-xs font-mono focus:border-signal-red focus:outline-none placeholder:text-obsidian-500 w-44"
          />
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={handleShare}
            className="px-3 py-1.5 bg-obsidian-850 hover:bg-signal-red hover:text-white text-chalk-200 border border-obsidian-700 text-xs font-mono uppercase tracking-wider flex items-center gap-1.5 transition-colors"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-signal-green" /> : <Share2 className="w-3.5 h-3.5" />}
            <span>{copied ? "Copied!" : "Share"}</span>
          </button>

          <button
            type="button"
            onClick={handlePrint}
            className="px-4 py-1.5 bg-signal-red hover:bg-signal-darkred text-white text-xs font-mono font-bold uppercase tracking-wider flex items-center gap-1.5 transition-colors shadow-sm"
          >
            <Printer className="w-3.5 h-3.5" />
            <span>Print / Save PDF</span>
          </button>
        </div>
      </div>

      {/* Printable Advisory Card */}
      <div
        id="kisan-advisory-print-card"
        className="bg-white border-2 border-obsidian-800 p-6 md:p-8 space-y-6 text-chalk-100 shadow-sm print:bg-white print:text-black print:border-black print:p-4 print:shadow-none print:m-0"
      >
        {/* Card Header */}
        <div className="border-b-2 border-obsidian-800 print:border-black pb-4 flex flex-col sm:flex-row justify-between items-start sm:items-end gap-3">
          <div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 bg-signal-red print:bg-black inline-block" />
              <span className="font-mono text-xs font-bold uppercase tracking-widest text-signal-red print:text-black">
                KARPO KRISHI ADVISORY DOSSIER
              </span>
            </div>
            <h2 className="font-display font-black text-2xl sm:text-3xl uppercase tracking-tight text-chalk-50 print:text-black mt-1">
              Field Crop & Economic Advisory
            </h2>
            <div className="flex flex-wrap items-center gap-3 text-xs font-mono text-obsidian-400 print:text-gray-600 mt-1">
              <span className="flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5" />
                {generationDate}
              </span>
              <span>&bull;</span>
              <span className="flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5" />
                {getStateName(state) || state} ({farmArea} {getUnitName(areaUnit)})
              </span>
              <span>&bull;</span>
              <span>Season: {getSeasonName(season) || season}</span>
            </div>
          </div>

          {(farmerName || fieldId) && (
            <div className="p-2.5 bg-obsidian-850 border border-obsidian-800 print:bg-gray-100 print:border-gray-400 text-right font-mono text-xs">
              {farmerName && (
                <div className="flex items-center justify-end gap-1.5 font-bold text-chalk-100 print:text-black">
                  <User className="w-3.5 h-3.5" />
                  <span>{farmerName}</span>
                </div>
              )}
              {fieldId && (
                <div className="text-[11px] text-obsidian-400 print:text-gray-700">
                  Field ID: {fieldId}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Primary Recommendation Banner */}
        <div className="p-4 bg-[#F7F5EF] border border-obsidian-800 print:bg-gray-50 print:border-black flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Sprout className="w-4 h-4 text-signal-red print:text-black" />
              <span className="font-mono text-[11px] uppercase tracking-wider text-obsidian-400 print:text-gray-700">
                Recommended Primary Cultivation ({getCategoryName(report.recommendation.category)})
              </span>
            </div>
            <div className="font-display font-black text-3xl sm:text-4xl uppercase tracking-tight text-chalk-50 print:text-black">
              {getCropName(report.recommendation.display_name) || report.recommendation.display_name}
            </div>
            <p className="font-sans text-xs text-obsidian-300 print:text-gray-800 max-w-xl">
              {report.recommendation.description}
            </p>
          </div>

          <div className="text-right font-mono shrink-0 p-3 bg-white border border-obsidian-800 print:bg-white print:border-black">
            <span className="text-[10px] text-obsidian-400 print:text-gray-600 uppercase block">Model Confidence</span>
            <span className="text-2xl font-black text-signal-red print:text-black">
              {report.recommendation.confidence_percent.toFixed(1)}%
            </span>
            <span className="text-[10px] text-obsidian-500 print:text-gray-600 block">RandomForest ML</span>
          </div>
        </div>

        {/* 4 Core Pillars Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 font-mono text-xs">
          {/* Pillar 1: Yield Forecast */}
          <div className="p-3.5 bg-obsidian-900 border border-obsidian-800 print:bg-white print:border-gray-400 space-y-1.5">
            <div className="flex items-center gap-1 text-[11px] text-obsidian-400 print:text-gray-600 uppercase font-semibold">
              <TrendingUp className="w-3.5 h-3.5 text-signal-red print:text-black" />
              <span>Projected Yield</span>
            </div>
            <div className="text-xl font-black text-chalk-100 print:text-black">
              {Math.round(report.yield_prediction.predicted_yield_kg_ha).toLocaleString()} <span className="text-xs font-normal text-obsidian-400 print:text-gray-600">kg/ha</span>
            </div>
            <div className="text-[11px] text-obsidian-300 print:text-gray-700 pt-1 border-t border-obsidian-800 print:border-gray-300">
              {report.yield_prediction.predicted_yield_quintals_acre.toFixed(2)} Q / {getUnitName("acre")}
            </div>
            <div className="text-[10px] text-obsidian-500 print:text-gray-600">
              Est. Total: {report.financials.total_production_quintals.toFixed(1)} Quintals
            </div>
          </div>

          {/* Pillar 2: Mandi Market Rate */}
          <div className="p-3.5 bg-obsidian-900 border border-obsidian-800 print:bg-white print:border-gray-400 space-y-1.5">
            <div className="flex items-center gap-1 text-[11px] text-obsidian-400 print:text-gray-600 uppercase font-semibold">
              <Database className="w-3.5 h-3.5 text-signal-red print:text-black" />
              <span>Mandi Price</span>
            </div>
            <div className="text-xl font-black text-chalk-100 print:text-black">
              ₹{report.market_price.modal_rs_per_quintal.toLocaleString()} <span className="text-xs font-normal text-obsidian-400 print:text-gray-600">/ Q</span>
            </div>
            <div className="text-[11px] text-obsidian-300 print:text-gray-700 pt-1 border-t border-obsidian-800 print:border-gray-300">
              ₹{report.market_price.price_per_kg.toFixed(2)} / kg
            </div>
            <div className="text-[10px] text-obsidian-500 print:text-gray-600">
              Source: AGMARKNET APMC
            </div>
          </div>

          {/* Pillar 3: Comprehensive C2 Cost */}
          <div className="p-3.5 bg-obsidian-900 border border-obsidian-800 print:bg-white print:border-gray-400 space-y-1.5">
            <div className="flex items-center gap-1 text-[11px] text-obsidian-400 print:text-gray-600 uppercase font-semibold">
              <DollarSign className="w-3.5 h-3.5 text-signal-red print:text-black" />
              <span>Cultivation C2 Cost</span>
            </div>
            <div className="text-xl font-black text-chalk-100 print:text-black">
              {report.financials.formatted_cost}
            </div>
            <div className="text-[11px] text-obsidian-300 print:text-gray-700 pt-1 border-t border-obsidian-800 print:border-gray-300">
              ₹{Math.round(report.financials.cost_per_acre).toLocaleString()} / {getUnitName("acre")}
            </div>
            <div className="text-[10px] text-obsidian-500 print:text-gray-600">
              CACP Benchmark
            </div>
          </div>

          {/* Pillar 4: Projected Net Farm Profit */}
          <div className="p-3.5 bg-obsidian-900 border border-obsidian-800 print:bg-white print:border-gray-400 space-y-1.5">
            <div className="flex items-center gap-1 text-[11px] text-obsidian-400 print:text-gray-600 uppercase font-semibold">
              <ShieldCheck className="w-3.5 h-3.5 text-[#357A4A] print:text-black" />
              <span>Net Farm Profit</span>
            </div>
            <div className={`text-xl font-black ${report.financials.net_profit >= 0 ? "text-[#357A4A] print:text-black" : "text-[#B54747] print:text-black"}`}>
              {report.financials.formatted_profit}
            </div>
            <div className="text-[11px] text-obsidian-300 print:text-gray-700 pt-1 border-t border-obsidian-800 print:border-gray-300">
              ROI: {report.financials.roi_percent.toFixed(1)}%
            </div>
            <div className="text-[10px] text-obsidian-500 print:text-gray-600">
              Rev: {report.financials.formatted_revenue}
            </div>
          </div>
        </div>

        {/* Agronomic Nutrient & Soil Management Guidance */}
        <div className="p-4 bg-white border border-obsidian-800 print:bg-gray-50 print:border-gray-400 space-y-3 font-mono text-xs">
          <div className="flex items-center gap-2 border-b border-obsidian-800 print:border-gray-300 pb-2">
            <FileText className="w-4 h-4 text-signal-red print:text-black" />
            <span className="font-bold uppercase tracking-wider text-chalk-200 print:text-black">
              Agronomic Soil Chemistry & Field Management
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div className="p-2.5 bg-[#F7F5EF] border border-obsidian-800 print:bg-white print:border-gray-300">
              <span className="text-[10px] text-obsidian-400 print:text-gray-600 uppercase block">Soil Nitrogen (N)</span>
              <span className="font-bold text-chalk-100 print:text-black text-sm">{soilData.n} kg/ha ({nStatus.label})</span>
              <p className="text-[11px] text-obsidian-400 print:text-gray-700 mt-0.5">{nStatus.note}</p>
            </div>

            <div className="p-2.5 bg-[#F7F5EF] border border-obsidian-800 print:bg-white print:border-gray-300">
              <span className="text-[10px] text-obsidian-400 print:text-gray-600 uppercase block">Soil Reaction (pH)</span>
              <span className="font-bold text-chalk-100 print:text-black text-sm">pH {soilData.ph.toFixed(1)} ({phStatus.label})</span>
              <p className="text-[11px] text-obsidian-400 print:text-gray-700 mt-0.5">{phStatus.note}</p>
            </div>

            <div className="p-2.5 bg-[#F7F5EF] border border-obsidian-800 print:bg-white print:border-gray-300">
              <span className="text-[10px] text-obsidian-400 print:text-gray-600 uppercase block">Soil Class & Moisture</span>
              <span className="font-bold text-chalk-100 print:text-black text-sm">{getSoilName(soilType) || soilType}</span>
              <p className="text-[11px] text-obsidian-400 print:text-gray-700 mt-0.5">Rainfall: {soilData.rainfall} mm &bull; Hum: {soilData.humidity}%</p>
            </div>
          </div>
        </div>

        {/* Cost Breakdown Details */}
        <div className="p-3 bg-white border border-obsidian-800 print:bg-gray-50 print:border-gray-400 font-mono text-xs">
          <div className="text-[10px] text-obsidian-400 print:text-gray-600 uppercase tracking-widest mb-2 font-bold">
            Operational C2 Cost Component Breakdown (₹/ha)
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            <div>
              <span className="text-obsidian-500 print:text-gray-600 block">Seeds:</span>
              <span className="font-bold">₹{Math.round(report.cultivation_cost.seed_cost_per_ha).toLocaleString()}</span>
            </div>
            <div>
              <span className="text-obsidian-500 print:text-gray-600 block">Fertilizers:</span>
              <span className="font-bold">₹{Math.round(report.cultivation_cost.fertilizer_cost_per_ha).toLocaleString()}</span>
            </div>
            <div>
              <span className="text-obsidian-500 print:text-gray-600 block">Human Labor:</span>
              <span className="font-bold">₹{Math.round(report.cultivation_cost.labor_cost_per_ha).toLocaleString()}</span>
            </div>
            <div>
              <span className="text-obsidian-500 print:text-gray-600 block">Machinery:</span>
              <span className="font-bold">₹{Math.round(report.cultivation_cost.machinery_cost_per_ha).toLocaleString()}</span>
            </div>
          </div>
        </div>

        {/* Traceability & Official Disclaimers */}
        <div className="pt-3 border-t border-obsidian-800 print:border-gray-400 font-mono text-[10px] text-obsidian-400 print:text-gray-600 space-y-1">
          <div className="flex flex-wrap justify-between gap-1">
            <span><strong>Data Provenance:</strong> Model Inference (RandomForest & XGBoost) &bull; AGMARKNET &bull; CACP</span>
            <span><strong>Verification Ref:</strong> KRP-ADV-{Date.now().toString(36).toUpperCase()}</span>
          </div>
          <p className="italic">
            * Advisory values reflect empirical agronomic modeling and regional wholesale benchmarks. Actual realizations depend on field-level pest outbreaks, monsoon timing, and market volatility. Verify with your local Krishi Vigyan Kendra (KVK).
          </p>
        </div>
      </div>
    </div>
  );
};
