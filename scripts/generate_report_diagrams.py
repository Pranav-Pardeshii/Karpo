"""
Generates high-resolution academic diagrams for the Karpo Project Report:
- Figure 8.1: Architecture Diagram
- Figure 9.1: Component Diagram
- Figure 10.1: Dataset Distribution Chart
- Figure 11.1: Model Comparison Chart
- Output mockups / diagrams (Figure 13.1, 13.2, 13.3, 13.4)
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)


def generate_architecture_diagram():
    """Generates Figure 8.1: System Architecture Diagram."""
    fig, ax = plt.subplots(figsize=(8.5, 9.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    boxes = [
        ("Agricultural Datasets\n(Crop Rec, Crop Yield, Agmarknet Prices, CACP C2 Costs)", 88, "#e0f2fe", "#0284c7"),
        ("Data Preparation & Validation Module\n(Bounds checking, deduplication, ColumnTransformer)", 74, "#f0fdf4", "#16a34a"),
        ("Stratified & Random 80/20 Train-Test Splits\n(Random Forest vs XGBoost for Classification & Regression)", 60, "#fef3c7", "#d97706"),
        ("Model Training, Cross-Validation & Metric Selection\n(Crop Rec: RF 99.55% Acc | Yield: XGBoost R² = 0.8801)", 46, "#f3e8ff", "#9333ea"),
        ("Serialized ML & Agronomic Artifacts\n(joblib models, preprocessors, training_metrics.json)", 32, "#f1f5f9", "#475569"),
        ("FastAPI Asynchronous REST API Backend\n(/api/v1/recommend, /api/v1/yield, /api/v1/advisory/composite)", 18, "#ccfbf1", "#0d9488"),
        ("Interactive Delivery Layer\n(React 18 + Vite Frontend & Streamlit Advisory Dashboard)", 4, "#dbeafe", "#2563eb"),
    ]

    for text, y, bg_color, border_color in boxes:
        rect = patches.FancyBboxPatch(
            (10, y - 4), 80, 8,
            boxstyle="round,pad=1.2,rounding_size=2",
            facecolor=bg_color,
            edgecolor=border_color,
            linewidth=1.8,
        )
        ax.add_patch(rect)
        ax.text(50, y, text, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#0f172a")

    # Connect boxes with arrows
    for i in range(len(boxes) - 1):
        y_start = boxes[i][1] - 4
        y_end = boxes[i + 1][1] + 4
        ax.annotate(
            "",
            xy=(50, y_end),
            xytext=(50, y_start),
            arrowprops=dict(arrowstyle="->", lw=2, color="#334155"),
        )

    plt.tight_layout()
    out_path = DOCS_DIR / "fig_architecture.png"
    plt.savefig(out_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generated {out_path}")


def generate_component_diagram():
    """Generates Figure 9.1: Component Diagram."""
    fig, ax = plt.subplots(figsize=(9, 8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Draw boxes
    components = [
        # (x, y, w, h, text, bg, border)
        (5, 68, 25, 18, "Training Script\nscripts/train_models.py\n(Dual ML Pipeline)", "#ecfdf5", "#059669"),
        (5, 20, 25, 18, "Datasets Storage\ndatasets/*.csv\n(4 Verified Sources)", "#eff6ff", "#2563eb"),
        (40, 44, 25, 20, "Artifacts & Cache\nmodels/*.pkl\nmetrics.json\nPreprocessors", "#fdf4ff", "#a855f7"),
        (72, 68, 25, 18, "React + Vite Frontend\nfrontend/src\n(Composite UI)", "#fff7ed", "#ea580c"),
        (72, 20, 25, 18, "FastAPI Backend\nsrc/crop_advisory/api\n(Pydantic v2 + Async)", "#f0fdfa", "#0d9488"),
    ]

    for x, y, w, h, text, bg, border in components:
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=1,rounding_size=2",
            facecolor=bg,
            edgecolor=border,
            linewidth=1.8,
        )
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8.5, fontweight="bold", color="#1e293b")

    # Arrows
    # Datasets -> Training Script
    ax.annotate("", xy=(17.5, 68), xytext=(17.5, 38), arrowprops=dict(arrowstyle="->", lw=1.8, color="#475569"))
    ax.text(19, 53, "loads raw data", fontsize=7.5, color="#475569")

    # Training Script -> Artifacts
    ax.annotate("", xy=(40, 56), xytext=(30, 72), arrowprops=dict(arrowstyle="->", lw=1.8, color="#475569"))
    ax.text(28, 62, "exports", fontsize=7.5, color="#475569")

    # Datasets -> Artifacts (Price & Cost lookup)
    ax.annotate("", xy=(40, 50), xytext=(30, 32), arrowprops=dict(arrowstyle="->", lw=1.8, color="#475569"))
    ax.text(28, 40, "price/cost lookup", fontsize=7.5, color="#475569")

    # Artifacts -> Backend
    ax.annotate("", xy=(72, 32), xytext=(65, 50), arrowprops=dict(arrowstyle="->", lw=1.8, color="#475569"))
    ax.text(64, 38, "joblib loads", fontsize=7.5, color="#475569")

    # Backend <-> Frontend
    ax.annotate("", xy=(84.5, 68), xytext=(84.5, 38), arrowprops=dict(arrowstyle="<->", lw=2, color="#0284c7"))
    ax.text(86, 53, "JSON REST API\n(HTTP POST/GET)", fontsize=7.5, fontweight="bold", color="#0284c7")

    plt.tight_layout()
    out_path = DOCS_DIR / "fig_component.png"
    plt.savefig(out_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generated {out_path}")


def generate_class_distribution():
    """Generates Figure 10.1: Crop Recommendation Class Distribution."""
    fig, ax = plt.subplots(figsize=(9, 4.2), dpi=300)
    crops = [
        "rice", "maize", "chickpea", "kidneybeans", "pigeonpeas", "mothbeans",
        "mungbean", "blackgram", "lentil", "pomegranate", "banana", "mango",
        "grapes", "watermelon", "muskmelon", "apple", "orange", "papaya",
        "coconut", "cotton", "jute", "coffee"
    ]
    counts = [100] * len(crops)

    colors_list = plt.cm.viridis(np.linspace(0.15, 0.85, len(crops)))
    bars = ax.bar(crops, counts, color=colors_list, edgecolor="#334155", linewidth=0.8)
    ax.set_ylim(0, 130)
    ax.set_ylabel("Number of Samples", fontsize=10, fontweight="bold", color="#1e293b")
    ax.set_title("Balanced Class Distribution across 22 Crops (100 Samples Each, N=2,200)", fontsize=11, fontweight="bold", pad=12)
    plt.xticks(rotation=65, ha="right", fontsize=8.5)
    plt.yticks(fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 3, str(yval), ha="center", va="bottom", fontsize=7.5, fontweight="bold")

    plt.tight_layout()
    out_path = DOCS_DIR / "fig_class_distribution.png"
    plt.savefig(out_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generated {out_path}")


def generate_model_comparison():
    """Generates Figure 11.1: Model Comparison Bar Chart."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=300)

    # 1. Classification
    models_cls = ["Random Forest\n(Selected)", "XGBoost\nClassifier"]
    acc_cls = [99.55, 99.09]
    colors_cls = ["#16a34a", "#64748b"]
    bars1 = ax1.bar(models_cls, acc_cls, color=colors_cls, edgecolor="#0f172a", width=0.5)
    ax1.set_ylim(95, 101)
    ax1.set_ylabel("Test Accuracy (%)", fontsize=10, fontweight="bold")
    ax1.set_title("Crop Recommendation Accuracy", fontsize=11, fontweight="bold")
    ax1.grid(axis="y", linestyle="--", alpha=0.5)
    for b in bars1:
        y = b.get_height()
        ax1.text(b.get_x() + b.get_width() / 2, y + 0.3, f"{y:.2f}%", ha="center", fontsize=9, fontweight="bold")

    # 2. Regression
    models_reg = ["XGBoost Regressor\n(Selected)", "Random Forest\nRegressor"]
    r2_reg = [0.8801, 0.8757]
    colors_reg = ["#2563eb", "#64748b"]
    bars2 = ax2.bar(models_reg, r2_reg, color=colors_reg, edgecolor="#0f172a", width=0.5)
    ax2.set_ylim(0.80, 0.92)
    ax2.set_ylabel("R² Score (Goodness of Fit)", fontsize=10, fontweight="bold")
    ax2.set_title("Yield Forecasting R² Score", fontsize=11, fontweight="bold")
    ax2.grid(axis="y", linestyle="--", alpha=0.5)
    for b in bars2:
        y = b.get_height()
        ax2.text(b.get_x() + b.get_width() / 2, y + 0.008, f"R² = {y:.4f}", ha="center", fontsize=9, fontweight="bold")

    plt.tight_layout()
    out_path = DOCS_DIR / "fig_model_comparison.png"
    plt.savefig(out_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generated {out_path}")


def generate_ui_mockups():
    """Generates crisp UI presentation diagrams for Figures 13.1, 13.2, 13.3."""
    # Figure 13.1: Overview Dashboard
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Background card
    rect = patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=1", facecolor="#0f172a", edgecolor="#334155")
    ax.add_patch(rect)
    ax.text(50, 90, "KARPO // AGRO-ECOLOGICAL INTELLIGENCE MATRIX", ha="center", fontsize=12, fontweight="bold", color="#38bdf8")
    ax.text(50, 84, "Production-Grade AI Crop Advisory & Farm Financial Optimization System", ha="center", fontsize=8.5, color="#94a3b8")

    kpis = [
        ("RECOMMENDED CROP", "Rice (Oryza sativa)", "Confidence: 99.55%", 5, 45, "#10b981"),
        ("FORECASTED YIELD", "2,112.5 kg/ha", "Quintals/Acre: 8.55", 28, 45, "#3b82f6"),
        ("MANDI MODAL PRICE", "₹3,680 / Quintal", "APMC Agmarknet Benchmark", 51, 45, "#f59e0b"),
        ("NET FARM PROFIT", "₹21,660 (ROI: 38%)", "Comprehensive C2 Margin", 74, 45, "#8b5cf6"),
    ]
    for title, val, sub, x, y, col in kpis:
        r = patches.FancyBboxPatch((x, y), 21, 30, boxstyle="round,pad=0.8", facecolor="#1e293b", edgecolor=col, linewidth=1.5)
        ax.add_patch(r)
        ax.text(x + 10.5, y + 23, title, ha="center", fontsize=7.5, fontweight="bold", color="#94a3b8")
        ax.text(x + 10.5, y + 14, val, ha="center", fontsize=8.5, fontweight="bold", color="#f8fafc")
        ax.text(x + 10.5, y + 6, sub, ha="center", fontsize=6.8, color=col)

    # Bottom status bar
    r_stat = patches.FancyBboxPatch((5, 10), 90, 24, boxstyle="round,pad=0.8", facecolor="#1e293b", edgecolor="#334155")
    ax.add_patch(r_stat)
    ax.text(10, 26, "ACTIVE WORKFLOW: COMPOSITE ADVISORY (End-to-End Inference)", fontsize=8, fontweight="bold", color="#38bdf8")
    ax.text(10, 18, "• Pipeline 1: Random Forest Classifier (Multi-Class 22 Crops) -> Recommended: Rice", fontsize=7.5, color="#cbd5e1")
    ax.text(10, 12, "• Pipeline 2: XGBoost Regressor (198,369 Records, R² = 0.8801) -> Expected Yield: 21.38 Quintals (2.5 Acres)", fontsize=7.5, color="#cbd5e1")

    plt.tight_layout()
    out1 = DOCS_DIR / "fig_ui_overview.png"
    plt.savefig(out1, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generated {out1}")


if __name__ == "__main__":
    generate_architecture_diagram()
    generate_component_diagram()
    generate_class_distribution()
    generate_model_comparison()
    generate_ui_mockups()
