import React from "react";
import { NavLink } from "react-router-dom";

export interface NavItem {
  label: string;
  path: string;
}

export const navItems: NavItem[] = [
  { label: "Overview", path: "/" },
  { label: "Crop Recommendation", path: "/recommend" },
  { label: "Yield Forecast", path: "/yield" },
  { label: "Market Intelligence", path: "/market" },
  { label: "Farm Economics", path: "/financials" },
  { label: "Composite Advisory", path: "/advisory" },
];

export const Navigation: React.FC = () => {
  return (
    <nav
      aria-label="Subsystem Navigation"
      className="bg-white overflow-x-auto scrollbar-none select-none border-t border-obsidian-800"
    >
      <div className="flex divide-x divide-obsidian-800 border-l border-obsidian-800 min-w-max">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `px-4 py-2 font-mono text-xs font-semibold tracking-technical flex items-center transition-colors ${
                isActive
                  ? "bg-obsidian-850 text-signal-red font-bold shadow-[inset_0_-2px_0_0_#244B35]"
                  : "bg-white text-obsidian-400 hover:bg-obsidian-850 hover:text-chalk-100"
              }`
            }
          >
            <span>{item.label}</span>
          </NavLink>
        ))}
      </div>
    </nav>
  );
};
