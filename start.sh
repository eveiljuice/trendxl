#!/bin/bash

# TrendXL Railway Startup Script

echo "🚀 Starting TrendXL on Railway..."

# Set environment variables
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8000}
export DEBUG=${DEBUG:-false}

# Build frontend if not exists
if [ ! -d "frontend/build" ]; then
    echo "📦 Building frontend..."
    cd frontend
    npm install
    npm run build
    cd ..
fi

# Start backend
echo "🔥 Starting backend server on $HOST:$PORT..."
python backend/main.py
