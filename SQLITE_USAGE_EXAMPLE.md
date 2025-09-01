# TrendXL SQLite Database - Пример использования

## 🚀 Быстрый старт с SQLite

### 1. Конфигурация

Убедитесь, что в вашем `.env` файле установлены следующие переменные:

```env
# Использовать SQLite вместо SeaTable
USE_SQLITE=true
SQLITE_DB_PATH=trendxl.db

# API ключи (для работы с TikTok и GPT)
ENSEMBLE_DATA_API_KEY=your_ensemble_data_key
OPENAI_API_KEY=your_openai_key
```

### 2. Запуск приложения

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Или через run.py
python run.py backend
```

### 3. Проверка работоспособности

```bash
# Проверка здоровья сервиса
curl http://localhost:8000/api/health
```

Ответ должен содержать:

```json
{
  "status": "healthy",
  "services": {
    "ensemble": true,
    "gpt": true,
    "database": true,
    "database_type": "SQLite"
  }
}
```

## 📊 Структура базы данных

### Таблица Users (Пользователи)

```sql
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL UNIQUE,           -- Имя пользователя TikTok
    Display_Name TEXT,                       -- Отображаемое имя
    Follower_Count INTEGER DEFAULT 0,        -- Количество подписчиков
    Following_Count INTEGER DEFAULT 0,       -- Количество подписок
    Video_Count INTEGER DEFAULT 0,           -- Количество видео
    Likes_Count INTEGER DEFAULT 0,           -- Количество лайков
    Bio TEXT,                                -- Биография
    Avatar_URL TEXT,                         -- URL аватара
    Verified BOOLEAN DEFAULT 0,              -- Верифицирован ли аккаунт
    Sec_UID TEXT,                            -- Вторичный UID
    UID TEXT,                                -- Основной UID
    Region TEXT,                             -- Регион
    Language TEXT,                           -- Язык
    Niche TEXT,                              -- Ниша (AI-анализ)
    Interests TEXT,                          -- Интересы (JSON)
    Keywords TEXT,                           -- Ключевые слова (JSON)
    Hashtags TEXT,                           -- Хэштеги (JSON)
    Target_Audience TEXT,                    -- Целевая аудитория
    Content_Style TEXT,                      -- Стиль контента
    Region_Focus TEXT,                       -- Фокус региона
    Created_At TEXT DEFAULT CURRENT_TIMESTAMP,
    Last_Updated TEXT DEFAULT CURRENT_TIMESTAMP
);
```

### Таблица Trends (Тренды)

```sql
CREATE TABLE Trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL,                  -- Пользователь (FK)
    Aweme_ID TEXT NOT NULL UNIQUE,           -- ID видео TikTok
    Description TEXT,                        -- Описание тренда
    Author_Username TEXT,                    -- Автор видео
    Author_Nickname TEXT,                    -- Ник автора
    Author_Followers INTEGER DEFAULT 0,      -- Подписчики автора
    Views INTEGER DEFAULT 0,                 -- Просмотры
    Likes INTEGER DEFAULT 0,                 -- Лайки
    Comments INTEGER DEFAULT 0,              -- Комментарии
    Shares INTEGER DEFAULT 0,                -- Репосты
    Downloads INTEGER DEFAULT 0,             -- Загрузки
    Favourited INTEGER DEFAULT 0,            -- Добавления в избранное
    Whatsapp_Shares INTEGER DEFAULT 0,       -- Репосты в WhatsApp
    Engagement_Rate REAL DEFAULT 0.0,        -- Коэффициент вовлеченности
    Duration INTEGER DEFAULT 0,              -- Длительность видео
    Video_Cover TEXT,                        -- Обложка видео
    Video_URL TEXT,                          -- URL видео
    Music_Title TEXT,                        -- Название музыки
    Music_Author TEXT,                       -- Автор музыки
    Music_ID TEXT,                           -- ID музыки
    Hashtags TEXT,                           -- Хэштеги (JSON)
    Region TEXT,                             -- Регион
    Video_Type TEXT,                         -- Тип видео
    Sound_Type TEXT,                         -- Тип звука
    Relevance_Score REAL DEFAULT 0.0,        -- Релевантность (AI)
    Relevance_Reason TEXT,                   -- Причина релевантности
    Trend_Category TEXT,                     -- Категория тренда
    Audience_Match BOOLEAN DEFAULT 0,        -- Совпадение аудитории
    Trend_Potential TEXT,                    -- Потенциал тренда
    Keyword TEXT,                            -- Ключевое слово
    Hashtag TEXT,                            -- Хэштег
    TikTok_URL TEXT,                         -- Полная ссылка TikTok
    Sentiment TEXT,                          -- Сентимент-анализ
    Audience TEXT,                           -- Тип аудитории
    Created_At TEXT DEFAULT CURRENT_TIMESTAMP,
    Saved_At TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Username) REFERENCES Users(Username) ON DELETE CASCADE
);
```

## 🔧 API Endpoints

### Анализ профиля

```bash
# Анализ профиля TikTok
POST /api/v1/analyze-profile
Content-Type: application/json

