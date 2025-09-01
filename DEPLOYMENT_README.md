# TrendXL Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- Docker (optional)

### 1. Clone Repository
```bash
git clone https://github.com/eveiljuice/trendxl.git
cd trendxl
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### 3. API Keys Required

1. **Ensemble Data API**: For TikTok data
   - Get from: https://ensembledata.com/
   - Key: `your_ensemble_api_key_here` (add to .env file)

2. **OpenAI API**: For AI-powered trend analysis
   - Get from: https://platform.openai.com/
   - Key: `your_openai_api_key_here` (add to .env file)

3. **SeaTable API**: Not required (SQLite-only mode)

## 🛠 Installation & Setup

### Option A: Docker (Recommended)
```bash
# Build and run
docker-compose up --build

# Access application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
```

### Option B: Manual Setup

#### Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Run backend
cd backend
python main.py
```

#### Frontend
```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm start
```

## 🔧 Configuration

Edit `.env` file:

```bash
# API Keys
ENSEMBLE_DATA_API_KEY=your_ensemble_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
SEATABLE_API_TOKEN=your_seatable_token_here

# Database Configuration
USE_SQLITE=true  # Set to false for SeaTable in production
SQLITE_DB_PATH=trendxl.db

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

## 🚀 Production Deployment

### Using Docker
```bash
# Production compose
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose up -d --scale trendxl=3
```

### Manual Production
```bash
# Set production environment
export DEBUG=false

# Build frontend
cd frontend && npm run build

# Run with production server
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Netlify (Frontend-only)

If you deploy only the React frontend to Netlify and run the FastAPI backend elsewhere (e.g., Render, Fly.io, VPS), configure Netlify as follows:

1) Add `netlify.toml` to repo root:

```toml
[build]
  base = "frontend"
  command = "npm run build"
  publish = "build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

2) Configure API base URL:

- Option A (Netlify redirects): add a production proxy to your backend URL:

```toml
# netlify.toml
[[redirects]]
  from = "/api/*"
  to = "https://YOUR_BACKEND_URL/:splat"
  status = 200
  force = true
```

- Option B (environment variable): set `REACT_APP_API_BASE` in Netlify UI and use it in the app to override `/api/v1`.

3) Backend CORS must allow your Netlify domain. In `backend/main.py`, extend `allow_origins` to include your Netlify site URL.

Common Netlify issues:
- Wrong publish dir: should be `build` when `base = "frontend"`.
- Missing SPA redirect: add the catch-all redirect to `/index.html`.
- Proxying to localhost in production: replace with real backend URL or omit.

## 🔍 Monitoring & Health Checks

### Health Endpoints
- `GET /api/health` - Overall system health
- `GET /api/v1/analytics/health` - Analytics health

### Logs
```bash
# Docker logs
docker-compose logs -f trendxl

# Application logs
tail -f logs/trendxl.log
```

## 📊 Database Management

### SQLite (Development)
```bash
# Database file: trendxl.db
# Automatic migration on startup
```

### SeaTable (Production)
```bash
# Set in .env
USE_SQLITE=false
SEATABLE_BASE_TOKEN=your_base_token
SEATABLE_TABLE_NAME=trends
```

## 🔧 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Check `.env` file exists
   - Verify API keys are valid
   - Check network connectivity

2. **Database Errors**
   - SQLite: Check file permissions
   - SeaTable: Verify token and table access

3. **Port Conflicts**
   - Change ports in docker-compose.yml
   - Update .env PORT variable

### Debug Mode
```bash
# Enable debug logging
export DEBUG=true
export VERBOSE_LOGGING=true
```

## 📈 Performance Tuning

### Memory Optimization
```bash
# Adjust Gunicorn workers
docker-compose.yml > command: ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
```

### Caching
```bash
# Enable Redis (optional)
# Uncomment redis service in docker-compose.yml
```

## 🔐 Security

### API Keys
- Never commit `.env` to version control
- Use environment-specific keys
- Rotate keys regularly

### HTTPS
```bash
# Add to docker-compose.prod.yml
environment:
  - HTTPS=true
```

## 📞 Support

- Issues: [GitHub Issues](https://github.com/eveiljuice/trendxl/issues)
- Documentation: [README.md](README.md)
- Wiki: [Project Wiki](https://github.com/eveiljuice/trendxl/wiki)
