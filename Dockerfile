# TrendXL Dockerfile
# Multi-stage build for Python backend and Node.js frontend

# ===========================================
# Base stage with system dependencies
# ===========================================
FROM python:3.12-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /home/app

WORKDIR /home/app

# ===========================================
# Python dependencies stage
# ===========================================
FROM base as python-deps

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ===========================================
# Node.js dependencies stage
# ===========================================
FROM base as node-deps

WORKDIR /home/app/frontend

COPY frontend/package*.json ./
RUN npm ci --only=production && npm cache clean --force

# ===========================================
# Frontend build stage
# ===========================================
FROM node-deps as frontend-build

COPY frontend/ ./
RUN npm run build

# ===========================================
# Final production stage
# ===========================================
FROM base as production

# Copy Python packages
COPY --from=python-deps /root/.local /home/app/.local
ENV PATH=/home/app/.local/bin:$PATH

# Copy Node.js packages
COPY --from=node-deps /home/app/frontend/node_modules ./frontend/node_modules

# Copy built frontend
COPY --from=frontend-build /home/app/frontend/build ./frontend/build

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Change ownership to app user
RUN chown -R app:app /home/app

# Switch to non-root user
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose ports
EXPOSE 8000 3000

# Default command
CMD ["python", "run.py", "dev"]
