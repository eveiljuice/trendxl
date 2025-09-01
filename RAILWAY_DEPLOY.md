# 🚀 TrendXL Railway Deploy Guide

## Быстрый деплой за 5 минут

### 1. Подготовка

✅ Проект готов к деплою!  
✅ Все конфигурации настроены  
✅ Frontend и Backend объединены

### 2. Создай проект на Railway

1. Иди на [railway.app](https://railway.app)
2. Залогинься через GitHub
3. Нажми "New Project" → "Deploy from GitHub repo"
4. Выбери репозиторий `trendxl`

### 3. Настрой Environment Variables

В Railway Dashboard → Variables, добавь:

```bash
# API Keys (ОБЯЗАТЕЛЬНО - подставь свои ключи)
ENSEMBLE_DATA_API_KEY=your_ensemble_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Database
USE_SQLITE=true
SQLITE_DB_PATH=trendxl.db

# SeaTable (если нужно)
SEATABLE_API_TOKEN=your_seatable_token_here
SEATABLE_BASE_UUID=your_seatable_base_uuid_here

# Server (Railway автоматически установит)
DEBUG=false
```

### 4. Deploy!

Railway автоматически:

- ✅ Установит Python 3.11 + Node.js 18
- ✅ Соберет frontend (npm run build)
- ✅ Установит Python зависимости
- ✅ Запустит backend сервер
- ✅ Даст публичный URL

### 5. Проверь деплой

Когда деплой завершится, получишь URL типа:
`https://trendxl-production.up.railway.app`

Проверь:

- Главная страница загружается ✅
- API работает: `your-url.railway.app/api/health` ✅
- Можешь анализировать TikTok профили ✅

## Настройки проекта

### Автосборка настроена:

- `nixpacks.toml` - конфигурация сборки
- `Procfile` - команды запуска
- `start.sh` - startup script
- `railway.toml` - Railway настройки

### API Endpoints:

- `GET /api/health` - проверка здоровья
- `POST /api/v1/analyze-profile` - анализ профиля
- `GET /api/v1/trends` - получить тренды
- `POST /api/v1/refresh-trends` - обновить тренды

### Frontend:

- React 18 + TypeScript
- Tailwind CSS для стилей
- Автоматически собирается и подается через FastAPI

## Troubleshooting

### Если деплой не работает:

1. **Проверь логи в Railway Dashboard**
2. **Убедись что все API ключи добавлены**
3. **Проверь что переменные USE_SQLITE=true**

### Если frontend не загружается:

1. Проверь что `frontend/build` создается при сборке
2. Убедись что статические файлы подаются правильно

### Если API не работает:

1. Проверь `/api/health` endpoint
2. Убедись что CORS настроены для Railway URL
3. Проверь что все API ключи валидны

## Обновления

Чтобы обновить приложение:

1. Коммить изменения в GitHub
2. Railway автоматически пересоберет

## Масштабирование

Railway автоматически:

- Поднимет ресурсы при нагрузке
- Обеспечит 99.9% uptime
- Даст бесплатно $5/месяц (достаточно для начала)

---

🎉 **Готово! Твой TrendXL теперь живет в продакшене!**
