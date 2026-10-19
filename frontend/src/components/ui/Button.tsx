import React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "contrast" | "danger" | "ghost";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = "primary",
  size = "md",
  isLoading = false,
  className = "",
  disabled,
  ...props
}) => {
  const base =
    "inline-flex items-center justify-center font-mono font-bold tracking-technical uppercase transition-all duration-150 rounded-none border disabled:opacity-40 disabled:cursor-not-allowed focus:outline-none focus-visible:ring-1 focus-visible:ring-signal-red select-none";

  const variants = {
    primary:
      "bg-signal-red text-white border-signal-red hover:bg-signal-darkred hover:border-signal-darkred shadow-brutal active:translate-x-0.5 active:translate-y-0.5 active:shadow-none",
    secondary:
      "bg-obsidian-800 text-chalk-100 border-obsidian-650 hover:bg-obsidian-750 hover:border-obsidian-500 hover:text-white shadow-brutal active:translate-x-0.5 active:translate-y-0.5 active:shadow-none",
    contrast:
      "bg-paper-100 text-obsidian-950 border-paper-100 hover:bg-white hover:border-white shadow-brutal active:translate-x-0.5 active:translate-y-0.5 active:shadow-none font-black",
    danger:
      "bg-signal-darkred text-white border-signal-red hover:bg-signal-red shadow-brutal active:translate-x-0.5 active:translate-y-0.5 active:shadow-none",
    ghost:
      "bg-transparent text-chalk-200 border-obsidian-700 hover:border-obsidian-500 hover:bg-obsidian-850 hover:text-white",
  };

  const sizes = {
    sm: "px-3 py-1.5 text-[11px]",
    md: "px-5 py-2.5 text-xs",
    lg: "px-7 py-3.5 text-xs sm:text-sm",
  };

  return (
    <button
      className={`${base} ${variants[variant]} ${sizes[size]} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <span className="inline-flex items-center gap-2">
          <svg className="w-4 h-4 animate-spin text-current" viewBox="0 0 24 24" fill="none">
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
            />
          </svg>
          <span>PROCESSING SIGNAL...</span>
        </span>
      ) : (
        children
      )}
    </button>
  );
};
