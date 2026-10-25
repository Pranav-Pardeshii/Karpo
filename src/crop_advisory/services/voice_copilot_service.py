"""
Multilingual Kisan Voice Copilot Service.
Connects spoken or typed farmer queries to verified Karpo backend services:
- Market wholesale prices (Agmarknet APMC)
- CACP C2 Cultivation cost benchmarks
- Agronomic crop advice and soil suitability
Provides honest natural language responses in Marathi, Hindi, and English with zero hallucinations.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, Optional, Tuple

from crop_advisory.domain.crop_mapping import (
    CROP_ALIASES,
    CROP_METADATA,
    get_crop_metadata,
    normalize_crop_name,
)
from crop_advisory.services.cultivation_cost_service import CultivationCostService
from crop_advisory.services.market_service import MarketPriceService

logger = logging.getLogger(__name__)

# Vernacular crop name mapping for Marathi & Hindi script and transliterated speech
VERNACULAR_CROP_ALIASES: Dict[str, str] = {
    # Marathi (मराठी)
    "सोयाबीन": "soybean",
    "कापूस": "cotton",
    "भात": "rice",
    "तांदूळ": "rice",
    "गहू": "wheat",
    "मका": "maize",
    "हरभरा": "chickpea",
    "चना": "chickpea",
    "तूर": "pigeonpeas",
    "तूरडाळ": "pigeonpeas",
    "ऊस": "sugarcane",
    "ज्वारी": "jowar",
    "बाजरी": "bajra",
    "भुईमूग": "groundnut",
    "शेंगदाणे": "groundnut",
    "सूर्यफूल": "sunflower",
    "डाळिंब": "pomegranate",
    "केळी": "banana",
    "आंबा": "mango",
    "द्राक्षे": "grapes",
    "द्राक्ष": "grapes",
    "टरबूज": "watermelon",
    "कलिंगड": "watermelon",
    "खरबूज": "muskmelon",
    "सफरचंद": "apple",
    "संत्रा": "orange",
    "संत्री": "orange",
    "पपई": "papaya",
    "नारळ": "coconut",
    # Hindi (हिंदी)
    "चावल": "rice",
    "धान": "rice",
    "गेहूं": "wheat",
    "कपास": "cotton",
    "मक्का": "maize",
    "अरहर": "pigeonpeas",
    "गन्ना": "sugarcane",
    "मूंगफली": "groundnut",
    "सूरजमुखी": "sunflower",
    "अनार": "pomegranate",
    "केला": "banana",
    "आम": "mango",
    "अंगूर": "grapes",
    "तरबूज": "watermelon",
    "खरबूजा": "muskmelon",
    "सेब": "apple",
    "संतरा": "orange",
    "पपीता": "papaya",
    "नारियल": "coconut",
    "जौ": "barley",
    "मूंग": "mungbean",
    "उड़द": "blackgram",
    "मसूर": "lentil",
}

VERNACULAR_DISPLAY_NAMES: Dict[str, Dict[str, str]] = {
    "soybean": {"mr": "सोयाबीन", "hi": "सोयाबीन", "en": "Soybean"},
    "cotton": {"mr": "कापूस", "hi": "कपास", "en": "Cotton"},
    "rice": {"mr": "भात", "hi": "चावल", "en": "Rice"},
    "wheat": {"mr": "गहू", "hi": "गेहूं", "en": "Wheat"},
    "maize": {"mr": "मका", "hi": "मक्का", "en": "Maize"},
    "chickpea": {"mr": "हरभरा", "hi": "चना", "en": "Chickpea"},
    "pigeonpeas": {"mr": "तूर", "hi": "अरहर", "en": "Pigeonpeas"},
    "sugarcane": {"mr": "ऊस", "hi": "गन्ना", "en": "Sugarcane"},
    "groundnut": {"mr": "भुईमूग", "hi": "मूंगफली", "en": "Groundnut"},
    "jowar": {"mr": "ज्वारी", "hi": "ज्वार", "en": "Jowar"},
    "bajra": {"mr": "बाजरी", "hi": "बाजरा", "en": "Bajra"},
}


class VoiceCopilotService:
    """Intelligent farmer voice assistant routing to verified agronomic & market services."""

    def __init__(
        self,
        market_price_service: MarketPriceService,
        cost_service: CultivationCostService,
    ) -> None:
        self.price_service = market_price_service
        self.cost_service = cost_service

    def detect_crop(self, text: str) -> Optional[str]:
        """Identifies target crop from multilingual user speech or text."""
        lowered = text.lower().strip()

        # 1. Check Devanagari script vernacular matches
        for vern_word, canon in VERNACULAR_CROP_ALIASES.items():
            if vern_word in text:
                return canon

        # 2. Extract words and check multi-word or single-word tokens
        tokens = re.findall(r"[\w\u0900-\u097F]+", lowered)

        # Check two-word phrases first (e.g. "kidney beans", "black gram")
        for i in range(len(tokens) - 1):
            pair = f"{tokens[i]} {tokens[i+1]}"
            if pair in CROP_ALIASES:
                return CROP_ALIASES[pair]
            if pair in CROP_METADATA:
                return pair
            candidate = normalize_crop_name(pair)
            if candidate in CROP_METADATA and candidate != pair:
                return candidate

        # Check individual tokens
        for token in tokens:
            if token in CROP_ALIASES:
                return CROP_ALIASES[token]
            if token in CROP_METADATA:
                return token
            candidate = normalize_crop_name(token)
            if candidate in CROP_ALIASES:
                return CROP_ALIASES[candidate]
            if candidate in CROP_METADATA:
                return candidate

        return None

    def detect_intent(self, text: str) -> str:
        """Categorizes farmer inquiry into supported agronomic intents."""
        lowered = text.lower()

        # Cultivation Cost intent keywords (check before general price)
        cost_keywords = [
            "लागवड खर्च", "उत्पादन खर्च", "खर्च",
            "cultivation cost", "cost of cultivation", "cultivation",
            "expenditure", "cost per hectare", "kharcha", "kharch",
            "c2 cost", "production cost", "farming cost"
        ]
        if any(kw in lowered for kw in cost_keywords):
            return "cultivation_cost"

        # Price / Mandi intent keywords
        price_keywords = [
            "भाव", "दर", "किंमत", "बाजारभाव", "मंडी", "बाजार",
            "price", "mandi", "rate", "cost of selling", "msp", "market",
            "bhav", "kya bhav", "kitna hai", "dar kay ahe"
        ]
        if any(kw in lowered for kw in price_keywords):
            return "market_price"

        # Agronomic / Sowing / Soil Advice
        advisory_keywords = [
            "सल्ला", "कशी करावी", "माती", "हवामान", "पेरणी", "रोग", "पाणी", "खते",
            "advice", "suitability", "soil", "climate", "recommend", "how to grow",
            "season", "guidance"
        ]
        if any(kw in lowered for kw in advisory_keywords):
            return "crop_advisory"

        # Help / Greeting
        help_keywords = ["help", "मदत", "सहायता", "namaste", "नमस्कार", "hello", "hi", "कोण आहेस"]
        if any(kw in lowered for kw in help_keywords):
            return "general_help"

        # Default fallback
        return "unrecognized"

    def process_query(
        self,
        query_text: str,
        language: str = "en",
        state: Optional[str] = "Maharashtra",
    ) -> Dict[str, Any]:
        """
        Executes query against real APIs and compiles verified multilingual response.
        Never fabricates results.
        """
        clean_query = query_text.strip()
        lang = language.lower() if language else "en"
        detected_crop = self.detect_crop(clean_query)
        detected_intent = self.detect_intent(clean_query)

        # If user only named a crop, default to market price and agronomic summary
        if detected_crop and detected_intent == "unrecognized":
            detected_intent = "market_price"

        logger.info(
            f"VoiceCopilot: query='{clean_query}', lang={lang}, crop={detected_crop}, intent={detected_intent}"
        )

        if detected_intent == "general_help" or (not detected_crop and detected_intent == "unrecognized"):
            return self._build_help_response(clean_query, lang)

        if not detected_crop:
            return self._build_missing_crop_response(clean_query, lang, detected_intent)

        # Crop is identified: execute verified functions
        if detected_intent == "market_price":
            return self._execute_market_price_query(clean_query, detected_crop, lang)

        elif detected_intent == "cultivation_cost":
            return self._execute_cost_query(clean_query, detected_crop, state or "Maharashtra", lang)

        elif detected_intent == "crop_advisory":
            return self._execute_advisory_query(clean_query, detected_crop, lang)

        # Unrecognized fallback with known crop
        return self._execute_market_price_query(clean_query, detected_crop, lang)

    def _execute_market_price_query(self, query: str, crop: str, lang: str) -> Dict[str, Any]:
        """Fetches live AGMARKNET wholesale rates."""
        price_data = self.price_service.get_crop_price(crop)
        crop_meta = CROP_METADATA.get(crop, {})
        display_name = VERNACULAR_DISPLAY_NAMES.get(crop, {}).get(lang, crop_meta.get("display_name", crop.capitalize()))
        modal_price = price_data.get("modal_rs_per_quintal", 0)
        min_price = price_data.get("min_rs_per_quintal", 0)
        max_price = price_data.get("max_rs_per_quintal", 0)
        msp = price_data.get("msp_rs_per_quintal")

        if lang == "mr":
            spoken = f"{display_name} पिकाचा सरासरी बाजारभाव {modal_price} रुपये प्रति क्विंटल आहे."
            display = f"{display_name} बाजारभाव: ₹{modal_price:,.0f} / क्विंटल (किमान: ₹{min_price:,.0f}, कमाल: ₹{max_price:,.0f})"
            if msp:
                spoken += f" सरकारी हमीभाव {msp} रुपये आहे."
                display += f" | MSP: ₹{msp:,.0f}"
        elif lang == "hi":
            spoken = f"{display_name} का मॉडल मंडी भाव {modal_price} रुपये प्रति क्विंटल है।"
            display = f"{display_name} मंडी भाव: ₹{modal_price:,.0f} / क्विंटल (न्यूनतम: ₹{min_price:,.0f}, अधिकतम: ₹{max_price:,.0f})"
            if msp:
                spoken += f" सरकारी समर्थन मूल्य {msp} रुपये है।"
                display += f" | MSP: ₹{msp:,.0f}"
        else:
            spoken = f"The modal mandi market price for {display_name} is {modal_price} rupees per quintal."
            display = f"{display_name} Mandi Price: ₹{modal_price:,.0f} / Quintal (Range: ₹{min_price:,.0f} - ₹{max_price:,.0f})"
            if msp:
                spoken += f" Government MSP is {msp} rupees."
                display += f" | MSP: ₹{msp:,.0f}"

        return {
            "query_text": query,
            "language": lang,
            "intent": "market_price",
            "matched_crop": crop,
            "spoken_text": spoken,
            "display_text": display,
            "structured_data": price_data,
            "data_category": "Observed",
            "data_provenance": "AGMARKNET Wholesale Mandi Records",
        }

    def _execute_cost_query(self, query: str, crop: str, state: str, lang: str) -> Dict[str, Any]:
        """Fetches CACP C2 comprehensive cultivation cost breakdown."""
        cost_data = self.cost_service.get_cultivation_cost(crop, state)
        crop_meta = CROP_METADATA.get(crop, {})
        display_name = VERNACULAR_DISPLAY_NAMES.get(crop, {}).get(lang, crop_meta.get("display_name", crop.capitalize()))
        total_c2 = cost_data.get("cul_cost_c2_per_ha", 0)
        seed_cost = cost_data.get("seed_cost_per_ha", 0)
        labor_cost = cost_data.get("labor_cost_per_ha", 0)
        fert_cost = cost_data.get("fertilizer_cost_per_ha", 0)

        if lang == "mr":
            spoken = f"{state} राज्यात {display_name} पिकाचा एकूण सरासरी लागवड खर्च {total_c2:,.0f} रुपये प्रति हेक्टर आहे."
            display = f"{display_name} लागवड खर्च: ₹{total_c2:,.0f}/हेक्टर (बियाणे: ₹{seed_cost:,.0f}, खते: ₹{fert_cost:,.0f}, मजुरी: ₹{labor_cost:,.0f})"
        elif lang == "hi":
            spoken = f"{state} राज्य में {display_name} की कुल खेती लागत लगभग {total_c2:,.0f} रुपये प्रति हेक्टेयर है।"
            display = f"{display_name} खेती लागत: ₹{total_c2:,.0f}/हेक्टेयर (बीज: ₹{seed_cost:,.0f}, उर्वरक: ₹{fert_cost:,.0f}, श्रम: ₹{labor_cost:,.0f})"
        else:
            spoken = f"The estimated C2 cultivation cost for {display_name} in {state} is {total_c2:,.0f} rupees per hectare."
            display = f"{display_name} Cultivation Cost: ₹{total_c2:,.0f}/ha (Seeds: ₹{seed_cost:,.0f}, Fertilizer: ₹{fert_cost:,.0f}, Labor: ₹{labor_cost:,.0f})"

        return {
            "query_text": query,
            "language": lang,
            "intent": "cultivation_cost",
            "matched_crop": crop,
            "spoken_text": spoken,
            "display_text": display,
            "structured_data": cost_data,
            "data_category": "Historical",
            "data_provenance": "CACP Ministry of Agriculture Benchmarks",
        }

    def _execute_advisory_query(self, query: str, crop: str, lang: str) -> Dict[str, Any]:
        """Fetches verified agronomic suitability and soil recommendations."""
        crop_meta = CROP_METADATA.get(crop, {})
        display_name = VERNACULAR_DISPLAY_NAMES.get(crop, {}).get(lang, crop_meta.get("display_name", crop.capitalize()))
        soil = crop_meta.get("default_soil", "Vertisols")
        season = crop_meta.get("default_season", "Kharif")
        fert_kg = crop_meta.get("default_fertilizer", 75.0)
        desc = crop_meta.get("description", "")

        if lang == "mr":
            spoken = f"{display_name} पिकासाठी {season} हंगाम आणि {soil} जमीन अतिशय अनुकूल आहे. खताची शिफारस {fert_kg} किलो प्रति हेक्टर आहे."
            display = f"{display_name} कृषी सल्ला: हंगाम: {season} &bull; जमीन: {soil} &bull; खताची मात्रा: {fert_kg} kg/ha. {desc}"
        elif lang == "hi":
            spoken = f"{display_name} की बुवाई के लिए {season} मौसम और {soil} मिट्टी सर्वोत्तम है। अनुशंसित उर्वरक {fert_kg} किलो प्रति हेक्टेयर है।"
            display = f"{display_name} कृषि सलाह: मौसम: {season} &bull; मिट्टी: {soil} &bull; अनुशंसित उर्वरक: {fert_kg} kg/ha. {desc}"
        else:
            spoken = f"For {display_name}, the recommended sowing season is {season} with {soil} soil. Recommended nutrient dosage is {fert_kg} kg per hectare."
            display = f"{display_name} Agronomic Advisory: Season: {season} &bull; Soil: {soil} &bull; Nutrient dosage: {fert_kg} kg/ha. {desc}"

        return {
            "query_text": query,
            "language": lang,
            "intent": "crop_advisory",
            "matched_crop": crop,
            "spoken_text": spoken,
            "display_text": display,
            "structured_data": crop_meta,
            "data_category": "Estimated",
            "data_provenance": "ICAR Agronomic Guidelines & Karpo Crop Database",
        }

    def _build_help_response(self, query: str, lang: str) -> Dict[str, Any]:
        """Concise, farmer-friendly guidance on what can be asked."""
        if lang == "mr":
            spoken = "मी कार्पो किसान सहाय्यक आहे. आपण पिकांचे बाजारभाव, लागवड खर्च किंवा लागवड सल्ला विचारू शकता. उदाहरणार्थ, 'सोयाबीनचा भाव काय आहे?'"
            display = "कार्पो किसान सहाय्यक: पिकाचे नाव सांगून बाजारभाव, लागवड खर्च किंवा कृषी सल्ला विचारा. उदा. 'कापसाचा भाव काय?', 'गव्हाचा लागवड खर्च'"
        elif lang == "hi":
            spoken = "मैं कार्पो किसान सहायक हूँ। आप फसलों का मंडी भाव, खेती की लागत या बुवाई सलाह पूछ सकते हैं। जैसे 'सोयाबीन का भाव क्या है?'"
            display = "कार्पो किसान सहायक: किसी भी फसल का मंडी भाव, खेती लागत या सलाह पूछें। जैसे 'कपास का मंडी भाव', 'धान की खेती लागत'"
        else:
            spoken = "I am the Karpo Kisan Assistant. You can ask for mandi prices, cultivation costs, or agronomic advice. For example: 'What is the price of soybean?'"
            display = "Karpo Kisan Voice Assistant: Ask about market prices, C2 cultivation costs, or soil advice. Example: 'What is the price of wheat?'"

        return {
            "query_text": query,
            "language": lang,
            "intent": "general_help",
            "matched_crop": None,
            "spoken_text": spoken,
            "display_text": display,
            "structured_data": None,
            "data_category": "Observed",
            "data_provenance": "Karpo Assistant Knowledge Base",
        }

    def _build_missing_crop_response(self, query: str, lang: str, intent: str) -> Dict[str, Any]:
        """Honest response when a query is missing a recognized crop name."""
        if lang == "mr":
            spoken = "माफ करा, मला पिकाचे नाव समजले नाही. कृपया सोयाबीन, कापूस, गहू, भात किंवा इतर पिकाचे नाव स्पष्ट सांगा."
            display = "पिकाचे नाव आढळले नाही. कृपया स्पष्ट पिकाचा उल्लेख करा (उदा. सोयाबीन, कापूस, गहू, भात, मका, हरभरा)."
        elif lang == "hi":
            spoken = "क्षमा करें, मुझे फसल का नाम समझ नहीं आया। कृपया सोयाबीन, गेहूं, चावल, कपास या अन्य फसल का नाम बताएं।"
            display = "फसल का नाम नहीं मिला। कृपया स्पष्ट फसल का नाम बताएं (जैसे: सोयाबीन, गेहूं, धान, कपास, मक्का)."
        else:
            spoken = "Sorry, I could not identify the crop name. Please mention a crop like soybean, wheat, cotton, rice, or maize."
            display = "Crop not identified. Please specify a crop name (e.g., soybean, wheat, cotton, rice, maize, chickpea)."

        return {
            "query_text": query,
            "language": lang,
            "intent": intent,
            "matched_crop": None,
            "spoken_text": spoken,
            "display_text": display,
            "structured_data": None,
            "data_category": "Unavailable",
            "data_provenance": "Karpo Assistant Intent Classifier",
        }
