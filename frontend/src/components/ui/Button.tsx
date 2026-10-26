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
      "bg-signal-red text-white font-bold border-signal-red hover:bg-signal-darkred hover:border-signal-darkred shadow-sm active:translate-x-0.5 active:translate-y-0.5 transition-all",
    secondary:
      "bg-obsidian-850 text-chalk-100 border-obsidian-800 hover:bg-[#DCE6D7] hover:border-signal-lime hover:text-chalk-100 shadow-sm active:translate-x-0.5 active:translate-y-0.5",
    contrast:
      "bg-white text-chalk-100 border-obsidian-800 hover:bg-obsidian-850 shadow-sm active:translate-x-0.5 active:translate-y-0.5 font-bold",
    danger:
      "bg-signal-error text-white border-signal-error hover:bg-[#9B3838] shadow-sm active:translate-x-0.5 active:translate-y-0.5",
    ghost:
      "bg-transparent text-chalk-100 border-obsidian-800 hover:border-signal-lime hover:bg-obsidian-850",
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
