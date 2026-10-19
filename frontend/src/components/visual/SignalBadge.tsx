import React from "react";

interface SignalBadgeProps {
  label: string;
  variant?: "signal" | "dark" | "neutral" | "contrast" | "success" | "warning";
  size?: "sm" | "md";
  className?: string;
  prefix?: string;
}

export const SignalBadge: React.FC<SignalBadgeProps> = ({
  label,
  variant = "neutral",
  size = "md",
  className = "",
  prefix,
}) => {
  const variantStyles = {
    signal: "bg-signal-red text-white border-signal-red font-bold",
    dark: "bg-obsidian-950 text-chalk-100 border-obsidian-700",
    neutral: "bg-obsidian-850 text-chalk-200 border-obsidian-750",
    contrast: "bg-paper-100 text-obsidian-950 border-paper-200 font-bold",
    success: "bg-emerald-950 text-emerald-300 border-emerald-700",
    warning: "bg-amber-950 text-amber-300 border-amber-700",
  };

  const sizeStyles = {
    sm: "px-1.5 py-0.5 text-[9px]",
    md: "px-2.5 py-1 text-[11px]",
  };

  return (
    <span
      className={`inline-flex items-center gap-1.5 font-mono uppercase tracking-technical border rounded-none ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
    >
      {prefix && <span className="opacity-60">{prefix}</span>}
      <span>{label}</span>
    </span>
  );
};
