"""
Multilingual translation dictionary and helpers for Smart Crop Advisory System.
Supports English, Marathi (मराठी), and Hindi (हिंदी).
"""

from typing import Dict

# Supported language identifiers
LANG_EN = "en"
LANG_MR = "mr"
LANG_HI = "hi"

LANGUAGE_OPTIONS = ["English", "मराठी (Marathi)", "हिंदी (Hindi)"]

LANG_CODE_MAP = {
    "English": LANG_EN,
    "मराठी (Marathi)": LANG_MR,
    "हिंदी (Hindi)": LANG_HI,
}

# Crop translations (canonical crop name -> vernacular names)
CROP_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "rice": {"en": "Rice", "mr": "भात / तांदूळ (Rice)", "hi": "चावल / धान (Rice)"},
    "wheat": {"en": "Wheat", "mr": "गहू (Wheat)", "hi": "गेहूं (Wheat)"},
    "maize": {"en": "Maize", "mr": "मका (Maize)", "hi": "मक्का (Maize)"},
    "chickpea": {"en": "Chickpea", "mr": "हरभरा / चना (Chickpea)", "hi": "चना (Chickpea)"},
    "kidneybeans": {
        "en": "Kidney Beans",
        "mr": "राजमा (Kidney Beans)",
        "hi": "राजमा (Kidney Beans)",
    },
    "pigeonpeas": {
        "en": "Pigeonpeas",
        "mr": "तूर (Pigeonpeas/Arhar)",
        "hi": "अरहर / तुअर (Pigeonpeas)",
    },
    "mothbeans": {"en": "Mothbeans", "mr": "मठ (Mothbeans)", "hi": "मोठ (Mothbeans)"},
    "mungbean": {"en": "Mungbean", "mr": "मूग (Mungbean)", "hi": "मूंग (Mungbean)"},
    "blackgram": {"en": "Blackgram", "mr": "उडीद (Blackgram)", "hi": "उड़द (Blackgram)"},
    "lentil": {"en": "Lentil", "mr": "मसूर (Lentil)", "hi": "मसूर (Lentil)"},
    "pomegranate": {"en": "Pomegranate", "mr": "डाळिंब (Pomegranate)", "hi": "अनार (Pomegranate)"},
    "banana": {"en": "Banana", "mr": "केळी (Banana)", "hi": "केला (Banana)"},
    "mango": {"en": "Mango", "mr": "आंबा (Mango)", "hi": "आम (Mango)"},
    "grapes": {"en": "Grapes", "mr": "द्राक्षे (Grapes)", "hi": "अंगूर (Grapes)"},
    "watermelon": {"en": "Watermelon", "mr": "कलिंगड (Watermelon)", "hi": "तरबूज (Watermelon)"},
    "muskmelon": {"en": "Muskmelon", "mr": "खरबूज (Muskmelon)", "hi": "खरबूजा (Muskmelon)"},
    "apple": {"en": "Apple", "mr": "सफरचंद (Apple)", "hi": "सेब (Apple)"},
    "orange": {"en": "Orange", "mr": "संत्रा (Orange)", "hi": "संतरा (Orange)"},
    "papaya": {"en": "Papaya", "mr": "पपई (Papaya)", "hi": "पपीता (Papaya)"},
    "coconut": {"en": "Coconut", "mr": "नारळ (Coconut)", "hi": "नारियल (Coconut)"},
    "cotton": {"en": "Cotton", "mr": "कापूस (Cotton)", "hi": "कपास (Cotton)"},
    "jute": {"en": "Jute", "mr": "ताग (Jute)", "hi": "पटसन / जूट (Jute)"},
    "coffee": {"en": "Coffee", "mr": "कॉफी (Coffee)", "hi": "कॉफी (Coffee)"},
    "sugarcane": {"en": "Sugarcane", "mr": "ऊस (Sugarcane)", "hi": "गन्ना (Sugarcane)"},
}

