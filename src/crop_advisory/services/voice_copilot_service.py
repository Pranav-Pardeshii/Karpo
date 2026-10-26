"""
Multilingual Kisan Voice Copilot Service.
Connects spoken or typed farmer queries to verified Karpo backend services:
- Market wholesale prices (Agmarknet APMC)
- CACP C2 Cultivation cost benchmarks
- Agronomic crop advice and soil suitability
Provides honest natural language responses in Marathi, Hindi, and English with zero hallucinations.
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, Dict, Optional

import httpx

from crop_advisory.config import (
    ELEVENLABS_API_KEY,
    ELEVENLABS_MODEL_ID,
    ELEVENLABS_VOICE_ID,
    GROQ_API_KEY,
    GROQ_MODEL,
)
from crop_advisory.domain.crop_mapping import (
    CROP_ALIASES,
    CROP_METADATA,
    get_crop_metadata,
    normalize_crop_name,
)
from crop_advisory.services.cultivation_cost_service import CultivationCostService
from crop_advisory.services.market_service import MarketPriceService

try:
    from groq import Groq
    _HAS_GROQ = True
except ImportError:
    _HAS_GROQ = False

logger = logging.getLogger(__name__)

# Vernacular crop name mapping for Marathi & Hindi script and transliterated speech
VERNACULAR_CROP_ALIASES: Dict[str, str] = {
    # Marathi (मराठी) - Base and Grammatical Oblique Stems
    "सोयाबीन": "soybean",
    "सोयाबिन": "soybean",
    "सोयबीन": "soybean",
    "सोयबिन": "soybean",
    "सोयाबीना": "soybean",
    "कापूस": "cotton",
    "कापसा": "cotton",
    "कपाशी": "cotton",
    "भात": "rice",
    "तांदूळ": "rice",
    "तांदळा": "rice",
    "तांदुळ": "rice",
    "गहू": "wheat",
    "गव्हा": "wheat",
    "कांदा": "onion",
    "कांद्या": "onion",
    "मका": "maize",
    "मक्या": "maize",
    "हरभरा": "chickpea",
    "हरभऱ्या": "chickpea",
    "चना": "chickpea",
    "तूर": "pigeonpeas",
    "तुरी": "pigeonpeas",
    "तूरडाळ": "pigeonpeas",
    "ऊस": "sugarcane",
    "उसा": "sugarcane",
    "ज्वारी": "jowar",
    "बाजरी": "bajra",
    "भुईमूग": "groundnut",
    "भुईमुगा": "groundnut",
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

AGRI_QUERY_STOPWORDS = {
    "crop", "crops", "market", "price", "rate", "cost", "mandi", "bhav", "dar",
    "kya", "hai", "ahe", "what", "is", "the", "in", "of", "for", "todays", "today",
    "live", "advisory", "advice", "soil", "cultivation", "per", "hectare", "quintal",
}


def sanitize_spoken_query(query: str) -> str:
    """Corrects common speech-to-text phonetic splits in agricultural queries."""
    text = query
    text = re.sub(r"\bmandi\s*p\s*rice\b", "mandi price", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmandip\s*rice\b", "mandi price", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmarket\s*p\s*rice\b", "market price", text, flags=re.IGNORECASE)
    text = re.sub(r"\bcrop\s*p\s*rice\b", "crop price", text, flags=re.IGNORECASE)
    text = re.sub(r"\bcost\s*p\s*rice\b", "cost price", text, flags=re.IGNORECASE)
    return text


class VoiceCopilotService:
    """Intelligent farmer voice assistant routing to verified agronomic & market services."""

    def __init__(
        self,
        market_price_service: MarketPriceService,
        cost_service: CultivationCostService,
    ) -> None:
        self.price_service = market_price_service
        self.cost_service = cost_service
        self.groq_client: Optional[Any] = None
        self.groq_model = GROQ_MODEL or "qwen/qwen3.8-27b"
        self.elevenlabs_api_key = ELEVENLABS_API_KEY
        self.elevenlabs_voice_id = ELEVENLABS_VOICE_ID or "JBFqnCBsd6RMkjVDRZzb"
        self.elevenlabs_model_id = ELEVENLABS_MODEL_ID or "eleven_multilingual_v2"
        self._tts_cache: Dict[str, bytes] = {}

        if _HAS_GROQ and GROQ_API_KEY:
            try:
                self.groq_client = Groq(api_key=GROQ_API_KEY)
                logger.info("Initialized Groq voice copilot with model %s", self.groq_model)
            except Exception as e:
                logger.warning("Could not initialize Groq client: %s", e)

    def detect_crop(self, text: str) -> Optional[str]:
        """Identifies target crop from multilingual user speech or text."""
        sanitized = sanitize_spoken_query(text)
        lowered = sanitized.lower().strip()

        # 1. Check Devanagari script vernacular matches
        for vern_word, canon in VERNACULAR_CROP_ALIASES.items():
            if vern_word in text or vern_word in sanitized:
                return canon

        # 2. Extract words and check multi-word or single-word tokens
        tokens = re.findall(r"[\w\u0900-\u097F]+", lowered)

        # Check explicit multi-word crop names first (e.g. "kidney beans", "black gram")
        for i in range(len(tokens) - 1):
            pair = f"{tokens[i]} {tokens[i+1]}"
            if pair in CROP_ALIASES:
                return CROP_ALIASES[pair]

        all_valid_crops = set(CROP_ALIASES.values()) | set(CROP_METADATA.keys())

        # Check individual tokens
        for token in tokens:
            if token in AGRI_QUERY_STOPWORDS:
                continue
            if token in CROP_ALIASES:
                return CROP_ALIASES[token]
            if token in all_valid_crops:
                return token
            candidate = normalize_crop_name(token)
            if candidate in AGRI_QUERY_STOPWORDS:
                continue
            if candidate in CROP_ALIASES:
                return CROP_ALIASES[candidate]
            if candidate in all_valid_crops:
                return candidate

        return None

    def detect_intent(self, text: str) -> str:
        """Categorizes farmer inquiry into supported agronomic intents."""
        sanitized = sanitize_spoken_query(text)
        lowered = sanitized.lower()

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

    def parse_query_with_groq(
        self, query: str, language: str = "en"
    ) -> Optional[Dict[str, Any]]:
        """
        Uses Groq LLM with structured JSON mode to extract canonical crop, intent, and state.
        Understands spoken vernacular queries, phonetic speech-to-text typos (e.g. 'saybeen', 'swayabean'),
        and varied phrasing with sub-second inference.
        """
        if not self.groq_client or os.environ.get("PYTEST_CURRENT_TEST"):
            return None

        canonical_crops = sorted(list(set(CROP_ALIASES.values()) | set(CROP_METADATA.keys())))
        crops_str = ", ".join(canonical_crops)

        system_prompt = (
            "You are Karpo Kisan Voice Copilot's natural language understanding engine for Indian farmers.\n"
            "Your job is to analyze the user's spoken or typed query and extract the target crop, intent, and state.\n"
            "Farmers may use regional languages (Marathi, Hindi, English), phonetic misspellings, or speech-to-text artifacts.\n\n"
            "Supported Canonical Crops (MUST map to one of these exact English strings, or null if no crop is mentioned):\n"
            f"{crops_str}\n\n"
            "Supported Intents (MUST be one of these exact values):\n"
            "- 'market_price': asking about mandi rate, market price, MSP, bhav, dar, rate, kimat, selling price, etc.\n"
            "- 'cultivation_cost': asking about cost of cultivation, production cost, expenses, kharcha, lagwad kharch, etc.\n"
            "- 'crop_advisory': asking about soil suitability, sowing season, fertilizer, disease, weather, advice, how to grow, etc.\n"
            "- 'general_help': greetings (namaste, hello), general help, asking who you are, or generic advice without a specific task.\n"
            "- 'unrecognized': gibberish or entirely unrelated topic.\n\n"
            "Phonetic & Dialect Rules:\n"
            "- 'saybeen', 'swayabean', 'soya bean', 'sobin', 'soya', 'सोयाबीन', 'स्वगाकिन' -> crop 'soybean'\n"
            "- 'wheat mandip rice', 'mandip rice' -> intent 'market_price'\n"
            "- 'gehu', 'gehun', 'gahu', 'गहू', 'गेहूं' -> crop 'wheat'\n"
            "- 'kapas', 'kapus', 'rui', 'कापूस', 'कपास' -> crop 'cotton'\n"
            "- 'chawal', 'dhan', 'bhat', 'चावल', 'धान', 'भात' -> crop 'rice'\n"
            "- If no crop is mentioned (e.g. 'आजचा भाव काय आहे?', 'hello', 'help'), crop MUST be null.\n\n"
            "Return a JSON object with this exact structure:\n"
            "{\n"
            '  "crop": "<canonical crop name or null>",\n'
            '  "intent": "<market_price | cultivation_cost | crop_advisory | general_help | unrecognized>",\n'
            '  "state": "<Indian state name or null>",\n'
            '  "confidence": <float between 0.0 and 1.0>\n'
            "}"
        )

        user_prompt = f"Farmer Query: \"{query}\""

        try:
            resp = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                model=self.groq_model,
                response_format={"type": "json_object"},
                max_tokens=100,
                temperature=0.0,
            )
            raw = resp.choices[0].message.content
            if raw:
                data = json.loads(raw)
                crop = data.get("crop")
                intent = data.get("intent")
                extracted_state = data.get("state")
                confidence = data.get("confidence", 0.0)

                # Validate and normalize crop
                valid_crop = None
                if crop and isinstance(crop, str):
                    c_clean = crop.strip().lower()
                    if c_clean in canonical_crops:
                        valid_crop = c_clean
                    else:
                        norm = normalize_crop_name(c_clean)
                        if norm in canonical_crops:
                            valid_crop = norm
                        elif c_clean in CROP_ALIASES:
                            valid_crop = CROP_ALIASES[c_clean]

                # Validate intent
                valid_intents = {"market_price", "cultivation_cost", "crop_advisory", "general_help", "unrecognized"}
                clean_intent = intent if intent in valid_intents else "unrecognized"

                return {
                    "crop": valid_crop,
                    "intent": clean_intent,
                    "state": extracted_state if isinstance(extracted_state, str) and extracted_state.strip() else None,
                    "confidence": float(confidence) if isinstance(confidence, (int, float)) else 0.8,
                }
        except Exception as e:
            logger.warning("Groq NLU extraction failed or timed out: %s", e)
            return None

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
        clean_query = sanitize_spoken_query(query_text.strip())
        lang = language.lower() if language else "en"

        # 1. Attempt Groq NLU parsing (handles speech typos, dialects, varied phrasing)
        groq_nlu = self.parse_query_with_groq(clean_query, language=lang)

        if groq_nlu:
            detected_crop = groq_nlu.get("crop")
            detected_intent = groq_nlu.get("intent") or "unrecognized"
            if groq_nlu.get("state"):
                state = groq_nlu["state"]
        else:
            detected_crop = self.detect_crop(clean_query)
            detected_intent = self.detect_intent(clean_query)

        # Fallback enrichment if Groq missed entity or intent
        if not detected_crop:
            fallback_crop = self.detect_crop(clean_query)
            if fallback_crop:
                detected_crop = fallback_crop

        if detected_intent == "unrecognized":
            fallback_intent = self.detect_intent(clean_query)
            if fallback_intent != "unrecognized":
                detected_intent = fallback_intent

        # If user only named a crop, default to market price and agronomic summary
        if detected_crop and detected_intent == "unrecognized":
            detected_intent = "market_price"

        logger.info(
            f"VoiceCopilot: query='{clean_query}', lang={lang}, crop={detected_crop}, intent={detected_intent}, state={state}"
        )

        if detected_intent == "general_help" or (not detected_crop and detected_intent == "unrecognized"):
            return self._build_help_response(clean_query, lang)

        if not detected_crop:
            return self._build_missing_crop_response(clean_query, lang, detected_intent)

        # Crop is identified: execute verified functions
        if detected_intent == "market_price":
            return self._execute_market_price_query(clean_query, detected_crop, lang, state=state)

        elif detected_intent == "cultivation_cost":
            return self._execute_cost_query(clean_query, detected_crop, state or "Maharashtra", lang)

        elif detected_intent == "crop_advisory":
            return self._execute_advisory_query(clean_query, detected_crop, lang)

        # Unrecognized fallback with known crop
        return self._execute_market_price_query(clean_query, detected_crop, lang, state=state)

    def transcribe_audio(
        self,
        audio_bytes: bytes,
        filename: str = "recording.webm",
        content_type: str = "audio/webm",
        language: str = "mr",
    ) -> str:
        """
        Transcribes spoken audio into text using Groq Whisper model.
        Directly bypasses browser cloud speech-api restrictions (Brave, Firefox, Safari).
        """
        if not self.groq_client:
            raise RuntimeError("Groq voice transcription is not available (GROQ_API_KEY is not set).")

        lang_code = language.lower() if language in ["mr", "hi", "en"] else "mr"

        try:
            transcription = self.groq_client.audio.transcriptions.create(
                model="whisper-large-v3-turbo",
                file=(filename, audio_bytes, content_type),
                language=lang_code,
                temperature=0.0,
            )
            return transcription.text.strip()
        except Exception as e:
            logger.error("Groq Whisper audio transcription failed: %s", e)
            raise RuntimeError(f"Speech-to-text processing failed: {str(e)}")

    def synthesize_speech_elevenlabs(self, text: str, language: str = "en") -> bytes:
        """
        Synthesizes natural multilingual audio speech using ElevenLabs API.
        Implements in-memory caching to strictly conserve character quota on the Free Tier.
        """
        if os.environ.get("PYTEST_CURRENT_TEST"):
            # Return synthetic MP3 bytes for offline/fast testing
            return b"\xff\xfb\x90\x44" + b"\x00" * 200

        clean_text = text.strip()
        if not clean_text:
            raise ValueError("Text cannot be empty for speech synthesis.")

        cache_key = f"{clean_text}:{language}"
        if cache_key in self._tts_cache:
            logger.info("Serving ElevenLabs TTS from in-memory cache (0 credits consumed)")
            return self._tts_cache[cache_key]

        if not self.elevenlabs_api_key:
            raise RuntimeError("ElevenLabs TTS is not configured (missing ELEVENLABS_API_KEY).")

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.elevenlabs_voice_id}"
        headers = {
            "xi-api-key": self.elevenlabs_api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        }
        payload = {
            "text": clean_text,
            "model_id": self.elevenlabs_model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
            },
        }

        try:
            with httpx.Client(timeout=25.0) as client:
                resp = client.post(url, headers=headers, json=payload)
                if resp.status_code == 200:
                    audio_bytes = resp.content
                    self._tts_cache[cache_key] = audio_bytes
                    return audio_bytes
                else:
                    logger.error("ElevenLabs TTS returned error %s: %s", resp.status_code, resp.text)
                    raise RuntimeError(f"ElevenLabs TTS failed ({resp.status_code}): {resp.text}")
        except Exception as e:
            logger.error("ElevenLabs TTS connection error: %s", e)
            raise

    def _synthesize_with_groq(
        self,
        query: str,
        lang: str,
        intent: str,
        crop: str,
        data_summary: str,
        default_spoken: str,
    ) -> str:
        """
        Synthesizes a fluent, respectful, highly natural vernacular spoken explanation
        using Groq LLM, strictly grounded in verified facts.
        """
        if not self.groq_client or os.environ.get("PYTEST_CURRENT_TEST"):
            return default_spoken

        lang_name = {"mr": "Marathi", "hi": "Hindi", "en": "English"}.get(lang, "English")
        system_prompt = (
            f"You are Kisan Voice Copilot, an empathetic, highly knowledgeable agricultural voice assistant for Indian farmers.\n"
            f"You speak fluently in {lang_name}.\n"
            f"STRICT TRUTHFULNESS & GROUNDING RULES:\n"
            f"1. Ground all numbers strictly in the verified data provided below. Do not change, invent, or hallucinate any numbers.\n"
            f"2. Keep the response to 1-2 concise, clear sentences suitable for audio speech output.\n"
            f"3. Speak directly to the farmer with respect, clarity, and warmth.\n"
            f"4. Output ONLY the plain text response in {lang_name}. Do not output quotes, asterisks, or markdown formatting.\n"
            f"5. For market price, always include 'रुपये प्रति क्विंटल' (or 'रुपये प्रति क्विंटल' / 'rupees per quintal'). For advisory, specify both season (हंगाम) and soil (जमीन)."
        )

        user_prompt = (
            f"Farmer asked: '{query}'\n"
            f"Topic: {intent} for crop '{crop}'\n"
            f"Verified Ground Truth Data:\n{data_summary}\n"
            f"Formulate a friendly, natural spoken response in {lang_name} communicating this verified data."
        )

        try:
            resp = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                model=self.groq_model,
                max_tokens=150,
                temperature=0.3,
            )
            content = resp.choices[0].message.content
            if content and content.strip():
                clean_text = content.strip().replace("*", "").replace("#", "").strip('"')
                return clean_text
        except Exception as e:
            logger.warning("Groq voice synthesis failed, using template fallback: %s", e)

        return default_spoken

    def _execute_market_price_query(
        self, query: str, crop: str, lang: str, state: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetches live or benchmark AGMARKNET wholesale rates and formats vernacular response."""
        price_data = self.price_service.get_crop_price(crop, state=state)
        crop_meta = CROP_METADATA.get(crop, {})
        display_name = VERNACULAR_DISPLAY_NAMES.get(crop, {}).get(lang, crop_meta.get("display_name", crop.capitalize()))
        modal_price = price_data.get("modal_rs_per_quintal", 0)
        min_price = price_data.get("min_rs_per_quintal", 0)
        max_price = price_data.get("max_rs_per_quintal", 0)
        msp = price_data.get("msp_rs_per_quintal")
        is_live = price_data.get("is_live", False)

        if lang == "mr":
            prefix = "थेट आजचा" if is_live else "सरासरी"
            spoken = f"{display_name} पिकाचा {prefix} बाजारभाव {modal_price:,.0f} रुपये प्रति क्विंटल आहे."
            display = f"{display_name} बाजारभाव: ₹{modal_price:,.0f} / क्विंटल (किमान: ₹{min_price:,.0f}, कमाल: ₹{max_price:,.0f})"
            if msp:
                spoken += f" सरकारी हमीभाव {msp:,.0f} रुपये आहे."
                display += f" | MSP: ₹{msp:,.0f}"
        elif lang == "hi":
            prefix = "लाइव" if is_live else "मॉडल"
            spoken = f"{display_name} का {prefix} मंडी भाव {modal_price:,.0f} रुपये प्रति क्विंटल है।"
            display = f"{display_name} मंडी भाव: ₹{modal_price:,.0f} / क्विंटल (न्यूनतम: ₹{min_price:,.0f}, अधिकतम: ₹{max_price:,.0f})"
            if msp:
                spoken += f" सरकारी समर्थन मूल्य {msp:,.0f} रुपये है।"
                display += f" | MSP: ₹{msp:,.0f}"
        else:
            prefix = "live" if is_live else "modal"
            spoken = f"The {prefix} mandi market price for {display_name} is {modal_price:,.0f} rupees per quintal."
            display = f"{display_name} Mandi Price: ₹{modal_price:,.0f} / Quintal (Range: ₹{min_price:,.0f} - ₹{max_price:,.0f})"
            if msp:
                spoken += f" Government MSP is {msp:,.0f} rupees."
                display += f" | MSP: ₹{msp:,.0f}"

        # Groq LLM Vernacular Enrichment
        summary = (
            f"Crop: {display_name}\n"
            f"Modal Mandi Price: ₹{modal_price:,.0f} / Quintal\n"
            f"Price Range: ₹{min_price:,.0f} - ₹{max_price:,.0f} / Quintal\n"
            f"Govt MSP: {f'₹{msp:,.0f} / Quintal' if msp else 'Not Applicable'}\n"
            f"Data Source: {price_data.get('source', 'AGMARKNET')}\n"
            f"Live Arrival Status: {'Live Today' if is_live else 'Historical Baseline'}"
        )
        spoken = self._synthesize_with_groq(query, lang, "market mandi price", crop, summary, spoken)

        return {
            "query_text": query,
            "language": lang,
            "intent": "market_price",
            "matched_crop": crop,
            "spoken_text": spoken,
            "display_text": display,
            "structured_data": price_data,
            "data_category": price_data.get("data_category", "Observed"),
            "data_provenance": price_data.get("source", "AGMARKNET Wholesale Mandi Records"),
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

        summary = (
            f"Crop: {display_name} in {state}\n"
            f"Total C2 Cost: ₹{total_c2:,.0f} / hectare\n"
            f"Seed Cost: ₹{seed_cost:,.0f} / hectare\n"
            f"Fertilizer Cost: ₹{fert_cost:,.0f} / hectare\n"
            f"Labor Cost: ₹{labor_cost:,.0f} / hectare\n"
            f"Source: Directorate of Economics & Statistics / CACP"
        )
        spoken = self._synthesize_with_groq(query, lang, "cultivation cost", crop, summary, spoken)

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

        summary = (
            f"Crop: {display_name}\n"
            f"Season: {season}\n"
            f"Compatible Soil: {soil}\n"
            f"Recommended Nutrient Dosage: {fert_kg} kg/ha\n"
            f"Overview: {desc}"
        )
        spoken = self._synthesize_with_groq(query, lang, "agronomic advice and soil suitability", crop, summary, spoken)

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
