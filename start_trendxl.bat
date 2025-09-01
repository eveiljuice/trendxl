@echo off
REM TrendXL Full Application Launcher
REM Starts both backend and frontend servers

echo.
echo ================================================
echo    🚀 Starting TrendXL - AI Trend Feed
echo ================================================
echo.

REM Check if we're in the right directory
if not exist "backend\main.py" (
    echo ❌ Error: Please run this script from the project root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found. Please create it manually.
    echo Required variables:
    echo - ENSEMBLE_DATA_API_KEY
    echo - OPENAI_API_KEY
    echo.
    echo Note: SQLite database will be created automatically
    echo.
)

echo 🔧 Stopping any existing processes...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1
timeout /t 2 >nul

echo.
echo 🔧 Starting Backend Server...
start "TrendXL Backend" cmd /k "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

echo ⏳ Waiting for backend to start...
timeout /t 3 >nul

echo.
echo 🎨 Starting Frontend Server...
start "TrendXL Frontend" cmd /k "cd frontend && npm start"

echo.
echo ================================================
echo    🎉 TrendXL is starting up!
echo ================================================
echo.
echo 🌐 Access URLs:
echo    Frontend:    http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Docs:    http://localhost:8000/docs
echo.
echo 📋 How to use:
echo 1. Open browser: http://localhost:3000
echo 2. Enter a TikTok profile URL
echo 3. Click "Analyze Profile" to get AI insights
echo 4. Click "Refresh Trends" for personalized recommendations
echo.
echo 🔧 Troubleshooting:
echo - If you see proxy errors, wait a moment and refresh
echo - Check the backend terminal for any errors
echo - Verify API keys are set in .env file
echo.
echo Press any key to close this window...
pause >nul
