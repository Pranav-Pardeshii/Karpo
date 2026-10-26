"""
Formal Academic Mini Project Report Generator for Karpo.
Strictly matches the structure, style, layout, indexing, and typography of:
Pune Vidyarthi Griha's College of Engineering, Technology and Management, Pune - 411009
(Affiliated to Savitribai Phule Pune University).

Contains all 13 required sections:
1. Aim
2. Problem Statement
3. Objectives
4. Libraries/Packages Used
5. Introduction
6. Theory
7. Methodology & Algorithm
8. Architecture Diagram
9. Component Diagram & Endpoints
10. Dataset Details
11. Results and Analysis
12. Conclusion & References
13. Output (Live React Frontend Screenshots)
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
    Image,
)
from reportlab.pdfgen import canvas

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
MODELS_DIR = BASE_DIR / "models"


class AcademicReportCanvas(canvas.Canvas):
    """
    Renders outer page border on every page and exact bottom-right page numbering,
    matching Pune Vidyarthi Griha's College format.
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
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        self.saveState()
        # Draw outer thin rectangular academic border on every page
        self.setStrokeColor(colors.HexColor("#333333"))
        self.setLineWidth(0.8)
        self.rect(36, 36, 612 - 72, 792 - 72)

        # Draw page number on bottom right (inside the border)
        self.setFont("Times-Roman", 10)
        self.setFillColor(colors.HexColor("#000000"))
        page_str = str(self._pageNumber)
        self.drawRightString(612 - 54, 45, page_str)

        self.restoreState()


