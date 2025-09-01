"""
TrendXL - AI Trend Feed Backend
Main FastAPI application entry point
"""

import sys
import os
import time
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend directory to Python path for imports
backend_dir = Path(__file__).parent
parent_dir = backend_dir.parent

if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# Import TrendXL modules with proper error handling
try:
    from routers.analysis import router as analysis_router
    from routers.trends import router as trends_router
    from routers.analytics import router as analytics_router
    from routers.debug import router as debug_router
    from services.ensemble_service import EnsembleService
    from services.gpt_service import GPTService
except ImportError as e:
    print(f"❌ Failed to import TrendXL modules: {e}")
    print(f"Current path: {sys.path}")
    print(f"Backend dir: {backend_dir}")
    print(f"Parent dir: {parent_dir}")
    sys.exit(1)

# Check Python version compatibility
if sys.version_info < (3, 8):
    print(
        f"❌ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    print("TrendXL requires Python 3.8 or higher")
    sys.exit(1)
elif sys.version_info >= (3, 12):
    print(
        f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - Compatible")
else:
    print(f"⚠️  Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - Compatible but consider upgrading to 3.12")

# Load environment variables
load_dotenv()

app = FastAPI(
    title="TrendXL API",
    description="AI-powered TikTok trend analysis platform",
    version="1.0.0"
)

# CORS middleware - Production ready
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.railway.app",
        "https://trendxl.railway.app",
        os.getenv("FRONTEND_URL", "*")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services will be done lazily to avoid startup errors

# Include routers
app.include_router(analysis_router, prefix="/api/v1", tags=["analysis"])
app.include_router(trends_router, prefix="/api/v1", tags=["trends"])
app.include_router(
    analytics_router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(debug_router, prefix="/api/debug", tags=["debug"])

# Serve static files (React build) in production
build_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "build")
if os.path.exists(build_dir):
    app.mount(
        "/static", StaticFiles(directory=os.path.join(build_dir, "static")), name="static")

    # Serve React app on all routes (SPA)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        from fastapi.responses import FileResponse

        # Don't serve frontend for API routes
        if full_path.startswith("api/"):
            raise HTTPException(
                status_code=404, detail="API endpoint not found")

        # Serve index.html for all frontend routes
        index_file = os.path.join(build_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        else:
            raise HTTPException(status_code=404, detail="Frontend not built")


@app.get("/api/health")
async def health_check():
    """Enhanced health check endpoint with environment variables diagnostics"""
    services_status = {}
    overall_status = "healthy"
    errors = []
    env_diagnostics = {}

    # Check environment variables first
    required_env_vars = {
        "ENSEMBLE_DATA_API_KEY": "EnsembleData API Key for TikTok data",
        "OPENAI_API_KEY": "OpenAI API Key for AI analysis",
        "USE_SQLITE": "Database mode selector"
    }
    
    for env_var, description in required_env_vars.items():
        value = os.getenv(env_var)
        env_diagnostics[env_var] = {
            "configured": bool(value),
            "description": description,
            "value_preview": f"{value[:8]}..." if value and len(value) > 8 else "Not set"
        }
        
        if not value and env_var in ["ENSEMBLE_DATA_API_KEY", "OPENAI_API_KEY"]:
            errors.append(f"❌ Missing {env_var}: {description}")
            overall_status = "unhealthy"

    # Test each service individually to provide detailed error information
    try:
        ensemble_service = EnsembleService()
        services_status["ensemble"] = ensemble_service.is_healthy()
    except Exception as e:
        services_status["ensemble"] = False
        errors.append(f"Ensemble service error: {str(e)}")
        overall_status = "degraded"

    try:
        gpt_service = GPTService()
        services_status["gpt"] = gpt_service.is_healthy()
    except Exception as e:
        services_status["gpt"] = False
        errors.append(f"GPT service error: {str(e)}")
        overall_status = "degraded"

    try:
        from services.database_adapter import database_service
        services_status["database"] = database_service.is_healthy()
        services_status["database_type"] = "SQLite"
    except Exception as e:
        services_status["database"] = False
        services_status["database_type"] = "SQLite"
        errors.append(f"Database service error: {str(e)}")
        overall_status = "degraded"

    response = {
        "status": overall_status,
        "services": services_status,
        "environment": env_diagnostics,
        "deployment_platform": "Railway" if os.getenv("RAILWAY_ENVIRONMENT") else "Local/Other",
        "timestamp": int(time.time())
    }

    if errors:
        response["errors"] = errors
        response["message"] = "Configuration issues detected. Check errors and environment variables."
        
        # Railway-specific help
        if os.getenv("RAILWAY_ENVIRONMENT"):
            response["railway_help"] = {
                "dashboard_url": "https://railway.app/dashboard",
                "steps": [
                    "1. Go to Railway Dashboard",
                    "2. Select your TrendXL project",
                    "3. Click 'Variables' tab",
                    "4. Add missing environment variables",
                    "5. Redeploy by clicking 'Deploy' or push to GitHub"
                ]
            }

    return response


@app.get("/api/debug/environment")
async def debug_environment():
    """Debug endpoint to check all environment variables (Railway deployment help)"""
    return {
        "platform_detection": {
            "is_railway": bool(os.getenv("RAILWAY_ENVIRONMENT")),
            "is_local": not bool(os.getenv("RAILWAY_ENVIRONMENT")),
            "railway_project_id": os.getenv("RAILWAY_PROJECT_ID", "Not detected"),
            "railway_service_id": os.getenv("RAILWAY_SERVICE_ID", "Not detected")
        },
        "required_variables": {
            "ENSEMBLE_DATA_API_KEY": {
                "configured": bool(os.getenv("ENSEMBLE_DATA_API_KEY")),
                "description": "EnsembleData API key for TikTok data access",
                "example": "your_ensemble_api_key_here",
                "priority": "CRITICAL"
            },
            "OPENAI_API_KEY": {
                "configured": bool(os.getenv("OPENAI_API_KEY")),
                "description": "OpenAI API key for AI analysis",
                "example": "sk-...",
                "priority": "CRITICAL"
            },
            "USE_SQLITE": {
                "configured": bool(os.getenv("USE_SQLITE")),
                "current_value": os.getenv("USE_SQLITE", "Not set"),
                "description": "Database mode (set to 'true' for Railway)",
                "example": "true",
                "priority": "RECOMMENDED"
            }
        },
        "railway_setup_guide": {
            "step_1": "Go to https://railway.app/dashboard",
            "step_2": "Find your TrendXL project",
            "step_3": "Click on 'Variables' tab",
            "step_4": "Add these variables:",
            "variables_to_add": [
                {
                    "name": "ENSEMBLE_DATA_API_KEY", 
                    "value": "your_ensemble_api_key_here",
                    "note": "Replace with your actual Ensemble API key"
                },
                {
                    "name": "OPENAI_API_KEY", 
                    "value": "your_openai_api_key_here", 
                    "note": "Replace with your actual OpenAI API key (sk-...)"
                },
                {
                    "name": "USE_SQLITE", 
                    "value": "true", 
                    "note": "Required for Railway deployment"
                },
                {
                    "name": "DEBUG", 
                    "value": "false", 
                    "note": "Set to false for production"
                }
            ],
            "step_5": "Click 'Deploy' button or push changes to GitHub to trigger redeploy"
        },
        "current_environment_sample": {
            var: "SET" if os.getenv(var) else "NOT SET" 
            for var in ["ENSEMBLE_DATA_API_KEY", "OPENAI_API_KEY", "USE_SQLITE", "DEBUG", "PORT", "HOST"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )
