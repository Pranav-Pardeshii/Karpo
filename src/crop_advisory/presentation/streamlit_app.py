"""
Smart Crop Advisory System — Streamlit Web Application.
Machine Learning Based Crop Recommendation, Yield Prediction & Profit Estimation.
Integrates Random Forest & XGBoost ML pipelines, CACP Cultivation Costs,
and Mandi Market Prices into a unified agronomic decision engine.
Supports English, Marathi (मराठी), and Hindi (हिंदी).
"""

import json

import pandas as pd
import streamlit as st

from crop_advisory.config import (
    CROP_REC_CONFUSION_MATRIX_FILENAME,
    CROP_REC_FEATURE_IMPORTANCE_FILENAME,
    METRICS_FILENAME,
    YIELD_ACTUAL_VS_PRED_FILENAME,
    YIELD_FEATURE_IMPORTANCE_FILENAME,
    get_artifact_path,
)
from crop_advisory.domain.calculations import (
    calculate_farm_financials,
    format_inr,
)
from crop_advisory.domain.crop_mapping import (
    get_crop_metadata,
)
from crop_advisory.ml.crop_recommender import CropRecommender
from crop_advisory.ml.yield_predictor import YieldPredictor
from crop_advisory.presentation.translations import (
    LANGUAGE_OPTIONS,
    get_translated_crop_name,
    t,
)
from crop_advisory.services.cultivation_cost_service import (
    get_available_states,
    get_cultivation_cost,
    load_cost_dataset,
)
from crop_advisory.services.market_service import get_crop_price, load_prices_dataset