def build_academic_report():
    output_pdf = DOCS_DIR / "Karpo_Mini_Project_Report.pdf"
    doc = SimpleDocTemplate(
        str(output_pdf),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Academic Typography Styles (Times Roman Standard)
    college_style = ParagraphStyle(
        "CollegeHeader",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.black,
    )

    affil_style = ParagraphStyle(
        "AffiliationHeader",
        parent=styles["Normal"],
        fontName="Times-Italic",
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.black,
        spaceAfter=15,
    )

    cover_report_type = ParagraphStyle(
        "ReportType",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.black,
        spaceBefore=8,
        spaceAfter=8,
    )

    cover_title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=15,
        leading=20,
        alignment=1,
        textColor=colors.black,
        spaceAfter=20,
    )

    cover_author_style = ParagraphStyle(
        "CoverAuthor",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=10.5,
        leading=15,
        alignment=1,
        textColor=colors.black,
    )

    sec_title = ParagraphStyle(
        "AcademicSecTitle",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=13,
        leading=17,
        textColor=colors.black,
        spaceBefore=10,
        spaceAfter=8,
        keepWithNext=True,
    )

    subsec_title = ParagraphStyle(
        "AcademicSubSecTitle",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=11,
        leading=15,
        textColor=colors.black,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
    )

    body = ParagraphStyle(
        "AcademicBody",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=10,
        leading=14.5,
        alignment=4,  # Justified
        textColor=colors.black,
        spaceAfter=8,
    )

    bullet_body = ParagraphStyle(
        "AcademicBullet",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=10,
        leading=14,
        leftIndent=18,
        firstLineIndent=-12,
        textColor=colors.black,
        spaceAfter=4,
    )

    caption_style = ParagraphStyle(
        "FigureCaption",
        parent=styles["Normal"],
        fontName="Times-Italic",
        fontSize=9.5,
        leading=13,
        alignment=1,
        textColor=colors.black,
        spaceBefore=4,
        spaceAfter=8,
    )

    th_style = ParagraphStyle(
        "THStyle",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=9,
        leading=11.5,
        alignment=0,
        textColor=colors.black,
    )

    td_style = ParagraphStyle(
        "TDStyle",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=8.5,
        leading=11,
        textColor=colors.black,
    )

    code_formula_style = ParagraphStyle(
        "CodeFormula",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8.5,
        leading=11,
        textColor=colors.black,
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE PAGE
    # =========================================================================
    pvg_logo_path = DOCS_DIR / "pvg_logo.png"
    if pvg_logo_path.exists():
        story.append(Spacer(1, 15))
        logo_img = Image(str(pvg_logo_path), width=78, height=106)
        logo_img.hAlign = "CENTER"
        story.append(logo_img)
        story.append(Spacer(1, 15))
    else:
        story.append(Spacer(1, 80))

    story.append(Paragraph("Pune Vidyarthi Griha's College of Engineering, Technology and<br/>Management, Pune- 411009.", college_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("(Affiliated to Savitribai Phule Pune University)", affil_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph("Mini Project Report On", cover_report_type))
    story.append(Paragraph('"Karpo: Smart Crop Advisory System using<br/>Machine Learning and Agricultural Economics"', cover_title_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("By", cover_report_type))
    story.append(Paragraph(
        "Pranav Pardeshi: 2044<br/>"
        "Ganesh Rokade: 2043<br/>"
        "Pranali Wadghule: 2060<br/>"
        "Prathamesh Subhedar: 2056",
        cover_author_style
    ))
    story.append(Spacer(1, 18))

    story.append(Paragraph("Under The Guidance of: <b>Prof.Mrs. Vijayalaxmi A. Kanade</b>", cover_author_style))
    story.append(Paragraph("Artificial Intelligence and Data Science Department", cover_author_style))
    story.append(Paragraph("Academic Year: 2026-2027", cover_author_style))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Date of Submission: 22/10/2026", ParagraphStyle("DateStyle", parent=cover_author_style, alignment=0)))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: INDEX
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>INDEX</b>", ParagraphStyle("IndexTitle", fontName="Times-Bold", fontSize=14, leading=18, alignment=1, spaceAfter=15)))

    index_table_data = [
        [Paragraph("<b>Sr.No.</b>", th_style), Paragraph("<b>Topic</b>", th_style), Paragraph("<b>Page No.</b>", th_style)],
        [Paragraph("1", td_style), Paragraph("Aim", td_style), Paragraph("3", td_style)],
        [Paragraph("2", td_style), Paragraph("Problem Statement", td_style), Paragraph("3", td_style)],
        [Paragraph("3", td_style), Paragraph("Objectives", td_style), Paragraph("4", td_style)],
        [Paragraph("4", td_style), Paragraph("Libraries/Packages Used", td_style), Paragraph("5", td_style)],
        [Paragraph("5", td_style), Paragraph("Introduction", td_style), Paragraph("6", td_style)],
        [Paragraph("6", td_style), Paragraph("Theory", td_style), Paragraph("7", td_style)],
        [Paragraph("7", td_style), Paragraph("Methodology", td_style), Paragraph("9", td_style)],
        [Paragraph("8", td_style), Paragraph("Architecture Diagram", td_style), Paragraph("11", td_style)],
        [Paragraph("9", td_style), Paragraph("Component Diagram", td_style), Paragraph("12", td_style)],
        [Paragraph("10", td_style), Paragraph("Dataset Details", td_style), Paragraph("14", td_style)],
        [Paragraph("11", td_style), Paragraph("Results and Analysis", td_style), Paragraph("16", td_style)],
        [Paragraph("12", td_style), Paragraph("Conclusion", td_style), Paragraph("18", td_style)],
        [Paragraph("13", td_style), Paragraph("Output", td_style), Paragraph("19", td_style)],
    ]
    t_index = Table(index_table_data, colWidths=[60, 360, 84])
    t_index.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.6, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t_index)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: 1. AIM & 2. PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("1. Aim", sec_title))
    story.append(Paragraph(
        "The primary aim of this mini project is to design, develop, and evaluate a complete, data-driven "
        "machine learning web application named <b>Karpo</b>. The platform integrates soil chemistry "
        "and meteorological profiling with precision harvest forecasting and agricultural economics. A multi-class "
        "classification pipeline is trained on empirical agro-climatic data to recommend optimal crops from 22 candidates. "
        "A secondary continuous gradient boosted regression engine forecasts expected yields across 198,000+ historical records. "
        "These models are served through an asynchronous FastAPI REST backend and presented through an interactive React 18 single-page "
        "dashboard with TypeScript and Tailwind CSS, dynamically computing farmer revenue, C2 cultivation expenses, net profit, and break-even points.",
        body
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Problem Statement", sec_title))
    story.append(Paragraph(
        "Agriculture forms the livelihood foundation for over 50% of the Indian workforce, yet farmers routinely endure severe "
        "financial distress stemming from three compounding vulnerabilities: biological misjudgments, yield unpredictability, and commercial price volatility.",
        body
    ))
    story.append(Paragraph(
        "First, traditional sowing decisions rely heavily on family convention or outdated regional habits rather than empirical soil nutrient profiling. "
        "Mismatches between soil nitrogen-phosphorus-potassium (NPK) ratios, pH, and shifted monsoon rainfall cause high seedling mortality, stunted growth, and wasted chemical fertilizers.",
        body
    ))
    story.append(Paragraph(
        "Second, farmers lack access to objective, data-driven yield forecasting tools. Without a reliable estimate of expected harvest per acre, farmers are unable "
        "to schedule farm machinery, arrange forward-selling contracts, or evaluate required credit and storage facilities.",
        body
    ))
    story.append(Paragraph(
        "Third, existing agricultural machine learning research suffers from a critical commercial disconnect: academic models output an isolated crop name "
        "(such as 'Watermelon' or 'Rice') but fail to answer the farmer's primary economic concern: <i>Will this crop generate a positive net profit after input expenses?</i> "
        "A biologically viable crop will cause catastrophic bankruptcy if local mandi prices crash or if cultivation costs exceed revenue.",
        body
    ))
    story.append(Paragraph(
        "This project solves the problem by chaining biological classification with non-linear yield regression and official Indian economic databases "
        "(Agmarknet APMC mandi prices and CACP Comprehensive C2 Cultivation Costs) into a single, automated, end-to-end composite advisory workflow.",
        body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: 3. OBJECTIVES
    # =========================================================================
    story.append(Paragraph("3. Objectives", sec_title))
    story.append(Paragraph("The specific academic and engineering objectives of this project are as follows:", body))

    objectives = [
        "1. To acquire, audit, and validate four empirical agricultural databases: Crop Recommendation (2,200 rows), Historical Yield Observations (198,369 rows), Agmarknet APMC Mandi Prices (122 commodities), and CACP Cultivation Cost Surveys (3,880 state records).",
        "2. To preprocess and sanitize agronomic vectors by handling negative sensor anomalies, bounding pH values to [3.0, 10.0], and standardizing state and district geographic nomenclatures.",
        "3. To build strictly leakage-free scikit-learn preprocessing pipelines using ColumnTransformer, StandardScaler, and OneHotEncoder fitted exclusively on training splits.",
        "4. To evaluate and benchmark tree-based ensemble algorithms: Random Forest Classifier versus XGBoost Classifier for multi-class crop recommendation across 22 classes.",
        "5. To develop and evaluate continuous non-linear regression models: XGBoost Regressor versus Random Forest Regressor for crop yield forecasting (kg/ha) across 21 crops and 20 states.",
        "6. To automate hyperparameter configuration and model selection using Macro-F1 for classification and Coefficient of Determination (R<sup>2</sup>) and RMSE for regression.",
        "7. To implement an agricultural economics calculation engine converting scientific yield (kg/ha) into Quintals, computing gross revenues, CACP Comprehensive C2 cultivation costs, net profits, and break-even points in Indian Currency (Rs.).",
        "8. To construct a high-performance, asynchronous REST API backend using FastAPI, Pydantic v2 schemas, and joblib singleton caching for sub-millisecond inference.",
        "9. To build a modern web user interface using React 18, Vite, TypeScript, Tailwind CSS, and Recharts, featuring Overview, Crop Recommendation, Yield Prediction, Market Intelligence, and Composite Advisory pages.",
        "10. To construct a comprehensive automated test suite (unit, integration, and API) with 100% test pass rates validating unit conversions, schema bounds, and composite pipelines.",
    ]
    for obj in objectives:
        story.append(Paragraph(obj, bullet_body))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: 4. LIBRARIES / PACKAGES USED
    # =========================================================================
    story.append(Paragraph("4. Libraries / Packages Used", sec_title))

    packages = [
        ("I. pandas, NumPy and openpyxl (Python):", [
            "&bull; pandas and NumPy are utilized to load, filter, clean, manipulate, and execute vectorized numerical and financial operations across 200,000+ agricultural data rows.",
            "&bull; openpyxl provides robust reading and parsing capabilities for structured Excel and CSV spreadsheets.",
        ]),
        ("II. scikit-learn 1.5+ (Python):", [
            "&bull; Provides ensemble machine learning algorithms: RandomForestClassifier and RandomForestRegressor.",
            "&bull; Provides preprocessing transformers: StandardScaler, OneHotEncoder, LabelEncoder, and ColumnTransformer to eliminate data leakage.",
            "&bull; Supplies evaluation metrics: accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, r2_score, mean_squared_error, and mean_absolute_error.",
        ]),
        ("III. XGBoost 2.1+ (Python):", [
            "&bull; Provides extreme gradient boosting algorithms: XGBClassifier and XGBRegressor.",
            "&bull; Employs histogram-based tree methods ('hist') for high-speed, parallel gradient boosting over 198,000+ records with continuous and sparse one-hot features.",
        ]),
        ("IV. joblib (Python):", [
            "&bull; Efficiently serializes and persists trained machine learning estimators and fitted ColumnTransformer pipelines to disk for zero-overhead runtime loading.",
        ]),
        ("V. FastAPI, Uvicorn, and Pydantic v2:", [
            "&bull; FastAPI structures the modern, asynchronous RESTful API backend.",
            "&bull; Uvicorn acts as the high-throughput ASGI server; Pydantic v2 enforces strict input validation, type coercion, and auto-generates Swagger UI (/docs).",
        ]),
        ("VI. pytest and httpx:", [
            "&bull; Used to author and execute 66 automated unit, integration, and concurrency test suites ensuring numerical stability and domain boundary compliance.",
        ]),
        ("VII. React 18, Vite, TypeScript, Tailwind CSS and Recharts:", [
            "&bull; Powers the modern, responsive single-page frontend application featuring interactive metric cards, sensitivity sliders, and live telemetry.",
            "&bull; React Router DOM manages single-page client routing (/recommend, /yield, /market, /financials, /advisory); Recharts renders interactive visualizations.",
        ]),
        ("VIII. GitHub, Uvicorn Local Daemon & Production Packaging:", [
            "&bull; uv package manager (astral.sh) manages deterministic dependency resolution via uv.lock and PEP 621 pyproject.toml.",
        ]),
    ]

    for title, items in packages:
        story.append(Paragraph(f"<b>{title}</b>", subsec_title))
        for item in items:
            story.append(Paragraph(item, bullet_body))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: 5. INTRODUCTION
    # =========================================================================
    story.append(Paragraph("5. Introduction", sec_title))
    story.append(Paragraph(
        "Precision agriculture leverages modern computational intelligence to replace subjective intuition with empirical evidence. "
        "India encompasses 15 diverse agro-climatic zones, varying from the fertile alluvial Gangetic plains to the arid zones of Rajasthan "
        "and the tropical black-soil Deccan plateau. In this intricate environment, agricultural productivity depends on complex non-linear "
        "relationships between soil macro-nutrients (Nitrogen, Phosphorus, Potassium), soil pH, ambient thermal conditions, relative atmospheric humidity, and monsoon rainfall.",
        body
    ))
    story.append(Paragraph(
        "Historically, farmers made cropping selections based purely on historical local custom or immediate neighbor habits. When erratic monsoon patterns "
        "emerge or soil fertility deteriorates due to prolonged monoculture, this lack of empirical guidance causes catastrophic crop failures. "
        "Furthermore, conventional agricultural extension services operate with severe delays and cannot offer tailored, farm-specific advisories at scale.",
        body
    ))
    story.append(Paragraph(
        "Recent advances in machine learning have demonstrated strong predictive capabilities for crop classification. However, almost all existing academic systems "
        "suffer from severe practical limitations: they terminate at recommending a biological crop name. Recommending a crop without forecasting harvest quantity "
        "or evaluating local APMC mandi market prices leaves the farmer vulnerable to severe market crashes.",
        body
    ))
    story.append(Paragraph(
        "<b>Karpo</b> represents a unified agro-ecological and financial intelligence matrix designed to bridge this divide. The system operates as a cohesive dual-engine pipeline: "
        "first, an ensemble classifier evaluates soil and climate parameters to identify the most biologically compatible crop. Second, a continuous gradient boosted regressor "
        "trained on decades of district-level harvest records forecasts productivity. Finally, an economic optimization engine queries live mandi prices and CACP C2 comprehensive "
        "cultivation costs to simulate net profit, return on investment (ROI %), and break-even safety buffers before planting begins.",
        body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: 6. THEORY (PART 1)
    # =========================================================================
    story.append(Paragraph("6. Theory", sec_title))
    story.append(Paragraph(
        "<b>Supervised Multiclass Classification and Regression:</b><br/>"
        "In supervised machine learning, models learn predictive mappings from multidimensional feature vectors X to ground-truth targets y. "
        "Karpo combines two distinct supervised paradigms: multiclass classification (for discrete crop choice from 22 classes) and continuous regression (for harvest productivity in kg/ha).",
        body
    ))

    story.append(Paragraph("<b>Classifiers and Regressors Compared:</b>", subsec_title))

    alg_table_data = [
        [Paragraph("<b>Algorithm</b>", th_style), Paragraph("<b>Core Theoretical Concept</b>", th_style), Paragraph("<b>Application in Karpo</b>", th_style)],
        [
            Paragraph("<b>Random Forest</b>", td_style),
            Paragraph("Bagging ensemble that constructs de-correlated decision trees on bootstrap samples. Aggregates outputs via majority vote or mean pooling to aggressively minimize variance.", td_style),
            Paragraph("Selected for Crop Recommendation (99.55% accuracy) due to robust multi-class boundaries across 22 crops.", td_style),
        ],
        [
            Paragraph("<b>XGBoost</b>", td_style),
            Paragraph("Boosting ensemble that sequentially minimizes regularized residual loss using gradient descent. Tree growth incorporates L1/L2 penalties and histogram feature binning.", td_style),
            Paragraph("Selected for Yield Forecasting (R<sup>2</sup> = 0.8801) due to superior handling of sparse one-hot categories and non-linear interactions.", td_style),
        ],
    ]
    t_alg = Table(alg_table_data, colWidths=[90, 240, 174])
    t_alg.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_alg)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Preprocessing & Leakage Prevention:</b>", subsec_title))
    story.append(Paragraph("&bull; <b>StandardScaler:</b> Rescales continuous features to zero mean and unit variance: z = (x - mu) / sigma. Prevents features with large numerical magnitudes (such as rainfall in mm) from dominating distance splits.", bullet_body))
    story.append(Paragraph("&bull; <b>OneHotEncoder:</b> Transforms nominal categorical features (Crop, Season, Soil, State) into binary indicators. Configured with <code>handle_unknown='ignore'</code> to ensure runtime inference resilience against unseen categories.", bullet_body))
    story.append(Paragraph("&bull; <b>ColumnTransformer:</b> Bundles scalers and encoders into an integrated object, strictly fitted on training splits to prevent data leakage.", bullet_body))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Stratified & Random K-Fold Cross-Validation:</b>", subsec_title))
    story.append(Paragraph(
        "For classification, Stratified 5-Fold Cross-Validation preserves exact class proportions across all validation folds, ensuring unbiased evaluation across all 22 crops. "
        "For regression, 5-Fold cross-validation over 198k records guarantees that the regressor does not overfit to regional or temporal harvest anomalies.",
        body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: 6. THEORY (PART 2 - REFINED METRICS & ECONOMIC EQUATIONS)
    # =========================================================================
    story.append(Paragraph("<b>Evaluation Metrics:</b>", subsec_title))
    story.append(Paragraph("&bull; <b>Accuracy:</b> The fraction of all crop predictions that are correct: (TP + TN) / (P + N).", bullet_body))
    story.append(Paragraph("&bull; <b>Precision & Recall:</b> Precision measures the purity of positive predictions; Recall measures the coverage of actual instances.", bullet_body))
    story.append(Paragraph("&bull; <b>Macro-F1 Score:</b> Unweighted harmonic mean of per-class F1 scores. Every crop variety counts equally, preventing majority dominance.", bullet_body))
    story.append(Paragraph("&bull; <b>R<sup>2</sup> Score (Goodness of Fit):</b> Proportion of variance in crop yield explained by the predictors: R<sup>2</sup> = 1 - (SS_res / SS_tot).", bullet_body))
    story.append(Paragraph("&bull; <b>RMSE & MAE:</b> RMSE penalizes large outlier errors quadratically; MAE measures average absolute error linearly.", bullet_body))

    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Agricultural Economics & CACP C2 Cost Standard:</b>", subsec_title))
    story.append(Paragraph(
        "A critical innovation of this project is the integration of official agricultural economic metrics. In India, the Commission for Agricultural Costs and Prices (CACP) "
        "and Directorate of Economics and Statistics (DES) define three distinct cultivation cost measures:<br/>"
        "&bull; <b>A2 Cost:</b> Covers only actual out-of-pocket expenses (seeds, chemical fertilizers, pesticides, hired human labor, tractor/machinery fuel).<br/>"
        "&bull; <b>A2 + FL Cost:</b> Encompasses A2 cash costs plus the imputed economic value of unpaid family labor.<br/>"
        "&bull; <b>C2 Comprehensive Cost:</b> The complete economic standard. It incorporates A2+FL costs <i>plus</i> the imputed rental value of owned agricultural land "
        "and interest on owned fixed capital assets. Karpo strictly adopts C2 Comprehensive Cost to prevent underestimating true farming liabilities.",
        body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Economic Equations & Formulations:</b>", subsec_title))

    econ_table_data = [
        [Paragraph("<b>#</b>", th_style), Paragraph("<b>Economic Parameter</b>", th_style), Paragraph("<b>Mathematical Formulation</b>", th_style), Paragraph("<b>Units</b>", th_style)],
        [Paragraph("1", td_style), Paragraph("Area Normalization", td_style), Paragraph("Area(ha) = Area(Acres) / 2.47105", code_formula_style), Paragraph("Hectares", td_style)],
        [Paragraph("2", td_style), Paragraph("Total Production", td_style), Paragraph("Production(Q) = [Yield(kg/ha) * Area(ha)] / 100", code_formula_style), Paragraph("Quintals", td_style)],
        [Paragraph("3", td_style), Paragraph("Gross Revenue", td_style), Paragraph("Gross_Revenue = Production(Q) * Modal_Price", code_formula_style), Paragraph("Rs. (INR)", td_style)],
        [Paragraph("4", td_style), Paragraph("Cultivation Cost", td_style), Paragraph("Total_Cost = Area(ha) * C2_Cost_per_Hectare", code_formula_style), Paragraph("Rs. (INR)", td_style)],
        [Paragraph("5", td_style), Paragraph("Net Farm Profit", td_style), Paragraph("Net_Profit = Gross_Revenue - Total_Cost", code_formula_style), Paragraph("Rs. (INR)", td_style)],
        [Paragraph("6", td_style), Paragraph("Return on Investment", td_style), Paragraph("ROI(%) = [Net_Profit / Total_Cost] * 100", code_formula_style), Paragraph("Percentage (%)", td_style)],
        [Paragraph("7", td_style), Paragraph("Break-Even Yield", td_style), Paragraph("BE_Yield(kg/ha) = Cost_per_ha / Price_per_kg", code_formula_style), Paragraph("kg/Hectare", td_style)],
        [Paragraph("8", td_style), Paragraph("Break-Even Price", td_style), Paragraph("BE_Price = Total_Cost / Production(Q)", code_formula_style), Paragraph("Rs. / Quintal", td_style)],
    ]
    t_econ = Table(econ_table_data, colWidths=[20, 115, 275, 94])
    t_econ.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_econ)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: 7. METHODOLOGY (PART 1)
    # =========================================================================
    story.append(Paragraph("7. Methodology", sec_title))
    story.append(Paragraph("The research and implementation methodology followed for engineering Karpo is divided into ten systematic phases:", body))

    phases = [
        ("1. Data Collection & Empirical Curation:",
         "Four authentic agricultural datasets were acquired: Crop_recommendation.csv (2,200 records), crop_yield_dataset.csv (198,369 records), india-crop-prices.csv (122 commodities), and cost-of-cultivation.csv (3,880 CACP state records). Zero synthetic data was used."),
        ("2. Data Auditing & Agronomic Cleaning:",
         "Feature columns were verified against physical agronomic bounds. Duplicate rows were removed. Negative sensor temperature anomalies were clipped to 5.0 deg C; pH values were bounded to [3.0, 10.0]. Combined district-state strings were parsed into standardized regional labels."),
        ("3. Train/Test Data Partitioning:",
         "For crop recommendation, a stratified 80/20 train-test split (1,760 train, 440 test) was established using random_state=42. For yield regression, an 80/20 split over 198k records was created."),
        ("4. Pipeline Preprocessing & Feature Engineering:",
         "Pipelines were constructed bundling StandardScaler for numerical features and OneHotEncoder for categorical variables (Crop, Season, Soil Type, State) inside a scikit-learn ColumnTransformer."),
        ("5. Model Training & Cross-Validation:",
         "Ensemble classifiers (Random Forest vs XGBoost) and continuous regressors (XGBoost vs Random Forest) were trained and evaluated using 5-fold cross-validation on training folds."),
        ("6. Automated Selection of Winning Estimators:",
         "Random Forest Classifier was selected for crop recommendation (Macro-F1: 0.9955, Accuracy: 99.55%). XGBoost Regressor was selected for yield forecasting (R<sup>2</sup> = 0.8801, RMSE: 516.15 kg/ha)."),
        ("7. Artifact Serialization & Registry:",
         "Best fitted estimators, fitted transformers, label mappings, and training_metrics.json were serialized to disk using joblib."),
        ("8. Asynchronous Backend API (FastAPI):",
         "A high-performance REST API was constructed using FastAPI. Endpoints (/recommend, /yield, /advisory/composite) load models via singleton memory caches and validate inputs via Pydantic v2."),
        ("9. Frontend Implementation (React 18 + Vite & TypeScript):",
         "An industrial React 18 single-page dashboard with TypeScript, Tailwind CSS, and Recharts was built, featuring live telemetry and interactive sensitivity modeling."),
        ("10. Automated Testing & Verification:",
         "A 66-test automated suite was built using pytest, achieving a 100% test pass rate across unit, integration, and API suites."),
    ]

    for p_title, p_desc in phases:
        story.append(Paragraph(f"<b>{p_title}</b>", subsec_title))
        story.append(Paragraph(p_desc, body))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: 7. METHODOLOGY (ALGORITHM)
    # =========================================================================
    story.append(Paragraph("<b>Composite Advisory Execution Algorithm:</b>", subsec_title))

    algo_steps = [
        "1. Start.",
        "2. Ingest user inputs: Soil NPK (kg/ha), pH, Temperature ( deg C), Humidity (%), Rainfall (mm), State, Season, Soil Type, and Farm Acreage.",
        "3. Validate all inputs against physiological bounds via Pydantic schema (raise HTTP 422 if invalid).",
        "4. Standardize input area into scientific Hectares: Area(ha) = Area(Acres) / 2.47105.",
        "5. Preprocess 7-dimensional soil/weather vector using fitted StandardScaler.",
        "6. Execute Random Forest classification inference: predict primary recommended crop label and extract class probabilities.",
        "7. Sort probability vector to identify Top-3 alternative crop candidates with percentage confidence scores.",
        "8. Map recommended crop to canonical yield/mandi index key via canonical mapping dictionary.",
        "9. Construct regression feature vector: [Crop, Season, Soil Type, State, N, P, K, Temp, Humidity, Rainfall, pH, Fertilizer, Pesticide].",
        "10. Transform regression vector through fitted ColumnTransformer (StandardScaler + OneHotEncoder).",
        "11. Execute XGBoost regression inference: compute predicted yield in kg/hectare.",
        "12. Query Agmarknet database for modal market price (Rs./Quintal) and Minimum Support Price (MSP).",
        "13. Query CACP database for state-specific Comprehensive C2 Cultivation Cost (Rs./Hectare).",
        "14. Calculate total harvest production in Quintals: Production(Q) = [Yield(kg/ha) * Area(ha)] / 100.",
        "15. Calculate Gross Revenue: Revenue(Rs.) = Production(Q) * Modal Price(Rs./Q).",
        "16. Calculate Total Cultivation Cost: Cost(Rs.) = Area(ha) * C2 Cost per Hectare.",
        "17. Calculate Net Profit: Profit(Rs.) = Gross Revenue - Total Cost.",
        "18. Calculate Return on Investment: ROI(%) = [Profit / Total Cost] * 100.",
        "19. Calculate Break-Even Yield: BE_Yield(kg/ha) = Cost per Hectare / Price per kg.",
        "20. Calculate Break-Even Price: BE_Price(Rs./Q) = Total Cost / Total Production.",
        "21. Package response payload and return to React presentation layer.",
        "22. End.",
    ]
    for step in algo_steps:
        story.append(Paragraph(step, bullet_body))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: 8. ARCHITECTURE DIAGRAM
    # =========================================================================
    story.append(Paragraph("8. Architecture Diagram", sec_title))
    arch_img_path = DOCS_DIR / "fig_architecture.png"
    if arch_img_path.exists():
        img = Image(str(arch_img_path), width=420, height=440)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Paragraph("Figure 8.1: System architecture of Karpo Smart Crop Advisory System", caption_style))

    story.append(Paragraph("The system architecture comprises the following seven modular layers:", subsec_title))
    arch_modules = [
        "&bull; <b>1. Agricultural Datasets:</b> Verified empirical repositories supplying training samples, mandi rates, and CACP costs.",
        "&bull; <b>2. Data Preparation & Validation:</b> Intercepts noise, handles bounds checking, and structures pipelines to eliminate data leakage.",
        "&bull; <b>3. Train-Test Splits:</b> Enforces reproducible 80/20 train-test partitions for classification and regression.",
        "&bull; <b>4. Model Training & Evaluation:</b> Parallel benchmarking of Random Forest and XGBoost with automated selection.",
        "&bull; <b>5. Serialized Artifact Storage:</b> Thread-safe joblib serialization storing estimators and preprocessor pipelines.",
        "&bull; <b>6. FastAPI Backend:</b> Asynchronous REST service exposing high-speed prediction and financial endpoints.",
        "&bull; <b>7. Delivery Layer:</b> Production React 18 / TypeScript frontend with brutalist telemetry and Recharts graphs.",
    ]
    for m in arch_modules:
        story.append(Paragraph(m, bullet_body))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: 9. COMPONENT DIAGRAM
    # =========================================================================
    story.append(Paragraph("9. Component Diagram", sec_title))
    comp_img_path = DOCS_DIR / "fig_component.png"
    if comp_img_path.exists():
        img = Image(str(comp_img_path), width=420, height=360)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Paragraph("Figure 9.1: Component diagram of Karpo Smart Crop Advisory System", caption_style))

    comp_modules = [
        "&bull; <b>1. Model Training Engine (scripts/train_models.py):</b> Reads datasets, evaluates models, and exports joblib artifacts.",
        "&bull; <b>2. Datasets Storage (datasets/*.csv):</b> Contains 100% empirical historical data from official agricultural portals.",
        "&bull; <b>3. Serialized Artifacts (models/):</b> Persists fitted models, ColumnTransformers, and training metrics JSON.",
        "&bull; <b>4. FastAPI Backend (src/crop_advisory/api):</b> Manages application lifespan, dependency injection, and routing.",
        "&bull; <b>5. React Frontend (frontend/src):</b> Single-page application providing rich visualization and scenario modeling.",
        "&bull; <b>6. Interactive API Docs:</b> Swagger UI (/docs) and ReDoc (/redoc) automatically generated from Pydantic schemas.",
    ]
    for cm in comp_modules:
        story.append(Paragraph(cm, bullet_body))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: 9. COMPONENT DIAGRAM (API ENDPOINTS TABLE)
    # =========================================================================
    story.append(Paragraph("<b>Main REST API Endpoints:</b>", subsec_title))

    api_endpoints_data = [
        [Paragraph("<b>Method</b>", th_style), Paragraph("<b>Endpoint Path</b>", th_style), Paragraph("<b>Description & Functionality</b>", th_style)],
        [Paragraph("GET", td_style), Paragraph("/health", td_style), Paragraph("System health diagnostics, uptime, and loaded model verification.", td_style)],
        [Paragraph("GET", td_style), Paragraph("/api/v1/meta/crops", td_style), Paragraph("Retrieves list of 22 supported crops, scientific names, and state aliases.", td_style)],
        [Paragraph("POST", td_style), Paragraph("/api/v1/recommend", td_style), Paragraph("Recommends optimal crop from 7 NPK/weather features (Random Forest, 99.55%).", td_style)],
        [Paragraph("POST", td_style), Paragraph("/api/v1/yield", td_style), Paragraph("Forecasts crop yield in kg/ha and Quintals/Acre (XGBoost Regressor).", td_style)],
        [Paragraph("GET", td_style), Paragraph("/api/v1/market/prices", td_style), Paragraph("Queries modal mandi price, min, max, and MSP from Agmarknet database.", td_style)],
        [Paragraph("GET", td_style), Paragraph("/api/v1/costs/cultivation", td_style), Paragraph("Queries state-specific CACP Comprehensive C2 Cultivation Costs.", td_style)],
        [Paragraph("POST", td_style), Paragraph("/api/v1/advisory/composite", td_style), Paragraph("End-to-end composite pipeline: recommendation + yield + C2 financial simulation.", td_style)],
        [Paragraph("POST", td_style), Paragraph("/api/v1/simulate/sensitivity", td_style), Paragraph("Simulates price and yield volatility (+/- 40%) to calculate break-even risk.", td_style)],
    ]
    t_api = Table(api_endpoints_data, colWidths=[60, 160, 284])
    t_api.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_api)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: 10. DATASET DETAILS (PART 1)
    # =========================================================================
    story.append(Paragraph("10. Dataset Details", sec_title))

    ds_table_data = [
        [Paragraph("<b>Dataset Property</b>", th_style), Paragraph("<b>Detailed Specification</b>", th_style)],
        [Paragraph("Dataset 1 Name", td_style), Paragraph("Crop Recommendation Dataset (Crop_recommendation.csv)", td_style)],
        [Paragraph("Dataset 1 Source", td_style), Paragraph("ICAR / Indian Agronomic Field Research Repository", td_style)],
        [Paragraph("Dataset 1 Records", td_style), Paragraph("2,200 samples (100 samples per crop class = perfectly balanced)", td_style)],
        [Paragraph("Dataset 1 Features", td_style), Paragraph("7 numerical features (N, P, K, Temperature, Humidity, pH, Rainfall)", td_style)],
        [Paragraph("Dataset 1 Target", td_style), Paragraph("Multi-Class Crop Target (22 distinct agricultural commodities)", td_style)],
        [Paragraph("Dataset 2 Name", td_style), Paragraph("Historical Crop Yield Dataset (crop_yield_dataset.csv)", td_style)],
        [Paragraph("Dataset 2 Source", td_style), Paragraph("Directorate of Economics & Statistics (DES), Ministry of Agriculture", td_style)],
        [Paragraph("Dataset 2 Records", td_style), Paragraph("198,369 historical district-level observations (1966 to 2017)", td_style)],
        [Paragraph("Dataset 2 Features", td_style), Paragraph("4 categorical features (Crop, Season, Soil Type, State) + 9 continuous features", td_style)],
        [Paragraph("Dataset 2 Target", td_style), Paragraph("Continuous Yield in kg/hectare (Range: 0.01 to 58,363 kg/ha)", td_style)],
        [Paragraph("Dataset 3 Name", td_style), Paragraph("India APMC Mandi Crop Prices (india-crop-prices.csv)", td_style)],
        [Paragraph("Dataset 3 Records", td_style), Paragraph("122 commodities with real modal prices, price bounds, and MSP rates", td_style)],
        [Paragraph("Dataset 4 Name", td_style), Paragraph("CACP Cost of Cultivation (cost-of-cultivation.csv)", td_style)],
        [Paragraph("Dataset 4 Records", td_style), Paragraph("3,880 state survey records detailing Comprehensive C2 Costs and inputs", td_style)],
        [Paragraph("Missing Values", td_style), Paragraph("Zero null entries across all processed feature matrices", td_style)],
        [Paragraph("Random Seed", td_style), Paragraph("Fixed seed = 42 for complete reproducibility across all splits", td_style)],
    ]
    t_ds = Table(ds_table_data, colWidths=[150, 354])
    t_ds.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_ds)
    story.append(Spacer(1, 10))

    dist_img_path = DOCS_DIR / "fig_class_distribution.png"
    if dist_img_path.exists():
        img = Image(str(dist_img_path), width=480, height=200)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Paragraph("Figure 10.1: Balanced class distribution across 22 crops in recommendation dataset", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: 10. DATASET DETAILS (INPUT FEATURES SPECIFICATION)
    # =========================================================================
    story.append(Paragraph("<b>Input Features Specification (16 Total System Variables):</b>", subsec_title))

    feat_table_data = [
        [Paragraph("<b>#</b>", th_style), Paragraph("<b>Feature Name</b>", th_style), Paragraph("<b>Agronomic Meaning & Scientific Units</b>", th_style), Paragraph("<b>Valid Bounds</b>", th_style)],
        [Paragraph("1", td_style), Paragraph("Nitrogen (N)", td_style), Paragraph("Ratio of Nitrogen content in soil (kg/ha)", td_style), Paragraph("0 - 140", td_style)],
        [Paragraph("2", td_style), Paragraph("Phosphorus (P)", td_style), Paragraph("Ratio of Phosphorus content in soil (kg/ha)", td_style), Paragraph("5 - 145", td_style)],
        [Paragraph("3", td_style), Paragraph("Potassium (K)", td_style), Paragraph("Ratio of Potassium content in soil (kg/ha)", td_style), Paragraph("5 - 205", td_style)],
        [Paragraph("4", td_style), Paragraph("Temperature", td_style), Paragraph("Ambient surface temperature in degrees Celsius ( deg C)", td_style), Paragraph("8.8 - 45.0", td_style)],
        [Paragraph("5", td_style), Paragraph("Humidity", td_style), Paragraph("Relative atmospheric moisture percentage (%)", td_style), Paragraph("14.0 - 100.0", td_style)],
        [Paragraph("6", td_style), Paragraph("Soil pH", td_style), Paragraph("Negative log of hydrogen ion activity (acidity/alkalinity)", td_style), Paragraph("3.5 - 9.9", td_style)],
        [Paragraph("7", td_style), Paragraph("Rainfall", td_style), Paragraph("Total seasonal precipitation depth in millimeters (mm)", td_style), Paragraph("20.0 - 300.0", td_style)],
        [Paragraph("8", td_style), Paragraph("Crop Type", td_style), Paragraph("Identity of crop (Rice, Wheat, Sugarcane, Cotton, etc.)", td_style), Paragraph("21 categories", td_style)],
        [Paragraph("9", td_style), Paragraph("Cropping Season", td_style), Paragraph("Agricultural cropping cycle (Kharif, Rabi, Summer, Whole Year)", td_style), Paragraph("4 categories", td_style)],
        [Paragraph("10", td_style), Paragraph("Soil Type", td_style), Paragraph("Taxonomic soil order (Vertisols, Inceptisols, Alfisols, etc.)", td_style), Paragraph("6 orders", td_style)],
        [Paragraph("11", td_style), Paragraph("State", td_style), Paragraph("Indian state jurisdiction (Maharashtra, UP, Punjab, etc.)", td_style), Paragraph("20 states", td_style)],
        [Paragraph("12", td_style), Paragraph("Fertilizer Rate", td_style), Paragraph("Chemical fertilizer application consumption (kg/ha)", td_style), Paragraph("0 - 500", td_style)],
        [Paragraph("13", td_style), Paragraph("Pesticide Rate", td_style), Paragraph("Chemical pesticide application consumption (kg/ha)", td_style), Paragraph("0 - 50", td_style)],
        [Paragraph("14", td_style), Paragraph("Farm Area", td_style), Paragraph("Physical landholding size input by farmer (Acres/ha)", td_style), Paragraph("> 0.01", td_style)],
        [Paragraph("15", td_style), Paragraph("Modal Price", td_style), Paragraph("Most frequently traded price in local APMC (Rs./Quintal)", td_style), Paragraph("Agmarknet Index", td_style)],
        [Paragraph("16", td_style), Paragraph("C2 Cost", td_style), Paragraph("Comprehensive cost of cultivation benchmark (Rs./ha)", td_style), Paragraph("CACP Index", td_style)],
    ]
    t_feat = Table(feat_table_data, colWidths=[24, 95, 295, 90])
    t_feat.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_feat)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 16: 11. RESULTS AND ANALYSIS (PART 1 - BENCHMARKS)
    # =========================================================================
    story.append(Paragraph("11. Results and Analysis", sec_title))
    story.append(Paragraph("<b>Model Benchmarking & Selection:</b>", subsec_title))

    res_comp_data = [
        [Paragraph("<b>Pipeline Task</b>", th_style), Paragraph("<b>Evaluated Model</b>", th_style), Paragraph("<b>Primary Metric</b>", th_style), Paragraph("<b>Secondary Metric</b>", th_style), Paragraph("<b>Selection Status</b>", th_style)],
        [
            Paragraph("Crop Recommendation", td_style),
            Paragraph("<b>Random Forest Classifier</b>", td_style),
            Paragraph("<b>Accuracy = 99.55%</b>", td_style),
            Paragraph("Macro-F1 = 0.9955", td_style),
            Paragraph(" <b>Selected Model</b>", td_style),
        ],
        [
            Paragraph("Crop Recommendation", td_style),
            Paragraph("XGBoost Classifier", td_style),
            Paragraph("Accuracy = 99.09%", td_style),
            Paragraph("Macro-F1 = 0.9909", td_style),
            Paragraph("Baseline", td_style),
        ],
        [
            Paragraph("Yield Forecasting", td_style),
            Paragraph("<b>XGBoost Regressor</b>", td_style),
            Paragraph("<b>R<sup>2</sup> Score = 0.8801</b>", td_style),
            Paragraph("<b>RMSE = 516.15 kg/ha</b>", td_style),
            Paragraph(" <b>Selected Model</b>", td_style),
        ],
        [
            Paragraph("Yield Forecasting", td_style),
            Paragraph("Random Forest Regressor", td_style),
            Paragraph("R<sup>2</sup> Score = 0.8757", td_style),
            Paragraph("RMSE = 525.41 kg/ha", td_style),
            Paragraph("Baseline", td_style),
        ],
    ]
    t_res_comp = Table(res_comp_data, colWidths=[110, 120, 110, 95, 69])
    t_res_comp.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_res_comp)
    story.append(Spacer(1, 8))

    model_comp_img = DOCS_DIR / "fig_model_comparison.png"
    if model_comp_img.exists():
        img = Image(str(model_comp_img), width=480, height=195)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Paragraph("Figure 11.1: Side-by-side performance comparison for classification and regression", caption_style))

    story.append(Paragraph(
        "<b>Analysis:</b> Random Forest outperformed XGBoost in multi-class crop recommendation because bagging ensembles create smooth "
        "decision hyperplanes across balanced 22-class clusters without sensitive gradient hyperparameter tuning. Conversely, XGBoost achieved "
        "a superior R<sup>2</sup> of 0.8801 and lower RMSE (516.15 kg/ha) on yield forecasting because gradient boosted trees minimize residuals sequentially "
        "and handle sparse one-hot encoded categories and complex nutrient-weather interactions with higher accuracy.",
        body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 17: 11. RESULTS AND ANALYSIS (HEATMAPS & ERROR PLOTS)
    # =========================================================================
    story.append(Paragraph("<b>Diagnostic Artifacts:</b>", subsec_title))

    cm_img_path = MODELS_DIR / "crop_rec_confusion_matrix.png"
    if cm_img_path.exists():
        img_cm = Image(str(cm_img_path), width=320, height=270)
        img_cm.hAlign = "CENTER"
        story.append(img_cm)
        story.append(Paragraph("Figure 11.2: Confusion matrix heatmap for 22 crops (Test Accuracy: 99.55%)", caption_style))

    story.append(Spacer(1, 4))
    yp_img_path = MODELS_DIR / "yield_actual_vs_predicted.png"
    if yp_img_path.exists():
        img_yp = Image(str(yp_img_path), width=300, height=230)
        img_yp.hAlign = "CENTER"
        story.append(img_yp)
        story.append(Paragraph("Figure 11.3: Actual versus predicted yield scatter plot along 45 deg line of identity", caption_style))

    story.append(Paragraph(
        "<b>Observations:</b> The confusion matrix exhibits near-perfect diagonal concentration across all 22 crops. "
        "The actual vs predicted yield scatter plot shows tight clustering along the red 45-degree line of identity, "
        "confirming that the XGBoost regressor generalizes effectively across rainfed, irrigated, and high-yielding cash crops.",
        body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 18: 12. CONCLUSION & REFERENCES
    # =========================================================================
    story.append(Paragraph("12. Conclusion", sec_title))
    story.append(Paragraph(
        "This project successfully engineered and validated an end-to-end agro-ecological and financial advisory web application named <b>Karpo</b>. "
        "By chaining multi-class botanical recommendation with non-linear yield regression and empirical economic datasets, the platform overcomes "
        "the commercial disconnect that limits traditional agricultural machine learning research.",
        body
    ))
    story.append(Paragraph(
        "The primary crop recommendation engine achieved <b>99.55% test accuracy</b> using Random Forest across 22 crops, with humidity and rainfall "
        "emerging as the dominant environmental predictors. The secondary yield forecasting engine achieved an <b>R<sup>2</sup> of 0.8801</b> and an RMSE of <b>516.15 kg/ha</b> "
        "using XGBoost over 198,369 historical harvest records. The economic engine converts these predictions into actionable farm economics using official "
        "CACP Comprehensive C2 Cultivation Costs and Agmarknet APMC modal prices, computing net profit, ROI %, and break-even thresholds.",
        body
    ))
    story.append(Paragraph(
        "<b>Project Limitations:</b> Current inputs rely on manually entered laboratory soil values; satellite NDVI vegetative health feeds are not yet automated; "
        "and seasonal pest outbreaks are not dynamically tracked.",
        body
    ))
    story.append(Paragraph(
        "<b>Future Scope:</b><br/>"
        "1. Direct wireless IoT soil telemetry integration for automated real-time NPK and moisture sensing.<br/>"
        "2. Ingestion of European Space Agency Sentinel-2 satellite imagery for remote vegetative index (NDVI) monitoring.<br/>"
        "3. Integration of deep learning weather forecasting models (LSTM / Transformers) for 15-day localized micro-climate forecasts.<br/>"
        "4. Development of a multilingual voice interface supporting Marathi, Hindi, and regional vernacular languages for rural accessibility.",
        body
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>References:</b>", subsec_title))
    refs = [
        "1. Directorate of Economics and Statistics (DES), Ministry of Agriculture & Farmers Welfare, Government of India. 'Cost of Cultivation of Principal Crops in India (CACP C2 Reports)'.",
        "2. Agmarknet (Agricultural Marketing Information Network), Ministry of Agriculture, Government of India. 'Mandi Market Commodity Price Bulletin'.",
        "3. Koklu, M. and Ozkan, I. A. (2020). 'Multiclass Classification of Dry Beans Using Computer Vision and Machine Learning Techniques.' Computers and Electronics in Agriculture, 174, 105507.",
        "4. Chen, T. and Guestrin, C. (2016). 'XGBoost: A Scalable Tree Boosting System.' In Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '16), pp. 785-794.",
        "5. Breiman, L. (2001). 'Random Forests.' Machine Learning, 45(1), pp. 5-32.",
        "6. Grinsztajn, L., Oyallon, E., and Varoquaux, G. (2022). 'Why do tree-based models still outperform deep learning on typical tabular data?' Advances in Neural Information Processing Systems (NeurIPS 2022).",
    ]
    for r in refs:
        story.append(Paragraph(r, bullet_body))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 19: 13. OUTPUT (PART 1 - REACT OVERVIEW & CROP RECOMMENDATION)
    # =========================================================================
    story.append(Paragraph("13. Output", sec_title))
    story.append(Paragraph("The software platform exposes a production-ready React 18 single-page application built with TypeScript, Vite, and Tailwind CSS:", body))

    react_overview_path = DOCS_DIR / "react_overview.png"
    if react_overview_path.exists():
        img_ov = Image(str(react_overview_path), width=480, height=255)
        img_ov.hAlign = "CENTER"
        story.append(img_ov)
        story.append(Paragraph("Figure 13.1: Overview Dashboard of Karpo React Application", caption_style))

    story.append(Spacer(1, 6))
    react_rec_path = DOCS_DIR / "react_recommend.png"
    if react_rec_path.exists():
        img_rec = Image(str(react_rec_path), width=480, height=255)
        img_rec.hAlign = "CENTER"
        story.append(img_rec)
        story.append(Paragraph("Figure 13.2: Crop Recommendation Page with 7-feature input form and confidence scores", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 20: 13. OUTPUT (PART 2 - REACT YIELD & COMPOSITE ADVISORY)
    # =========================================================================
    react_yield_path = DOCS_DIR / "react_yield.png"
    if react_yield_path.exists():
        img_y = Image(str(react_yield_path), width=480, height=255)
        img_y.hAlign = "CENTER"
        story.append(img_y)
        story.append(Paragraph("Figure 13.3: Precision Crop Yield Prediction Page with Agronomic Feature Selectors", caption_style))

    story.append(Spacer(1, 6))
    react_adv_path = DOCS_DIR / "react_advisory.png"
    if react_adv_path.exists():
        img_adv = Image(str(react_adv_path), width=480, height=255)
        img_adv.hAlign = "CENTER"
        story.append(img_adv)
        story.append(Paragraph("Figure 13.4: Composite Advisory Page with Chained Machine Learning and Financial KPIs", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 21: 13. OUTPUT (PART 3 - REACT FINANCIALS & MARKET INTELLIGENCE)
    # =========================================================================
    react_fin_path = DOCS_DIR / "react_financials.png"
    if react_fin_path.exists():
        img_fin = Image(str(react_fin_path), width=480, height=255)
        img_fin.hAlign = "CENTER"
        story.append(img_fin)
        story.append(Paragraph("Figure 13.5: Farm Financial Analysis Page with Net Profit, ROI %, and Break-Even Thresholds", caption_style))

    story.append(Spacer(1, 6))
    react_mkt_path = DOCS_DIR / "react_market.png"
    if react_mkt_path.exists():
        img_mkt = Image(str(react_mkt_path), width=480, height=255)
        img_mkt.hAlign = "CENTER"
        story.append(img_mkt)
        story.append(Paragraph("Figure 13.6: Real-Time Mandi Market Intelligence Page querying Agmarknet APMC rates", caption_style))

    # Build PDF
    doc.build(story, canvasmaker=AcademicReportCanvas)
    print(f"Successfully generated formal academic report at: {output_pdf}")


if __name__ == "__main__":
    build_academic_report()
