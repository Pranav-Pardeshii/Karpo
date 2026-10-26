# ==============================================================================
# Production Dockerfile for Smart Crop Advisory ML API
# ==============================================================================
FROM python:3.12-slim AS builder

# Install uv from official binary image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Configure Python and uv environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies first for maximum Docker layer caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy application source code, models, and datasets
COPY src/ src/
COPY models/ models/
COPY datasets/ datasets/
COPY README.md ./

# Install project package
RUN uv sync --frozen --no-dev

# ==============================================================================
# Runtime Stage
# ==============================================================================
FROM python:3.12-slim AS runner

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    CROP_ADVISORY_HOST=0.0.0.0 \
    CROP_ADVISORY_PORT=8000 \
    CROP_ADVISORY_LOG_LEVEL=INFO

WORKDIR /app

# Create a non-root system user for security
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/sh -m appuser

# Copy installed virtual environment and application from builder
COPY --from=builder --chown=appuser:appgroup /app /app

USER appuser

EXPOSE 8000

# Container healthcheck testing the liveness probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import os, urllib.request; port = os.environ.get('PORT', '8000'); urllib.request.urlopen(f'http://127.0.0.1:{port}/api/v1/health/live', timeout=2)" || exit 1

# Start the asynchronous ASGI application supporting dynamic Render $PORT
CMD ["sh", "-c", "uvicorn crop_advisory.api.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]

