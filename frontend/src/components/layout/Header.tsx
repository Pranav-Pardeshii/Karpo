import React, { useState } from "react";
import { Link, NavLink, useLocation } from "react-router-dom";
import { Menu, X } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { api } from "../../api/client";
import { useLanguage } from "../../context/LanguageContext";
import { LanguageSwitcher } from "./LanguageSwitcher";

export const Header: React.FC = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();
  const { t } = useLanguage();

  const navItems = [
    { label: t("nav_overview"), path: "/" },
    { label: t("nav_recommend"), path: "/recommend" },
    { label: t("nav_yield"), path: "/yield" },
    { label: t("nav_market"), path: "/market" },
    { label: t("nav_financials"), path: "/financials" },
    { label: t("nav_advisory"), path: "/advisory" },
  ];

  const { data: health, isError } = useQuery({
    queryKey: ["healthReady"],
    queryFn: api.getHealthReady,
    refetchInterval: 60000,
    retry: 1,
  });

  const isReady = health?.status === "ready" && health?.models_loaded;

  // Close mobile menu on route change
  React.useEffect(() => {
    setMobileMenuOpen(false);
  }, [location.pathname]);

  return (
    <header className="border-b border-obsidian-750 bg-obsidian-950/95 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-8">
        <div className="flex items-center justify-between h-16 sm:h-18">
          {/* Brand Wordmark & Restrained Descriptor */}
          <div className="flex items-baseline gap-3 shrink-0">
            <Link
              to="/"
              className="font-display font-black text-2xl sm:text-3xl tracking-tighter text-chalk-50 uppercase hover:text-white transition-colors"
            >
              KARPO
            </Link>
            <span className="font-mono text-[10px] tracking-widest text-obsidian-400 uppercase hidden sm:inline select-none">
              {t("brand_sub")}
            </span>
            {/* Discreet operational status indicator */}
            <span
              className={`w-1.5 h-1.5 rounded-full inline-block ${
                isReady ? "bg-signal-green" : isError ? "bg-signal-red" : "bg-signal-amber animate-pulse"
              }`}
              title={isReady ? t("status_operational") : isError ? t("status_offline") : t("status_connecting")}
              aria-label={isReady ? t("status_operational") : t("status_connecting")}
            />
          </div>

          {/* Desktop Navigation Links & Language Switcher */}
          <div className="hidden lg:flex items-center gap-3">
            <nav
              aria-label="Main Navigation"
              className="flex items-center gap-1 xl:gap-2 font-mono text-xs"
            >
              {navItems.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    `px-3 py-1.5 transition-colors uppercase tracking-technical ${
                      isActive
                        ? "text-chalk-50 bg-obsidian-850 border border-obsidian-700 shadow-brutal-subtle font-bold"
                        : "text-obsidian-300 hover:text-chalk-100 hover:bg-obsidian-900 border border-transparent"
                    }`
                  }
                >
                  {item.label}
                </NavLink>
              ))}
            </nav>

            {/* Language Switcher at Top of Desktop App */}
            <LanguageSwitcher />
          </div>

          {/* Mobile Menu Button */}
          <div className="lg:hidden flex items-center gap-2">
            <LanguageSwitcher />
            <button
              type="button"
              onClick={() => setMobileMenuOpen((prev) => !prev)}
              className="p-2 text-chalk-100 hover:text-white bg-obsidian-900 border border-obsidian-750 focus:outline-none focus:ring-1 focus:ring-signal-red"
              aria-label="Toggle navigation menu"
              aria-expanded={mobileMenuOpen}
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Accessible Mobile Drawer / Dropdown */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-t border-obsidian-800 bg-obsidian-950 px-4 py-3 space-y-2 font-mono text-xs">
          <div className="space-y-1">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `block px-3 py-2.5 uppercase tracking-technical transition-colors ${
                    isActive
                      ? "bg-obsidian-850 text-chalk-50 border-l-2 border-signal-red font-bold"
                      : "text-obsidian-300 hover:text-white hover:bg-obsidian-900"
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </div>
          <LanguageSwitcher isMobile />
        </div>
      )}
    </header>
  );
};
