"""
Script to generate a comprehensive, publication-grade PDF guide for the
Karpo Smart Crop Advisory System Presentation and Viva Voce Defense.
Uses ReportLab to render a clean, beautifully styled document with page numbering.
"""

import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable,
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print 'Page X of Y'
    along with running header and footer rules.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4b5563"))

        # Skip header on cover/first page
        if self._pageNumber > 1:
            # Running header
            self.drawString(54, 11 * 72 - 36, "KARPO — Smart Crop Advisory System (ML)")
            self.drawRightString(8.5 * 72 - 54, 11 * 72 - 36, "Presentation & Viva Defense Guide")
            self.setStrokeColor(colors.HexColor("#d1d5db"))
            self.setLineWidth(0.5)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Running footer on all pages
        self.setStrokeColor(colors.HexColor("#e5e7eb"))
        self.setLineWidth(0.5)
        self.line(54, 45, 8.5 * 72 - 54, 45)

        footer_text = "CONFIDENTIAL & ACADEMIC DEFENSE • MACHINE LEARNING PROJECT"
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawString(54, 32, footer_text)
        self.drawRightString(8.5 * 72 - 54, 32, page_str)

        self.restoreState()


def create_presentation_pdf(output_filename: str):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom Palettes
    c_primary = colors.HexColor("#1b4332")     # Deep forest green
    c_secondary = colors.HexColor("#2d6a4f")   # Medium forest green
    c_accent = colors.HexColor("#b45309")      # Amber dark
    c_dark = colors.HexColor("#111827")        # Dark slate text
    c_muted = colors.HexColor("#4b5563")       # Slate gray
    c_bg_light = colors.HexColor("#f8fafc")    # Cool light background
    c_box_bg = colors.HexColor("#ecfdf5")      # Light emerald box background
    c_box_border = colors.HexColor("#10b981")  # Emerald border

    # Custom Typography Styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=30,
        textColor=c_primary,
        alignment=0,
        spaceAfter=6,
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=c_muted,
        spaceAfter=15,
    )

    h1_style = ParagraphStyle(
        "SectionHeading1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "SectionHeading2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "CleanBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=6,
    )

    bullet_style = ParagraphStyle(
        "CleanBullet",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=13,
        textColor=c_dark,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3,
    )

    script_quote_style = ParagraphStyle(
        "ScriptQuote",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#065f46"),
    )

    q_style = ParagraphStyle(
        "VivaQuestion",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1e3a8a"),  # Deep blue
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True,
    )

    ans_style = ParagraphStyle(
        "VivaAnswer",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=13.2,
        textColor=c_dark,
        spaceAfter=6,
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=c_dark,
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11.5,
        textColor=c_primary,
    )

    formula_style = ParagraphStyle(
        "FormulaText",
        parent=styles["Normal"],
        fontName="Courier-Bold",
        fontSize=8.8,
        leading=12,
        textColor=colors.HexColor("#0f172a"),
    )

    story = []

    # =========================================================================
    # COVER / HEADER BANNER
    # =========================================================================
    badge_table = Table(
        [[
            Paragraph("<b>PROJECT VIVA DEFENSE GUIDE</b>", ParagraphStyle("B", fontName="Helvetica-Bold", fontSize=8, textColor=colors.HexColor("#065f46"))),
            Paragraph("<b>MACHINE LEARNING (CS/IT)</b>", ParagraphStyle("B2", fontName="Helvetica-Bold", fontSize=8, alignment=2, textColor=c_muted)),
        ]],
        colWidths=[250, 254],
    )
    badge_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("🌾 KARPO: Smart Crop Advisory System", title_style))
    story.append(Paragraph("Machine Learning-Based Crop Recommendation, Precision Yield Forecasting & Farm Financial Optimization", subtitle_style))

    # Meta card table
    meta_data = [
        [
            Paragraph("<b>Domain:</b> AI in Precision Agriculture", body_style),
            Paragraph("<b>Classifiers:</b> Random Forest vs. XGBoost", body_style),
        ],
        [
            Paragraph("<b>Yield Regressor:</b> XGBoost (R² = 0.8801)", body_style),
            Paragraph("<b>Economic Data:</b> Agmarknet Mandi & CACP C2 Costs", body_style),
        ],
        [
            Paragraph("<b>Tech Stack:</b> Python, FastAPI, React, TS, Streamlit", body_style),
            Paragraph("<b>Target Audience:</b> Project Guide / ML Viva Panel", body_style),
        ]
    ]
    t_meta = Table(meta_data, colWidths=[250, 254])
    t_meta.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 1: THE 60-SECOND ELEVATOR PITCH
    # =========================================================================
    story.append(Paragraph("1. The 60-Second Elevator Pitch (What to Say When You Start)", h1_style))
    story.append(Paragraph("Memorize and speak these exact words when your ML teacher asks you to introduce your project:", body_style))

    pitch_box = [
        [Paragraph(
            "<b>🎙️ Exact Spoken Pitch:</b><br/>"
            "<i>\"Good morning, Ma'am. Most conventional agricultural machine learning projects stop after recommending a crop name like 'Rice' or 'Cotton'. But in reality, telling a farmer what to grow without estimating harvest quantity or financial viability is incomplete and commercially risky.<br/><br/>"
            "Our project, <b>Karpo</b>, solves this by chaining two machine learning engines with official Indian agricultural databases:<br/>"
            "• <b>Step 1:</b> A <b>Random Forest Classifier</b> evaluates 7 soil and weather features (NPK, pH, temperature, humidity, rainfall) to recommend the optimal crop with <b>99.55% accuracy</b> across 22 crops.<br/>"
            "• <b>Step 2:</b> An <b>XGBoost Regressor</b> trained on <b>198,000+ historical harvest records</b> forecasts the expected yield in kg/hectare (<b>R² = 0.8801</b>).<br/>"
            "• <b>Step 3:</b> The system integrates real-world <b>Agmarknet APMC Mandi prices</b> and <b>CACP Comprehensive C2 cultivation costs</b> to compute <b>Gross Revenue, Net Profit, ROI %</b>, and <b>Break-Even thresholds</b> in Indian Rupees.<br/><br/>"
            "In short, it connects soil chemistry directly to the farmer's bank balance before they invest a single rupee.\"</i>",
            script_quote_style
        )]
    ]
    t_pitch = Table(pitch_box, colWidths=[504])
    t_pitch.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), c_box_bg),
        ("BOX", (0, 0), (-1, -1), 1, c_box_border),
        ("PADDING", (0, 0), (-1, -1), 9),
    ]))
    story.append(t_pitch)
    story.append(Spacer(1, 12))

    # =========================================================================
    # SECTION 2: WHY IT IS CALLED "COMPOSITE ADVISORY"
    # =========================================================================
    story.append(Paragraph("2. Clarification: What Does 'Composite Advisory' Mean?", h1_style))
    story.append(Paragraph("Your teacher may ask why the main advisory page is named <b>Composite Advisory</b>:", body_style))
    story.append(Paragraph("• <b>Simple Definition:</b> 'Composite' means a unified multi-stage pipeline combining biological suitability, production quantity, and financial economics.", bullet_style))
    story.append(Paragraph("• <b>Technical Mechanism:</b> In traditional software, crop recommendation and yield prediction exist in isolation. In Karpo, the classification output (recommended crop) is automatically passed into the regression model (yield predictor) along with location and soil data, which then queries the price and C2 cost tables to execute farm accounting in one single asynchronous request.", bullet_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 3: SYSTEM ARCHITECTURE & 4-STAGE PIPELINE
    # =========================================================================
    story.append(Paragraph("3. System Architecture & The 4-Stage Pipeline", h1_style))
    story.append(Paragraph("The complete dataflow through the platform is structured into four sequential stages:", body_style))

    arch_data = [
        [Paragraph("<b>Pipeline Stage</b>", table_header_style), Paragraph("<b>Model / Source</b>", table_header_style), Paragraph("<b>Inputs / Features</b>", table_header_style), Paragraph("<b>Key Output</b>", table_header_style)],
        [
            Paragraph("<b>Stage 1: Crop Recommendation</b>", table_cell_bold),
            Paragraph("Random Forest Classifier (100 trees, depth 15)", table_cell_style),
            Paragraph("N, P, K, pH, Temperature, Humidity, Rainfall (7 features)", table_cell_style),
            Paragraph("Optimal crop from 22 classes (99.55% Acc) + top-3 alternatives", table_cell_style),
        ],
        [
            Paragraph("<b>Stage 2: Yield Forecasting</b>", table_cell_bold),
            Paragraph("XGBoost Regressor (120 trees, lr 0.08, hist)", table_cell_style),
            Paragraph("Crop, Season, Soil, State, Weather, Fertilizer, Pesticides", table_cell_style),
            Paragraph("Yield in kg/ha, Quintals/ha, and Quintals/Acre (R² = 0.8801)", table_cell_style),
        ],
        [
            Paragraph("<b>Stage 3: Market & Cost Query</b>", table_cell_bold),
            Paragraph("Agmarknet Portal & CACP Survey Data", table_cell_style),
            Paragraph("Recommended Crop + Farm State", table_cell_style),
            Paragraph("Modal Mandi Price (₹/Q) + Comprehensive C2 Cost (₹/ha)", table_cell_style),
        ],
        [
            Paragraph("<b>Stage 4: Financial Simulator</b>", table_cell_bold),
            Paragraph("Deterministic Agronomic Math Engine", table_cell_style),
            Paragraph("Acreage, Production, Modal Price, C2 Cultivation Cost", table_cell_style),
            Paragraph("Gross Revenue, Net Profit, ROI %, Break-Even Yield & Price", table_cell_style),
        ],
    ]
    t_arch = Table(arch_data, colWidths=[105, 125, 140, 134])
    t_arch.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), c_primary),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 4: MACHINE LEARNING BENCHMARKS & DEEP DIVE
    # =========================================================================
    story.append(Paragraph("4. Machine Learning Methodology & Benchmark Results", h1_style))
    story.append(Paragraph("Both pipelines were trained using an 80/20 train-test split with fixed random states (`random_state=42`) for reproducibility.", body_style))

    story.append(Paragraph("<b>4.1 Pipeline 1: Crop Recommendation (Multi-Class Classification)</b>", h2_style))
    story.append(Paragraph("• <b>Dataset:</b> 2,200 rows across 22 crops (100 samples per crop class = perfectly balanced).<br/>"
                           "• <b>Preprocessing:</b> Numerical features normalized with <code>StandardScaler</code>; labels encoded with <code>LabelEncoder</code>.<br/>"
                           "• <b>Feature Importance Ranking:</b> Humidity (22.8%) > Rainfall (21.4%) > Phosphorus (16.2%) > Potassium (15.8%) > Nitrogen (11.7%) > Temperature (7.1%) > pH (5.0%).", body_style))

    crop_rec_table = [
        [Paragraph("<b>Classification Model</b>", table_header_style), Paragraph("<b>Test Accuracy</b>", table_header_style), Paragraph("<b>Precision (Macro)</b>", table_header_style), Paragraph("<b>Recall (Macro)</b>", table_header_style), Paragraph("<b>F1-Score (Macro)</b>", table_header_style), Paragraph("<b>Selection Status</b>", table_header_style)],
        [
            Paragraph("<b>Random Forest Classifier</b>", table_cell_bold),
            Paragraph("<b>99.55%</b>", table_cell_style),
            Paragraph("0.9958", table_cell_style),
            Paragraph("0.9955", table_cell_style),
            Paragraph("0.9955", table_cell_style),
            Paragraph("🏆 <b>Selected Model</b>", table_cell_bold),
        ],
        [
            Paragraph("XGBoost Classifier", table_cell_style),
            Paragraph("99.09%", table_cell_style),
            Paragraph("0.9922", table_cell_style),
            Paragraph("0.9909", table_cell_style),
            Paragraph("0.9911", table_cell_style),
            Paragraph("Baseline", table_cell_style),
        ],
    ]
    t_rec = Table(crop_rec_table, colWidths=[120, 75, 75, 75, 75, 84])
    t_rec.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), c_secondary),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_rec)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>4.2 Pipeline 2: Crop Yield Prediction (Continuous Regression)</b>", h2_style))
    story.append(Paragraph("• <b>Dataset:</b> 198,369 historical harvest observations spanning 1966–2017 across 309 districts in 20 states.<br/>"
                           "• <b>Preprocessing:</b> Bundled inside scikit-learn <code>ColumnTransformer</code>: <code>StandardScaler</code> for continuous variables and <code>OneHotEncoder(handle_unknown='ignore')</code> for categories (Crop, Season, Soil Type, State) to strictly eliminate data leakage.<br/>"
                           "• <b>Top Predictors:</b> Fertilizer application rate, annual rainfall, crop type (e.g. Sugarcane/Rice), potassium level, soil type.", body_style))

    yield_table = [
        [Paragraph("<b>Regression Model</b>", table_header_style), Paragraph("<b>R² Score</b>", table_header_style), Paragraph("<b>RMSE (kg/ha)</b>", table_header_style), Paragraph("<b>MAE (kg/ha)</b>", table_header_style), Paragraph("<b>Selection Status</b>", table_header_style)],
        [
            Paragraph("<b>XGBoost Regressor</b>", table_cell_bold),
            Paragraph("<b>0.8801</b>", table_cell_style),
            Paragraph("<b>516.15</b>", table_cell_style),
            Paragraph("<b>308.29</b>", table_cell_style),
            Paragraph("🏆 <b>Selected Model</b>", table_cell_bold),
        ],
        [
            Paragraph("Random Forest Regressor", table_cell_style),
            Paragraph("0.8757", table_cell_style),
            Paragraph("525.41", table_cell_style),
            Paragraph("318.92", table_cell_style),
            Paragraph("Baseline", table_cell_style),
        ],
    ]
    t_yield = Table(yield_table, colWidths=[140, 80, 95, 95, 94])
    t_yield.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), c_secondary),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_yield)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 5: AGRICULTURAL ECONOMICS & FORMULAS
    # =========================================================================
    story.append(Paragraph("5. Agricultural Economics & Real-World Formulas", h1_style))
    story.append(Paragraph("The platform converts biological harvest predictions into financial metrics using official government standards:", body_style))

    story.append(Paragraph("<b>5.1 Why We Use CACP Comprehensive C2 Cost:</b>", h2_style))
    story.append(Paragraph("In agricultural economics, there are two primary cost metrics: <b>A2 Cost</b> (cash expenses on seeds, fertilizers, pesticides, fuel) and <b>C2 Cost</b>. Our system incorporates <b>C2 Comprehensive Cost</b> because it reflects true economic costs: direct out-of-pocket expenses <i>plus</i> rental value of owned land, interest on owned capital, and the imputed value of family labor.", body_style))

    formulas = [
        [Paragraph("<b>Metric Name</b>", table_header_style), Paragraph("<b>Mathematical Formula</b>", table_header_style), Paragraph("<b>Agronomic Explanation</b>", table_header_style)],
        [
            Paragraph("<b>Area Normalization</b>", table_cell_bold),
            Paragraph("Area (ha) = Area (Acres) / 2.47105", formula_style),
            Paragraph("Converts farmer's familiar acre input into SI scientific hectares.", table_cell_style),
        ],
        [
            Paragraph("<b>Total Production</b>", table_cell_bold),
            Paragraph("Prod (Q) = [Yield (kg/ha) × Area (ha)] / 100", formula_style),
            Paragraph("Converts kg into Indian market Quintals (1 Quintal = 100 kg).", table_cell_style),
        ],
        [
            Paragraph("<b>Gross Revenue</b>", table_cell_bold),
            Paragraph("Revenue = Prod (Q) × Modal Mandi Price (₹/Q)", formula_style),
            Paragraph("Modal price is the most frequent trading price in local APMC.", table_cell_style),
        ],
        [
            Paragraph("<b>Cultivation Cost</b>", table_cell_bold),
            Paragraph("Cost (₹) = Area (ha) × C2 Cost per Hectare", formula_style),
            Paragraph("State-specific C2 cost benchmark from CACP surveys.", table_cell_style),
        ],
        [
            Paragraph("<b>Net Profit & ROI</b>", table_cell_bold),
            Paragraph("Net Profit = Revenue - Total Cost<br/>ROI % = (Net Profit / Total Cost) × 100", formula_style),
            Paragraph("Net margin remaining in the farmer's hand after all expenses.", table_cell_style),
        ],
        [
            Paragraph("<b>Break-Even Yield</b>", table_cell_bold),
            Paragraph("BE Yield (kg/ha) = Cost per ha / Price per kg", formula_style),
            Paragraph("Minimum harvest required to avoid financial loss.", table_cell_style),
        ],
        [
            Paragraph("<b>Break-Even Price</b>", table_cell_bold),
            Paragraph("BE Price (₹/Q) = Total Cost / Total Prod (Q)", formula_style),
            Paragraph("Lowest mandi rate at which farmer breaks even.", table_cell_style),
        ],
    ]
    t_form = Table(formulas, colWidths=[110, 204, 190])
    t_form.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), c_primary),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_form)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 6: LIVE DEMO SCRIPT
    # =========================================================================
    story.append(Paragraph("6. Step-by-Step Live Demo Script for the Panel", h1_style))
    story.append(Paragraph("Follow this order during your live software demonstration:", body_style))
    story.append(Paragraph("1. <b>Navigate to Overview Page:</b> Show the high-level KPI cards and highlight the 4 distinct architectural pillars.", bullet_style))
    story.append(Paragraph("2. <b>Open Crop Recommendation:</b> Select a preset (e.g. <i>Deccan Plateau</i>: N=85, P=40, K=42, pH=6.5, Temp=25°C, Humidity=80%, Rainfall=180mm). Click 'Run Recommendation'. Point out the primary prediction (<b>Rice</b>) and the top-3 confidence bars.", bullet_style))
    story.append(Paragraph("3. <b>Open Yield Prediction:</b> Show how the model predicts continuous harvest in kg/ha (e.g., 2,112 kg/ha) based on crop, state, season, and soil.", bullet_style))
    story.append(Paragraph("4. <b>Open Composite Advisory Page:</b> Set Farm Area to <b>2.5 Acres</b>. Show the complete financial calculation: Total Production (~21.38 Quintals), Revenue (₹78,678), C2 Cost (₹57,017), Net Profit (₹21,660), and ROI (37.99%).", bullet_style))
    story.append(Paragraph("5. <b>Demonstrate Sensitivity Sliders:</b> Slide the market price slider down by 25% to demonstrate how a price crash affects farmer margins, showing the automated break-even warning threshold.", bullet_style))
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 7: TOP 25 VIVA VOCE QUESTIONS & DIRECT ANSWERS
    # =========================================================================
    story.append(Paragraph("7. Master Viva Voce Questions & Technical Answers", h1_style))
    story.append(Paragraph("Categorized into the 5 core areas ML professors prioritize during examinations:", body_style))

    viva_qa = [
        # Domain A: ML Algorithms & Theory
        ("Q1: Why use Machine Learning instead of a traditional rule-based expert system?",
         "Agricultural parameters exhibit continuous, non-linear cross-interactions. For example, high nitrogen with low moisture causes crop burn, whereas the same nitrogen with adequate rainfall boosts yields. Rule-based systems (nested if-else) cannot generalize across 15 agro-climatic zones. Machine learning models like Random Forest and XGBoost learn multi-dimensional hyperplanes and generalize to unseen seasonal variations without brittle hand-coded thresholds."),

        ("Q2: What is the core algorithmic difference between Random Forest and XGBoost?",
         "Random Forest uses Bagging (Bootstrap Aggregating). It builds de-correlated decision trees in parallel on random data subsets and feature sub-spaces, averaging outputs to reduce model variance. XGBoost uses Gradient Boosting. It builds trees sequentially, where each consecutive tree fits to the negative gradient (residuals) of the loss function, aggressively minimizing bias through regularized objective optimization."),

        ("Q3: Why did Random Forest win for Recommendation, while XGBoost won for Yield Prediction?",
         "In Crop Recommendation, the dataset has 2,200 samples across 22 discrete classes with clean botanical clusters. Random Forest's voting ensemble provides stable multi-class boundaries without gradient overshoot. In Yield Prediction, the target is continuous and spans 198,000+ records with high categorical sparsity (states, seasons, soil types). XGBoost's histogram-based gradient boosting and L1/L2 regularization handle sparse categorical interactions and continuous residuals with higher fidelity (R² = 0.8801)."),

        ("Q4: What hyperparameters did you tune for each model?",
         "For Random Forest: n_estimators=100, max_depth=15, and min_samples_split=3 to prevent leaf memorization. For XGBoost Regressor: n_estimators=120, learning_rate=0.08, max_depth=7, subsample=0.85, colsample_bytree=0.85, and tree_method='hist' for fast histogram binning across 198k rows."),

        ("Q5: What is the purpose of subsample and colsample_bytree in XGBoost?",
         "Subsample=0.85 means each tree trains on a random 85% subset of observations. Colsample_bytree=0.85 samples 85% of features per tree. Both act as stochastic regularization, preventing any single dominant feature (such as fertilizer rate) from overpowering all decision splits."),

        # Domain B: Data Preprocessing & Validation
        ("Q6: Did you use synthetic data or fabricate records?",
         "No. 100% of our datasets are empirical records from government agricultural research institutes: 2,200 ICAR recommendation rows, 198,369 DES yield records, Agmarknet APMC market price index (122 commodities), and CACP state cultivation surveys (3,880 records)."),

        ("Q7: What is Target Leakage and how did you prevent it?",
         "Target leakage occurs when future or test-set information leaks into model training (e.g. fitting scalers before train-test splitting). We prevented this by splitting data into 80/20 train-test partitions first, and wrapping StandardScaler and OneHotEncoder inside a scikit-learn ColumnTransformer that is strictly fitted on the training split and only used to transform the test split."),

        ("Q8: Why did you use OneHotEncoder with handle_unknown='ignore'?",
         "In real-world deployment, a user might submit a district or state not present in the historical training slice. By setting handle_unknown='ignore', the one-hot encoder sets all binary flags to 0 instead of throwing an uncaught exception, ensuring inference resilience."),

        ("Q9: How did you clean sensor noise and data anomalies?",
         "We verified zero missing values across feature matrices, clipped negative sensor temperatures to a physiological lower bound of 5.0°C, constrained pH to [3.0, 10.0], parsed clean State names from combined 'Region' strings, and purged non-positive historical yield records."),

        # Domain C: Metrics & Evaluation
        ("Q10: What does an R² score of 0.8801 physically represent?",
         "R² (Coefficient of Determination) represents the proportion of total yield variance explained by the model's predictors (weather, soil, nutrients, fertilizers). An R² of 0.8801 means 88.01% of yield variance across 20 Indian states is captured by our pipeline, with only ~12% left unexplained due to unrecorded micro-factors like flash floods, hail, or localized pest attacks."),

        ("Q11: Why evaluate both RMSE (516.15 kg/ha) and MAE (308.29 kg/ha)?",
         "MAE measures the average absolute prediction error linearly. RMSE squares errors before averaging, penalizing large outliers much more severely. The difference between MAE (308 kg/ha) and RMSE (516 kg/ha) shows that while typical yield errors are small, occasional extreme weather anomalies produce larger residual deviations."),

        ("Q12: Why use Weighted / Macro F1-score rather than raw accuracy?",
         "Accuracy can mask minority class failures. Macro/Weighted F1 computes the harmonic mean of precision and recall for every single crop class, confirming that the model achieves near-perfect discrimination (0.9955) uniformly across all 22 crops, including niche pulses."),

        ("Q13: How did you analyze feature importance?",
         "We extracted the Gini importance (mean decrease in impurity) from Random Forest and gradient gain scores from XGBoost. In crop recommendation, Humidity (22.8%) and Rainfall (21.4%) emerged as the primary environmental determinants, while Fertilizer consumption and seasonal rainfall dominated yield forecasting."),

        # Domain D: Domain & Economic Logic
        ("Q14: What is the difference between Modal Price and Minimum Support Price (MSP)?",
         "MSP is the price floor guaranteed by the Government for 23 mandated crops. Modal Price is the empirical price at which the largest transaction volume took place in the local APMC mandi on that day. We use Modal Price because it reflects the actual market cash flow the farmer will receive."),

        ("Q15: What is CACP C2 Cost and why is it preferred over A2 Cost?",
         "A2 cost only covers paid-out cash expenses (seeds, fertilizer, fuel, hired labor). C2 Comprehensive Cost includes A2 plus the rental value of owned farmland, interest on fixed capital, and the imputed cash value of family labor. C2 is the gold standard recommended by the Swaminathan Commission because it prevents underestimating true farming costs."),

        ("Q16: How do you calculate Break-Even Yield and Break-Even Price?",
         "Break-Even Yield = Total C2 Cost per Hectare / Mandi Price per kg. It shows the minimum harvest volume needed to avoid debt. Break-Even Price = Total Cultivation Cost / Total Production (Quintals). It shows the lowest market rate at which the farmer will not make a loss."),

        ("Q17: If the recommended crop has a poor mandi price, how does the system help?",
         "The Composite Advisory engine detects negative net profit and displays an economic risk warning. The farmer can immediately inspect the Top-3 alternative crops from Stage 1 (along with their confidence probabilities) and run simulated scenarios to pick a profitable alternative."),

        # Domain E: Professor Trap Questions
        ("Q18: Your recommendation accuracy is 99.55%. Is this model severely overfitting?",
         "No, Ma'am. First, 99.55% was measured on an independent 20% holdout test set that the model never saw during training. Second, different agricultural crops have well-separated ecological niches (e.g., Rice requires high water >200mm, Apple requires low temperatures, Cotton requires high potassium and warm weather). Because botanical clusters in 7-dimensional NPK/climate space have distinct separation, the decision boundaries are clean. We validated this with 5-fold cross-validation and confusion matrix diagnostics."),

        ("Q19: Why not use Deep Learning (Neural Networks / Transformers)?",
         "For tabular, structured datasets, multiple peer-reviewed benchmarks (e.g. Grinsztajn et al., NeurIPS 2022) prove that tree-based ensembles (Random Forest and XGBoost) outperform deep neural networks. Tree ensembles handle mixed feature types without artificial embedding layers, remain robust to un-normalized outliers, require zero GPU infrastructure, execute in sub-millisecond latencies, and provide full feature explainability."),

        ("Q20: What happens if a farmer enters an impossible value, like pH = 15 or Rainfall = -50?",
         "We implemented strict agronomic schema validation in `feature_validation.py` using Pydantic v2. Inputs outside physiological bounds (e.g. pH outside 3.0–10.0 or negative rainfall) are intercepted before reaching the ML models, returning a structured HTTP 422 Unprocessable Entity error with user-friendly corrective feedback."),

        ("Q21: How is the backend deployed and how does it prevent concurrency bottlenecks?",
         "The backend is built using FastAPI with asynchronous endpoints (`async def`). Both machine learning models and preprocessing pipelines are loaded once at startup using a thread-safe singleton cache (`joblib`), avoiding repeated disk I/O. Pydantic v2 handles high-speed data validation, supporting hundreds of concurrent requests with bounded memory."),

        ("Q22: Why did you write unit and integration tests for ML models?",
         "ML applications can suffer silent degradation (e.g. wrong unit conversions, label drift, or incorrect one-hot matrix shapes). We built a 66-test automated suite using `pytest` covering agronomic bounds, unit conversions (acres to ha, kg to quintals), market lookup fallbacks, and end-to-end composite inference pipelines, maintaining a 100% pass rate."),

        ("Q23: How would you extend this system into production for millions of farmers?",
         "Future scope includes: 1) Integrating wireless IoT soil telemetry for automated NPK/moisture readings; 2) Ingesting Sentinel-2 satellite NDVI remote sensing for crop health monitoring; 3) 15-day localized weather forecasts via meteorological APIs; and 4) A multilingual voice interface supporting regional Indian languages."),

        ("Q24: What is the unit of yield in the database vs what farmers use?",
         "The scientific model predicts yield in kilograms per hectare (kg/ha). However, Indian farmers measure land in Acres and commercial grain in Quintals (100 kg). The financial engine automatically converts kg/ha into Quintals per Acre and total Quintals harvested."),

        ("Q25: What is the overall social and economic impact of this project?",
         "By combining botanical feasibility with market price forecasting and CACP C2 cost accounting, Karpo transforms agricultural machine learning from an academic classification exercise into an actionable financial risk-mitigation tool for Indian farming communities.")
    ]

    for q_text, a_text in viva_qa:
        q_p = Paragraph(f"<b>{q_text}</b>", q_style)
        a_p = Paragraph(f"<b>Answer:</b> {a_text}", ans_style)
        # Keep each Q&A together so it doesn't get awkwardly split across pages
        story.append(KeepTogether([q_p, a_p, Spacer(1, 4)]))

    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 8: NUMBERS CHEAT SHEET TABLE
    # =========================================================================
    story.append(Paragraph("8. Master Numbers Cheat Sheet (Commit to Memory)", h1_style))
    story.append(Paragraph("Memorize these key statistics for immediate recall during viva:", body_style))

    cheat_data = [
        [Paragraph("<b>Metric / Parameter</b>", table_header_style), Paragraph("<b>Key Value to State</b>", table_header_style), Paragraph("<b>Context / Explanation</b>", table_header_style)],
        [
            Paragraph("<b>Recommendation Model</b>", table_cell_bold),
            Paragraph("Random Forest Classifier", table_cell_style),
            Paragraph("100 estimators, max depth 15, bagging ensemble.", table_cell_style),
        ],
        [
            Paragraph("<b>Recommendation Accuracy</b>", table_cell_bold),
            Paragraph("99.55% (F1 = 0.9955)", table_cell_style),
            Paragraph("Evaluated on 20% holdout test set (440 samples).", table_cell_style),
        ],
        [
            Paragraph("<b>Recommendation Classes</b>", table_cell_bold),
            Paragraph("22 distinct crops", table_cell_style),
            Paragraph("2,200 total records (100 samples per crop class).", table_cell_style),
        ],
        [
            Paragraph("<b>Top Recommendation Drivers</b>", table_cell_bold),
            Paragraph("Humidity (22.8%), Rainfall (21.4%)", table_cell_style),
            Paragraph("Climatic factors dominate over base soil NPK.", table_cell_style),
        ],
        [
            Paragraph("<b>Yield Prediction Model</b>", table_cell_bold),
            Paragraph("XGBoost Regressor", table_cell_style),
            Paragraph("120 trees, lr 0.08, depth 7, histogram method.", table_cell_style),
        ],
        [
            Paragraph("<b>Yield Model R² Score</b>", table_cell_bold),
            Paragraph("0.8801 (88.01% variance explained)", table_cell_style),
            Paragraph("Beats Random Forest Regressor (0.8757).", table_cell_style),
        ],
        [
            Paragraph("<b>Yield Error Metrics</b>", table_cell_bold),
            Paragraph("RMSE = 516.15 kg/ha | MAE = 308.29 kg/ha", table_cell_style),
            Paragraph("Tight clustering along 45° line of identity.", table_cell_style),
        ],
        [
            Paragraph("<b>Yield Historical Records</b>", table_cell_bold),
            Paragraph("198,369 observations", table_cell_style),
            Paragraph("1966–2017 across 309 districts and 20 states.", table_cell_style),
        ],
        [
            Paragraph("<b>Mandi Market Index</b>", table_cell_bold),
            Paragraph("122 commodities (Agmarknet)", table_cell_style),
            Paragraph("Real-world Modal, Min, Max, and MSP prices.", table_cell_style),
        ],
        [
            Paragraph("<b>CACP Cultivation Records</b>", table_cell_bold),
            Paragraph("3,880 state survey records", table_cell_style),
            Paragraph("Comprehensive C2 Cost standard (₹/ha & ₹/Acre).", table_cell_style),
        ],
        [
            Paragraph("<b>Unit Conversion 1</b>", table_cell_bold),
            Paragraph("1 Hectare = 2.47105 Acres", table_cell_style),
            Paragraph("Standard scientific to Indian farm acreage.", table_cell_style),
        ],
        [
            Paragraph("<b>Unit Conversion 2</b>", table_cell_bold),
            Paragraph("1 Quintal = 100 kg", table_cell_style),
            Paragraph("Standard Indian commercial grain trading unit.", table_cell_style),
        ],
        [
            Paragraph("<b>Automated Test Suite</b>", table_cell_bold),
            Paragraph("66 Automated Tests Passing (100%)", table_cell_style),
            Paragraph("Unit, integration, and FastAPI concurrency suites.", table_cell_style),
        ],
    ]
    t_cheat = Table(cheat_data, colWidths=[130, 160, 214])
    t_cheat.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), c_primary),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_cheat)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {output_filename}")


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "docs"
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / "Karpo_ML_Presentation_and_Viva_Defense_Guide.pdf"
    create_presentation_pdf(str(pdf_path))
