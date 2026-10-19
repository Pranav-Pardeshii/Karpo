import React from "react";

interface MetricCardProps {
  label: string;
  value: string | number;
  unit?: string;
  secondary?: string;
  tag?: string;
  variant?: "dark" | "contrast" | "signal" | "default";
  className?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  label,
  value,
  unit,
  secondary,
  tag,
  variant = "dark",
  className = "",
}) => {
  // Normalize default to dark
  const effectiveVariant = variant === "default" ? "dark" : variant;

  const variantStyles = {
    dark: "bg-obsidian-950 border-obsidian-700 text-chalk-100 shadow-brutal",
    contrast: "bg-paper-100 border-paper-200 text-obsidian-950 shadow-brutal",
    signal: "bg-signal-red border-signal-red text-white shadow-brutal",
  };

  const tagColor = {
    dark: "text-obsidian-400 border-obsidian-750 bg-obsidian-900",
    contrast: "text-obsidian-700 border-obsidian-400/40 bg-paper-200",
    signal: "text-white/90 border-white/40 bg-black/20",
  };

  return (
    <div
      className={`relative p-5 border rounded-none transition-all duration-150 ${variantStyles[effectiveVariant]} ${className}`}
    >
      {/* Reticle corner decoration */}
      <span className="absolute -top-1.5 -left-1.5 font-mono text-[9px] text-obsidian-500 pointer-events-none select-none">
        +
      </span>
      <span className="absolute -bottom-1.5 -right-1.5 font-mono text-[9px] text-obsidian-500 pointer-events-none select-none">
        +
      </span>

      {/* Header with technical label and optional index tag */}
      <div className="flex items-center justify-between gap-2 mb-3">
        <span
          className={`font-mono text-[10px] tracking-technical uppercase font-semibold ${
            effectiveVariant === "contrast" ? "text-obsidian-800" : "text-obsidian-400"
          }`}
        >
          {label}
        </span>
        {tag && (
          <span
            className={`font-mono text-[9px] tracking-widest px-1.5 py-0.5 border ${tagColor[effectiveVariant]}`}
          >
            {tag}
          </span>
        )}
      </div>

      {/* Primary Massive Numerical Display */}
      <div className="flex items-baseline gap-2">
        <span className="font-display font-black text-3xl sm:text-4xl tracking-tight tabular-nums">
          {value}
        </span>
        {unit && (
          <span
            className={`font-mono text-xs tracking-technical uppercase font-bold ${
              effectiveVariant === "contrast" ? "text-obsidian-700" : "text-obsidian-400"
            }`}
          >
            {unit}
          </span>
        )}
      </div>

      {/* Secondary microcopy / comparison context */}
      {secondary && (
        <div
          className={`mt-3 pt-2.5 border-t font-mono text-[11px] tracking-tight ${
            effectiveVariant === "contrast"
              ? "border-obsidian-300 text-obsidian-700"
              : effectiveVariant === "signal"
              ? "border-white/20 text-white/90"
              : "border-obsidian-800 text-obsidian-400"
          }`}
        >
          {secondary}
        </div>
      )}
    </div>
  );
};
