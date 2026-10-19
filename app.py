"""
Root entry point for Smart Crop Advisory Streamlit Application.
Delegates to crop_advisory.presentation.streamlit_app.
"""

import sys
from pathlib import Path

# Ensure 'src' is on Python path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from crop_advisory.presentation.streamlit_app import main

if __name__ == "__main__":
    main()
