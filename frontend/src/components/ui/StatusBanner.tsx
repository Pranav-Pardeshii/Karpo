import React from "react";
import { AlertCircle, CheckCircle, Info, RefreshCw } from "lucide-react";

interface StatusBannerProps {
  type?: "error" | "warning" | "success" | "info" | "loading";
  title?: string;
  message: string;
  requestId?: string;
  onRetry?: () => void;
  className?: string;
}

export const StatusBanner: React.FC<StatusBannerProps> = ({
  type = "info",
  title,
  message,
  requestId,
  onRetry,
  className = "",
}) => {
  const configs = {
    error: {
      bg: "bg-red-950/40 border-signal-red text-signal-red",
      icon: AlertCircle,
      badge: "FAULT // 500",
      textColor: "text-red-200",
    },
    warning: {
      bg: "bg-amber-950/40 border-amber-500 text-amber-400",
      icon: AlertCircle,
      badge: "WARN // 422",
      textColor: "text-amber-200",
    },
    success: {
      bg: "bg-emerald-950/40 border-emerald-500 text-emerald-400",
      icon: CheckCircle,
      badge: "VERIFIED // 200",
      textColor: "text-emerald-200",
    },
    info: {
      bg: "bg-obsidian-850 border-obsidian-700 text-chalk-100",
      icon: Info,
      badge: "NOTICE // INFO",
      textColor: "text-obsidian-300",
    },
    loading: {
      bg: "bg-obsidian-850 border-obsidian-700 text-chalk-100",
      icon: RefreshCw,
      badge: "PROCESSING",
      textColor: "text-obsidian-300",
    },
  };

  const { bg, icon: Icon, badge, textColor } = configs[type];

  return (
    <div
      className={`p-4 border rounded-none flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 font-mono text-xs ${bg} ${className}`}
      role={type === "error" ? "alert" : "status"}
    >
      <div className="flex items-start gap-3">
        <Icon className={`w-4 h-4 mt-0.5 shrink-0 ${type === "loading" ? "animate-spin" : ""}`} />
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="font-bold tracking-technical uppercase">
              {title || badge}
            </span>
            {requestId && (
              <span className="text-[10px] opacity-70 tracking-widest font-normal">
                [ID: {requestId}]
              </span>
            )}
          </div>
          <p className={`${textColor} tracking-tight leading-relaxed`}>{message}</p>
        </div>
      </div>

      {onRetry && (
        <button
          onClick={onRetry}
          className="px-3 py-1 bg-obsidian-750 text-white hover:bg-signal-red text-[11px] font-mono tracking-technical uppercase shrink-0 transition-colors border border-obsidian-600 hover:border-signal-red"
        >
          RETRY SIGNAL
        </button>
      )}
    </div>
  );
};
