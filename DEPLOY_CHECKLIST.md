# ✅ TrendXL Railway Deploy Checklist

## Перед деплоем - убедись что есть:

### 🔑 API Keys

- [ ] **EnsembleData API Key** - для TikTok данных
- [ ] **OpenAI API Key** - для AI анализа
- [ ] Ключи валидны и активны

### 📁 Файлы готовы к деплою

- [x] `railway.toml` - конфигурация Railway
- [x] `nixpacks.toml` - настройки сборки
- [x] `Procfile` - команды запуска
- [x] `start.sh` - startup script
- [x] `requirements.txt` - Python зависимости
- [x] `package.json` - Node.js конфигурация
- [x] `.railwayignore` - исключения для деплоя

### 🔧 Code fixes

- [x] API client поддерживает environment URLs
- [x] CORS настроены для production
- [x] Frontend build конфигурация готова
- [x] Static files serving настроен
- [x] Health check endpoints работают

## Деплой на Railway:

### 1. Создай проект

- [ ] Зарегистрируйся на railway.app
- [ ] New Project → Deploy from GitHub repo
- [ ] Выбери репозиторий trendxl

### 2. Environment Variables

Добавь в Railway Dashboard → Variables:

```bash
ENSEMBLE_DATA_API_KEY=your_ensemble_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
USE_SQLITE=true
DEBUG=false
```

### 3. Проверь деплой

- [ ] Build успешен (в Railway логах)
- [ ] Приложение запустилось
- [ ] Получи публичный URL

### 4. Проверь функциональность

- [ ] Главная страница загружается
- [ ] `your-url/api/health` отвечает 200
- [ ] Можешь вставить TikTok URL и анализировать
- [ ] API запросы работают

## В случае проблем:

### Build failed?

- Проверь Railway logs
- Убедись что все зависимости в requirements.txt
- Проверь что Node.js версия 18+

### App не запускается?

- Проверь environment variables
- Убедись что API ключи корректны
- Проверь порт (Railway автоматически установит PORT)

### Frontend не загружается?

- Проверь что `frontend/build` создался при сборке
- Убедись что static files paths правильные

### API не работает?

- Проверь `/api/health` endpoint
- Убедись что CORS включает Railway URL
- Проверь что backend запущен на правильном порту

---

## 🎉 После успешного деплоя:

✅ **Твой TrendXL живёт в продакшене!**  
✅ **URL доступен 24/7**  
✅ **Auto-scaling включен**  
✅ **SSL сертификат активен**

**Следующие шаги:**

- Добавь custom domain (опционально)
- Настрой monitoring
- Обнови README с live URL
- Поделись ссылкой!
