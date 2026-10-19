"""
Root entry point wrapper for model training pipeline.
Delegates execution to scripts/train_models.py.
"""

import sys
from pathlib import Path

# Add project root and src to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "src"))
sys.path.insert(0, str(BASE_DIR))

from scripts.train_models import main

if __name__ == "__main__":
    main()
