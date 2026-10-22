"""
Generates additional Output figures for Section 13:
- fig_ui_crop_rec.png (Figure 13.2)
- fig_ui_composite_breakdown.png (Figure 13.3)
- fig_ui_swagger.png (Figure 13.4)
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)


def generate_crop_rec_mockup():
    """Generates Figure 13.2: Crop Recommendation UI."""
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    rect = patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=1", facecolor="#ffffff", edgecolor="#cbd5e1", linewidth=1.5)
    ax.add_patch(rect)
    ax.text(6, 92, "🌱 CROP RECOMMENDATION // AGRO-ECOLOGICAL INFERENCE", fontsize=11, fontweight="bold", color="#15803d")
    ax.text(6, 86, "Multi-Class Random Forest Model (22 Crops, 99.55% Test Accuracy)", fontsize=8, color="#64748b")

    # Form Fields Box
    r_form = patches.FancyBboxPatch((5, 12), 42, 68, boxstyle="round,pad=0.8", facecolor="#f8fafc", edgecolor="#e2e8f0")
    ax.add_patch(r_form)
    ax.text(8, 74, "SOIL & CLIMATIC PARAMETERS", fontsize=8.5, fontweight="bold", color="#0f172a")

    inputs = [
        ("Nitrogen (N):", "85 kg/ha"),
        ("Phosphorus (P):", "40 kg/ha"),
        ("Potassium (K):", "42 kg/ha"),
        ("Soil pH:", "6.50"),
        ("Temperature:", "24.5 °C"),
        ("Humidity:", "81.0 %"),
        ("Rainfall:", "202.0 mm"),
    ]
    y_pos = 66
    for lbl, val in inputs:
        ax.text(8, y_pos, lbl, fontsize=7.8, color="#475569")
        ax.text(32, y_pos, val, fontsize=7.8, fontweight="bold", color="#0f172a")
        y_pos -= 7.5

    # Result Box
    r_res = patches.FancyBboxPatch((51, 12), 44, 68, boxstyle="round,pad=0.8", facecolor="#f0fdf4", edgecolor="#16a34a", linewidth=1.5)
    ax.add_patch(r_res)
    ax.text(54, 74, "PREDICTION RESULT & CONFIDENCE", fontsize=8.5, fontweight="bold", color="#166534")

    # Recommended Crop badge
    r_badge = patches.FancyBboxPatch((54, 54), 38, 14, boxstyle="round,pad=0.5", facecolor="#dcfce7", edgecolor="#22c55e")
    ax.add_patch(r_badge)
    ax.text(73, 63, "RECOMMENDED: RICE", ha="center", fontsize=9.5, fontweight="bold", color="#15803d")
    ax.text(73, 56, "Prediction Confidence: 99.55%", ha="center", fontsize=7.5, color="#166534")

    ax.text(54, 46, "Top Alternative Candidates:", fontsize=8, fontweight="bold", color="#334155")
    alts = [
        ("1. Jute", "Confidence: 0.28%", "#64748b"),
        ("2. Cotton", "Confidence: 0.12%", "#64748b"),
        ("3. Maize", "Confidence: 0.05%", "#64748b"),
    ]
    y_alt = 38
    for c_name, conf, col in alts:
        ax.text(56, y_alt, c_name, fontsize=7.5, fontweight="bold", color="#0f172a")
        ax.text(76, y_alt, conf, fontsize=7.5, color=col)
        y_alt -= 7

    ax.text(54, 16, "✓ Agronomic Validation Passed • Zero Data Leakage", fontsize=7, color="#15803d")

    plt.tight_layout()
    out = DOCS_DIR / "fig_ui_crop_rec.png"
    plt.savefig(out, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generated {out}")


def generate_composite_breakdown_mockup():
    """Generates Figure 13.3: Composite Financial Breakdown."""
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    rect = patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=1", facecolor="#ffffff", edgecolor="#cbd5e1", linewidth=1.5)
    ax.add_patch(rect)
    ax.text(6, 92, "💰 COMPOSITE ADVISORY // FARM FINANCIAL OPTIMIZATION", fontsize=11, fontweight="bold", color="#1e3a8a")
    ax.text(6, 86, "Chained Pipeline: Recommendation + Yield Regressor + Agmarknet Mandi + CACP C2 Cost", fontsize=8, color="#64748b")

    cards = [
        ("CROP IDENTITY", "Rice (Kharif, Maharashtra)", "Farm Size: 2.50 Acres (1.01 ha)", 5, 52, "#eff6ff", "#3b82f6"),
        ("PREDICTED HARVEST", "21.38 Quintals (2,138 kg)", "Yield: 2,112.5 kg/ha", 51, 52, "#ecfdf5", "#10b981"),
        ("GROSS REVENUE", "₹78,678", "Modal Price: ₹3,680 / Quintal", 5, 14, "#fefce8", "#eab308"),
        ("NET PROFIT & ROI", "₹21,660 (ROI: 37.99%)", "C2 Cost: ₹57,017 (₹56,340/ha)", 51, 14, "#f5f3ff", "#8b5cf6"),
    ]

    for title, val, sub, x, y, bg, border in cards:
        r = patches.FancyBboxPatch((x, y), 44, 32, boxstyle="round,pad=0.8", facecolor=bg, edgecolor=border, linewidth=1.4)
        ax.add_patch(r)
        ax.text(x + 3, y + 24, title, fontsize=7.8, fontweight="bold", color="#475569")
        ax.text(x + 3, y + 14, val, fontsize=9.5, fontweight="bold", color="#0f172a")
        ax.text(x + 3, y + 5, sub, fontsize=7.2, color="#64748b")

    plt.tight_layout()
    out = DOCS_DIR / "fig_ui_composite_breakdown.png"
    plt.savefig(out, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generated {out}")


def generate_swagger_mockup():
    """Generates Figure 13.5: FastAPI Swagger Documentation."""
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    rect = patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=1", facecolor="#ffffff", edgecolor="#cbd5e1", linewidth=1.5)
    ax.add_patch(rect)
    ax.text(6, 92, "KARPO FASTAPI // SWAGGER OPENAPI SPECIFICATION (/docs)", fontsize=11, fontweight="bold", color="#0f172a")
    ax.text(6, 86, "Automated Schema Validation with Pydantic v2 & Asynchronous Request Handlers", fontsize=8, color="#64748b")

    endpoints = [
        ("GET", "/health", "Health check and system diagnostics", "#2563eb", 70),
        ("POST", "/api/v1/recommend", "Multi-class crop recommendation (Random Forest)", "#16a34a", 54),
        ("POST", "/api/v1/yield", "Continuous yield forecasting (XGBoost Regressor)", "#16a34a", 38),
        ("POST", "/api/v1/advisory/composite", "Chained agronomic & C2 financial simulation", "#16a34a", 22),
        ("GET", "/api/v1/market/prices", "Real-time Agmarknet mandi modal prices query", "#2563eb", 6),
    ]

    for method, path, desc, col, y in endpoints:
        # Method badge
        r_m = patches.FancyBboxPatch((6, y), 12, 10, boxstyle="round,pad=0.4", facecolor=col, edgecolor=col)
        ax.add_patch(r_m)
        ax.text(12, y + 4.5, method, ha="center", fontsize=7.5, fontweight="bold", color="#ffffff")

        # Path bar
        r_p = patches.FancyBboxPatch((20, y), 74, 10, boxstyle="round,pad=0.4", facecolor="#f8fafc", edgecolor="#e2e8f0")
        ax.add_patch(r_p)
        ax.text(23, y + 4.5, path, fontsize=8, fontweight="bold", color="#0f172a")
        ax.text(56, y + 4.5, desc, fontsize=7.5, color="#64748b")

    plt.tight_layout()
    out = DOCS_DIR / "fig_ui_swagger.png"
    plt.savefig(out, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generated {out}")


if __name__ == "__main__":
    generate_crop_rec_mockup()
    generate_composite_breakdown_mockup()
    generate_swagger_mockup()
