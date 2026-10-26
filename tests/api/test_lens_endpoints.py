"""
API integration tests for Karpo Lens endpoints (/api/v1/lens).
"""

import io
import pytest
from httpx import AsyncClient
from PIL import Image


def create_test_image_bytes(format="JPEG", size=(200, 200)):
    img = Image.new("RGB", size, color=(80, 160, 40))
    buf = io.BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()


@pytest.mark.asyncio
async def test_lens_inspect_endpoint_success(async_client: AsyncClient):
    img_bytes = create_test_image_bytes()
    files = {"image": ("field_sample.jpg", img_bytes, "image/jpeg")}
    data = {"crop": "rice"}

    response = await async_client.post("/api/v1/lens/inspect", files=files, data=data)
    assert response.status_code == 200
    res = response.json()
    assert res["filename"] == "field_sample.jpg"
    assert res["format"] == "JPEG"
    assert res["width"] == 200
    assert res["height"] == 200
    assert res["status"] in {"model_unavailable", "quota_exceeded", "verified"}
    assert len(res["icar_symptom_guide"]) > 0


@pytest.mark.asyncio
async def test_lens_inspect_endpoint_mock_verified(async_client: AsyncClient, monkeypatch):
    """Verifies that when Z.ai returns a valid diagnosis, status is 'verified' with confidence score."""
    from crop_advisory.services.lens_service import KarpoLensService

    def mock_zai_call(self, image_bytes, img_format, crop_name=None):
        return {
            "status": "verified",
            "diagnosis": "Rice Blast (Pyricularia oryzae)",
            "confidence": 0.94,
            "visual_symptoms": "Spindle-shaped lesions observed across leaf blade.",
            "treatment_recommendation": "Avoid excessive nitrogen; apply recommended bio-fungicide.",
            "urgency": "High",
            "message": "Z.ai Vision (glm-5.3-flash) diagnosis complete: Rice Blast.",
        }

    monkeypatch.setattr(KarpoLensService, "_call_zai_vision", mock_zai_call)

    img_bytes = create_test_image_bytes()
    files = {"image": ("rice_leaf.jpg", img_bytes, "image/jpeg")}
    data = {"crop": "rice"}

    response = await async_client.post("/api/v1/lens/inspect", files=files, data=data)
    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "verified"
    assert res["diagnosis"] == "Rice Blast (Pyricularia oryzae)"
    assert res["confidence"] == 0.94
    assert res["data_category"] == "Predicted"
    assert "Z.ai Multimodal Vision" in res["data_provenance"]


@pytest.mark.asyncio
async def test_lens_inspect_corrupt_file_returns_400(async_client: AsyncClient):
    files = {"image": ("corrupted.jpg", b"NOT_A_VALID_JPEG_HEADER", "image/jpeg")}
    response = await async_client.post("/api/v1/lens/inspect", files=files)
    assert response.status_code == 400
    assert "not a valid or decipherable image" in response.json()["message"]
