import React from "react";

interface AgroSystemVisualProps {
  className?: string;
}

export const AgroSystemVisual: React.FC<AgroSystemVisualProps> = ({ className = "" }) => {
  return (
    <div
      className={`border border-obsidian-750 bg-obsidian-950 p-4 select-none ${className}`}
      aria-label="Abstract topographic field elevation visualization"
    >
      {/* Discreet Header Label */}
      <div className="flex items-center justify-between border-b border-obsidian-800 pb-2 mb-3 font-mono text-[11px] text-obsidian-400">
        <span className="font-semibold text-chalk-200 uppercase tracking-technical">
          FIELD TOPOGRAPHY &bull; ELEVATION PROFILE
        </span>
        <span className="text-[10px] text-obsidian-500 uppercase">
          CONTOUR MAPPING
        </span>
      </div>

      {/* Topographic Vector SVG Canvas */}
      <div className="relative w-full aspect-[16/10] bg-obsidian-900 border border-obsidian-800/80 overflow-hidden">
        <svg
          viewBox="0 0 500 320"
          className="w-full h-full"
          preserveAspectRatio="xMidYMid meet"
          role="img"
          aria-label="Layered topographic elevation lines representing field slope"
        >
          {/* Subtle Orthogonal Baseline Grid */}
          <line x1="30" y1="20" x2="30" y2="290" stroke="#1D222E" strokeWidth="1" />
          <line x1="30" y1="290" x2="480" y2="290" stroke="#1D222E" strokeWidth="1" />

          {/* Abstract Field Parcels */}
          <polygon
            points="60,110 220,80 270,220 120,240"
            fill="#121620"
            stroke="#262F42"
            strokeWidth="1"
          />
          <polygon
            points="220,80 430,95 460,230 270,220"
            fill="#0F131C"
            stroke="#262F42"
            strokeWidth="1"
          />

          {/* Smooth Topographic Elevation Contours */}
          <g fill="none">
            {/* Contour 1 - Baseline */}
            <path
              d="M 40,260 C 100,245 160,275 240,250 C 320,225 390,255 470,230"
              stroke="#262F42"
              strokeWidth="1"
            />
            {/* Contour 2 */}
            <path
              d="M 40,220 C 110,195 180,235 260,205 C 340,175 410,215 470,185"
              stroke="#313B52"
              strokeWidth="1"
            />
            {/* Contour 3 - Index Contour (Signal Accent) */}
            <path
              d="M 50,175 C 130,145 200,190 290,155 C 370,125 420,165 470,135"
              stroke="#FF2A2A"
              strokeWidth="1.2"
            />
            {/* Contour 4 */}
            <path
              d="M 70,130 C 145,100 220,145 310,110 C 390,80 430,115 470,90"
              stroke="#3B4764"
              strokeWidth="1"
            />
            {/* Contour 5 - Upper Ridge */}
            <path
              d="M 100,90 C 170,65 240,105 330,70 C 400,45 440,75 470,55"
              stroke="#4E5C80"
              strokeWidth="1"
              strokeDasharray="3 3"
            />
          </g>

          {/* Elevation Level Labels */}
          <text x="38" y="264" fill="#606D8A" fontSize="9" fontFamily="JetBrains Mono">
            180m
          </text>
          <text x="38" y="224" fill="#606D8A" fontSize="9" fontFamily="JetBrains Mono">
            220m
          </text>
          <text x="42" y="179" fill="#FF2A2A" fontSize="9" fontFamily="JetBrains Mono" fontWeight="bold">
            260m
          </text>
          <text x="60" y="134" fill="#8694B0" fontSize="9" fontFamily="JetBrains Mono">
            300m
          </text>
          <text x="88" y="94" fill="#8694B0" fontSize="9" fontFamily="JetBrains Mono">
            340m
          </text>
        </svg>

        {/* Quiet Footnote */}
        <div className="absolute bottom-2 right-2 font-mono text-[9px] text-obsidian-400 bg-obsidian-950/80 px-2 py-0.5 border border-obsidian-800 select-none">
          ELEVATION GRADIENT &bull; 40m INTERVALS
        </div>
      </div>
    </div>
  );
};