# General UI Translations
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # App Header
    "hero_title": {
        "en": "🌾 Smart Crop Advisory System",
        "mr": "🌾 स्मार्ट पीक सल्लागार प्रणाली",
        "hi": "🌾 स्मार्ट फसल सलाहकार प्रणाली",
    },
    "hero_subtitle": {
        "en": "Machine Learning Based Crop Recommendation, Yield Prediction & Profit Estimation",
        "mr": "मशीन लर्निंग आधारित पीक शिफारस, उत्पादन अंदाज आणि नफा विश्लेषण",
        "hi": "मशीन लर्निंग आधारित फसल सिफारिश, उपज अनुमान और लाभ विश्लेषण",
    },
    "select_language": {
        "en": "Select Language",
        "mr": "भाषा निवडा",
        "hi": "भाषा चुनें",
    },
    "language": {
        "en": "Language",
        "mr": "भाषा",
        "hi": "भाषा",
    },
    # Sidebar
    "sidebar_farm_setup": {
        "en": "🌾 Farm & Environment Setup",
        "mr": "🌾 शेत आणि पर्यावरण तपशील",
        "hi": "🌾 खेत और पर्यावरण सेटअप",
    },
    "preset_label": {
        "en": "⚡ Select Agro-Climatic Preset:",
        "mr": "⚡ कृषी-हवामान प्रीसेट निवडा:",
        "hi": "⚡ कृषि-जलवायु प्रीसेट चुनें:",
    },
    "preset_custom": {
        "en": "Custom Parameters",
        "mr": "सानुकूल मापदंड (Custom Parameters)",
        "hi": "कस्टम पैरामीटर्स (Custom Parameters)",
    },
    "preset_gangetic": {
        "en": "🌾 Gangetic Plains (Alluvial / Rice-Wheat)",
        "mr": "🌾 गंगा मैदान (गाळाची माती / भात-गहू)",
        "hi": "🌾 गंगा का मैदान (जलोढ़ / चावल-गेहूं)",
    },
    "preset_deccan": {
        "en": "🌿 Deccan Plateau (Black Soil / Cotton-Gram)",
        "mr": "🌿 दख्खनचे पठार (काळी माती / कापूस-हरभरा)",
        "hi": "🌿 दक्कन का पठार (काली मिट्टी / कपास-चना)",
    },
    "preset_semiarid": {
        "en": "☀️ Semi-Arid Rajasthan (Bajra / Pulses)",
        "mr": "☀️ निम-शुष्क राजस्थान (बाजरी / कडधान्ये)",
        "hi": "☀️ अर्ध-शुष्क राजस्थान (बाजरा / दालें)",
    },
    "preset_coastal": {
        "en": "🌴 Coastal Humid (Paddy / Plantation)",
        "mr": "🌴 किनारपट्टी दमट हवामान (भात / बागायत)",
        "hi": "🌴 तटीय आर्द्र (धान / बागवानी)",
    },
    "sec_soil": {
        "en": "🧪 Soil Nutrients (NPK & pH)",
        "mr": "🧪 मातीचे पोषक घटक (NPK व सामू/pH)",
        "hi": "🧪 मिट्टी के पोषक तत्व (NPK व pH)",
    },
    "sec_climate": {
        "en": "🌦️ Climate & Weather Parameters",
        "mr": "🌦️ हवामान आणि पर्जन्य घटक",
        "hi": "🌦️ मौसम और जलवायु पैरामीटर",
    },
    "sec_geography": {
        "en": "📍 Geographic & Agronomic Profile",
        "mr": "📍 भौगोलिक व कृषी प्रोफाइल",
        "hi": "📍 भौगोलिक और कृषि प्रोफाइल",
    },
    "sec_land": {
        "en": "📐 Landholding & Farm Area",
        "mr": "📐 शेतजमीन आणि क्षेत्रफळ",
        "hi": "📐 खेत का क्षेत्रफल व आकार",
    },
    "nitrogen": {
        "en": "Nitrogen (N) kg/ha",
        "mr": "नायट्रोजन (N) किलो/हेक्टर",
        "hi": "नाइट्रोजन (N) किग्रा/हेक्टेयर",
    },
    "phosphorus": {
        "en": "Phosphorus (P) kg/ha",
        "mr": "फॉस्फरस (P) किलो/हेक्टर",
        "hi": "फास्फोरस (P) किग्रा/हेक्टेयर",
    },
    "potassium": {
        "en": "Potassium (K) kg/ha",
        "mr": "पोटॅशियम (K) किलो/हेक्टर",
        "hi": "पोटेशियम (K) किग्रा/हेक्टेयर",
    },
    "ph": {
        "en": "Soil pH",
        "mr": "मातीचा सामू (pH)",
        "hi": "मिट्टी का pH",
    },
    "temperature": {
        "en": "Temperature (°C)",
        "mr": "तापमान (°C)",
        "hi": "तापमान (°C)",
    },
    "humidity": {
        "en": "Humidity (%)",
        "mr": "हवेतील आर्द्रता (%)",
        "hi": "हवा की आर्द्रता / नमी (%)",
    },
    "rainfall": {
        "en": "Rainfall (mm)",
        "mr": "वार्षिक पाऊस (मिमी)",
        "hi": "वार्षिक वर्षा (मिमी)",
    },
    "state": {
        "en": "State:",
        "mr": "राज्य:",
        "hi": "राज्य:",
    },
    "soil_class": {
        "en": "Soil Classification:",
        "mr": "मातीचा प्रकार:",
        "hi": "मिट्टी का वर्गीकरण:",
    },
    "season": {
        "en": "Cropping Season:",
        "mr": "हंगाम:",
        "hi": "फसल का मौसम:",
    },
    "farm_size": {
        "en": "Farm Size:",
        "mr": "शेताचे क्षेत्रफळ:",
        "hi": "खेत का आकार:",
    },
    "unit": {
        "en": "Unit:",
        "mr": "एकक:",
        "hi": "इकाई:",
    },
    "unit_acre": {
        "en": "Acre",
        "mr": "एकर",
        "hi": "एकड़",
    },
    "unit_hectare": {
        "en": "Hectare",
        "mr": "हेक्टर",
        "hi": "हेक्टेयर",
    },
    "sidebar_footer": {
        "en": "Smart Crop Advisory System | Powered by Deep Learning & Agronomic Economics",
        "mr": "स्मार्ट पीक सल्लागार प्रणाली | मशीन लर्निंग व कृषी अर्थशास्त्र समर्थित",
        "hi": "स्मार्ट फसल सलाहकार प्रणाली | मशीन लर्निंग और कृषि अर्थशास्त्र द्वारा संचालित",
    },
    # Tabs
    "tab_advisory": {
        "en": "🌾 Advisory Dashboard",
        "mr": "🌾 सल्लागार डॅशबोर्ड",
        "hi": "🌾 सलाहकार डैशबोर्ड",
    },
    "tab_technical": {
        "en": "📊 Model Metrics & Visualizations",
        "mr": "📊 मॉडेल मेट्रिक्स आणि आलेख",
        "hi": "📊 मॉडल मेट्रिक्स और विज़ुअलाइज़ेशन",
    },
    "tab_price_explorer": {
        "en": "💰 Price & Cost Reference",
        "mr": "💰 बाजारभाव आणि खर्च संदर्भ",
        "hi": "💰 बाजार भाव और लागत संदर्भ",
    },
    # Metric Cards
    "metric_recommended_crop": {
        "en": "🌱 Recommended Crop",
        "mr": "🌱 शिफारस केलेले पीक",
        "hi": "🌱 अनुशंसित फसल",
    },
    "metric_confidence": {
        "en": "Confidence:",
        "mr": "विश्वासार्हता:",
        "hi": "विश्वसनीयता:",
    },
    "metric_predicted_yield": {
        "en": "📊 Predicted Yield",
        "mr": "📊 अंदाजित उत्पादन",
        "hi": "📊 अनुमानित उपज",
    },
    "metric_market_price": {
        "en": "💰 Market Price",
        "mr": "💰 बाजारभाव",
        "hi": "💰 बाजार भाव",
    },
    "metric_cultivation_cost": {
        "en": "💵 Cultivation Cost",
        "mr": "💵 लागवड खर्च",
        "hi": "💵 खेती की लागत",
    },
    "metric_total_revenue": {
        "en": "📈 Total Revenue",
        "mr": "📈 एकूण उत्पन्न",
        "hi": "📈 कुल आय",
    },
    "metric_estimated_profit": {
        "en": "🟢 Estimated Profit",
        "mr": "🟢 अंदाजित नफा",
        "hi": "🟢 अनुमानित लाभ",
    },
    "per_quintal": {
        "en": "Per Quintal",
        "mr": "प्रति क्विंटल",
        "hi": "प्रति क्विंटल",
    },
    "per_acre": {
        "en": "Per Acre",
        "mr": "प्रति एकर",
        "hi": "प्रति एकड़",
    },
    "production": {
        "en": "Production:",
        "mr": "उत्पादन:",
        "hi": "उत्पादन:",
    },
    "quintals": {
        "en": "Quintals",
        "mr": "क्विंटल",
        "hi": "क्विंटल",
    },
    "roi": {
        "en": "ROI:",
        "mr": "परतावा (ROI):",
        "hi": "प्रतिफल (ROI):",
    },
    # Crop Recommendation Analysis Section
    "rec_analysis_title": {
        "en": "🌱 Crop Recommendation Analysis",
        "mr": "🌱 पीक शिफारस सखोल विश्लेषण",
        "hi": "🌱 फसल सिफारिश गहन विश्लेषण",
    },
    "primary_match": {
        "en": "Primary Agronomic Match:",
        "mr": "प्रमुख कृषी जुळणी:",
        "hi": "प्राथमिक कृषि मिलान:",
    },
    "description_label": {
        "en": "Description:",
        "mr": "माहिती:",
        "hi": "विवरण:",
    },
    "top_candidates_title": {
        "en": "🏆 Top Candidate Crops by Model Confidence:",
        "mr": "🏆 मॉडेल विश्वासार्हतेनुसार इतर संभाव्य पिके:",
        "hi": "🏆 मॉडल विश्वसनीयता के अनुसार शीर्ष विकल्प फसलें:",
    },
    "candidate_crop": {
        "en": "Candidate Crop",
        "mr": "संभाव्य पीक",
        "hi": "उम्मीदवार फसल",
    },
    "category": {
        "en": "Category",
        "mr": "प्रवर्ग",
        "hi": "श्रेणी",
    },
    "confidence_score": {
        "en": "Confidence Score (%)",
        "mr": "विश्वासार्हता गुण (%)",
        "hi": "विश्वसनीयता स्कोर (%)",
    },
    "soil_diag_title": {
        "en": "🧪 Agronomic Soil Diagnosis:",
        "mr": "🧪 मातीचे कृषी आरोग्य निदान:",
        "hi": "🧪 मिट्टी का कृषि स्वास्थ्य निदान:",
    },
    "soil_optimal": {
        "en": "✅ Soil NPK nutrients and pH are within optimal agronomic thresholds for this crop.",
        "mr": "✅ या पिकासाठी मातीतील NPK पोषक घटक आणि सामू (pH) योग्य प्रमाणात आहेत.",
        "hi": "✅ इस फसल के लिए मिट्टी के NPK पोषक तत्व और pH अनुकूल स्तर पर हैं।",
    },
    # Financial Table
    "fin_breakdown_title": {
        "en": "📊 Financial & Production Breakdown",
        "mr": "📊 आर्थिक व उत्पादन तपशील",
        "hi": "📊 वित्तीय और उत्पादन विवरण",
    },
    "param_farm_size": {
        "en": "Farm Operational Size",
        "mr": "शेताचे कार्यात्मक क्षेत्र",
        "hi": "खेत का परिचालन आकार",
    },
    "param_total_harvest": {
        "en": "Total Expected Harvest",
        "mr": "एकूण अपेक्षित उत्पादन",
        "hi": "कुल अपेक्षित उपज",
    },
    "param_gross_revenue": {
        "en": "Gross Revenue (Market Sale)",
        "mr": "एकूण महसूल (बाजार विक्री)",
        "hi": "सकल राजस्व (बाजार बिक्री)",
    },
    "param_cul_cost": {
        "en": "Comprehensive Cultivation Cost (C2)",
        "mr": "एकूण लागवड खर्च (C2)",
        "hi": "व्यापक खेती लागत (C2)",
    },
    "param_net_profit": {
        "en": "Estimated Net Profit",
        "mr": "अंदाजित निव्वळ नफा",
        "hi": "अनुमानित शुद्ध लाभ",
    },
    "param_profit_per_acre": {
        "en": "Net Profit Per Acre",
        "mr": "प्रति एकर निव्वळ नफा",
        "hi": "प्रति एकड़ शुद्ध लाभ",
    },
    "param_roi": {
        "en": "Return on Investment (ROI)",
        "mr": "गुंतवणुकीवर परतावा (ROI)",
        "hi": "निवेश पर प्रतिफल (ROI)",
    },
    "param_breakeven_yield": {
        "en": "Break-Even Harvest Yield",
        "mr": "किफायतशीर किमान उत्पादन (Break-Even Yield)",
        "hi": "न्यूनतम व्यवहार्य उपज (Break-Even Yield)",
    },
    "param_breakeven_price": {
        "en": "Break-Even Market Price",
        "mr": "किफायतशीर किमान भाव (Break-Even Price)",
        "hi": "न्यूनतम व्यवहार्य मूल्य (Break-Even Price)",
    },
    "col_parameter": {
        "en": "Parameter",
        "mr": "घटक",
        "hi": "पैरामीटर",
    },
    "col_estimated_val": {
        "en": "Estimated Value",
        "mr": "अंदाजित मूल्य",
        "hi": "अनुमानित मान",
    },
    "cost_comp_title": {
        "en": "💵 C2 Cost Composition per Hectare:",
        "mr": "💵 प्रति हेक्टर C2 खर्च रचना:",
        "hi": "💵 प्रति हेक्टेयर C2 लागत संरचना:",
    },
    # Cost Breakdown Categories
    "cost_seed": {
        "en": "Seed & Planting",
        "mr": "बियाणे व रोपे",
        "hi": "बीज और रोपाई",
    },
    "cost_fertilizer": {
        "en": "Fertilizers & Nutrients",
        "mr": "खते व पोषक तत्वे",
        "hi": "उर्वरक और पोषक तत्व",
    },
    "cost_labor": {
        "en": "Human Labor",
        "mr": "मानवी मजूर",
        "hi": "मानव श्रम",
    },
    "cost_machinery": {
        "en": "Machinery & Fuel",
        "mr": "यंत्रसामग्री व इंधन",
        "hi": "मशीनरी और ईंधन",
    },
    "cost_rent": {
        "en": "Land Rent & Fixed Capital",
        "mr": "जमीन भाडे व भांडवल",
        "hi": "भूमि किराया और निश्चित पूंजी",
    },
    "input_category": {
        "en": "Input Category",
        "mr": "खर्च प्रकार",
        "hi": "लागत श्रेणी",
    },
    "amount_rs_ha": {
        "en": "Amount (₹/ha)",
        "mr": "रक्कम (₹/हेक्टर)",
        "hi": "राशि (₹/हेक्टेयर)",
    },
    # Sensitivity Simulation
    "scenario_title": {
        "en": "📈 Dynamic Price & Yield Scenario Simulation",
        "mr": "📈 भाव आणि उत्पादन परिस्थिती सिम्युलेशन",
        "hi": "📈 मूल्य और उपज परिदृश्य सिमुलेशन",
    },
    "scenario_desc": {
        "en": "Simulate how market price fluctuations or weather variability impact your bottom line:",
        "mr": "बाजारभावातील चढउतार किंवा हवामानातील बदलांमुळे नफ्यावर होणारा परिणाम तपासा:",
        "hi": "बाजार मूल्य में उतार-चढ़ाव या मौसम परिवर्तन का अपने लाभ पर प्रभाव देखें:",
    },
    "sim_price_delta": {
        "en": "Market Price Change (%)",
        "mr": "बाजारभाव बदल (%)",
        "hi": "बाजार मूल्य परिवर्तन (%)",
    },
    "sim_yield_delta": {
        "en": "Harvest Yield Change (%)",
        "mr": "उत्पादन बदल (%)",
        "hi": "उपज परिवर्तन (%)",
    },
    "sim_revenue": {
        "en": "Simulated Revenue",
        "mr": "सिम्युलेटेड उत्पन्न",
        "hi": "सिम्युलेटेड आय",
    },
    "sim_profit": {
        "en": "Simulated Net Profit",
        "mr": "सिम्युलेटेड निव्वळ नफा",
        "hi": "सिम्युलेटेड शुद्ध लाभ",
    },
    "sim_profit_acre": {
        "en": "Profit Per Acre",
        "mr": "प्रति एकर नफा",
        "hi": "प्रति एकड़ लाभ",
    },
    # Download & Disclaimer
    "download_csv": {
        "en": "📥 Download Advisory Report as CSV",
        "mr": "📥 सल्लागार अहवाल CSV स्वरूपात डाउनलोड करा",
        "hi": "📥 सलाहकार रिपोर्ट CSV डाउनलोड करें",
    },
    "disclaimer": {
        "en": "<b>⚠️ Official Disclaimer:</b> Profit and revenue values are estimates based on the selected reference price and cultivation-cost data and may vary with actual market and farming conditions.",
        "mr": "<b>⚠️ अधिकृत सूचना:</b> नफा आणि उत्पन्नाची आकडेवारी निवडलेले बाजारभाव आणि लागवड खर्च डेटावर आधारित अंदाज आहेत आणि प्रत्यक्ष शेती व बाजार परिस्थितीनुसार बदलू शकतात.",
        "hi": "<b>⚠️ आधिकारिक अस्वीकरण:</b> लाभ और आय के आंकड़े चयनित संदर्भ मूल्य और खेती लागत डेटा पर आधारित अनुमान हैं और वास्तविक बाजार व कृषि स्थितियों के अनुसार भिन्न हो सकते हैं।",
    },
    # Technical Tab
    "tech_title": {
        "en": "### 🔬 Machine Learning Model Evaluation & Visualizations",
        "mr": "### 🔬 मशीन लर्निंग मॉडेल मूल्यांकन आणि आलेख",
        "hi": "### 🔬 मशीन लर्निंग मॉडल मूल्यांकन और विज़ुअलाइज़ेशन",
    },
    "tech_desc": {
        "en": "Both tasks evaluate **Random Forest** and **XGBoost** algorithms with reproducible seeds and automated winning model selection.",
        "mr": "दोन्ही कामांसाठी **रँडम फॉरेस्ट** आणि **एक्सजीबूस्ट** अल्गोरिदमचे पुनरावृत्तीयोग्य बियाण्यांसह मूल्यांकन केले जाते.",
        "hi": "दोनों कार्यों के लिए **रैंडम फॉरेस्ट** और **एक्सजीबूस्ट** एल्गोरिदम का मूल्यांकन और स्वचालित सर्वश्रेष्ठ मॉडल चयन किया जाता है।",
    },
    "tech_model_rec": {
        "en": "#### 🌱 1. Crop Recommendation Model",
        "mr": "#### 🌱 १. पीक शिफारस मॉडेल",
        "hi": "#### 🌱 1. फसल सिफारिश मॉडल",
    },
    "tech_model_yield": {
        "en": "#### 📊 2. Yield Prediction Regressor",
        "mr": "#### 📊 २. उत्पादन अंदाज मॉडेल",
        "hi": "#### 📊 2. उपज पूर्वानुमान मॉडल",
    },
    "tech_plots_title": {
        "en": "#### 📈 Saved Model Evaluation Plots",
        "mr": "#### 📈 सेव्ह केलेले मॉडेल मूल्यांकन आलेख",
        "hi": "#### 📈 सहेजे गए मॉडल मूल्यांकन आलेख",
    },
    # Mandi Explorer Tab
    "mandi_title": {
        "en": "### 💰 Mandi Market Price & CACP Cultivation Cost Explorer",
        "mr": "### 💰 कृषी उत्पन्न बाजार समिती (मंडी) भाव व CACP लागवड खर्च शोधक",
        "hi": "### 💰 मंडी बाजार भाव और CACP खेती लागत खोजकर्ता",
    },
    "mandi_desc": {
        "en": "Inspect reference datasets covering **122 market prices** and **CACP field crop cultivation cost surveys**.",
        "mr": "संदर्भ डेटासेट मधील **१२२ बाजारभाव** आणि **CACP पीक लागवड खर्च सर्वेक्षण** तपासा.",
        "hi": "संदर्भ डेटासेट में **122 बाजार भाव** और **CACP फसल खेती लागत सर्वेक्षण** देखें।",
    },
    "filter_crop": {
        "en": "🔍 Filter Market Prices by Crop Name:",
        "mr": "🔍 पिकाच्या नावाने बाजारभाव शोधा:",
        "hi": "🔍 फसल के नाम से बाजार भाव खोजें:",
    },
    "filter_state": {
        "en": "Filter Cost Data by State:",
        "mr": "राज्यानुसार खर्च डेटा निवडा:",
        "hi": "राज्य अनुसार लागत डेटा चुनें:",
    },
    "mandi_market_prices": {
        "en": "Mandi Market Prices",
        "mr": "मंडी बाजारभाव",
        "hi": "मंडी बाजार भाव",
    },
    "cost_of_cultivation": {
        "en": "Cost of Cultivation",
        "mr": "लागवड खर्च",
        "hi": "खेती की लागत",
    },
    "winning_model": {
        "en": "Winning Model:",
        "mr": "सर्वोत्कृष्ट मॉडेल:",
        "hi": "सर्वश्रेष्ठ मॉडल:",
    },
    "test_accuracy": {
        "en": "Test Accuracy:",
        "mr": "चाचणी अचूकता (Accuracy):",
        "hi": "परीक्षण सटीकता (Accuracy):",
    },
    "weighted_f1": {
        "en": "Weighted F1-Score:",
        "mr": "वेटेड F1-स्कोअर:",
        "hi": "वेटेड F1-स्कोर:",
    },
    "r2_score": {
        "en": "Coefficient of Determination (R²):",
        "mr": "निर्धारण गुणांक (R²):",
        "hi": "निर्धारण गुणांक (R²):",
    },
    "rmse": {
        "en": "Root Mean Squared Error (RMSE):",
        "mr": "रूट मीन स्क्वेअर एरर (RMSE):",
        "hi": "रूट मीन स्क्वेयर्ड एरर (RMSE):",
    },
    "mae": {
        "en": "Mean Absolute Error (MAE):",
        "mr": "मीन अब्सोल्युट एरर (MAE):",
        "hi": "मीन एब्सोल्यूट एरर (MAE):",
    },
}


def get_lang_code(language_name: str) -> str:
    """Map display language string to internal language code."""
    if "मराठी" in language_name or language_name.lower().startswith("mr"):
        return LANG_MR
    if "हिंदी" in language_name or language_name.lower().startswith("hi"):
        return LANG_HI
    return LANG_EN


def t(key: str, lang: str = "en") -> str:
    """
    Get translated text for a given key and language.
    Falls back to English if translation is missing.
    """
    lang_code = get_lang_code(lang)
    entry = TRANSLATIONS.get(key)
    if not entry:
        return key
    return entry.get(lang_code, entry.get(LANG_EN, key))


def get_translated_crop_name(crop_name: str, lang: str = "en") -> str:
    """Return localized display name for a crop."""
    lang_code = get_lang_code(lang)
    clean_crop = crop_name.lower().replace(" ", "")
    if clean_crop in CROP_TRANSLATIONS:
        return CROP_TRANSLATIONS[clean_crop].get(lang_code, CROP_TRANSLATIONS[clean_crop][LANG_EN])
    return crop_name.title()
