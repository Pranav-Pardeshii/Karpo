import React, { createContext, useContext, useState } from "react";

export type Language = "en" | "mr" | "hi";

export interface LanguageOption {
  code: Language;
  label: string;
  nativeLabel: string;
}

export const LANGUAGE_OPTIONS: LanguageOption[] = [
  { code: "en", label: "English", nativeLabel: "English" },
  { code: "mr", label: "Marathi", nativeLabel: "मराठी" },
  { code: "hi", label: "Hindi", nativeLabel: "हिंदी" },
];

export const CROP_NAMES: Record<string, { en: string; mr: string; hi: string }> = {
  "rice": { en: "Rice", mr: "भात / तांदूळ (Rice)", hi: "चावल / धान (Rice)" },
  "wheat": { en: "Wheat", mr: "गहू (Wheat)", hi: "गेहूं (Wheat)" },
  "maize": { en: "Maize", mr: "मका (Maize)", hi: "मक्का (Maize)" },
  "chickpea": { en: "Chickpea", mr: "हरभरा (Chickpea)", hi: "चना (Chickpea)" },
  "kidneybeans": { en: "Kidney Beans", mr: "राजमा (Kidney Beans)", hi: "राजमा (Kidney Beans)" },
  "pigeonpeas": { en: "Pigeonpeas", mr: "तूर (Pigeonpeas)", hi: "अरहर / तुअर (Pigeonpeas)" },
  "pigeonpea": { en: "Pigeonpea", mr: "तूर (Pigeonpea)", hi: "अरहर (Pigeonpea)" },
  "mothbeans": { en: "Mothbeans", mr: "मठ (Mothbeans)", hi: "मोठ (Mothbeans)" },
  "mungbean": { en: "Mungbean", mr: "मूग (Mungbean)", hi: "मूंग (Mungbean)" },
  "blackgram": { en: "Blackgram", mr: "उडीद (Blackgram)", hi: "उड़द (Blackgram)" },
  "lentil": { en: "Lentil", mr: "मसूर (Lentil)", hi: "मसूर (Lentil)" },
  "pomegranate": { en: "Pomegranate", mr: "डाळिंब (Pomegranate)", hi: "अनार (Pomegranate)" },
  "banana": { en: "Banana", mr: "केळी (Banana)", hi: "केला (Banana)" },
  "mango": { en: "Mango", mr: "आंबा (Mango)", hi: "आम (Mango)" },
  "grapes": { en: "Grapes", mr: "द्राक्षे (Grapes)", hi: "अंगूर (Grapes)" },
  "watermelon": { en: "Watermelon", mr: "कलिंगड (Watermelon)", hi: "तरबूज (Watermelon)" },
  "muskmelon": { en: "Muskmelon", mr: "खरबूज (Muskmelon)", hi: "खरबूजा (Muskmelon)" },
  "apple": { en: "Apple", mr: "सफरचंद (Apple)", hi: "सेब (Apple)" },
  "orange": { en: "Orange", mr: "संत्रा (Orange)", hi: "संतरा (Orange)" },
  "papaya": { en: "Papaya", mr: "पपई (Papaya)", hi: "पपीता (Papaya)" },
  "coconut": { en: "Coconut", mr: "नारळ (Coconut)", hi: "नारियल (Coconut)" },
  "cotton": { en: "Cotton", mr: "कापूस (Cotton)", hi: "कपास (Cotton)" },
  "jute": { en: "Jute", mr: "ताग (Jute)", hi: "पटसन (Jute)" },
  "coffee": { en: "Coffee", mr: "कॉफी (Coffee)", hi: "कॉफी (Coffee)" },
  "sugarcane": { en: "Sugarcane", mr: "ऊस (Sugarcane)", hi: "गन्ना (Sugarcane)" },
  "barley": { en: "Barley", mr: "जव (Barley)", hi: "जौ (Barley)" },
  "pearl millet": { en: "Pearl Millet", mr: "बाजरी (Pearl Millet)", hi: "बाजरा (Pearl Millet)" },
  "sorghum": { en: "Sorghum", mr: "ज्वारी (Sorghum)", hi: "ज्वार (Sorghum)" },
  "sorghum (kharif)": { en: "Sorghum (Kharif)", mr: "खरीप ज्वारी", hi: "खरीफ ज्वार" },
  "groundnut": { en: "Groundnut", mr: "भुईमूग (Groundnut)", hi: "मूंगफली (Groundnut)" },
  "soybean": { en: "Soybean", mr: "सोयाबीन (Soybean)", hi: "सोयाबीन (Soybean)" },
  "sunflower": { en: "Sunflower", mr: "सूर्यफूल (Sunflower)", hi: "सूरजमुखी (Sunflower)" },
  "sesamum": { en: "Sesamum", mr: "तीळ (Sesamum)", hi: "तिल (Sesamum)" },
  "onion": { en: "Onion", mr: "कांदा (Onion)", hi: "प्याज (Onion)" },
  "minor pulses": { en: "Minor Pulses", mr: "इतर कडधान्ये", hi: "अन्य दलहन" },
};

export const CATEGORY_NAMES: Record<string, { en: string; mr: string; hi: string }> = {
  "ALL": { en: "ALL", mr: "सर्व", hi: "सभी" },
  "All Crops": { en: "All Crops", mr: "सर्व पिके", hi: "सभी फसलें" },
  "Cereals & Grains": { en: "Cereals & Grains", mr: "धान्य व तृणधान्ये", hi: "अनाज व खाद्यान्न" },
  "Pulses & Legumes": { en: "Pulses & Legumes", mr: "कडधान्ये व डाळी", hi: "दलहन व दालें" },
  "Oilseeds": { en: "Oilseeds", mr: "गळितधान्ये / तेलबिया", hi: "तिलहन" },
  "Commercial & Fibre": { en: "Commercial & Fibre", mr: "नगदी व फायबर पिके", hi: "व्यावसायिक व रेशेदार" },
  "Fruits & Horticultural": { en: "Fruits & Horticultural", mr: "फळे व बागायत", hi: "फल व बागवानी" },
  "Cereal": { en: "Cereal", mr: "धान्य", hi: "अनाज" },
  "Pulses": { en: "Pulses", mr: "कडधान्य", hi: "दालें" },
  "Cash Crop": { en: "Cash Crop", mr: "नगदी पीक", hi: "नकदी फसल" },
  "Fruit": { en: "Fruit", mr: "फळ", hi: "फल" },
  "Plantation": { en: "Plantation", mr: "बागायत", hi: "बागवानी" },
  "Field Crop": { en: "Field Crop", mr: "शेती पीक", hi: "खेत फसल" },
};

export const SEASON_NAMES: Record<string, { en: string; mr: string; hi: string }> = {
  "Kharif": { en: "Kharif (Monsoon)", mr: "खरीप (पावसाळी)", hi: "खरीफ (मानसून)" },
  "Rabi": { en: "Rabi (Winter)", mr: "रब्बी (हिवाळी)", hi: "रबी (सर्दियों)" },
  "Whole Year": { en: "Whole Year", mr: "वर्षभर", hi: "पूरे वर्ष" },
  "Summer": { en: "Summer", mr: "उन्हाळी / झायेद", hi: "गर्मी / जायद" },
  "Autumn": { en: "Autumn", mr: "शरद ऋतू", hi: "शरद ऋतु" },
  "Winter": { en: "Winter", mr: "हिवाळा", hi: "शीतकालीन" },
};