def main():
    # Page Configuration
    st.set_page_config(
        page_title="Smart Crop Advisory System",
        page_icon="🌾",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS for polished, modern UI
    st.markdown(
        """
    <style>
        /* Main container styling */
        .main {
            background-color: #f8fafc;
        }
        
        /* Top title styling */
        .hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #1b5e20;
            margin-bottom: 0.2rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            line-height: 1.2;
        }
        .hero-subtitle {
            font-size: 1.0rem;
            color: #475569;
            margin-bottom: 1.2rem;
            font-weight: 500;
        }
        
        /* Metric Card Styling - Adaptive for Light and Dark Modes */
        .metric-card {
            background: rgba(128, 128, 128, 0.07);
            border-radius: 12px;
            padding: 1.1rem 1.2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            border: 1px solid rgba(128, 128, 128, 0.2);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 18px rgba(0,0,0,0.12);
        }
        .metric-title {
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94a3b8;
            font-weight: 700;
            margin-bottom: 0.3rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }
        .metric-value {
            font-size: 1.65rem;
            font-weight: 800;
            line-height: 1.2;
        }
        .metric-sub {
            font-size: 0.8rem;
            color: #94a3b8;
            margin-top: 0.3rem;
        }
        .profit-positive {
            color: #22c55e !important;
        }
        .profit-negative {
            color: #ef4444 !important;
        }

        /* Custom Badges */
        .badge-primary {
            background-color: #dcfce7;
            color: #15803d;
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.85rem;
            display: inline-block;
        }
        .badge-secondary {
            background-color: #e0f2fe;
            color: #0369a1;
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.85rem;
            display: inline-block;
        }

        /* Disclaimer box */
        .disclaimer-box {
            background-color: #fffbeb;
            border-left: 4px solid #f59e0b;
            padding: 0.9rem 1.2rem;
            border-radius: 6px;
            color: #92400e;
            font-size: 0.88rem;
            margin-top: 1.8rem;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------
    # LANGUAGE STATE & TOP APP HEADER WITH LANGUAGE SELECTOR
    # ---------------------------------------------------------
    if "app_language" not in st.session_state:
        st.session_state["app_language"] = "English"

    current_lang = st.session_state["app_language"]

    # Prominent Top Bar: App Header & Language Switcher
    top_col1, top_col2 = st.columns([3.6, 1.4], vertical_alignment="center")
    with top_col1:
        st.markdown(
            f'<div class="hero-title">{t("hero_title", current_lang)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="hero-subtitle">{t("hero_subtitle", current_lang)}</div>',
            unsafe_allow_html=True,
        )
    with top_col2:
        lang_idx = 0
        if "मराठी" in current_lang:
            lang_idx = 1
        elif "हिंदी" in current_lang:
            lang_idx = 2
        selected_lang = st.selectbox(
            f"🌐 {t('language', current_lang)} / Language",
            options=LANGUAGE_OPTIONS,
            index=lang_idx,
            key="top_app_language_selector",
            help="Select preferred language / भाषा निवडा / भाषा चुनें (English, Marathi, Hindi)",
        )
        if selected_lang != st.session_state["app_language"]:
            st.session_state["app_language"] = selected_lang
            st.rerun()

    # ---------------------------------------------------------
    # CACHED MODEL & DATA LOADERS
    # ---------------------------------------------------------
    @st.cache_resource(show_spinner=False)
    def load_recommender():
        return CropRecommender()

    @st.cache_resource(show_spinner=False)
    def load_predictor():
        return YieldPredictor()

    @st.cache_data(show_spinner=False)
    def get_states_cached():
        return get_available_states()

    @st.cache_data(show_spinner=False)
    def load_metrics_cached():
        metrics_path = get_artifact_path(METRICS_FILENAME)
        if metrics_path.exists():
            with open(metrics_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    # Load models and resources
    try:
        crop_recommender = load_recommender()
        yield_predictor = load_predictor()
        available_states = get_states_cached()
        training_metrics = load_metrics_cached()
    except Exception as e:
        st.error(
            f"Error loading trained models: {e}. Please ensure you ran 'python scripts/train_models.py' first."
        )
        st.stop()

    # ---------------------------------------------------------
    # SIDEBAR: PARAMETERS & INPUT CONFIGURATION
    # ---------------------------------------------------------
    st.sidebar.image("https://img.icons8.com/color/96/000000/wheat.png", width=64)
    st.sidebar.markdown(f"### {t('sidebar_farm_setup', current_lang)}")

    # Preset Selector with Multilingual Labels
    preset_map = {
        t("preset_custom", current_lang): "custom",
        t("preset_gangetic", current_lang): "gangetic",
        t("preset_deccan", current_lang): "deccan",
        t("preset_semiarid", current_lang): "semiarid",
        t("preset_coastal", current_lang): "coastal",
    }
    preset_chosen = st.sidebar.selectbox(
        t("preset_label", current_lang),
        list(preset_map.keys()),
    )
    preset_key = preset_map.get(preset_chosen, "custom")

    # Preset Values Configuration
    defaults = {
        "n": 90.0,
        "p": 42.0,
        "k": 43.0,
        "temp": 24.5,
        "hum": 75.0,
        "ph": 6.8,
        "rain": 180.0,
        "state": "Uttar Pradesh",
        "soil": "Inceptisols",
        "season": "Kharif",
        "area": 2.5,
        "unit": "acre",
    }

    if preset_key == "gangetic":
        defaults.update(
            {
                "n": 95.0,
                "p": 48.0,
                "k": 45.0,
                "temp": 24.0,
                "hum": 80.0,
                "ph": 7.0,
                "rain": 200.0,
                "state": "Uttar Pradesh",
                "soil": "Inceptisols",
                "season": "Kharif",
            }
        )
    elif preset_key == "deccan":
        defaults.update(
            {
                "n": 115.0,
                "p": 42.0,
                "k": 22.0,
                "temp": 26.5,
                "hum": 68.0,
                "ph": 7.6,
                "rain": 85.0,
                "state": "Maharashtra",
                "soil": "Vertisols",
                "season": "Kharif",
            }
        )
    elif preset_key == "semiarid":
        defaults.update(
            {
                "n": 40.0,
                "p": 25.0,
                "k": 20.0,
                "temp": 30.0,
                "hum": 45.0,
                "ph": 8.0,
                "rain": 45.0,
                "state": "Rajasthan",
                "soil": "Aridisols",
                "season": "Kharif",
            }
        )
    elif preset_key == "coastal":
        defaults.update(
            {
                "n": 80.0,
                "p": 55.0,
                "k": 45.0,
                "temp": 28.0,
                "hum": 88.0,
                "ph": 6.2,
                "rain": 240.0,
                "state": "Kerala",
                "soil": "Alfisols",
                "season": "Whole Year",
            }
        )

    # Collapsible Sidebar Sections
    with st.sidebar.expander(t("sec_soil", current_lang), expanded=True):
        col_n, col_p = st.columns(2)
        with col_n:
            input_n = st.number_input(
                t("nitrogen", current_lang),
                min_value=0.0,
                max_value=250.0,
                value=defaults["n"],
                step=1.0,
            )
        with col_p:
            input_p = st.number_input(
                t("phosphorus", current_lang),
                min_value=0.0,
                max_value=200.0,
                value=defaults["p"],
                step=1.0,
            )

        col_k, col_ph = st.columns(2)
        with col_k:
            input_k = st.number_input(
                t("potassium", current_lang),
                min_value=0.0,
                max_value=250.0,
                value=defaults["k"],
                step=1.0,
            )
        with col_ph:
            input_ph = st.number_input(
                t("ph", current_lang), min_value=3.5, max_value=10.0, value=defaults["ph"], step=0.1
            )

    with st.sidebar.expander(t("sec_climate", current_lang), expanded=True):
        input_temp = st.slider(
            t("temperature", current_lang),
            min_value=8.0,
            max_value=48.0,
            value=defaults["temp"],
            step=0.5,
        )
        input_hum = st.slider(
            t("humidity", current_lang),
            min_value=10.0,
            max_value=100.0,
            value=defaults["hum"],
            step=1.0,
        )
        input_rain = st.slider(
            t("rainfall", current_lang),
            min_value=10.0,
            max_value=500.0,
            value=defaults["rain"],
            step=5.0,
        )

    with st.sidebar.expander(t("sec_geography", current_lang), expanded=True):
        state_index = (
            available_states.index(defaults["state"])
            if defaults["state"] in available_states
            else 0
        )
        input_state = st.selectbox(t("state", current_lang), available_states, index=state_index)

        soil_types = [
            "Vertisols (Black)",
            "Inceptisols (Alluvial)",
            "Alfisols (Red)",
            "Aridisols (Sandy/Desert)",
            "Mollisols (Hilly/Loam)",
            "Entisols",
        ]
        default_soil_idx = 1 if "Inceptisols" in defaults["soil"] else 0
        input_soil = st.selectbox(
            t("soil_class", current_lang), soil_types, index=default_soil_idx
        ).split(" ")[0]

        seasons = ["Kharif (Monsoon)", "Rabi (Winter)", "Whole Year / Zaid (Summer)"]
        default_season_idx = 0 if "Kharif" in defaults["season"] else 1
        input_season = st.selectbox(
            t("season", current_lang), seasons, index=default_season_idx
        ).split(" ")[0]

    with st.sidebar.expander(t("sec_land", current_lang), expanded=True):
        col_a1, col_a2 = st.columns([2, 1.2])
        with col_a1:
            farm_area_val = st.number_input(
                t("farm_size", current_lang),
                min_value=0.1,
                max_value=500.0,
                value=defaults["area"],
                step=0.5,
            )
        with col_a2:
            unit_display = [t("unit_acre", current_lang), t("unit_hectare", current_lang)]
            selected_unit_display = st.selectbox(t("unit", current_lang), unit_display, index=0)
            farm_area_unit = (
                "acre" if selected_unit_display == t("unit_acre", current_lang) else "hectare"
            )

    st.sidebar.markdown("---")
    st.sidebar.caption(t("sidebar_footer", current_lang))

    # ---------------------------------------------------------
    # RUN MODEL PREDICTION PIPELINE
    # ---------------------------------------------------------
    # 1. Crop Recommendation Model
    rec_result = crop_recommender.predict(
        n=input_n,
        p=input_p,
        k=input_k,
        temperature=input_temp,
        humidity=input_hum,
        ph=input_ph,
        rainfall=input_rain,
        top_k=3,
    )
    recommended_crop = rec_result["primary_crop"]
    crop_meta = get_crop_metadata(recommended_crop)
    localized_crop_name = get_translated_crop_name(recommended_crop, current_lang)

    # 2. Yield Prediction Model
    yield_result = yield_predictor.predict(
        crop=recommended_crop,
        season=input_season,
        soil_type=input_soil,
        state=input_state,
        temperature=input_temp,
        rainfall=input_rain,
        humidity=input_hum,
        ph=input_ph,
        nitrogen=input_n,
        phosphorus=input_p,
        potassium=input_k,
        fertilizer=float(crop_meta.get("default_fertilizer", 75.0)),
        pesticide=float(crop_meta.get("default_pesticide", 0.35)),
    )
    predicted_yield_ha = yield_result["predicted_yield_kg_ha"]

    # 3. Market Price Lookup
    price_data = get_crop_price(recommended_crop)
    modal_price = price_data["modal_rs_per_quintal"]

    # 4. Cultivation Cost Lookup
    cost_data = get_cultivation_cost(recommended_crop, state_name=input_state)
    c2_cost_ha = cost_data["cul_cost_c2_per_ha"]

    # 5. Farm Financials Calculation
    financials = calculate_farm_financials(
        yield_kg_per_ha=predicted_yield_ha,
        farm_area=farm_area_val,
        area_unit=farm_area_unit,
        price_per_quintal=modal_price,
        cost_per_ha=c2_cost_ha,
    )

    # ---------------------------------------------------------
    # MAIN NAVIGATION TABS
    # ---------------------------------------------------------
    tab_dashboard, tab_technical, tab_price_explorer = st.tabs(
        [
            t("tab_advisory", current_lang),
            t("tab_metrics", current_lang),
            t("tab_price_explorer", current_lang),
        ]
    )

    # =========================================================================
    # TAB 1: ADVISORY DASHBOARD
    # =========================================================================
    with tab_dashboard:
        # 6 PRIMARY METRIC CARDS
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-title">{t("metric_recommended_crop", current_lang)}</div>
                <div class="metric-value" style="font-size: 1.25rem; color: #15803d;">{localized_crop_name}</div>
                <div class="metric-sub">{t("metric_confidence", current_lang)} <b>{rec_result["confidence_percent"]:.1f}%</b></div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-title">{t("metric_predicted_yield", current_lang)}</div>
                <div class="metric-value">{financials["yield_quintals_per_acre"]:.1f} <span style="font-size:0.95rem; font-weight:500;">Q/{t("unit_acre", current_lang)}</span></div>
                <div class="metric-sub">{financials["yield_kg_per_ha"]:,.0f} kg/ha ({financials["yield_quintals_per_ha"]:.1f} Q/ha)</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col3:
            msp_tag = (
                f" (MSP ₹{price_data['msp_rs_per_quintal']:,.0f})"
                if price_data["msp_rs_per_quintal"]
                else ""
            )
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-title">{t("metric_market_price", current_lang)}</div>
                <div class="metric-value">{format_inr(price_data["modal_rs_per_quintal"])}</div>
                <div class="metric-sub">{t("per_quintal", current_lang)} (₹{price_data["price_per_kg"]:.1f}/kg){msp_tag}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col4:
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-title">{t("metric_cultivation_cost", current_lang)}</div>
                <div class="metric-value">{format_inr(cost_data["cul_cost_c2_per_acre"])}</div>
                <div class="metric-sub">{t("per_acre", current_lang)} ({format_inr(cost_data["cul_cost_c2_per_ha"])}/ha)</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col5:
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-title">{t("metric_total_revenue", current_lang)}</div>
                <div class="metric-value">{financials["formatted_revenue_short"]}</div>
                <div class="metric-sub">{t("production", current_lang)} {financials["total_production_quintals"]} {t("quintals", current_lang)}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col6:
            profit_class = "profit-positive" if financials["net_profit"] >= 0 else "profit-negative"
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-title">{t("metric_estimated_profit", current_lang)}</div>
                <div class="metric-value {profit_class}">{financials["formatted_profit_short"]}</div>
                <div class="metric-sub">{t("roi", current_lang)} <b>{financials["roi_percent"]:.1f}%</b> | {format_inr(financials["profit_per_acre"])}/{t("unit_acre", current_lang)}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        dash_col1, dash_col2 = st.columns([1.1, 1])

        with dash_col1:
            with st.container(border=True):
                st.markdown(f"### {t('rec_analysis_title', current_lang)}")
                st.write(
                    f"**{t('primary_match', current_lang)}** {localized_crop_name} ({rec_result['category']})"
                )
                st.info(
                    f"💡 **{t('description_label', current_lang)}** {crop_meta.get('description', '')}"
                )

                st.markdown(f"##### {t('top_candidates_title', current_lang)}")
                recs = rec_result["recommendations"]
                rec_df = pd.DataFrame(
                    [
                        {
                            t("candidate_crop", current_lang): get_translated_crop_name(
                                r.get("primary_crop", r["display_name"]), current_lang
                            ),
                            t("category", current_lang): r["category"],
                            t("confidence_score", current_lang): r["confidence_score"],
                        }
                        for r in recs
                    ]
                )
                st.dataframe(rec_df, hide_index=True, use_container_width=True)

                # Soil nutrient advisory
                st.markdown(f"##### {t('soil_diag_title', current_lang)}")
                if rec_result["soil_advisory_notes"]:
                    for note in rec_result["soil_advisory_notes"]:
                        st.warning(f"⚠️ {note}")
                else:
                    st.success(t("soil_optimal", current_lang))

        with dash_col2:
            with st.container(border=True):
                st.markdown(f"### {t('fin_breakdown_title', current_lang)}")

                fin_table_data = [
                    (
                        t("param_farm_size", current_lang),
                        f"{financials['input_area']} {financials['input_unit'].title()} ({financials['area_hectares']} ha)",
                    ),
                    (
                        t("param_total_harvest", current_lang),
                        f"{financials['total_production_quintals']:,.1f} {t('quintals', current_lang)} ({financials['total_production_kg']:,.0f} kg)",
                    ),
                    (t("param_gross_revenue", current_lang), f"{financials['formatted_revenue']}"),
                    (t("param_cul_cost", current_lang), f"{financials['formatted_cost']}"),
                    (t("param_net_profit", current_lang), f"{financials['formatted_profit']}"),
                    (
                        t("param_profit_per_acre", current_lang),
                        f"{financials['formatted_profit_per_acre']}",
                    ),
                    (t("param_roi", current_lang), f"{financials['roi_percent']:.1f} %"),
                    (
                        t("param_breakeven_yield", current_lang),
                        f"{financials['breakeven_yield_kg_per_ha']:,.0f} kg/ha",
                    ),
                    (
                        t("param_breakeven_price", current_lang),
                        f"{format_inr(financials['breakeven_price_per_quintal'])} / {t('quintals', current_lang).rstrip('s')}",
                    ),
                ]
                fin_df = pd.DataFrame(
                    fin_table_data,
                    columns=[
                        t("col_parameter", current_lang),
                        t("col_estimated_val", current_lang),
                    ],
                )
                st.dataframe(fin_df, hide_index=True, use_container_width=True)

                # Input Cost Composition
                st.markdown(f"##### {t('cost_comp_title', current_lang)}")
                cost_breakdown = pd.DataFrame(
                    {
                        t("input_category", current_lang): [
                            t("cost_seed", current_lang),
                            t("cost_fertilizer", current_lang),
                            t("cost_labor", current_lang),
                            t("cost_machinery", current_lang),
                            t("cost_rent", current_lang),
                        ],
                        t("amount_rs_ha", current_lang): [
                            cost_data["seed_cost_per_ha"],
                            cost_data["fertilizer_cost_per_ha"],
                            cost_data["labor_cost_per_ha"],
                            cost_data["machinery_cost_per_ha"],
                            max(
                                0.0,
                                cost_data["cul_cost_c2_per_ha"]
                                - (
                                    cost_data["seed_cost_per_ha"]
                                    + cost_data["fertilizer_cost_per_ha"]
                                    + cost_data["labor_cost_per_ha"]
                                    + cost_data["machinery_cost_per_ha"]
                                ),
                            ),
                        ],
                    }
                )
                st.bar_chart(cost_breakdown.set_index(t("input_category", current_lang)))

        # SENSITIVITY & SCENARIO ANALYSIS
        with st.expander(t("scenario_title", current_lang), expanded=False):
            st.markdown(t("scenario_desc", current_lang))
            sim_col1, sim_col2 = st.columns(2)
            with sim_col1:
                sim_price_delta = st.slider(
                    t("sim_price_delta", current_lang), min_value=-40, max_value=60, value=0, step=5
                )
            with sim_col2:
                sim_yield_delta = st.slider(
                    t("sim_yield_delta", current_lang), min_value=-40, max_value=60, value=0, step=5
                )

            adjusted_price = modal_price * (1.0 + sim_price_delta / 100.0)
            adjusted_yield = predicted_yield_ha * (1.0 + sim_yield_delta / 100.0)
            sim_financials = calculate_farm_financials(
                yield_kg_per_ha=adjusted_yield,
                farm_area=farm_area_val,
                area_unit=farm_area_unit,
                price_per_quintal=adjusted_price,
                cost_per_ha=c2_cost_ha,
            )

            sim_c1, sim_c2, sim_c3 = st.columns(3)
            sim_c1.metric(
                t("sim_revenue", current_lang),
                sim_financials["formatted_revenue"],
                f"{sim_price_delta + sim_yield_delta}%",
            )
            sim_c2.metric(
                t("sim_profit", current_lang),
                sim_financials["formatted_profit"],
                f"{sim_financials['roi_percent']:.1f}% ROI",
            )
            sim_c3.metric(
                t("sim_profit_acre", current_lang), sim_financials["formatted_profit_per_acre"]
            )

        # Download summary report
        st.markdown("<br>", unsafe_allow_html=True)
        report_dict = {
            "Recommended Crop": [rec_result["display_name"]],
            "Cropping Season": [input_season],
            "Soil Classification": [input_soil],
            "State": [input_state],
            "Farm Area": [f"{farm_area_val} {farm_area_unit}"],
            "Predicted Yield (Q/Acre)": [financials["yield_quintals_per_acre"]],
            "Total Production (Q)": [financials["total_production_quintals"]],
            "Market Price (Rs/Q)": [modal_price],
            "Cost of Cultivation (Rs/Acre)": [cost_data["cul_cost_c2_per_acre"]],
            "Estimated Revenue (Rs)": [financials["total_revenue"]],
            "Total Cost (Rs)": [financials["total_cost"]],
            "Net Profit (Rs)": [financials["net_profit"]],
            "ROI (%)": [financials["roi_percent"]],
        }
        report_csv = pd.DataFrame(report_dict).to_csv(index=False).encode("utf-8")
        st.download_button(
            label=t("download_csv", current_lang),
            data=report_csv,
            file_name=f"crop_advisory_{recommended_crop}_{input_state}.csv",
            mime="text/csv",
        )

        # DISCLAIMER BOX
        st.markdown(
            f"""
            <div class="disclaimer-box">
                {t("disclaimer", current_lang)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # =========================================================================
    # TAB 2: TECHNICAL & MODEL EVALUATION
    # =========================================================================
    with tab_technical:
        st.markdown(t("tech_title", current_lang))
        st.markdown(t("tech_desc", current_lang))

        # Metric summary cards
        if training_metrics:
            crm = training_metrics.get("crop_recommendation", {})
            ypm = training_metrics.get("yield_prediction", {})

            mcol1, mcol2 = st.columns(2)
            with mcol1:
                with st.container(border=True):
                    st.markdown(t("tech_model_rec", current_lang))
                    st.markdown(f"**{t('winning_model', current_lang)}** `{crm.get('best_model')}`")
                    st.write(f"- **{t('test_accuracy', current_lang)}** `{crm.get('accuracy')}%`")
                    st.write(f"- **{t('weighted_f1', current_lang)}** `{crm.get('f1_score')}`")
                    st.write(
                        f"- **RF Accuracy:** `{crm.get('rf_accuracy')}%` | **XGB Accuracy:** `{crm.get('xgb_accuracy')}%`"
                    )

            with mcol2:
                with st.container(border=True):
                    st.markdown(t("tech_model_yield", current_lang))
                    st.markdown(f"**{t('winning_model', current_lang)}** `{ypm.get('best_model')}`")
                    st.write(f"- **{t('r2_score', current_lang)}** `{ypm.get('r2_score')}`")
                    st.write(f"- **{t('rmse', current_lang)}** `{ypm.get('rmse')} kg/ha`")
                    st.write(f"- **{t('mae', current_lang)}** `{ypm.get('mae')} kg/ha`")
                    st.write(
                        f"- **RF R²:** `{ypm.get('rf_r2')}` | **XGB R²:** `{ypm.get('xgb_r2')}`"
                    )

        # EVALUATION PLOTS
        st.markdown(t("tech_plots_title", current_lang))
        pcol1, pcol2 = st.columns(2)

        cm_img_path = get_artifact_path(CROP_REC_CONFUSION_MATRIX_FILENAME)
        rec_feat_path = get_artifact_path(CROP_REC_FEATURE_IMPORTANCE_FILENAME)
        yield_feat_path = get_artifact_path(YIELD_FEATURE_IMPORTANCE_FILENAME)
        act_pred_path = get_artifact_path(YIELD_ACTUAL_VS_PRED_FILENAME)

        with pcol1:
            if cm_img_path.exists():
                st.image(
                    str(cm_img_path),
                    caption="Crop Recommendation — Multi-Class Confusion Matrix",
                    use_container_width=True,
                )
            if rec_feat_path.exists():
                st.image(
                    str(rec_feat_path),
                    caption="Crop Recommendation — Relative Feature Importance",
                    use_container_width=True,
                )

        with pcol2:
            if act_pred_path.exists():
                st.image(
                    str(act_pred_path),
                    caption="Yield Prediction — Actual vs Predicted Yield (kg/ha)",
                    use_container_width=True,
                )
            if yield_feat_path.exists():
                st.image(
                    str(yield_feat_path),
                    caption="Yield Prediction — Top 15 Predictor Importance",
                    use_container_width=True,
                )

    # =========================================================================
    # TAB 3: PRICE & COST EXPLORER
    # =========================================================================
    with tab_price_explorer:
        st.markdown(t("mandi_title", current_lang))
        st.markdown(t("mandi_desc", current_lang))

        exp_tab1, exp_tab2 = st.tabs(
            [t("mandi_market_prices", current_lang), t("cost_of_cultivation", current_lang)]
        )

        with exp_tab1:
            prices_df = load_prices_dataset()
            search_crop = st.text_input(t("filter_crop", current_lang), "")
            if search_crop:
                filtered_prices = prices_df[
                    prices_df["crop"].str.contains(search_crop, case=False, na=False)
                ]
            else:
                filtered_prices = prices_df

            st.dataframe(
                filtered_prices[["crop", "modal_rs_per_quintal", "min", "max", "msp"]].rename(
                    columns={
                        "crop": "Crop",
                        "modal_rs_per_quintal": "Modal Price (₹/Q)",
                        "min": "Min Price (₹/Q)",
                        "max": "Max Price (₹/Q)",
                        "msp": "MSP (₹/Q)",
                    }
                ),
                hide_index=True,
                use_container_width=True,
            )

        with exp_tab2:
            cost_df = load_cost_dataset()
            cost_state_filter = st.selectbox(
                t("filter_state", current_lang), [t("all_states", current_lang)] + available_states
            )
            if cost_state_filter != t("all_states", current_lang):
                filtered_cost = cost_df[cost_df["state_name"] == cost_state_filter]
            else:
                filtered_cost = cost_df

            st.dataframe(
                filtered_cost[
                    [
                        "crop_name",
                        "state_name",
                        "cul_cost_c2",
                        "prod_cost_c2",
                        "derived_yield",
                        "opr_cost_seed",
                        "opr_cost_fertilizer",
                    ]
                ]
                .rename(
                    columns={
                        "crop_name": "Crop",
                        "state_name": "State",
                        "cul_cost_c2": "C2 Cultivation Cost (₹/ha)",
                        "prod_cost_c2": "Production Cost (₹/Q)",
                        "derived_yield": "Survey Yield (Q/ha)",
                        "opr_cost_seed": "Seed Cost (₹/ha)",
                        "opr_cost_fertilizer": "Fertilizer Cost (₹/ha)",
                    }
                )
                .head(50),
                hide_index=True,
                use_container_width=True,
            )


if __name__ == "__main__":
    main()
