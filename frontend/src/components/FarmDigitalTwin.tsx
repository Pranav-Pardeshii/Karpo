import React, { useRef, useEffect, useState } from "react";

interface FarmDigitalTwinProps {
  crop?: string;
  soilType?: string;
  rainfallMm?: number;
  temperatureC?: number;
}

export const FarmDigitalTwin: React.FC<FarmDigitalTwinProps> = ({
  crop = "rice",
  soilType = "Vertisols",
  rainfallMm = 900,
  temperatureC = 25,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [moistureLevel, setMoistureLevel] = useState<number>(
    Math.min(100, Math.max(20, Math.round((rainfallMm / 1500) * 100)))
  );

  const canonCrop = crop.toLowerCase();

  // Root architecture type
  const isTaproot = [
    "cotton",
    "pigeonpeas",
    "chickpea",
    "soybean",
    "blackgram",
    "mungbean",
  ].includes(canonCrop);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Retina display scaling
    const dpr = window.devicePixelRatio || 1;
    const width = 640;
    const height = 360;

    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = "100%";
    canvas.style.height = "auto";
    ctx.scale(dpr, dpr);

    // Clear
    ctx.clearRect(0, 0, width, height);

    // Sky / Atmosphere (0 to 120 px)
    const skyGrad = ctx.createLinearGradient(0, 0, 0, 120);
    skyGrad.addColorStop(0, "#090d16");
    skyGrad.addColorStop(1, "#141c2e");
    ctx.fillStyle = skyGrad;
    ctx.fillRect(0, 0, width, 120);

    // Rain effect if high moisture
    if (moistureLevel > 60) {
      ctx.strokeStyle = "rgba(100, 180, 255, 0.25)";
      ctx.lineWidth = 1;
      for (let i = 0; i < 20; i++) {
        const rx = (i * 37) % width;
        const ry = (i * 17) % 110;
        ctx.beginPath();
        ctx.moveTo(rx, ry);
        ctx.lineTo(rx - 4, ry + 12);
        ctx.stroke();
      }
    }

    // Ground Surface Line
    const groundY = 120;
    ctx.fillStyle = "#3d2817";
    ctx.fillRect(0, groundY - 2, width, 4);

    // Soil Horizon A: Topsoil 0 - 15 cm (120 to 190 px)
    // Darker when moisture is higher
    const aSat = Math.round(30 + (moistureLevel / 100) * 35);
    const topsoilGrad = ctx.createLinearGradient(0, groundY, 0, 190);
    topsoilGrad.addColorStop(0, `rgb(${35 - aSat * 0.2}, ${25 - aSat * 0.15}, ${18 - aSat * 0.1})`);
    topsoilGrad.addColorStop(1, `rgb(${45 - aSat * 0.2}, ${32 - aSat * 0.15}, ${22 - aSat * 0.1})`);
    ctx.fillStyle = topsoilGrad;
    ctx.fillRect(0, groundY, width, 70);

    // Soil Horizon B: Subsoil 15 - 45 cm (190 to 280 px)
    const subsoilGrad = ctx.createLinearGradient(0, 190, 0, 280);
    const bColor = soilType === "Vertisols" ? "rgb(38, 35, 33)" : "rgb(65, 45, 30)";
    subsoilGrad.addColorStop(0, bColor);
    subsoilGrad.addColorStop(1, "rgb(55, 40, 28)");
    ctx.fillStyle = subsoilGrad;
    ctx.fillRect(0, 190, width, 90);

    // Soil Horizon C: Deep Substratum / Bedrock (280 to 360 px)
    const cGrad = ctx.createLinearGradient(0, 280, 0, 360);
    cGrad.addColorStop(0, "rgb(40, 38, 36)");
    cGrad.addColorStop(1, "rgb(25, 24, 23)");
    ctx.fillStyle = cGrad;
    ctx.fillRect(0, 280, width, 80);

    // Moisture Saturation Boundary Line (Dynamic based on slider)
    const moistureDepthY = groundY + (moistureLevel / 100) * 190;
    ctx.strokeStyle = "rgba(56, 189, 248, 0.4)";
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(0, moistureDepthY);
    ctx.lineTo(width, moistureDepthY);
    ctx.stroke();
    ctx.setLineDash([]);

    // Horizon Labels
    ctx.font = "10px monospace";
    ctx.fillStyle = "rgba(255, 255, 255, 0.45)";
    ctx.fillText("HORIZON A: Topsoil (0 - 15 cm)", 15, groundY + 20);
    ctx.fillText("HORIZON B: Subsoil (15 - 45 cm)", 15, 210);
    ctx.fillText("HORIZON C: Deep Horizon (45 - 90 cm)", 15, 300);

    // Moisture line text
    ctx.fillStyle = "#38bdf8";
    ctx.fillText(
      `Percolation Front: ~${Math.round((moistureLevel / 100) * 60)} cm depth`,
      width - 230,
      moistureDepthY - 6
    );

    // Crop Plant Center
    const plantX = width / 2;

    // ROOT SYSTEM
    ctx.lineWidth = 2;
    ctx.strokeStyle = "#e2d9c8";

    if (isTaproot) {
      // Deep Taproot (down to 270 px)
      ctx.beginPath();
      ctx.moveTo(plantX, groundY);
      ctx.lineTo(plantX, groundY + 140);
      ctx.stroke();

      // Lateral roots branching off taproot
      ctx.lineWidth = 1;
      const branches = [20, 45, 75, 105];
      branches.forEach((by, idx) => {
        const len = 35 - idx * 6;
        ctx.beginPath();
        ctx.moveTo(plantX, groundY + by);
        ctx.lineTo(plantX - len, groundY + by + 12);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(plantX, groundY + by);
        ctx.lineTo(plantX + len, groundY + by + 12);
        ctx.stroke();
      });
    } else {
      // Shallow Fibrous Root System (cluster spreading in top 70 px)
      ctx.lineWidth = 1.2;
      for (let i = -4; i <= 4; i++) {
        const spreadX = plantX + i * 9;
        const depthY = groundY + 45 + Math.abs(i) * 6;
        ctx.beginPath();
        ctx.moveTo(plantX, groundY);
        ctx.quadraticCurveTo(plantX + i * 15, groundY + 25, spreadX, depthY);
        ctx.stroke();
      }
    }

    // ABOVE GROUND STEM & FOLIAGE (120 px up to ~30 px)
    const stemHeight = Math.min(85, Math.max(50, 40 + (moistureLevel / 100) * 45));
    const foliageTopY = groundY - stemHeight;

    // Stem
    ctx.strokeStyle = "#22c55e";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(plantX, groundY);
    ctx.lineTo(plantX, foliageTopY + 15);
    ctx.stroke();

    // Leaves / Foliage
    ctx.fillStyle = "#16a34a";
    // Leaf 1
    ctx.beginPath();
    ctx.ellipse(plantX - 16, foliageTopY + 30, 18, 8, -0.4, 0, Math.PI * 2);
    ctx.fill();
    // Leaf 2
    ctx.beginPath();
    ctx.ellipse(plantX + 16, foliageTopY + 35, 18, 8, 0.4, 0, Math.PI * 2);
    ctx.fill();
    // Leaf 3
    ctx.beginPath();
    ctx.ellipse(plantX - 12, foliageTopY + 10, 14, 6, -0.3, 0, Math.PI * 2);
    ctx.fill();
    // Leaf 4
    ctx.beginPath();
    ctx.ellipse(plantX + 12, foliageTopY + 12, 14, 6, 0.3, 0, Math.PI * 2);
    ctx.fill();

    // Canopy top bud
    ctx.fillStyle = "#4ade80";
    ctx.beginPath();
    ctx.arc(plantX, foliageTopY + 4, 7, 0, Math.PI * 2);
    ctx.fill();

    // Metadata Tag on Canvas
    ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
    ctx.fillRect(15, 15, 160, 48);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
    ctx.strokeRect(15, 15, 160, 48);

    ctx.fillStyle = "#f8fafc";
    ctx.font = "bold 11px sans-serif";
    ctx.fillText(`${crop.toUpperCase()}`, 25, 32);

    ctx.font = "10px monospace";
    ctx.fillStyle = "#94a3b8";
    ctx.fillText(`Root: ${isTaproot ? "Deep Taproot" : "Fibrous Horizon"}`, 25, 45);
    ctx.fillText(`Soil: ${soilType}`, 25, 56);
  }, [crop, soilType, moistureLevel, isTaproot]);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-800 gap-2">
        <div className="flex items-center gap-2">
          <span className="text-xl">🌱</span>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-base font-semibold text-slate-100">
                Farm Digital Twin: Soil & Root Horizon
              </h3>
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-amber-950/80 text-amber-400 border border-amber-800">
                SIMULATION
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Interactive 2.5D cross-section illustrating root horizon penetration and rainfall percolation front.
            </p>
          </div>
        </div>

        <div className="text-xs text-slate-400 font-mono">
          Temp: <span className="text-slate-200">{temperatureC}°C</span> | Soil:{" "}
          <span className="text-slate-200">{soilType}</span>
        </div>
      </div>

      {/* Canvas Viewport */}
      <div className="my-4 rounded-lg overflow-hidden border border-slate-800/90 bg-slate-950 shadow-inner">
        <canvas
          ref={canvasRef}
          className="w-full block"
          style={{ maxHeight: "360px" }}
        />
      </div>

      {/* Interactive Controls */}
      <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800/80 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-3 w-full sm:w-auto flex-1">
          <label className="text-slate-400 whitespace-nowrap">
            Rainfall Percolation Infiltration:
          </label>
          <input
            type="range"
            min={20}
            max={100}
            value={moistureLevel}
            onChange={(e) => setMoistureLevel(Number(e.target.value))}
            className="w-full accent-emerald-500 bg-slate-800 h-1.5 rounded cursor-pointer"
          />
          <span className="text-emerald-400 font-mono font-bold w-12 text-right">
            {moistureLevel}%
          </span>
        </div>

        <div className="text-[11px] text-slate-400">
          Architecture:{" "}
          <strong className="text-slate-200">
            {isTaproot ? "Deep Taproot (~60-80 cm)" : "Shallow Fibrous (~25-35 cm)"}
          </strong>
        </div>
      </div>

      {/* Mandatory Operating Principle: Scientific Disclaimer */}
      <div className="mt-3 pt-2 border-t border-slate-800/80 flex items-start gap-2 text-[10px] text-slate-500 leading-normal">
        <span className="text-amber-400 font-bold">ℹ️ Note:</span>
        <p>
          This is an agronomic schematic simulation based on published ICAR and CRIDA root penetration studies.
          It visually maps hypothetical moisture horizons and does not represent an in-situ biological scan or physical ground-penetrating measurement.
        </p>
      </div>
    </div>
  );
};
