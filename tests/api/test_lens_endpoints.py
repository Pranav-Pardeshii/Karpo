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
    assert res["status"] == "model_unavailable"
    assert res["diagnosis"] is None
    assert res["confidence"] is None
    assert res["data_category"] == "Unavailable"
    assert len(res["icar_symptom_guide"]) > 0


@pytest.mark.asyncio
async def test_lens_inspect_corrupt_file_returns_400(async_client: AsyncClient):
    files = {"image": ("corrupted.jpg", b"NOT_A_VALID_JPEG_HEADER", "image/jpeg")}
    response = await async_client.post("/api/v1/lens/inspect", files=files)
    assert response.status_code == 400
    assert "not a valid or decipherable image" in response.json()["message"]
