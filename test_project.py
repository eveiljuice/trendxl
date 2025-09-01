#!/usr/bin/env python3
"""
Test script to verify TrendXL project is working correctly
"""

import sys
import subprocess
import time
import requests
from pathlib import Path


def test_imports():
    """Test that all critical imports work"""
    print("🧪 Testing imports...")

    try:
        # Test backend imports
        sys.path.insert(0, str(Path(__file__).parent / "backend"))
        import main
        from services.ensemble_service import EnsembleService
        from services.gpt_service import GPTService
        from services.seatable_service import SeaTableService
        print("✅ Backend imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_fastapi_app():
    """Test that FastAPI app can be created"""
    print("🧪 Testing FastAPI app creation...")

    try:
        sys.path.insert(0, str(Path(__file__).parent / "backend"))
        import main
        app = main.app
        print(f"✅ FastAPI app created: {app.title}")
        return True
    except Exception as e:
        print(f"❌ FastAPI app creation failed: {e}")
        return False


def test_dependencies():
    """Test that critical dependencies are installed"""
    print("🧪 Testing dependencies...")

    dependencies = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'openai',
        'requests'
    ]

    failed = []
    for dep in dependencies:
        try:
            __import__(dep.replace('-', '_'))
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            failed.append(dep)

    if failed:
        print(f"❌ Missing dependencies: {', '.join(failed)}")
        return False

    print("✅ All critical dependencies installed")
    return True


def test_env_file():
    """Test that environment file exists and has basic structure"""
    print("🧪 Testing environment configuration...")

    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        print("⚠️  .env file not found (this is normal for testing)")
        return True

    try:
        from dotenv import load_dotenv
        load_dotenv()

        # Check for critical environment variables
        import os
        critical_vars = ['ENSEMBLE_DATA_API_KEY',
                         'OPENAI_API_KEY', 'SEATABLE_API_TOKEN']
        missing = []

        for var in critical_vars:
            if not os.getenv(var):
                missing.append(var)

        if missing:
            print(f"⚠️  Missing environment variables: {', '.join(missing)}")
            print("   This is expected if you haven't configured API keys yet")
        else:
            print("✅ Environment variables configured")

        return True

    except Exception as e:
        print(f"❌ Environment test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 TrendXL Project Test Suite")
    print("=" * 40)

    tests = [
        test_dependencies,
        test_imports,
        test_fastapi_app,
        test_env_file
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} passed")

    if passed == total:
        print("🎉 All tests passed! Project is ready to run.")
        print("\nNext steps:")
        print("1. Configure your .env file with API keys")
        print("2. Run 'python run.py install' to ensure all dependencies")
        print("3. Run 'python run.py dev' to start the application")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nTroubleshooting:")
        print("1. Run 'python run.py diagnose' for detailed diagnostics")
        print("2. Check that all dependencies are installed")
        print("3. Verify Python version is 3.8+")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
