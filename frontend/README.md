# KARPO // FIELD//SIGNAL — Agricultural Intelligence Matrix

An experimental industrial brutalist web application for interpreting complex agricultural and environmental data, powered by the Smart Crop Advisory ML FastAPI backend.

---

## 🌾 Design Philosophy: FIELD//SIGNAL

> *"Treat agriculture as a complex system of signals, probabilities, environmental conditions, and economic outcomes. Build an interface that makes these relationships visible."*

KARPO fuses:
- **Experimental Swiss Editorial Design**: High-contrast typography, asymmetrical grids, deliberate whitespace, and technical section annotations.
- **Scientific Research Instrumentation**: Coordinate axes, topographic contour motifs, reticle crosshair markers (`+`), and tabular precision.
- **High-End Intelligence Platform**: Monochromatic core palette (`#111111` Ink Black, `#F4F1E8` Chalk White) punctuated by controlled bursts of `#F04438` Signal Red.
- **Interactive Visualization Laboratory**: Responsive Recharts probability distributions, yield benchmark comparisons, and economic break-even sensitivity models.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|:---|:---|:---|
| **Framework** | React 18 + Vite 6 | Lightning-fast component rendering and HMR |
| **Language** | TypeScript (Strict) | End-to-end typed API contracts matching FastAPI schemas |
| **Styling** | Tailwind CSS 3 | Custom brutalist design tokens, utility classes, and hard shadows |
| **Routing** | React Router 6 | Client-side navigation with route-level code splitting (`React.lazy`) |
| **Server State** | TanStack Query 5 | Real-time caching, background polling, and loading/error handling |
| **Visuals & Charts** | Recharts + Custom SVG | Responsive candidate distributions, yield benchmarks, and financial charts |
| **Icons** | Lucide React | Unified scientific and technical iconography |

---

## 🚀 Quickstart Guide

### Prerequisites
- **Node.js** v18+ or v22+
- **FastAPI Backend** running on `http://127.0.0.1:8000` (see root README)

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Launch Development Server
```bash
npm run dev
```
The application will launch at `http://127.0.0.1:5173/`.
*Note: Vite dev server automatically proxies all `/api` requests to `http://127.0.0.1:8000`, eliminating CORS friction during local development.*

### 3. Build for Production
```bash
npm run build
```
Creates an optimized, tree-shaken, and code-split production bundle in `dist/`.

---

## 🧭 Analytical Workflows & Routes

1. **`00 // OVERVIEW` (`/`)**:
   - Editorial intelligence briefing on agro-climatic decision support.
   - Real-time backend status probe verifying model preloading and dataset availability.
   - Interactive historical yield benchmark chart across Indian agro-climatic zones.
   - Canonical 22-crop taxonomy matrix with categorical filters (Cereals, Pulses, Fruits, Cash Crops, Fibers).

2. **`01 // CROP RECOMMENDATION` (`/recommend`)**:
   - 7-feature soil chemistry (NPK, pH) and microclimatic (temperature, humidity, rainfall) input vector.
   - Quick agro-climatic presets (Alluvial Paddy, Black Cotton, Winter Chickpea).
   - Offloaded multi-class Random Forest inference via `POST /api/v1/crops/recommend`.
   - Top recommended crop profile, candidate probability distribution bar chart, and actionable soil advisory diagnostics.

3. **`02 // YIELD FORECASTING` (`/yield`)**:
   - Regional jurisdiction, cropping season, soil taxonomy, and chemical input rates.
   - Non-linear gradient boosted regression via `POST /api/v1/yield/predict`.
   - 2x2 forecast matrix (kg/ha, Q/ha, kg/acre, Q/acre).
   - National historical benchmark variance panel (Min, Median, Max harvest capacity from DES records).

4. **`03 // MANDI INTELLIGENCE` (`/market`)**:
   - Real-time search and pagination across 122 APMC wholesale commodity markets.
   - Technical pricing data table displaying Modal Wholesale Rates (₹/Q), price ranges, statutory MSP benchmarks, and per-kg valuations.

5. **`04 // FARM ECONOMICS` (`/financials`)**:
   - Area scaler (acre, hectare, bigha), realized wholesale price, and CACP C2 cultivation expenditure.
   - "Auto-Fill Benchmarks" button syncing real-time CACP survey data and APMC mandi prices.
   - Computes Net Farm Surplus (₹), Return on Investment (ROI %), profit per acre, and break-even harvest/price thresholds via `POST /api/v1/financial-analysis`.

6. **`05 // COMPOSITE ADVISORY` (`/advisory`)**:
   - Single-shot unified intelligence pipeline executing `POST /api/v1/advisory/full`.
   - Full Unified Advisory Dossier orchestrating recommendation, yield, mandi rate, C2 expenditure, and net surplus in one cohesive report with print support.

---

## 🎨 Design System Tokens

```css
/* Core Color Palette */
--bg-chalk: #F4F1E8;       /* Primary warm paper background */
--text-ink: #111111;       /* Deep high-contrast ink black */
--signal-red: #F04438;     /* Controlled accent & alert badge */
--border-dark: #222222;    /* Hard-edged brutalist boundary */
--border-light: #DDD8C8;   /* Subtle divider rule */

/* Typography */
--font-display: "Space Grotesk", sans-serif; /* Headlines & metrics */
--font-sans: "Inter", sans-serif;            /* Body & application controls */
--font-mono: "JetBrains Mono", monospace;    /* Annotations, units & coordinates */
```
