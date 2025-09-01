# TrendXL - Быстрый запуск в режиме SQLite

## 🚀 Запуск проекта TrendXL

### Предварительные требования

- Python 3.13+
- Node.js (установлен в `D:\PROGS.TIMO\`)
- Все зависимости установлены

### Шаг 1: Настройка конфигурации

```bash
# Скопировать конфигурацию для SQLite режима
Copy-Item .env.sqlite .env
```

### Шаг 2: Запуск Backend (Python + FastAPI)

```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Проверка работы:**

```bash
Invoke-WebRequest -Uri http://localhost:8000/docs -UseBasicParsing
```

✅ Должен вернуть статус 200

### Шаг 3: Запуск Frontend (React)

```bash
cd frontend

# Установка зависимостей (если нужно)
& "D:\PROGS.TIMO\npm.cmd" install

# Запуск сервера разработки
& "D:\PROGS.TIMO\npm.cmd" start
```

### Шаг 4: Проверка работы

```bash
# Backend API
Invoke-WebRequest -Uri http://localhost:8000/docs -UseBasicParsing

# Frontend
Invoke-WebRequest -Uri http://localhost:3000 -UseBasicParsing
```

## 🌐 Доступ к приложению

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API документация**: http://localhost:8000/docs

## 🔧 Устранение проблем

### Порт занят

```bash
# Убить процессы Python
taskkill /f /im python.exe

# Убить процессы Node.js
taskkill /f /im node.exe
```

### Зависимости backend

```bash
cd backend
pip install -r ../requirements.txt
```

### Проблемы с Node.js

Использовать полный путь:

```bash
& "D:\PROGS.TIMO\npm.cmd" install
& "D:\PROGS.TIMO\npm.cmd" start
```

## 📋 Использование

1. Открыть браузер: http://localhost:3000
2. Ввести URL TikTok профиля
3. Нажать "Analyze Profile"
4. Просмотреть AI-анализ и рекомендации

## ⚙️ Режимы работы

- **SQLite** (текущий): Полностью автономный, локальная БД
- **SeaTable**: Требует API токены и подключение к SeaTable

## 🛠️ Альтернативный запуск

Использовать batch файл:

```bash
.\start_trendxl.bat
```

⚠️ Может требовать корректной кодировки файла

---

**Статус**: ✅ Работает в режиме SQLite без SeaTable