{
  "tiktok_url": "https://www.tiktok.com/@username"
}
```

### Обновление трендов

```bash
# Обновление трендов для пользователя
POST /api/v1/refresh-trends
Content-Type: application/json

{
  "username": "testuser",
  "max_results": 10
}
```

### Получение данных

```bash
# Получение профиля пользователя
GET /api/v1/profile/{username}

# Получение трендов пользователя
GET /api/v1/trends/{username}?limit=20

# Получение всех трендов
GET /api/v1/trends?limit=50
```

## 📈 Работа с базой данных напрямую

### Python пример

```python
from backend.services.database_adapter import database_service
import asyncio

async def example():
    # Создание профиля пользователя
    profile_data = {
        'username': 'techguru',
        'display_name': 'Tech Guru',
        'follower_count': 50000,
        'bio': 'Technology and programming tutorials',
        'verified': False
    }

    analysis_data = {
        'niche': 'Technology',
        'interests': ['programming', 'AI', 'web development'],
        'keywords': ['tech', 'coding', 'programming'],
        'hashtags': ['#tech', '#programming', '#coding'],
        'target_audience': 'developers',
        'content_style': 'educational'
    }

    # Сохранение профиля
    user_id = await database_service.create_user_profile(profile_data, analysis_data)
    print(f"User created with ID: {user_id}")

    # Получение профиля
    user = await database_service.get_user_profile('techguru')
    print(f"User niche: {user['Niche']}")

    # Получение трендов
    trends = await database_service.get_user_trends('techguru', limit=10)
    print(f"Found {len(trends)} trends")

# Запуск
asyncio.run(example())
```

### SQL запросы

```sql
-- Топ пользователей по подписчикам
SELECT Username, Display_Name, Follower_Count, Niche
FROM Users
ORDER BY Follower_Count DESC
LIMIT 10;

-- Тренды с высокой релевантностью
SELECT t.Description, t.Relevance_Score, u.Username
FROM Trends t
JOIN Users u ON t.Username = u.Username
WHERE t.Relevance_Score > 0.8
ORDER BY t.Relevance_Score DESC
LIMIT 20;

-- Статистика по нишам
SELECT Niche, COUNT(*) as user_count, AVG(Follower_Count) as avg_followers
FROM Users
GROUP BY Niche
ORDER BY user_count DESC;
```

## 🔄 Миграция с SeaTable

Если у вас есть данные в SeaTable и вы хотите перенести их в SQLite:

```bash
# Запуск скрипта миграции
python migrate_to_sqlite.py

# Или миграция конкретной базы
python migrate_to_sqlite.py --db-path /path/to/old/database.db
```

## ⚡ Производительность

SQLite в TrendXL оптимизирован для:

- **Быстрые чтения**: Индексы на часто используемых полях
- **Эффективные запросы**: Прямые SQL запросы без HTTP overhead
- **Локальная разработка**: Не требует интернет-соединения
- **Резервное копирование**: Простое копирование файла базы данных

## 🛠️ Troubleshooting

### Проблема: "Database not found"

```bash
# Решение: Проверьте путь к файлу базы данных
ls -la trendxl.db

# Или создайте новую базу данных
python -c "from backend.services.sqlite_service import SQLiteService; s = SQLiteService(); print('DB created')"
```

### Проблема: "FOREIGN KEY constraint failed"

```sql
-- Включите поддержку внешних ключей
PRAGMA foreign_keys = ON;
```

### Проблема: "Database is locked"

```bash
# Закройте все соединения с базой данных
# Перезапустите приложение
python run.py restart
```

## 📚 Дополнительные ресурсы

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SeaTable API](https://api.seatable.io/) (для production использования)

---

**TrendXL SQLite** - Быстрая, надежная и простая в использовании база данных для локальной разработки! 🚀