export const SOIL_NAMES: Record<string, { en: string; mr: string; hi: string }> = {
  "Vertisols": { en: "Vertisols (Black Soil)", mr: "काळी माती (काळी जमीन / Vertisols)", hi: "काली मिट्टी (Vertisols)" },
  "Inceptisols": { en: "Inceptisols (Alluvial)", mr: "गाळाची माती (Inceptisols)", hi: "जलोढ़ मिट्टी (Inceptisols)" },
  "Alfisols": { en: "Alfisols (Red Soil)", mr: "तांबडी / लाल माती (Alfisols)", hi: "लाल मिट्टी (Alfisols)" },
  "Aridisols": { en: "Aridisols (Desert/Sandy)", mr: "वाळवंटी / रेताड माती (Aridisols)", hi: "रेतीली / मरुस्थलीय (Aridisols)" },
  "Mollisols": { en: "Mollisols (Hilly/Loam)", mr: "डोंगर उताराची माती (Mollisols)", hi: "पहाड़ी / दोमट (Mollisols)" },
  "Entisols": { en: "Entisols (Recent Alluvial)", mr: "नवीन गाळाची माती (Entisols)", hi: "नवीन जलोढ़ मिट्टी (Entisols)" },
};

export const STATE_NAMES: Record<string, { en: string; mr: string; hi: string }> = {
  "maharashtra": { en: "Maharashtra", mr: "महाराष्ट्र", hi: "महाराष्ट्र" },
  "punjab": { en: "Punjab", mr: "पंजाब", hi: "पंजाब" },
  "uttar pradesh": { en: "Uttar Pradesh", mr: "उत्तर प्रदेश", hi: "उत्तर प्रदेश" },
  "gujarat": { en: "Gujarat", mr: "गुजरात", hi: "गुजरात" },
  "karnataka": { en: "Karnataka", mr: "कर्नाटक", hi: "कर्नाटक" },
  "tamil nadu": { en: "Tamil Nadu", mr: "तामिळनाडू", hi: "तमिलनाडु" },
  "haryana": { en: "Haryana", mr: "हरियाणा", hi: "हरियाणा" },
  "madhya pradesh": { en: "Madhya Pradesh", mr: "मध्य प्रदेश", hi: "मध्य प्रदेश" },
  "rajasthan": { en: "Rajasthan", mr: "राजस्थान", hi: "राजस्थान" },
  "andhra pradesh": { en: "Andhra Pradesh", mr: "आंध्र प्रदेश", hi: "आंध्र प्रदेश" },
  "west bengal": { en: "West Bengal", mr: "पश्चिम बंगाल", hi: "पश्चिम बंगाल" },
  "bihar": { en: "Bihar", mr: "बिहार", hi: "बिहार" },
  "telangana": { en: "Telangana", mr: "तेलंगणा", hi: "तेलंगाना" },
  "odisha": { en: "Odisha", mr: "ओडिशा", hi: "ओडिशा" },
  "kerala": { en: "Kerala", mr: "केरळ", hi: "केरल" },
  "assam": { en: "Assam", mr: "आसाम", hi: "असम" },
};

export const UNIT_NAMES: Record<string, { en: string; mr: string; hi: string }> = {
  "acre": { en: "Acres", mr: "एकर", hi: "एकड़" },
  "acres": { en: "Acres", mr: "एकर", hi: "एकड़" },
  "hectare": { en: "Hectares", mr: "हेक्टर", hi: "हेक्टेयर" },
  "hectares": { en: "Hectares", mr: "हेक्टर", hi: "हेक्टेयर" },
  "bigha": { en: "Bigha", mr: "बिघा", hi: "बीघा" },
};

