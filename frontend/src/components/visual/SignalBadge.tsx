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
    dark: "bg-white text-chalk-100 border-obsidian-800",
    neutral: "bg-obsidian-850 text-chalk-100 border-obsidian-800",
    contrast: "bg-white text-chalk-100 border-obsidian-800 font-bold",
    success: "bg-[#EAF0E6] text-[#357A4A] border-[#357A4A]/30 font-semibold",
    warning: "bg-[#FDF8F0] text-[#A66B18] border-[#A66B18]/30 font-semibold",
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
