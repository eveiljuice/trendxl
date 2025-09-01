# 🚨 ИСПРАВЛЕНИЕ ОШИБКИ RAILWAY: "ENSEMBLE_DATA_API_KEY environment variable is required"

## ПРОБЛЕМА
Ваш проект на Railway выдает ошибку: **"ENSEMBLE_DATA_API_KEY environment variable is required"**

Это означает, что переменная окружения не настроена в Railway Dashboard.

## ✅ БЫСТРОЕ ИСПРАВЛЕНИЕ (5 минут)

### ШАГ 1: Откройте Railway Dashboard
1. Перейдите на [railway.app/dashboard](https://railway.app/dashboard)
2. Найдите ваш проект **TrendXL**
3. Кликните на проект

### ШАГ 2: Добавьте переменные окружения
1. В проекте найдите вкладку **"Variables"** (Переменные)
2. Кликните **"New Variable"** (Новая переменная)
3. Добавьте эти переменные **ТОЧНО с такими именами**:

```bash
Name: ENSEMBLE_DATA_API_KEY
Value: [ВАШ_ENSEMBLE_API_KEY]

Name: OPENAI_API_KEY  
Value: [ВАШ_OPENAI_API_KEY]

Name: USE_SQLITE
Value: true

Name: DEBUG
Value: false
```

> **⚠️ ВАЖНО:** Используйте ваши реальные API ключи:
> - `ENSEMBLE_DATA_API_KEY`: Ваш ключ от EnsembleData (из .env файла)
> - `OPENAI_API_KEY`: Ваш ключ от OpenAI (начинается с sk-)

### ШАГ 3: Redeploy
1. Кликните **"Deploy"** в Railway Dashboard
2. Или сделайте git push в ваш GitHub репозиторий

### ШАГ 4: Проверьте исправление
1. Дождитесь завершения деплоя (2-3 минуты)
2. Откройте ваш сайт
3. Или проверьте: `your-url.railway.app/api/health`

---

## 🔍 ДИАГНОСТИКА ПРОБЛЕМЫ

### Проверить статус переменных:
Откройте: `https://your-url.railway.app/api/debug/environment`

Этот endpoint покажет:
- ✅ Какие переменные настроены
- ❌ Какие отсутствуют
- 📝 Точные инструкции по исправлению

### Проверить health status:
Откройте: `https://your-url.railway.app/api/health`

Должен показать:
```json
{
  "status": "healthy",
  "services": {
    "ensemble": true,
    "gpt": true,
    "database": true
  }
}
```

---

## 📸 СКРИНШОТ-ИНСТРУКЦИЯ RAILWAY

### 1. Dashboard → Ваш проект
```
🔍 Railway Dashboard
├── 📁 My Projects
    ├── 🚀 trendxl (ваш проект)
    │   ├── 📊 Deployments
    │   ├── ⚙️ Variables ← СЮДА!
    │   ├── 🔧 Settings
    │   └── 📋 Logs
```

### 2. Variables Tab
```
⚙️ Variables
┌─────────────────────────────────────────┐
│ + New Variable                          │
├─────────────────────────────────────────┤
│ Name: ENSEMBLE_DATA_API_KEY            │
│ Value: [ВАШ_ENSEMBLE_KEY]              │
│                                         │
│ Name: OPENAI_API_KEY                   │  
│ Value: [ВАШ_OPENAI_KEY]                │
│                                         │
│ Name: USE_SQLITE                       │
│ Value: true                            │
└─────────────────────────────────────────┘
```

---

## 🚨 ЧАСТЫЕ ОШИБКИ

### ❌ Неправильное имя переменной
```bash
# НЕПРАВИЛЬНО:
ENSEMBLE_API_KEY=...

# ПРАВИЛЬНО:
ENSEMBLE_DATA_API_KEY=...
```

### ❌ Лишние пробелы
```bash
# НЕПРАВИЛЬНО:
ENSEMBLE_DATA_API_KEY = your_api_key_here

# ПРАВИЛЬНО:
ENSEMBLE_DATA_API_KEY=your_api_key_here
```

### ❌ Забыли redeploy
После добавления переменных **ОБЯЗАТЕЛЬНО** нужно:
1. Кликнуть **"Deploy"** в Railway
2. Или сделать git push

---

## 📞 ЕСЛИ НЕ ПОМОГЛО

### 1. Проверьте логи Railway
1. Railway Dashboard → Ваш проект
2. Вкладка **"Deployments"**
3. Кликните на последний деплой
4. Смотрите **"Build Logs"** и **"Deploy Logs"**

### 2. Проверьте переменные еще раз
Откройте: `your-url.railway.app/api/debug/environment`

Должно показать:
```json
{
  "required_variables": {
    "ENSEMBLE_DATA_API_KEY": {
      "configured": true,  ← ДОЛЖНО БЫТЬ true!
      "priority": "CRITICAL"
    }
  }
}
```

### 3. Если все еще не работает
1. Удалите все переменные в Railway
2. Добавьте их заново
3. Redeploy проект
4. Проверьте через 5 минут

---

## ✅ УСПЕШНОЕ ИСПРАВЛЕНИЕ

После исправления вы должны увидеть:

### В логах Railway:
```
✅ EnsembleService initialized with API key: [first8chars]...
🚀 Starting TrendXL on Railway...
Server running on 0.0.0.0:8000
```

### На сайте:
- Главная страница загружается
- Можете вставить TikTok URL
- API анализирует профили
- Нет ошибок в консоли

---

🎉 **ГОТОВО! Ваш TrendXL теперь работает на Railway без ошибок!**

*Если нужна помощь - проверьте `/api/debug/environment` endpoint для диагностики.*