export const TRANSLATIONS: Record<Language, Record<string, string>> = {
  en: {
    // Header & Navigation
    brand_sub: "AGRICULTURAL INTELLIGENCE",
    nav_overview: "Overview",
    nav_recommend: "Crop Recommendation",
    nav_yield: "Yield Forecast",
    nav_market: "Market Intelligence",
    nav_financials: "Farm Economics",
    nav_advisory: "Composite Advisory",
    status_operational: "System Operational",
    status_offline: "Backend Offline",
    status_connecting: "Connecting...",
    select_language: "Language",
    footer_desc:
      "Empirical decision support bridging soil-climatic suitability classification, yield forecasting, mandi market intelligence, and farm economic feasibility.",
    footer_sources: "DATA SOURCES: AGMARKNET • DES • CACP",
    footer_disclaimer:
      "Probabilistic advisory • Realized yields and prices vary with local conditions",

    // Overview Page
    hero_headline: "THE LAND IS A SYSTEM.",
    hero_subheadline:
      "KARPO analyzes environmental conditions, crop suitability, expected yields, and agricultural economics in one unified platform. Make informed planting decisions backed by empirical agronomic data.",
    explore_crop_rec: "Explore Crop Recommendation",
    view_full_advisory: "View Full Advisory",
    system_inventory: "SYSTEM INVENTORY",
    official_datasets: "OFFICIAL REFERENCE DATASETS",
    supported_crops: "SUPPORTED CROPS",
    species_unit: "SPECIES",
    across_categories: "Across 6 agricultural categories",
    mandi_coverage: "MANDI COVERAGE",
    commodities_unit: "COMMODITIES",
    mandi_sub: "APMC wholesale market prices & MSP",
    cost_benchmarks: "COST BENCHMARKS",
    records_unit: "RECORDS",
    cacp_sub: "CACP state cultivation expenditure",
    historical_harvests: "HISTORICAL HARVESTS",
    surveys_unit: "SURVEYS",
    yield_sub: "Longitudinal crop yield data records",
    benchmarks_heading: "Historical Yield Reference Benchmarks",
    benchmarks_sub: "National Median Harvest across Indian Agro-Climatic Zones",
    median_harvest: "Median Harvest:",
    historical_range: "Historical Range:",
    source_des: "SOURCE: DIRECTORATE OF ECONOMICS & STATISTICS",
    forecast_yield_btn: "Forecast Harvest Yield",
    core_capabilities: "Core Capabilities",
    integrated_tools: "Integrated agronomic and economic tools",
    suitability_title: "Crop Suitability",
    suitability_desc:
      "Evaluates soil macronutrients (NPK), chemical reaction (pH), and local climate to recommend best-matched crops.",
    yield_forecasting_title: "Yield Forecasting",
    yield_forecasting_desc:
      "Projects expected production in both metric (kg/ha) and farm (quintals/acre) units based on regional conditions.",
    mandi_intel_title: "Mandi Market Intelligence",
    mandi_intel_desc:
      "Provides official APMC wholesale commodity auction rates, min/max ranges, and statutory Minimum Support Prices.",
    farm_econ_title: "Farm Economic Feasibility",
    farm_econ_desc:
      "Simulates operational revenue, comprehensive C2 costs, net profit, and break-even thresholds per acre and hectare.",
    explore_arrow: "Explore →",
    supported_crops_heading: "Supported Agricultural Crops (22 Species)",
    supported_crops_sub:
      "Agricultural inventory supported across the suitability and yield models",

    // Crop Recommendation Page
    rec_page_title: "Crop Suitability Recommendation",
    rec_page_desc:
      "Input soil macronutrient levels (NPK), chemical reaction (pH), and local weather conditions to identify the optimal crops for your land.",
    soil_presets: "SOIL PRESETS:",
    preset_alluvial: "Alluvial Paddy",
    preset_black_cotton: "Black Cotton",
    preset_winter_chickpea: "Winter Chickpea",
    soil_env_inputs: "Soil & Environmental Inputs",
    soil_macronutrients: "Soil Macronutrients (kg/ha)",
    nitrogen_label: "Nitrogen (N)",
    phosphorus_label: "Phosphorus (P)",
    potassium_label: "Potassium (K)",
    soil_reaction: "Soil Reaction (pH)",
    climatic_metrics: "Climatic & Weather Metrics",
    temp_label: "Temperature (°C)",
    humidity_label: "Humidity (%)",
    rainfall_label: "Rainfall (mm)",
    rec_button: "Analyze Soil & Recommend Crops",
    rec_analyzing: "Running Agronomic Pipeline...",
    rec_primary_title: "Primary Agronomic Match",
    rec_confidence: "Confidence Score",
    rec_top_candidates: "Top Candidate Crops",
    rec_soil_diag: "Soil Chemistry Diagnosis",
    rec_proceed_yield: "Proceed to Yield Forecast →",

    // Yield Prediction Page
    yield_page_title: "Crop Yield Forecasting",
    yield_page_desc:
      "Project expected harvest volume per hectare and acre based on crop choice, regional climate, soil classification, and input applications.",
    yield_crop_label: "Crop Choice",
    yield_season_label: "Cropping Season",
    yield_state_label: "State",
    yield_soil_label: "Soil Classification",
    yield_fertilizer_label: "Fertilizer (kg/ha)",
    yield_pesticide_label: "Pesticide (kg/ha)",
    yield_btn: "Compute Yield Forecast",
    yield_computing: "Running Regression Engine...",
    yield_predicted_label: "Predicted Harvest Yield",
    yield_proceed_fin: "Proceed to Farm Economics →",

    // Mandi Price Intelligence
    mandi_page_title: "Mandi Price Intelligence",
    mandi_page_desc:
      "Agricultural Produce Market Committee (APMC) modal wholesale auction rates, price spreads, and statutory Minimum Support Price (MSP) benchmarks across India.",
    mandi_search_placeholder: "Filter by commodity (e.g. Rice, Wheat, Cotton, Maize, Mustard)...",
    col_commodity: "Commodity",
    col_modal_price: "Modal Price (₹/Q)",
    col_min_price: "Min Price (₹/Q)",
    col_max_price: "Max Price (₹/Q)",
    col_msp: "Statutory MSP (₹/Q)",
    col_unit_price: "Price per kg",

    // Farm Economics
    fin_page_title: "Farm Financial Feasibility",
    fin_page_desc:
      "Simulate production revenue, comprehensive C2 costs, net profit, and break-even thresholds per acre and hectare.",
    fin_farm_area: "Farm Area",
    fin_area_unit: "Area Unit",
    fin_yield: "Expected Harvest Yield (kg/ha)",
    fin_price: "Realized Market Price (₹/Quintal)",
    fin_cost: "Cultivation Cost C2 (₹/ha)",
    fin_btn: "Simulate Farm Economics",
    fin_gross_revenue: "Gross Production Revenue",
    fin_total_cost: "Total Operational Cost (C2)",
    fin_net_profit: "Estimated Net Profit",
    fin_roi: "Return on Investment (ROI)",
    fin_breakeven_yield: "Break-Even Harvest Yield",
    fin_breakeven_price: "Break-Even Market Price",

    // Farm Economics & Advisory extra
    sync_benchmarks: "SYNC BENCHMARKS",
    econ_sim_inputs: "Economic Simulation Inputs",
    market_rate_standards: "Market Rate & Cost Standards",
    fin_failed: "FINANCIAL ANALYSIS FAILED",
    feasibility_summary: "FEASIBILITY SUMMARY",
    net_farm_profit: "NET FARM PROFIT",
    q_harvest: "Q harvest",
    comprehensive_c2: "Comprehensive C2",
    margin: "Margin",
    profit_per_acre: "PROFIT PER ACRE",
    normalized_acreage_income: "Normalized acreage net income",
    profit_per_ha: "PROFIT PER HECTARE",
    standard_metric_realization: "Standard metric realization",
    rev_vs_exp_breakdown: "Revenue vs. Expenditure Breakdown",
    critical_breakeven_thresholds: "Critical Break-Even Thresholds",
    min_harvest_operational_costs: "Minimum harvest to cover operational costs",
    floor_market_price: "Floor market realization price",
    cacp_methodology_standards: "CACP METHODOLOGY STANDARDS",
    generate_full_advisory_link: "Generate Full Advisory Report",
    awaiting_fin_desc: "Enter farm area, expected yield, and market rates on the left, or use \"Sync Benchmarks\" to auto-populate state cost standards.",
    amount_label: "Amount",
    adv_page_title: "Composite Farm Advisory",
    adv_page_desc: "Execute the complete agronomic decision workflow: analyzes soil suitability, projects expected yield, references wholesale mandi rates, applies CACP cost benchmarks, and calculates net profitability.",
    adv_btn: "Generate Full Advisory",
    adv_print: "Print Dossier",
    adv_failed: "ADVISORY GENERATION FAILED",
    comprehensive_inputs: "Comprehensive Inputs",
    crop_recommendation_tag: "CROP RECOMMENDATION",
    projected_yield_title: "Projected Yield",
    metric_density: "Metric Density",
    farm_standard: "Farm Standard:",
    mandi_wholesale_price: "Mandi Wholesale Price",
    modal_wholesale_rate: "Modal Wholesale Rate",
    cultivation_expenditure_breakdown: "Cultivation Expenditure Breakdown (CACP C2)",
    state_applied: "STATE:",
    cost_seed: "Seed Cost",
    cost_fertilizer: "Fertilizer",
    cost_labor: "Human Labor",
    cost_machinery: "Machinery",
    total_cost_per_ha: "Total Cost per Hectare:",
    farm_profitability_roi: "Farm Profitability & Return on Investment",
    awaiting_adv_desc: "Configure soil parameters, region, and farm area on the left, then click \"Generate Full Advisory\" to run the integrated analysis.",
    total_harvest_label: "Total harvest:",
    acre_cost_label: "Acre cost:",
    profit_label: "Profit:",
    msp_label: "MSP:",
    soil_chemistry_title: "Soil Chemistry (N-P-K & pH)",
    retained_from_rec: "Retained from Crop Recommendation",
    retained_from_yield: "Retained from Yield Forecast",
    retained_from_fin: "Retained from Farm Economics",
    forecast_this_candidate: "Forecast Yield →",

    // Awaiting states & result badges
    awaiting_soil_title: "Awaiting Soil Parameters",
    awaiting_soil_desc:
      "Adjust soil macronutrients or pick a preset on the left, then click \"Analyze Crop Suitability\" to evaluate crop compatibility.",
    primary_crop_badge: "RECOMMENDED PRIMARY CROP",
    match_badge: "MATCH",
    soil_advisory_label: "Agronomic Soil Advisory:",
    suitable_for_soil: "SUITABLE FOR ENTERED SOIL CONDITIONS",
    candidate_prob_dist: "Candidate Probability Distribution",
    suitability_score_unit: "Ranked suitability scores across top evaluated crops",
    awaiting_yield_title: "Awaiting Yield Parameters",
    awaiting_yield_desc:
      "Select crop, season, state, and soil properties on the left, then compute expected yields.",
    awaiting_fin_title: "Awaiting Financial Parameters",
    awaiting_adv_title: "Awaiting Advisory Parameters",
  },
  mr: {
    // Header & Navigation
    brand_sub: "कृषी बुद्धिमत्ता प्रणाली",
    nav_overview: "विहंगावलोकन",
    nav_recommend: "पीक शिफारस",
    nav_yield: "उत्पादन अंदाज",
    nav_market: "बाजारभाव",
    nav_financials: "शेती अर्थशास्त्र",
    nav_advisory: "समग्र सल्ला",
    status_operational: "प्रणाली कार्यरत आहे",
    status_offline: "बॅकएंड ऑफलाइन",
    status_connecting: "कनेक्ट करत आहे...",
    select_language: "भाषा निवडा",
    footer_desc:
      "माती व हवामान अनुकूलता वर्गीकरण, पीक उत्पादन अंदाज, कृषी उत्पन्न बाजारभाव आणि आर्थिक नफा विश्लेषण एकात्मिक करणारी निर्णय समर्थन प्रणाली.",
    footer_sources: "माहिती स्रोत: ॲगमार्कनेट • डीईएस • सीएसीपी",
    footer_disclaimer:
      "संभाव्य कृषी सल्ला • प्रत्यक्ष उत्पादन व भाव स्थानिक शेती व बाजार परिस्थितीनुसार बदलू शकतात",

    // Overview Page
    hero_headline: "जमीन ही एक परिपूर्ण प्रणाली आहे.",
    hero_subheadline:
      "कार्पो (KARPO) एकाच मंचावर माती व हवामान परिस्थिती, पीक अनुकूलता, अपेक्षित उत्पादन आणि कृषी अर्थशास्त्राचे सखोल विश्लेषण करते. अधिकृत कृषी डेटावर आधारित योग्य पेरणीचे निर्णय घ्या.",
    explore_crop_rec: "पीक शिफारस तपासा",
    view_full_advisory: "संपूर्ण कृषी सल्ला पहा",
    system_inventory: "प्रणाली माहिती संग्रह",
    official_datasets: "शासकीय अधिकृत संदर्भ डेटासेट",
    supported_crops: "समाविष्ट पिके",
    species_unit: "प्रजाती",
    across_categories: "६ प्रमुख कृषी प्रवर्गांमध्ये",
    mandi_coverage: "मंडी बाजार व्याप्ती",
    commodities_unit: "शेतमाल",
    mandi_sub: "घाऊक बाजारभाव आणि हमीभाव (MSP)",
    cost_benchmarks: "लागवड खर्च मापदंड",
    records_unit: "नोंदी",
    cacp_sub: "CACP राज्यनिहाय लागवड खर्च सर्वेक्षण",
    historical_harvests: "ऐतिहासिक उत्पादन डेटा",
    surveys_unit: "सर्वेक्षणे",
    yield_sub: "दीर्घकालीन पीक उत्पादन डेटा नोंदी",
    benchmarks_heading: "ऐतिहासिक पीक उत्पादन संदर्भ मापदंड",
    benchmarks_sub: "भारतीय कृषी-हवामान विभागांमधील राष्ट्रीय सरासरी उत्पादन",
    median_harvest: "सरासरी उत्पादन:",
    historical_range: "ऐतिहासिक मर्यादा:",
    source_des: "स्रोत: अर्थशास्त्र आणि सांख्यिकी संचालनालय (DES)",
    forecast_yield_btn: "उत्पादन अंदाज वर्तवा",
    core_capabilities: "प्रमुख वैशिष्ट्ये व क्षमता",
    integrated_tools: "एकात्मिक कृषी व आर्थिक विश्लेषण साधने",
    suitability_title: "पीक अनुकूलता",
    suitability_desc:
      "मातीतील मुख्य पोषक घटक (NPK), सामू (pH) आणि स्थानिक हवामानाचे विश्लेषण करून सर्वात योग्य पिकांची शिफारस करते.",
    yield_forecasting_title: "उत्पादन अंदाज (Yield Forecast)",
    yield_forecasting_desc:
      "प्रादेशिक परिस्थितीच्या आधारे मेट्रिक (किलो/हेक्टर) आणि शेतकरी (क्विंटल/एकर) दोन्ही एककांमध्ये अपेक्षित उत्पादनाचा अंदाज देते.",
    mandi_intel_title: "मंडी बाजारभाव माहिती",
    mandi_intel_desc:
      "अधिकृत कृषी उत्पन्न बाजार समिती (APMC) चे घाऊक लिलाव भाव, किमान/कमाल मर्यादा आणि हमीभाव (MSP) पुरवते.",
    farm_econ_title: "शेती आर्थिक व्यवहार्यता",
    farm_econ_desc:
      "प्रति एकर व हेक्टर संभाव्य उत्पन्न, सर्वंकष C2 लागवड खर्च, निव्वळ नफा आणि नफा-तोटा समतोल (Break-even) चे विश्लेषण करते.",
    explore_arrow: "तपासा →",
    supported_crops_heading: "समाविष्ट कृषी पिके (२२ प्रमुख पिके)",
    supported_crops_sub:
      "पीक अनुकूलता आणि उत्पादन अंदाज मॉडेलमध्ये समाविष्ट पिकांची सूची",

    // Crop Recommendation Page
    rec_page_title: "पीक अनुकूलता व शिफारस",
    rec_page_desc:
      "आपल्या शेतासाठी सर्वात योग्य पीक शोधण्यासाठी मातीतील मुख्य पोषक घटक (NPK), सामू (pH) आणि स्थानिक हवामानाची नोंद करा.",
    soil_presets: "मातीचे प्रीसेट:",
    preset_alluvial: "गाळाची जमीन / भात",
    preset_black_cotton: "काळी माती / कापूस",
    preset_winter_chickpea: "हिवाळी हरभरा",
    soil_env_inputs: "माती आणि पर्यावरण मापदंड",
    soil_macronutrients: "मातीतील मुख्य पोषक घटक (किलो/हेक्टर)",
    nitrogen_label: "नायट्रोजन (N)",
    phosphorus_label: "फॉस्फरस (P)",
    potassium_label: "पोटॅशियम (K)",
    soil_reaction: "मातीचा सामू (pH)",
    climatic_metrics: "हवामान आणि पर्जन्य मापदंड",
    temp_label: "तापमान (°C)",
    humidity_label: "हवेतील आर्द्रता (%)",
    rainfall_label: "पाऊस (मिमी)",
    rec_button: "मातीचे विश्लेषण करा व पीक शिफारस मिळवा",
    rec_analyzing: "कृषी विश्लेषण चालू आहे...",
    rec_primary_title: "सर्वोत्तम शिफारस केलेले पीक",
    rec_confidence: "मॉडेल विश्वासार्हता",
    rec_top_candidates: "इतर संभाव्य पर्याय पिके",
    rec_soil_diag: "माती रसायन व आरोग्य निदान",
    rec_proceed_yield: "उत्पादन अंदाजाकडे पुढे जा →",

    // Yield Prediction Page
    yield_page_title: "पीक उत्पादन अंदाज (Yield Forecasting)",
    yield_page_desc:
      "पीक निवड, प्रादेशिक हवामान, मातीचा प्रकार आणि खतांच्या प्रमाणावर आधारित प्रति हेक्टर आणि एकर अपेक्षित उत्पादनाचा अंदाज मिळवा.",
    yield_crop_label: "पिकाची निवड",
    yield_season_label: "हंगाम",
    yield_state_label: "राज्य",
    yield_soil_label: "मातीचा प्रकार",
    yield_fertilizer_label: "खते (किलो/हेक्टर)",
    yield_pesticide_label: "कीटकनाशके (किलो/हेक्टर)",
    yield_btn: "उत्पादन अंदाजाची गणना करा",
    yield_computing: "उत्पादन मॉडेल गणना करत आहे...",
    yield_predicted_label: "अंदाजित पीक उत्पादन",
    yield_proceed_fin: "शेती अर्थशास्त्राकडे पुढे जा →",

    // Mandi Price Intelligence
    mandi_page_title: "मंडी बाजारभाव माहिती",
    mandi_page_desc:
      "देशभरातील कृषी उत्पन्न बाजार समित्यांमधील (APMC) सरासरी घाऊक भाव, किमान-कमाल मर्यादा आणि शासकीय हमीभाव (MSP).",
    mandi_search_placeholder: "शेतमालाच्या नावाने शोधा (उदा. भात, गहू, कापूस, मका)...",
    col_commodity: "शेतमाल",
    col_modal_price: "सरासरी भाव (₹/क्विंटल)",
    col_min_price: "किमान भाव (₹/क्विंटल)",
    col_max_price: "कमाल भाव (₹/क्विंटल)",
    col_msp: "शासकीय हमीभाव MSP (₹/क्विंटल)",
    col_unit_price: "प्रति किलो भाव",

    // Farm Economics
    fin_page_title: "शेती आर्थिक व्यवहार्यता व नफा विश्लेषण",
    fin_page_desc:
      "प्रति एकर व हेक्टर अपेक्षित उत्पन्न, C2 सर्वंकष लागवड खर्च, निव्वळ नफा आणि नफा-तोटा समतोल सीमा यांचे सिमुलेशन.",
    fin_farm_area: "शेताचे क्षेत्रफळ",
    fin_area_unit: "एकक",
    fin_yield: "अपेक्षित उत्पादन (किलो/हेक्टर)",
    fin_price: "बाजारभाव (₹/क्विंटल)",
    fin_cost: "C2 लागवड खर्च (₹/हेक्टर)",
    fin_btn: "आर्थिक व्यवहार्यतेचे सिमुलेशन करा",
    fin_gross_revenue: "एकूण उत्पादन महसूल",
    fin_total_cost: "एकूण लागवड खर्च (C2)",
    fin_net_profit: "अंदाजित निव्वळ नफा",
    fin_roi: "गुंतवणूक परतावा (ROI)",
    fin_breakeven_yield: "किफायतशीर किमान उत्पादन (Break-Even)",
    fin_breakeven_price: "किफायतशीर किमान बाजारभाव (Break-Even)",

    // Farm Economics & Advisory extra
    sync_benchmarks: "संदर्भ खर्च सिंक करा",
    econ_sim_inputs: "आर्थिक सिमुलेशन इनपुट",
    market_rate_standards: "बाजारभाव आणि लागवड खर्च मापदंड",
    fin_failed: "आर्थिक विश्लेषण अयशस्वी",
    feasibility_summary: "व्यवहार्यता सारांश",
    net_farm_profit: "शेतीचा निव्वळ नफा",
    q_harvest: "क्विंटल उत्पादन",
    comprehensive_c2: "सर्वंकष C2 खर्च",
    margin: "नफा प्रमाण",
    profit_per_acre: "प्रति एकर नफा",
    normalized_acreage_income: "प्रति एकर निव्वळ शेती उत्पन्न",
    profit_per_ha: "प्रति हेक्टर नफा",
    standard_metric_realization: "प्रमाणित हेक्टर उत्पादन प्राप्ती",
    rev_vs_exp_breakdown: "एकूण महसूल वि. एकूण खर्च तुलना",
    critical_breakeven_thresholds: "किफायतशीर समतोल मर्यादा (Break-Even)",
    min_harvest_operational_costs: "लागवड खर्च भरून काढण्यासाठी आवश्यक किमान उत्पादन",
    floor_market_price: "खर्च भरून काढण्यासाठी किमान आवश्यक बाजारभाव",
    cacp_methodology_standards: "CACP शासकीय पद्धती मापदंड",
    generate_full_advisory_link: "संपूर्ण कृषी सल्ला अहवाल तयार करा",
    awaiting_fin_desc: "डाव्या बाजूला शेताचे क्षेत्रफळ, अपेक्षित उत्पादन आणि बाजारभाव प्रविष्ट करा, किंवा शासकीय संदर्भ खर्च मिळवण्यासाठी 'संदर्भ खर्च सिंक करा' वापरा.",
    amount_label: "रक्कम",
    adv_page_title: "एकात्मिक सर्वंकष कृषी सल्लागार प्रणाली",
    adv_page_desc: "संपूर्ण कृषी निर्णय प्रक्रिया: माती अनुकूलता तपासणे, अपेक्षित उत्पादनाचा अंदाज, घाऊक बाजारभाव संदर्भ, CACP खर्च मापदंड आणि निव्वळ नफा विश्लेषण एकाच ठिकाणी.",
    adv_btn: "सर्वंकष कृषी सल्ला तयार करा",
    adv_print: "अहवाल प्रिंट / डाउनलोड करा",
    adv_failed: "कृषी सल्ला निर्मिती अयशस्वी",
    comprehensive_inputs: "सर्वंकष शेती इनपुट्स",
    crop_recommendation_tag: "पीक शिफारस",
    projected_yield_title: "अपेक्षित उत्पादन अंदाज",
    metric_density: "हेक्टरी उत्पादन घनता",
    farm_standard: "शेतकरी प्रमाण:",
    mandi_wholesale_price: "मंडी घाऊक बाजारभाव",
    modal_wholesale_rate: "सरासरी घाऊक दर",
    cultivation_expenditure_breakdown: "लागवड खर्च तपशील (CACP C2)",
    state_applied: "राज्य:",
    cost_seed: "बियाणे खर्च",
    cost_fertilizer: "रासायनिक व सेंद्रिय खते",
    cost_labor: "मानवी मजूर खर्च",
    cost_machinery: "यंत्रसामग्री खर्च",
    total_cost_per_ha: "प्रति हेक्टर एकूण खर्च:",
    farm_profitability_roi: "शेती नफा आणि गुंतवणूक परतावा (ROI)",
    awaiting_adv_desc: "डाव्या बाजूला मातीचे घटक, प्रदेश आणि शेताचे क्षेत्रफळ प्रविष्ट करा, नंतर एकात्मिक विश्लेषणासाठी 'सर्वंकष कृषी सल्ला तयार करा' वर क्लिक करा.",
    total_harvest_label: "एकूण उत्पादन:",
    acre_cost_label: "प्रति एकर खर्च:",
    profit_label: "निव्वळ नफा:",
    msp_label: "शासकीय हमीभाव MSP:",
    soil_chemistry_title: "माती रसायन (N-P-K आणि सामू pH)",
    retained_from_rec: "पीक शिफारसीमधून माहिती प्राप्त झाली",
    retained_from_yield: "उत्पादन अंदाजावरून माहिती प्राप्त झाली",
    retained_from_fin: "शेती अर्थशास्त्रावरून माहिती प्राप्त झाली",
    forecast_this_candidate: "उत्पादन अंदाज घ्या →",

    // Awaiting states & result badges
    awaiting_soil_title: "माती मापदंडांची प्रतीक्षा",
    awaiting_soil_desc:
      "डाव्या बाजूला मातीचे घटक समायोजित करा किंवा प्रीसेट निवडा, नंतर पीक अनुकूलतेचे मूल्यांकन करण्यासाठी \"मातीचे विश्लेषण करा\" वर क्लिक करा.",
    primary_crop_badge: "सर्वोत्कृष्ट शिफारस केलेले पीक",
    match_badge: "अनुकूलता",
    soil_advisory_label: "कृषी माती आरोग्य सल्ला:",
    suitable_for_soil: "नोंदवलेल्या माती परिस्थितीसाठी अनुकूल",
    candidate_prob_dist: "संभाव्य पिकांचे अनुकूलता गुण वितरण",
    suitability_score_unit: "सर्वोत्कृष्ट मूल्यमापन केलेल्या पिकांचे अनुकूलता गुण",
    awaiting_yield_title: "उत्पादन मापदंडांची प्रतीक्षा",
    awaiting_yield_desc:
      "डाव्या बाजूला पीक, हंगाम, राज्य आणि मातीचे गुणधर्म निवडा आणि अपेक्षित उत्पादनाची गणना करा.",
    awaiting_fin_title: "आर्थिक मापदंडांची प्रतीक्षा",
    awaiting_adv_title: "सल्लागार मापदंडांची प्रतीक्षा",
  },
  hi: {
    // Header & Navigation
    brand_sub: "कृषि बुद्धिमत्ता प्रणाली",
    nav_overview: "अवलोकन",
    nav_recommend: "फसल सिफारिश",
    nav_yield: "उपज पूर्वानुमान",
    nav_market: "बाजार भाव",
    nav_financials: "कृषि अर्थशास्त्र",
    nav_advisory: "समग्र सलाह",
    status_operational: "सिस्टम चालू है",
    status_offline: "बैकएंड ऑफलाइन",
    status_connecting: "कनेक्ट हो रहा है...",
    select_language: "भाषा चुनें",
    footer_desc:
      "मिट्टी और जलवायु अनुकूलता वर्गीकरण, फसल उपज पूर्वानुमान, मंडी बाजार भाव और कृषि आर्थिक व्यवहार्यता को जोड़ने वाली निर्णय प्रणाली।",
    footer_sources: "डेटा स्रोत: एग्मार्कनेट • डीईएस • सीएसीपी",
    footer_disclaimer:
      "संभाव्य कृषि सलाह • वास्तविक उपज और मूल्य स्थानीय परिस्थितियों के अनुसार भिन्न हो सकते हैं",

    // Overview Page
    hero_headline: "भूमि एक समग्र व्यवस्था है।",
    hero_subheadline:
      "कार्पो (KARPO) एक ही मंच पर पर्यावरणीय स्थिति, फसल उपयुक्तता, अपेक्षित उपज और कृषि अर्थशास्त्र का विश्लेषण करता है। आधिकारिक कृषि डेटा द्वारा समर्थित सटीक बुआई निर्णय लें।",
    explore_crop_rec: "फसल सिफारिश देखें",
    view_full_advisory: "पूर्ण कृषि सलाह देखें",
    system_inventory: "सिस्टम डेटा सूची",
    official_datasets: "सरकारी आधिकारिक संदर्भ डेटासेट",
    supported_crops: "समर्थित फसलें",
    species_unit: "प्रजातियां",
    across_categories: "6 प्रमुख कृषि श्रेणियों में",
    mandi_coverage: "मंडी बाजार कवरेज",
    commodities_unit: "कृषि जिंस",
    mandi_sub: "थोक बाजार मूल्य और न्यूनतम समर्थन मूल्य (MSP)",
    cost_benchmarks: "लागत बेंचमार्क",
    records_unit: "रिकॉर्ड",
    cacp_sub: "CACP राज्यवार खेती व्यय सर्वेक्षण",
    historical_harvests: "ऐतिहासिक उपज डेटा",
    surveys_unit: "सर्वेक्षण",
    yield_sub: "दीर्घकालिक फसल उपज डेटा रिकॉर्ड",
    benchmarks_heading: "ऐतिहासिक फसल उपज संदर्भ मानक",
    benchmarks_sub: "भारतीय कृषि-जलवायु क्षेत्रों में राष्ट्रीय औसत उपज",
    median_harvest: "औसत उपज:",
    historical_range: "ऐतिहासिक सीमा:",
    source_des: "स्रोत: अर्थशास्त्र और सांख्यिकी निदेशालय (DES)",
    forecast_yield_btn: "फसल उपज का अनुमान लगाएं",
    core_capabilities: "प्रमुख क्षमताएं और विशेषताएं",
    integrated_tools: "एकीकृत कृषि और आर्थिक विश्लेषण उपकरण",
    suitability_title: "फसल उपयुक्तता",
    suitability_desc:
      "मिट्टी के पोषक तत्वों (NPK), pH और स्थानीय मौसम का विश्लेषण करके सबसे उपयुक्त फसलों की सिफारिश करता है।",
    yield_forecasting_title: "उपज पूर्वानुमान (Yield Forecast)",
    yield_forecasting_desc:
      "क्षेत्रीय परिस्थितियों के आधार पर मीट्रिक (किग्रा/हेक्टेयर) और किसान (क्विंटल/एकड़) दोनों इकाइयों में अनुमानित उपज प्रस्तुत करता है।",
    mandi_intel_title: "मंडी बाजार भाव सूचना",
    mandi_intel_desc:
      "आधिकारिक कृषि उपज मंडी (APMC) के थोक नीलामी भाव, न्यूनतम/अधिकतम सीमा और न्यूनतम समर्थन मूल्य (MSP) प्रदान करता है।",
    farm_econ_title: "कृषि आर्थिक व्यवहार्यता",
    farm_econ_desc:
      "प्रति एकड़ और हेक्टेयर अनुमानित राजस्व, व्यापक C2 खेती लागत, शुद्ध लाभ और ब्रेक-ईवन सीमा का विश्लेषण करता है।",
    explore_arrow: "देखें →",
    supported_crops_heading: "समर्थित कृषि फसलें (22 प्रमुख फसलें)",
    supported_crops_sub: "फसल उपयुक्तता और उपज मॉडल में समर्थित फसलों की सूची",

    // Crop Recommendation Page
    rec_page_title: "फसल उपयुक्तता व सिफारिश",
    rec_page_desc:
      "अपने खेत के लिए सर्वोत्तम फसल जानने के लिए मिट्टी के पोषक तत्व (NPK), pH और स्थानीय मौसम दर्ज करें।",
    soil_presets: "मिट्टी प्रीसेट:",
    preset_alluvial: "जलोढ़ धान",
    preset_black_cotton: "काली मिट्टी कपास",
    preset_winter_chickpea: "सर्दियों का चना",
    soil_env_inputs: "मिट्टी और पर्यावरण पैरामीटर",
    soil_macronutrients: "मिट्टी के मुख्य पोषक तत्व (किग्रा/हेक्टेयर)",
    nitrogen_label: "नाइट्रोजन (N)",
    phosphorus_label: "फास्फोरस (P)",
    potassium_label: "पोटेशियम (K)",
    soil_reaction: "मिट्टी का pH",
    climatic_metrics: "मौसम और वर्षा पैरामीटर",
    temp_label: "तापमान (°C)",
    humidity_label: "आर्द्रता (%)",
    rainfall_label: "वर्षा (मिमी)",
    rec_button: "मिट्टी का विश्लेषण करें और फसल सिफारिश पाएं",
    rec_analyzing: "कृषि विश्लेषण जारी है...",
    rec_primary_title: "सर्वश्रेष्ठ अनुशंसित फसल",
    rec_confidence: "मॉडल विश्वसनीयता",
    rec_top_candidates: "अन्य वैकल्पिक फसलें",
    rec_soil_diag: "मिट्टी रसायन और स्वास्थ्य निदान",
    rec_proceed_yield: "उपज पूर्वानुमान की ओर बढ़ें →",

    // Yield Prediction Page
    yield_page_title: "फसल उपज पूर्वानुमान",
    yield_page_desc:
      "फसल चयन, क्षेत्रीय जलवायु, मिट्टी के प्रकार और उर्वरक इनपुट के आधार पर प्रति हेक्टेयर और एकड़ अनुमानित उपज प्राप्त करें।",
    yield_crop_label: "फसल का चयन",
    yield_season_label: "फसल का मौसम",
    yield_state_label: "राज्य",
    yield_soil_label: "मिट्टी का प्रकार",
    yield_fertilizer_label: "उर्वरक (किग्रा/हेक्टेयर)",
    yield_pesticide_label: "कीटनाशक (किग्रा/हेक्टेयर)",
    yield_btn: "उपज पूर्वानुमान की गणना करें",
    yield_computing: "उपज मॉडल गणना कर रहा है...",
    yield_predicted_label: "अनुमानित फसल उपज",
    yield_proceed_fin: "कृषि अर्थशास्त्र की ओर बढ़ें →",

    // Mandi Price Intelligence
    mandi_page_title: "मंडी बाजार भाव सूचना",
    mandi_page_desc:
      "देश भर की कृषि उपज मंडियों (APMC) के थोक औसत भाव, न्यूनतम-अधिकतम सीमा और सरकारी न्यूनतम समर्थन मूल्य (MSP)।",
    mandi_search_placeholder: "जिंस के नाम से खोजें (उदा. चावल, गेहूं, कपास, मक्का)...",
    col_commodity: "कृषि जिंस",
    col_modal_price: "औसत भाव (₹/क्विंटल)",
    col_min_price: "न्यूनतम भाव (₹/क्विंटल)",
    col_max_price: "अधिकतम भाव (₹/क्विंटल)",
    col_msp: "सरकारी MSP (₹/क्विंटल)",
    col_unit_price: "प्रति किग्रा भाव",

    // Farm Economics
    fin_page_title: "कृषि वित्तीय व्यवहार्यता और लाभ विश्लेषण",
    fin_page_desc:
      "प्रति एकड़ और हेक्टेयर अनुमानित आय, C2 खेती लागत, शुद्ध लाभ और ब्रेक-ईवन सीमा का सिमुलेशन।",
    fin_farm_area: "खेत का क्षेत्रफल",
    fin_area_unit: "इकाई",
    fin_yield: "अपेक्षित उपज (किग्रा/हेक्टेयर)",
    fin_price: "बाजार भाव (₹/क्विंटल)",
    fin_cost: "C2 खेती लागत (₹/हेक्टेयर)",
    fin_btn: "वित्तीय व्यवहार्यता का सिमुलेशन करें",
    fin_gross_revenue: "सकल उत्पादन राजस्व",
    fin_total_cost: "कुल खेती लागत (C2)",
    fin_net_profit: "अनुमानित शुद्ध लाभ",
    fin_roi: "निवेश पर प्रतिफल (ROI)",
    fin_breakeven_yield: "न्यूनतम व्यवहार्य उपज (Break-Even)",
    fin_breakeven_price: "न्यूनतम व्यवहार्य मूल्य (Break-Even)",

    // Farm Economics & Advisory extra
    sync_benchmarks: "बेंचमार्क सिंक करें",
    econ_sim_inputs: "आर्थिक सिमुलेशन इनपुट",
    market_rate_standards: "बाजार भाव और खेती लागत मानक",
    fin_failed: "वित्तीय विश्लेषण विफल",
    feasibility_summary: "व्यवहार्यता सारांश",
    net_farm_profit: "खेत का शुद्ध लाभ",
    q_harvest: "क्विंटल उपज",
    comprehensive_c2: "व्यापक C2 लागत",
    margin: "लाभ मार्जिन",
    profit_per_acre: "प्रति एकड़ लाभ",
    normalized_acreage_income: "प्रति एकड़ शुद्ध कृषि आय",
    profit_per_ha: "प्रति हेक्टेयर लाभ",
    standard_metric_realization: "मानक हेक्टेयर उत्पादन प्राप्ति",
    rev_vs_exp_breakdown: "सकल राजस्व बनाम कुल व्यय तुलना",
    critical_breakeven_thresholds: "महत्वपूर्ण ब्रेक-ईवन सीमाएं (Break-Even)",
    min_harvest_operational_costs: "लागत पूरी करने के लिए आवश्यक न्यूनतम उपज",
    floor_market_price: "लागत निकालने के लिए न्यूनतम आवश्यक बाजार भाव",
    cacp_methodology_standards: "CACP सरकारी पद्धति मानक",
    generate_full_advisory_link: "पूर्ण कृषि सलाह रिपोर्ट तैयार करें",
    awaiting_fin_desc: "बाईं ओर खेत का क्षेत्रफल, अपेक्षित उपज और बाजार दर दर्ज करें, या सरकारी लागत मानक प्राप्त करने के लिए 'बेंचमार्क सिंक करें' पर क्लिक करें।",
    amount_label: "राशि",
    adv_page_title: "एकीकृत समग्र कृषि सलाहकार प्रणाली",
    adv_page_desc: "संपूर्ण कृषि निर्णय प्रक्रिया: मिट्टी उपयुक्तता विश्लेषण, अपेक्षित उपज पूर्वानुमान, थोक मंडी भाव संदर्भ, CACP लागत मानक और शुद्ध लाभ गणना एक ही स्थान पर।",
    adv_btn: "समग्र कृषि सलाह तैयार करें",
    adv_print: "रिपोर्ट प्रिंट / डाउनलोड करें",
    adv_failed: "कृषि सलाह निर्माण विफल",
    comprehensive_inputs: "समग्र कृषि इनपुट",
    crop_recommendation_tag: "फसल सिफारिश",
    projected_yield_title: "अनुमानित उपज",
    metric_density: "हेक्टेयर उपज घनता",
    farm_standard: "खेत मानक:",
    mandi_wholesale_price: "मंडी थोक बाजार भाव",
    modal_wholesale_rate: "औसत थोक दर",
    cultivation_expenditure_breakdown: "खेती लागत विवरण (CACP C2)",
    state_applied: "राज्य:",
    cost_seed: "बीज लागत",
    cost_fertilizer: "उर्वरक लागत",
    cost_labor: "मानव श्रम लागत",
    cost_machinery: "मशीनरी लागत",
    total_cost_per_ha: "प्रति हेक्टेयर कुल लागत:",
    farm_profitability_roi: "कृषि लाभ और निवेश पर प्रतिफल (ROI)",
    awaiting_adv_desc: "बाईं ओर मिट्टी के पैरामीटर, राज्य और खेत का क्षेत्रफल चुनें, फिर एकीकृत विश्लेषण के लिए 'समग्र कृषि सलाह तैयार करें' पर क्लिक करें।",
    total_harvest_label: "कुल उपज:",
    acre_cost_label: "प्रति एकड़ लागत:",
    profit_label: "शुद्ध लाभ:",
    msp_label: "सरकारी एमएसपी MSP:",
    soil_chemistry_title: "मिट्टी रसायन (N-P-K और pH)",
    retained_from_rec: "फसल सिफारिश से प्राप्त जानकारी",
    retained_from_yield: "उपज पूर्वानुमान से प्राप्त जानकारी",
    retained_from_fin: "कृषि अर्थशास्त्र से प्राप्त जानकारी",
    forecast_this_candidate: "उपज पूर्वानुमान देखें →",

    // Awaiting states & result badges
    awaiting_soil_title: "मिट्टी मापदंडों की प्रतीक्षा",
    awaiting_soil_desc:
      "बाईं ओर मिट्टी के तत्व समायोजित करें या प्रीसेट चुनें, फिर अनुकूलता जानने के लिए \"विश्लेषण करें\" पर क्लिक करें।",
    primary_crop_badge: "सर्वश्रेष्ठ अनुशंसित फसल",
    match_badge: "अनुकूलता",
    soil_advisory_label: "कृषि मिट्टी स्वास्थ्य सलाह:",
    suitable_for_soil: "दर्ज की गई मिट्टी स्थितियों के लिए उपयुक्त",
    candidate_prob_dist: "उम्मीदवार फसलों का उपयुक्तता वितरण",
    suitability_score_unit: "शीर्ष मूल्यांकित फसलों के उपयुक्तता स्कोर",
    awaiting_yield_title: "उपज मापदंडों की प्रतीक्षा",
    awaiting_yield_desc:
      "बाईं ओर फसल, मौसम, राज्य और मिट्टी के गुण चुनें और अपेक्षित उपज की गणना करें।",
    awaiting_fin_title: "वित्तीय मापदंडों की प्रतीक्षा",
    awaiting_adv_title: "सलाहकार मापदंडों की प्रतीक्षा",
  },
};

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: string, defaultText?: string) => string;
  getCropName: (crop?: string) => string;
  getCategoryName: (cat?: string) => string;
  getSeasonName: (season?: string) => string;
  getSoilName: (soil?: string) => string;
  getStateName: (state?: string) => string;
  getUnitName: (unit?: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [language, setLanguageState] = useState<Language>(() => {
    try {
      const saved = localStorage.getItem("karpo_language") as Language;
      if (saved && (saved === "en" || saved === "mr" || saved === "hi")) {
        return saved;
      }
    } catch {
      // ignore localStorage errors
    }
    return "en";
  });

  const setLanguage = (lang: Language) => {
    setLanguageState(lang);
    try {
      localStorage.setItem("karpo_language", lang);
    } catch {
      // ignore
    }
  };

  const t = (key: string, defaultText?: string): string => {
    const langDict = TRANSLATIONS[language] || TRANSLATIONS.en;
    return langDict[key] || TRANSLATIONS.en[key] || defaultText || key;
  };

  const getCropName = (crop?: string): string => {
    if (!crop) return "";
    const clean = crop.toLowerCase().trim();
    if (CROP_NAMES[clean]) {
      return CROP_NAMES[clean][language] || CROP_NAMES[clean].en;
    }
    return crop;
  };

  const getCategoryName = (cat?: string): string => {
    if (!cat) return "";
    if (CATEGORY_NAMES[cat]) {
      return CATEGORY_NAMES[cat][language] || CATEGORY_NAMES[cat].en;
    }
    return cat;
  };

  const getSeasonName = (season?: string): string => {
    if (!season) return "";
    if (SEASON_NAMES[season]) {
      return SEASON_NAMES[season][language] || SEASON_NAMES[season].en;
    }
    return season;
  };

  const getSoilName = (soil?: string): string => {
    if (!soil) return "";
    if (SOIL_NAMES[soil]) {
      return SOIL_NAMES[soil][language] || SOIL_NAMES[soil].en;
    }
    return soil;
  };

  const getStateName = (st?: string): string => {
    if (!st) return "";
    const clean = st.toLowerCase().trim();
    if (STATE_NAMES[clean]) {
      return STATE_NAMES[clean][language] || STATE_NAMES[clean].en;
    }
    return st;
  };

  const getUnitName = (u?: string): string => {
    if (!u) return "";
    const clean = u.toLowerCase().trim();
    if (UNIT_NAMES[clean]) {
      return UNIT_NAMES[clean][language] || UNIT_NAMES[clean].en;
    }
    return u;
  };

  return (
    <LanguageContext.Provider
      value={{
        language,
        setLanguage,
        t,
        getCropName,
        getCategoryName,
        getSeasonName,
        getSoilName,
        getStateName,
        getUnitName,
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = (): LanguageContextType => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error("useLanguage must be used within a LanguageProvider");
  }
  return context;
};
