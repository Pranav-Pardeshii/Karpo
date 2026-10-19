# Migration Guide: Repository Modernization & uv Packaging

## 1. Overview & Objectives

This document details the structural modernization of the **Smart Crop Advisory ML** repository. The objective of this phase was to refactor the legacy repository into a clean, modular, production-oriented Python architecture using `uv` for dependency and environment management, while preserving 100% of the existing machine learning behavior, trained artifacts, datasets, and presentation interfaces.

> **Scope Note**: This phase represents the foundational architectural modernization. It does not introduce FastAPI, database ORMs, or asynchronous message queues, keeping the core ML domain decoupled and clean.

---

## 2. Audit of Legacy State

Prior to refactoring, a comprehensive repository audit identified the following structural limitations:

| Area | Legacy State | Bottleneck / Risk |
| :--- | :--- | :--- |
| **Dependency Management** | Flat `requirements.txt` with loose `>=` bounds, no lockfile | Non-reproducible builds, lack of dev/test dependency segregation |
| **Directory Structure** | Flat modules inside `src/`, root-level `app.py` (613 lines) and `train_models.py` | UI, business logic, ML training, and inference tightly coupled |
| **Path Resolution** | Fragile relative paths using `os.path.join(os.path.dirname(__file__), "..")` | Execution failed if invoked from directories other than root |
| **Data Contracts** | Ad-hoc Python dictionaries without schema validation | Silent feature order errors or out-of-range numerical anomalies |
| **Model Artifacts** | Artifact loading logic duplicated across multiple modules | Lack of caching, risk of repeated disk I/O on inference |
| **Testing** | Single 206-line test script (`tests/test_pipeline.py`) without fixtures | Monolithic test execution; no dedicated unit test suites |

---

## 3. Structural Refactoring Map

The codebase was restructured into a modular package under `src/crop_advisory/`:

| Legacy Location | Modern Target Location | Description |
| :--- | :--- | :--- |
| `requirements.txt` | `pyproject.toml`, `uv.lock` | PEP 621 packaging with `uv` lockfile and dependency groups |
| *(None)* | `.python-version` | Pinned to Python 3.12 |
| *(None)* | `.env.example` | Environment variable template for paths and ports |
| *(None)* | `Makefile` | Standard developer targets (`install`, `test`, `run`, `lint`) |
| `src/crop_mapping.py` | `src/crop_advisory/domain/crop_mapping.py` | Canonical crop metadata and cross-dataset normalization |
| `src/profit_calculation.py` | `src/crop_advisory/domain/calculations.py` | Unit conversions, INR formatting, and farm economics math |
| *(None)* | `src/crop_advisory/domain/schemas.py` | Typed dataclasses for input validation and output payloads |
| *(None)* | `src/crop_advisory/config.py` | Centralized `pathlib.Path` resolution and feature bounds |
| *(None)* | `src/crop_advisory/exceptions.py` | Domain-specific exception hierarchy |
| `src/preprocessing.py` | `src/crop_advisory/ml/preprocessing.py` | Dataset cleaning, train-test splitting, ColumnTransformers |
| `src/crop_recommendation.py` | `src/crop_advisory/ml/crop_recommender.py` | Recommendation inference and classifier training |
| `src/yield_prediction.py` | `src/crop_advisory/ml/yield_predictor.py` | Yield inference, horticultural fallback, and regressor training |
| *(None)* | `src/crop_advisory/ml/model_loader.py` | Thread-safe, cached artifact loader |
| *(None)* | `src/crop_advisory/ml/feature_validation.py` | Strict feature ordering and biological bounds checks |
| `src/price_lookup.py` | `src/crop_advisory/services/market_service.py` | Agmarknet Mandi price lookup service with caching |
| `src/cost_lookup.py` | `src/crop_advisory/services/cultivation_cost_service.py` | CACP cultivation cost query service |
| *(None)* | `src/crop_advisory/services/financial_analysis_service.py` | End-to-end advisory orchestrator decoupled from UI |
| `app.py` | `src/crop_advisory/presentation/streamlit_app.py` | Modernized Streamlit application |
| `app.py` (Root) | `app.py` | Backward-compatible entrypoint shim delegating to package |
| `train_models.py` | `scripts/train_models.py` | Modernized CLI training script |
| `train_models.py` (Root)| `train_models.py` | Backward-compatible wrapper delegating to scripts |
| `tests/test_pipeline.py`| `tests/test_pipeline.py` | Preserved 15 regression tests |
| *(None)* | `tests/conftest.py` | Shared pytest fixtures |
| *(None)* | `tests/unit/*.py` | Modular unit tests (calculations, schemas, mappings, services) |
| *(None)* | `tests/integration/*.py` | Integration tests (ML inference, financial flows, legacy shims) |

