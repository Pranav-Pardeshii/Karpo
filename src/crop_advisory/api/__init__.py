"""
API package for Smart Crop Advisory System.
Provides a versioned, asynchronous FastAPI REST backend.
"""

from crop_advisory.api.main import app, create_app

__all__ = ["create_app", "app"]
