import React from "react";
import { Outlet } from "react-router-dom";
import { Header } from "./Header";
import { ContourGrid } from "../visual/ContourGrid";
import { KisanVoiceAssistant } from "../KisanVoiceAssistant";
import { useLanguage } from "../../context/LanguageContext";

export const Layout: React.FC = () => {
  const { t } = useLanguage();

  return (
    <div className="min-h-screen flex flex-col bg-obsidian-950 text-chalk-100 relative selection:bg-signal-red selection:text-white">
      {/* Compact Predictable Brand Header & Navigation with Language Selector */}
      <Header />

      <main className="flex-1 relative">
        <ContourGrid />
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-8 py-8 sm:py-12">
          <Outlet />
        </div>
      </main>

      {/* Multilingual Voice Copilot */}
      <KisanVoiceAssistant />

      {/* Clean Brutalist Footer */}
      <footer className="border-t border-obsidian-800 bg-white mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-8 py-8 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6 font-mono text-xs text-obsidian-400">
          <div>
            <div className="font-bold text-chalk-100 tracking-technical uppercase mb-1">
              KARPO — {t("brand_sub")}
            </div>
            <p className="max-w-xl text-[11px] text-obsidian-400 leading-relaxed">
              {t("footer_desc")}
            </p>
          </div>

          <div className="flex flex-col sm:text-right shrink-0 gap-1 text-[11px]">
            <span className="text-chalk-300 font-semibold uppercase">
              {t("footer_sources")}
            </span>
            <span className="text-signal-red font-medium">
              {t("footer_disclaimer")}
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
};