---

## 4. Backward Compatibility Guarantee

To prevent breaking existing notebooks (`notebooks/01_crop_recommendation.ipynb`, `notebooks/02_yield_prediction.ipynb`), existing test suites, or external tools, a shim layer was established in `src/`:

```python
# Example: src/crop_recommendation.py
from crop_advisory.ml.crop_recommender import CropRecommender, train_and_evaluate_crop_models
from crop_advisory.config import MODELS_DIR, CROP_REC_MODEL_FILENAME

MODEL_PATH = str(MODELS_DIR / CROP_REC_MODEL_FILENAME)
__all__ = ["CropRecommender", "train_and_evaluate_crop_models", "MODEL_PATH"]
```

Legacy import statements such as:
```python
from src.crop_recommendation import CropRecommender
from src.yield_prediction import YieldPredictor
from src.price_lookup import get_crop_price
```
continue to function identically and pass all test suites.

---

## 5. Dependency Migration to uv

The project now utilizes `pyproject.toml` with `uv`:
- **Python Compatibility**: `>=3.10` (tested on 3.12.10).
- **Core Dependencies**:
  - `pandas>=2.0.0`
  - `numpy>=1.24.0`
  - `scikit-learn>=1.3.0`
  - `xgboost>=2.0.0`
  - `joblib>=1.3.0`
  - `streamlit>=1.30.0`
  - `matplotlib>=3.7.0`
  - `seaborn>=0.12.0`
- **Development & Testing Dependencies** (`[dependency-groups]`):
  - `pytest>=7.4.0`
  - `ruff>=0.4.0`

### Commands
- Environment Sync: `uv sync --all-groups`
- Running Tests: `uv run pytest`
- Launching App: `uv run streamlit run src/crop_advisory/presentation/streamlit_app.py`
- Training Models: `uv run python scripts/train_models.py`
- Code Quality: `uv run ruff check .`

---

## 6. Verification Summary

| Check | Command Executed | Result | Notes |
| :--- | :--- | :--- | :--- |
| **Lockfile Generation** | `uv lock` | ✅ Success (2.63s) | Resolved 79 packages |
| **Environment Sync** | `uv sync --all-groups` | ✅ Success | Virtual environment created at `.venv` |
| **Full Test Suite** | `uv run pytest` | ✅ 42/42 Passed (1.13s) | 15 legacy + 27 new unit/integration tests |
| **Lint & Style** | `uv run ruff check .` | ✅ All checks passed | Clean compliance across all modules |
| **Streamlit Entrypoint** | `uv run streamlit run src/...` | ✅ HTTP 200 OK | Rendered on port 8501 |
| **Root Wrapper App** | `uv run streamlit run app.py` | ✅ HTTP 200 OK | Rendered on port 8503 |
| **Model Artifacts Loading**| `ModelLoader.load_*()` | ✅ Verified | Deserialized without retraining |
| **Dataset Loading** | `load_cost_dataset()`, etc. | ✅ Verified | All 4 CSVs load cleanly |

---

## 7. Resolved Technical Debt & Next Steps

### Resolved in this Phase:
- Eliminated fragile working-directory assumptions with deterministic path resolution.
- Separated presentation UI from model inference and domain economics.
- Replaced unpinned `requirements.txt` with standard `pyproject.toml` and locked dependencies.
- Added agronomic feature ordering and biological bounds checks.
- Established a complete, tiered test architecture (unit, integration, regression).
- Fixed a subtle string search bug where `"bigha"` triggered `"ha"` in area unit conversion.

### Reserved for Backend Implementation Phase:
- FastAPI REST service layer wrapping `FinancialAnalysisService`.
- OpenAPI / Swagger documentation for external system integrations.
- Asynchronous Celery/Redis tasks for large batch inference.
