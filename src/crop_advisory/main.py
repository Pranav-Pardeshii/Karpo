"""
ASGI Entry Point alias.
Provides direct access to crop_advisory.api.main.app.
"""

from crop_advisory.api.main import app, create_app

__all__ = ["app", "create_app"]
