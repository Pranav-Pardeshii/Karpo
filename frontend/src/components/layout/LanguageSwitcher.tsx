import React from "react";
import { Globe } from "lucide-react";
import { useLanguage, LANGUAGE_OPTIONS } from "../../context/LanguageContext";

export const LanguageSwitcher: React.FC<{ isMobile?: boolean }> = ({ isMobile }) => {
  const { language, setLanguage } = useLanguage();

  if (isMobile) {
    return (
      <div className="pt-2 pb-1 border-t border-obsidian-800">
        <div className="flex items-center gap-2 mb-2 px-1 text-[11px] font-mono uppercase tracking-widest text-obsidian-400">
          <Globe className="w-3.5 h-3.5" />
          <span>Language / भाषा:</span>
        </div>
        <div className="grid grid-cols-3 gap-1">
          {LANGUAGE_OPTIONS.map((opt) => (
            <button
              key={opt.code}
              type="button"
              onClick={() => setLanguage(opt.code)}
              className={`py-2 px-2 text-center font-mono text-xs uppercase tracking-technical border transition-colors ${
                language === opt.code
                  ? "bg-obsidian-800 text-chalk-50 border-signal-green font-bold shadow-brutal-subtle"
                  : "bg-obsidian-900 text-obsidian-400 hover:text-white border-obsidian-750"
              }`}
            >
              <div className="font-sans font-medium text-xs">{opt.nativeLabel}</div>
              <div className="text-[10px] text-obsidian-400">{opt.label}</div>
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="inline-flex items-center gap-1 border border-obsidian-750 bg-obsidian-900/90 p-0.5 rounded shadow-brutal-subtle">
      <div className="pl-1.5 pr-0.5 text-obsidian-400 select-none" title="Select Language">
        <Globe className="w-3.5 h-3.5" />
      </div>
      <div className="flex items-center">
        {LANGUAGE_OPTIONS.map((opt) => (
          <button
            key={opt.code}
            type="button"
            onClick={() => setLanguage(opt.code)}
            title={`Switch to ${opt.label} (${opt.nativeLabel})`}
            className={`px-2 py-0.5 text-xs font-mono tracking-technical transition-colors rounded-sm ${
              language === opt.code
                ? "bg-obsidian-750 text-chalk-50 font-bold border-b border-signal-green"
                : "text-obsidian-400 hover:text-chalk-100 hover:bg-obsidian-850"
            }`}
          >
            <span className="hidden xl:inline">{opt.nativeLabel}</span>
            <span className="xl:hidden">{opt.code.toUpperCase()}</span>
          </button>
        ))}
      </div>
    </div>
  );
};
