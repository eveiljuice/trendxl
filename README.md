# TrendXL - AI-Powered TikTok Trend Analysis Platform

TrendXL is an advanced AI-powered platform for analyzing TikTok trends using the EnsembleData API and GPT intelligence. It provides comprehensive trend insights, user analytics, and real-time data processing with a modern React frontend and robust FastAPI backend.

## ✨ Features

- 🚀 **Real-time TikTok Data Analysis** - Live trend monitoring and analysis
- 🧠 **AI-Powered Insights** - GPT-enhanced content analysis and trend prediction
- 📊 **Advanced Analytics** - Comprehensive metrics and correlation analysis
- 🎯 **Niche Detection** - Smart categorization and trend segmentation
- 🔄 **Real-time Updates** - Live data streaming and notifications
- 🌐 **Modern UI/UX** - Responsive React interface with Tailwind CSS
- 🐳 **Docker Ready** - Containerized deployment for easy scaling
- 💾 **SQLite Database** - Efficient local data storage

## 🏗️ Tech Stack

### Backend

- **FastAPI** - High-performance Python web framework
- **SQLite** - Lightweight database for development
- **EnsembleData API** - TikTok data provider
- **OpenAI GPT** - AI analysis engine
- **Uvicorn** - ASGI server

### Frontend

- **React 18** - Modern UI library
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first styling
- **Lucide Icons** - Beautiful icon system
- **Axios** - API client

### DevOps

- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (recommended 3.12)
- Node.js 18+
- Docker (optional)

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/trendxl.git
cd trendxl

# Create environment file
cp .env.example .env
# Edit .env with your API keys
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run backend development server
cd backend
python main.py
```

### 3. Frontend Setup

```bash
# Install Node dependencies
cd frontend
npm install

# Start React development server
npm start
```

### 4. Docker Deployment (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 🔧 Configuration

Create a `.env` file in the root directory:

```env
# API Keys
ENSEMBLE_API_KEY=your_ensemble_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Database
DATABASE_TYPE=sqlite
SQLITE_DB_PATH=trendxl.db

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false

# AI Configuration
GPT_MODEL=gpt-3.5-turbo
MAX_TOKENS=1000
```

## 📚 API Documentation

Once running, visit:

- **Interactive API Docs**: http://localhost:8000/docs
- **OpenAPI Spec**: http://localhost:8000/openapi.json

### Key Endpoints

- `GET /api/v1/trends` - Get trending content
- `POST /api/v1/analysis/profile` - Analyze user profiles
- `GET /api/v1/analytics/metrics` - Get analytics data
- `GET /api/health` - Health check

## 🏃‍♂️ Development

### Project Structure

```
trendxl/
├── backend/                 # FastAPI backend
│   ├── main.py             # Application entry point
│   ├── routers/            # API endpoints
│   ├── services/           # Business logic
│   ├── models/            # Data models
│   └── prompts/           # AI prompts
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── lib/          # Utilities
│   │   └── types/        # TypeScript types
│   └── public/           # Static assets
├── docker-compose.yml     # Docker configuration
├── Dockerfile            # Container setup
└── requirements.txt      # Python dependencies
```

### Running Tests

```bash
# Backend tests
python -m pytest

# Frontend tests
cd frontend && npm test
```

## 🚀 Deployment

### Docker Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Deployment

1. Set `DEBUG=false` in `.env`
2. Build frontend: `cd frontend && npm run build`
3. Run backend: `python run.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [EnsembleData](https://ensembledata.com) for TikTok API access
- [OpenAI](https://openai.com) for GPT API
- [FastAPI](https://fastapi.tiangolo.com) for the amazing framework
- [React](https://reactjs.org) for the frontend framework
