"""
Unit tests for VoiceCopilotService.
Verifies multilingual intent detection, vernacular crop name extraction,
and verified API responses in Marathi, Hindi, and English with zero fabricated fallbacks.
"""

import pytest
from crop_advisory.services.cultivation_cost_service import CultivationCostService
from crop_advisory.services.market_service import MarketPriceService
from crop_advisory.services.voice_copilot_service import VoiceCopilotService


@pytest.fixture
def voice_copilot():
    price_svc = MarketPriceService()
    cost_svc = CultivationCostService()
    return VoiceCopilotService(market_price_service=price_svc, cost_service=cost_svc)


def test_marathi_soybean_price_query(voice_copilot):
    result = voice_copilot.process_query("सोयाबीनचा भाव काय आहे?", language="mr")
    assert result["matched_crop"] == "soybean"
    assert result["intent"] == "market_price"
    assert result["language"] == "mr"
    assert "सोयाबीन" in result["spoken_text"]
    assert "रुपये प्रति क्विंटल" in result["spoken_text"]
    assert result["data_category"] == "Observed"
    assert "AGMARKNET" in result["data_provenance"]
    assert result["structured_data"]["modal_rs_per_quintal"] > 0


def test_hindi_cotton_price_query(voice_copilot):
    result = voice_copilot.process_query("कपास का मंडी भाव क्या है?", language="hi")
    assert result["matched_crop"] == "cotton"
    assert result["intent"] == "market_price"
    assert result["language"] == "hi"
    assert "कपास" in result["spoken_text"] or "Cotton" in result["spoken_text"]
    assert "मंडी भाव" in result["spoken_text"] or "रुपये" in result["spoken_text"]
    assert result["data_category"] == "Observed"


def test_english_wheat_cost_query(voice_copilot):
    result = voice_copilot.process_query(
        "What is the cultivation cost for wheat?",
        language="en",
        state="Punjab",
    )
    assert result["matched_crop"] == "wheat"
    assert result["intent"] == "cultivation_cost"
    assert result["language"] == "en"
    assert "cultivation cost" in result["spoken_text"].lower()
    assert result["data_category"] == "Historical"
    assert result["structured_data"]["cul_cost_c2_per_ha"] > 0


def test_marathi_rice_agronomic_advisory(voice_copilot):
    result = voice_copilot.process_query("भात पिकासाठी माती आणि खताचा सल्ला द्या", language="mr")
    assert result["matched_crop"] == "rice"
    assert result["intent"] == "crop_advisory"
    assert "जमीन" in result["spoken_text"] or "हंगाम" in result["spoken_text"]
    assert result["data_category"] == "Estimated"


def test_greeting_help_query(voice_copilot):
    result = voice_copilot.process_query("नमस्कार", language="mr")
    assert result["intent"] == "general_help"
    assert result["matched_crop"] is None
    assert "कार्पो किसान सहाय्यक" in result["spoken_text"]


def test_missing_crop_query_does_not_fabricate(voice_copilot):
    result = voice_copilot.process_query("आजचा भाव काय आहे?", language="mr")
    assert result["matched_crop"] is None
    assert result["data_category"] == "Unavailable"
    assert "पिकाचे नाव समजले नाही" in result["spoken_text"]
