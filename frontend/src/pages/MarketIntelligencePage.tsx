import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Search, Database, ShieldCheck, ChevronLeft, ChevronRight, TrendingUp } from "lucide-react";
import { api } from "../api/client";

export const MarketIntelligencePage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [debouncedQuery, setDebouncedQuery] = useState<string>("");
  const [currentPage, setCurrentPage] = useState<number>(0);
  const pageSize = 15;

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setSearchQuery(val);
    setCurrentPage(0);
    const timeout = setTimeout(() => setDebouncedQuery(val), 300);
    return () => clearTimeout(timeout);
  };

  const handleQuickFilter = (crop: string) => {
    setSearchQuery(crop);
    setDebouncedQuery(crop);
    setCurrentPage(0);
  };

  const { data, isLoading, isError } = useQuery({
    queryKey: ["marketPrices", debouncedQuery, currentPage],
    queryFn: () =>
      api.getMarketPrices({
        query: debouncedQuery || undefined,
        limit: pageSize,
        offset: currentPage * pageSize,
      }),
  });

  const totalPages = data ? Math.ceil(data.total_records / pageSize) : 1;

  const quickCrops = ["ALL", "RICE", "WHEAT", "COTTON", "MAIZE", "SOYABEAN", "CHICKPEA", "ONION"];

  return (
    <div className="space-y-12">
      {/* Title Header */}
      <div className="border-b border-obsidian-750 pb-6 flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="font-display font-black text-3xl sm:text-4xl lg:text-5xl tracking-tight text-chalk-50 uppercase">
            Mandi Price Intelligence
          </h1>
          <p className="font-sans text-xs sm:text-sm text-obsidian-300 mt-1 max-w-2xl leading-relaxed">
            Agricultural Produce Market Committee (APMC) modal wholesale auction rates, price spreads, and statutory Minimum Support Price (MSP) benchmarks across India.
          </p>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs text-obsidian-400 shrink-0">
          <Database className="w-4 h-4 text-signal-red" />
          <span>SOURCE: AGMARKNET APMC DATASET</span>
        </div>
      </div>

      {/* Search, Filter & Counter Bar */}
      <div className="space-y-3">
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 p-4 border border-obsidian-750 bg-obsidian-950 shadow-brutal">
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3 top-3 text-obsidian-400" />
            <input
              type="text"
              placeholder="Filter by commodity (e.g. Rice, Wheat, Cotton, Maize, Mustard)..."
              value={searchQuery}
              onChange={handleSearchChange}
              className="w-full bg-obsidian-900 border border-obsidian-700 text-chalk-100 pl-10 pr-4 py-2 font-mono text-xs uppercase placeholder:text-obsidian-500 focus:outline-none focus:border-signal-red"
            />
          </div>

          <div className="flex items-center justify-between sm:justify-end gap-3 font-mono text-xs text-obsidian-400 shrink-0">
            <span>
              Showing {data?.prices.length ?? 0} of {data?.total_records ?? 0} commodities
            </span>
          </div>
        </div>

        {/* Quick Filter Chips */}
        <div className="flex flex-wrap items-center gap-1.5 font-mono text-xs">
          <span className="text-obsidian-400 text-[10px] uppercase mr-1">QUICK FILTER:</span>
          {quickCrops.map((crop) => (
            <button
              key={crop}
              onClick={() => handleQuickFilter(crop === "ALL" ? "" : crop)}
              className={`px-2.5 py-1 border text-[11px] uppercase tracking-technical transition-colors ${
                (crop === "ALL" && !searchQuery) || searchQuery.toUpperCase() === crop
                  ? "bg-signal-red text-white border-signal-red font-bold"
                  : "bg-obsidian-900 text-obsidian-400 border-obsidian-750 hover:bg-obsidian-850 hover:text-chalk-100"
              }`}
            >
              {crop}
            </button>
          ))}
        </div>
      </div>

      {/* Dense High-Contrast Technical Price Table */}
      <div className="border border-obsidian-750 bg-obsidian-950 shadow-brutal overflow-x-auto">
        <table className="w-full text-left border-collapse font-mono text-xs">
          <thead>
            <tr className="border-b border-obsidian-750 bg-obsidian-900 text-obsidian-300 uppercase text-[11px] tracking-technical">
              <th className="p-3.5 border-r border-obsidian-800 font-bold">Commodity</th>
              <th className="p-3.5 border-r border-obsidian-800 font-bold text-right">
                Modal Auction (₹/Q)
              </th>
              <th className="p-3.5 border-r border-obsidian-800 font-bold text-right">
                Price Spread (₹/Q)
              </th>
              <th className="p-3.5 border-r border-obsidian-800 font-bold text-right">
                Statutory MSP
              </th>
              <th className="p-3.5 border-r border-obsidian-800 font-bold text-right">
                Unit Rate (₹/kg)
              </th>
              <th className="p-3.5 font-bold">Source Registry</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-obsidian-800">
            {isLoading ? (
              <tr>
                <td colSpan={6} className="p-12 text-center text-obsidian-400">
                  Retrieving APMC commodity prices...
                </td>
              </tr>
            ) : isError ? (
              <tr>
                <td colSpan={6} className="p-12 text-center text-signal-red">
                  Unable to retrieve mandi price records. Please check backend connection.
                </td>
              </tr>
            ) : data && data.prices.length > 0 ? (
              data.prices.map((item, idx) => (
                <tr
                  key={`${item.canonical_name}-${idx}`}
                  className="hover:bg-obsidian-900/80 transition-colors duration-100"
                >
                  <td className="p-3.5 border-r border-obsidian-800 font-bold text-chalk-100 uppercase flex items-center gap-2">
                    <span className="text-white">{item.matched_crop_name}</span>
                    <span className="text-[10px] text-obsidian-400 font-normal">
                      [{item.canonical_name}]
                    </span>
                  </td>
                  <td className="p-3.5 border-r border-obsidian-800 text-right font-display font-black text-sm text-chalk-50 tabular-nums">
                    ₹{item.modal_rs_per_quintal.toLocaleString()}
                  </td>
                  <td className="p-3.5 border-r border-obsidian-800 text-right text-obsidian-300 tabular-nums">
                    ₹{item.min_rs_per_quintal.toLocaleString()} – ₹{item.max_rs_per_quintal.toLocaleString()}
                  </td>
                  <td className="p-3.5 border-r border-obsidian-800 text-right">
                    {item.msp_rs_per_quintal ? (
                      <span className="inline-flex items-center gap-1 text-emerald-400 font-semibold tabular-nums">
                        <ShieldCheck className="w-3.5 h-3.5" />
                        ₹{item.msp_rs_per_quintal.toLocaleString()}
                      </span>
                    ) : (
                      <span className="text-obsidian-500 text-[10px]">No MSP</span>
                    )}
                  </td>
                  <td className="p-3.5 border-r border-obsidian-800 text-right font-bold text-chalk-100 tabular-nums">
                    ₹{item.price_per_kg.toFixed(2)}
                  </td>
                  <td className="p-3.5 text-[10px] text-obsidian-400 truncate max-w-xs">
                    {item.source}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={6} className="p-12 text-center text-obsidian-400">
                  No commodities matched "{searchQuery}".
                </td>
              </tr>
            )}
          </tbody>
        </table>

        {/* Pagination Bar */}
        {data && data.total_records > pageSize && (
          <div className="p-3.5 border-t border-obsidian-750 bg-obsidian-900 flex items-center justify-between font-mono text-xs">
            <span className="text-obsidian-400 text-[11px]">
              Page {currentPage + 1} of {totalPages}
            </span>
            <div className="flex items-center gap-2">
              <button
                disabled={currentPage === 0}
                onClick={() => setCurrentPage((p) => Math.max(0, p - 1))}
                className="px-2.5 py-1 bg-obsidian-850 text-chalk-200 border border-obsidian-700 disabled:opacity-30 disabled:cursor-not-allowed hover:bg-signal-red hover:text-white flex items-center gap-1 uppercase tracking-technical transition-colors"
              >
                <ChevronLeft className="w-3.5 h-3.5" /> Prev
              </button>
              <button
                disabled={currentPage >= totalPages - 1}
                onClick={() => setCurrentPage((p) => p + 1)}
                className="px-2.5 py-1 bg-obsidian-850 text-chalk-200 border border-obsidian-700 disabled:opacity-30 disabled:cursor-not-allowed hover:bg-signal-red hover:text-white flex items-center gap-1 uppercase tracking-technical transition-colors"
              >
                Next <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Regulatory Context Notice */}
      <div className="border border-obsidian-750 bg-obsidian-950 p-4 font-mono text-xs text-obsidian-300 flex items-start gap-3">
        <TrendingUp className="w-4 h-4 text-signal-red shrink-0 mt-0.5" />
        <p className="font-sans leading-relaxed text-xs">
          <strong className="text-chalk-100 uppercase font-mono">Market Notice:</strong> Rates
          reflect official Agricultural Produce Market Committee (APMC) modal wholesale auction
          benchmarks. Realized prices vary daily with quality grade and market arrivals.
        </p>
      </div>
    </div>
  );
};
