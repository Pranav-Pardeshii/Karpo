"""
Unit tests for KarpoLensService.
Verifies image decoding, size/dimension validation, and honest offline model reporting.
"""

import io
import pytest
from PIL import Image
from crop_advisory.services.lens_service import KarpoLensService


@pytest.fixture
def lens_service():
    return KarpoLensService()


def create_test_image(format="JPEG", size=(200, 200), color=(100, 180, 50)):
    """Helper creating memory byte stream of a synthetic valid image for testing."""
    img = Image.new("RGB", size, color=color)
    buf = io.BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()


def test_valid_jpeg_inspection(lens_service):
    img_bytes = create_test_image(format="JPEG", size=(300, 400))
    result = lens_service.validate_and_inspect_image(img_bytes, filename="leaf_test.jpg", crop_name="rice")

    assert result["filename"] == "leaf_test.jpg"
    assert result["format"] == "JPEG"
    assert result["width"] == 300
    assert result["height"] == 400
    assert result["size_bytes"] > 0
    # Mandatory Operating Principle: Honest status, never fabricating fake predictions
    assert result["status"] in {"model_unavailable", "quota_exceeded", "verified"}
    if result["status"] != "verified":
        assert result["diagnosis"] is None
        assert result["confidence"] is None
    assert len(result["icar_symptom_guide"]) > 0
    assert "Rice Blast" in result["icar_symptom_guide"][0]["disease_name"]


def test_empty_image_raises_error(lens_service):
    with pytest.raises(ValueError, match="Uploaded image is empty"):
        lens_service.validate_and_inspect_image(b"")


def test_corrupted_bytes_raises_error(lens_service):
    with pytest.raises(ValueError, match="not a valid or decipherable image"):
        lens_service.validate_and_inspect_image(b"THIS_IS_NOT_AN_IMAGE_FILE_DATA")


def test_tiny_resolution_raises_error(lens_service):
    tiny_bytes = create_test_image(size=(20, 20))
    with pytest.raises(ValueError, match="Image resolution .* is too low"):
        lens_service.validate_and_inspect_image(tiny_bytes)


def test_cotton_icar_guidelines(lens_service):
    img_bytes = create_test_image(format="PNG", size=(150, 150))
    result = lens_service.validate_and_inspect_image(img_bytes, crop_name="cotton")
    assert result["crop_evaluated"] == "cotton"
    assert any("Cotton Leaf Curl" in g["disease_name"] for g in result["icar_symptom_guide"])
