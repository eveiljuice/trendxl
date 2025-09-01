# TrendXL - AI Trend Feed MVP

## 🎯 Project Overview
Разработай MVP веб-приложения TrendXL — AI Trend Feed с многофайловой структурой на React 18+ (TypeScript), Tailwind CSS (dark minimal UI), используя Ensemble Data API (только TikTok), OpenAI GPT API для фильтрации, и SQLite в качестве хранилища.

## 🏗️ Architecture Requirements

### Frontend (React 18+ + TypeScript + Tailwind)
- **Modern Stack**: React 18+, TypeScript, Tailwind CSS
- **UI Theme**: Dark minimal design
- **State Management**: React hooks + Context
- **Routing**: React Router (if needed)
- **API Client**: Axios for backend communication

### Backend (FastAPI + Python)
- **Framework**: FastAPI for high performance
- **Database**: SQLite with SQLAlchemy
- **APIs**: Ensemble Data (TikTok), OpenAI GPT
- **Security**: Environment variables for API keys
- **Documentation**: Auto-generated API docs

### Key Features
- ✅ **Real-time TikTok Trends**: Live data from Ensemble API
- ✅ **AI Analysis**: GPT-powered trend filtering and insights
- ✅ **Modern UI**: Dark theme with smooth animations
- ✅ **Responsive**: Mobile-first design
- ✅ **Performance**: Optimized for speed
- ✅ **Security**: API keys protected in environment

## 📋 Functional Requirements

### Core Functionality
1. **Trend Discovery**
   - Fetch trending hashtags from TikTok
   - Real-time data updates
   - Category-based filtering

2. **AI-Powered Analysis**
   - GPT analysis of trend content
   - Sentiment analysis
   - Trend prediction insights

3. **User Interface**
   - Clean, modern dashboard
   - Interactive trend visualization
   - Search and filter capabilities

4. **Data Storage**
   - SQLite database for local storage
   - Efficient data caching
   - Automatic cleanup

## 🔧 Technical Specifications

### Frontend Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── TrendCard.tsx
│   │   ├── TrendAnalytics.tsx
│   │   ├── SearchBar.tsx
│   │   └── Dashboard.tsx
│   ├── hooks/
│   │   ├── useTrends.ts
│   │   └── useAnalytics.ts
│   ├── services/
│   │   └── api.ts
│   ├── types/
│   │   └── index.ts
│   ├── utils/
│   │   └── helpers.ts
│   └── styles/
│       └── globals.css
```

### Backend Structure
```
backend/
├── main.py              # FastAPI app
├── routers/
│   ├── trends.py       # Trend endpoints
│   └── analytics.py    # Analytics endpoints
├── services/
│   ├── ensemble_service.py
│   ├── gpt_service.py
│   └── database_service.py
├── models/
│   └── schemas.py      # Pydantic models
└── prompts/
    └── gpt_prompts.py  # AI prompts
```

## 🚀 API Integration

### Ensemble Data API
```typescript
// Example usage
import { EDClient } from "ensembledata";
const client = new EDClient({ token: "your_ensemble_api_key_here" });
const result = await client.tiktok.hashtagSearch({ hashtag: "magic" });
console.log(result.data)
```

### OpenAI GPT Integration
- Реализуй логику фильтрации и категоризации через GPT (используй ключ: your_openai_api_key_here — безопасно храни на backend в .env файле).
- Запись и чтение ленты только через SQLite (локальная база данных).

## 📤 Вывод
Tailwind + dark minimal UI. Использовать React 18+, OpenAI SDK, Ensemble Data Python SDK (https://ensembledata.com/apis/docs#tag/Tiktok), JS / Python.

Open AI API Key: your_openai_api_key_here (add to .env file)
Ensemble Data Key: your_ensemble_api_key_here
SQLite Database: Local file-based storage

Требования:
- Строго используйте JS или Python на backend (по выбору), React 18+ и Tailwind для frontend.
- Для OpenAI, SQLite, Ensemble Data — заведи модули/обёртки в api.ts и общий сервисный слой обработки данных.
- Реализуй реал-тайм обновления трендов каждые 5 минут.
- Добавь кеширование данных для производительности.
- Сделай responsive дизайн для мобильных устройств.

## 🎨 UI/UX Requirements

### Design System
- **Colors**: Dark theme (#0f0f0f, #1a1a1a, #2a2a2a)
- **Typography**: Modern sans-serif fonts
- **Spacing**: Consistent 8px grid system
- **Components**: Reusable UI components
- **Animations**: Smooth transitions and micro-interactions

### Key Screens
1. **Dashboard**: Trend overview with charts
2. **Trend Details**: Detailed analysis view
3. **Search**: Advanced filtering options
4. **Settings**: Configuration panel

## 🔒 Security & Best Practices

### API Key Management
- Environment variables (.env file)
- Never commit secrets to version control
- Secure key rotation process

### Data Protection
- Input validation on all endpoints
- SQL injection prevention
- XSS protection on frontend

### Performance
- API rate limiting
- Database query optimization
- Frontend bundle optimization
- Caching strategies

## 📊 Success Metrics

### Technical Metrics
- API response time < 500ms
- Frontend bundle size < 200KB
- Database query time < 100ms
- 99.9% uptime

### User Experience
- Page load time < 2 seconds
- Mobile responsiveness
- Intuitive navigation
- Real-time updates

## 🚀 Deployment & DevOps

### Development
```bash
# Backend
pip install -r requirements.txt
python backend/main.py

# Frontend
cd frontend
npm install
npm start
```

### Production
- Docker containerization
- Environment-based configuration
- Automated testing
- CI/CD pipeline

## 📚 Documentation

### Code Documentation
- Inline comments for complex logic
- API endpoint documentation
- Component prop documentation
- TypeScript interfaces

### User Documentation
- Setup instructions
- API usage examples
- Troubleshooting guide
- Feature documentation

---

## 🎯 Final Deliverables

1. **Working MVP Application**
   - Fully functional TrendXL platform
   - Real TikTok data integration
   - AI-powered analysis
   - Modern responsive UI

2. **Complete Documentation**
   - Setup and deployment guides
   - API documentation
   - Code documentation
   - User manual

3. **Production Ready**
   - Docker configuration
   - Environment setup
   - Security best practices
   - Performance optimization

4. **Source Code**
   - Well-structured codebase
   - TypeScript/React frontend
   - FastAPI/Python backend
   - SQLite database integration
   - Git repository with clean history
