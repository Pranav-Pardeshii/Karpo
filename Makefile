.PHONY: help install sync test test-unit test-integration test-api run run-api train lint format typecheck frontend-install frontend-dev frontend-build clean

help:
	@echo "Available commands:"
	@echo "  make install         - Install Python dependencies and create virtual environment using uv"
	@echo "  make sync            - Sync locked dependencies using uv sync"
	@echo "  make test            - Run all tests using pytest"
	@echo "  make test-unit       - Run unit tests only"
	@echo "  make test-int        - Run integration tests only"
	@echo "  make test-api        - Run API tests only"
	@echo "  make run             - Launch Streamlit application"
	@echo "  make run-api         - Launch FastAPI Uvicorn application"
	@echo "  make frontend-install- Install frontend npm packages"
	@echo "  make frontend-dev    - Launch KARPO React frontend in dev mode"
	@echo "  make frontend-build  - Build KARPO production bundle"
	@echo "  make train           - Retrain and evaluate ML models"
	@echo "  make lint            - Run ruff linter"
	@echo "  make format          - Format code with ruff"
	@echo "  make typecheck       - Run mypy static type checking"
	@echo "  make clean           - Remove cache and temporary files"

install:
	uv sync --all-groups

sync:
	uv sync

test:
	uv run pytest

test-unit:
	uv run pytest tests/unit

test-int:
	uv run pytest tests/integration

test-api:
	uv run pytest tests/api

run:
	uv run streamlit run src/crop_advisory/presentation/streamlit_app.py

run-api:
	uv run uvicorn crop_advisory.api.main:app --reload --host 127.0.0.1 --port 8000

frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

frontend-build:
	cd frontend && npm run build

train:
	uv run python scripts/train_models.py

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy src/crop_advisory/api

clean:
	python -c "import shutil, glob, os; [shutil.rmtree(p, ignore_errors=True) for p in glob.glob('**/__pycache__', recursive=True) + glob.glob('**/.pytest_cache', recursive=True) + glob.glob('**/.ruff_cache', recursive=True)]"
