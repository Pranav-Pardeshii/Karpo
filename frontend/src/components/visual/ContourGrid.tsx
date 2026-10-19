import React from "react";

interface ContourGridProps {
  className?: string;
}

export const ContourGrid: React.FC<ContourGridProps> = ({ className = "" }) => {
  return (
    <div
      className={`pointer-events-none absolute inset-0 overflow-hidden select-none ${className}`}
      aria-hidden="true"
    >
      {/* Subtle corner datum crosses that strictly stay in corners */}
      <div className="absolute top-4 left-4 font-mono text-[10px] text-obsidian-700 select-none">
        +
      </div>
      <div className="absolute top-4 right-4 font-mono text-[10px] text-obsidian-700 select-none">
        +
      </div>
    </div>
  );
};
