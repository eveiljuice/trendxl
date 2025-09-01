# TrendXL GitHub Upload Guide

## Quick Upload Instructions

### 1. Create Repository on GitHub

1. Зайдите на [GitHub.com](https://github.com)
2. Нажмите "New repository" (зеленая кнопка)
3. Название: `trendxl`
4. Описание: `TrendXL - AI-powered TikTok trend analysis platform`
5. Выберите Public/Private по желанию
6. ✅ Initialize with README
7. Нажмите "Create repository"

### 2. Clone and Upload via Git

```bash
# Clone your new repository
git clone https://github.com/YOUR_USERNAME/trendxl.git
cd trendxl

# Copy all project files (исключая ненужные)
# НЕ копируйте эти папки/файлы:
# - node_modules/ (в корне и в frontend/)
# - __pycache__/ (все директории)
# - *.db файлы
# - *.csv файлы (кроме sample данных)
# - frontend/build/

# Add all files
git add .
git commit -m "Initial commit: TrendXL AI trend analysis platform

- FastAPI backend with TikTok analysis
- React frontend with modern UI
- Docker containerization
- SQLite database
- AI-powered insights"

git push origin main
```

### 3. Alternative: GitHub Web Upload

1. Откройте ваш новый репозиторий на GitHub
2. Нажмите "uploading an existing file"
3. Перетащите папки/файлы (исключая ненужные)
4. Добавьте commit message
5. Нажмите "Commit changes"

## Project Structure to Upload

✅ **Include these:**

```
trendxl/
├── .gitignore                    ✅
├── README.md                     ✅
├── requirements.txt              ✅
├── package.json                  ✅
├── docker-compose.yml            ✅
├── Dockerfile                    ✅
├── run.py                        ✅
├── backend/                      ✅
│   ├── main.py
│   ├── models/
│   ├── routers/
│   ├── services/
│   └── prompts/
├── frontend/                     ✅
│   ├── package.json
│   ├── src/
│   ├── public/
│   ├── tailwind.config.js
│   └── tsconfig.json
└── *.md documentation files     ✅
```

❌ **Exclude these:**

```
- node_modules/           ❌
- __pycache__/           ❌
- frontend/build/        ❌
- *.db files             ❌
- *.csv data files       ❌
- logs/                  ❌
```

## Repository Configuration

После загрузки, рекомендую:

1. **Add topics/tags:**

   - `ai`
   - `tiktok`
   - `trend-analysis`
   - `fastapi`
   - `react`
   - `typescript`
   - `docker`

2. **Setup GitHub Pages** (если нужно):

   - Settings → Pages → Source: GitHub Actions

3. **Add collaborators** (если нужно):
   - Settings → Collaborators

## Environment Setup for Contributors

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/trendxl.git
cd trendxl

# Backend setup
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
cd ..

# Run development
python run.py dev
```
