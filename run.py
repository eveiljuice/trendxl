#!/usr/bin/env python3
"""
TrendXL - AI Trend Feed
Main application runner script
"""

import os
import sys
import subprocess
import signal
import time
import json
import shutil
from pathlib import Path
from typing import Optional, Dict, Any

# Add backend to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Configuration
PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"


def check_system_requirements():
    """Check if system meets minimum requirements"""
    print("🔍 Checking system requirements...")

    # Check Python version
    if sys.version_info < (3, 8):
        print(
            f"❌ Python {sys.version_info.major}.{sys.version_info.minor} detected")
        print("TrendXL requires Python 3.8 or higher")
        return False
    elif sys.version_info >= (3, 12):
        print(
            f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - Perfect!")
    else:
        print(
            f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - Compatible")

    # Check if we're in the right directory
    if not (PROJECT_ROOT / "requirements.txt").exists():
        print("❌ requirements.txt not found. Please run from the project root directory")
        return False

    print("✅ System requirements check passed")
    return True


def install_dependencies():
    """Install Python and Node.js dependencies"""
    if not check_system_requirements():
        return False

    print("🔧 Installing Python dependencies...")

    # Upgrade pip first
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                       check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("⚠️  Could not upgrade pip, continuing with current version")

    try:
        # Set environment variable for PyO3 compatibility with Python 3.13+
        env = os.environ.copy()
        if sys.version_info >= (3, 13):
            env['PYO3_USE_ABI3_FORWARD_COMPATIBILITY'] = '1'
            print("⚠️  Python 3.13 detected - enabling PyO3 ABI compatibility mode")

        # Install Python dependencies
        cmd = [sys.executable, "-m", "pip",
               "install", "-r", "requirements.txt"]
        subprocess.run(cmd, check=True, cwd=PROJECT_ROOT, env=env)
        print("✅ Python dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python dependencies: {e}")
        return False

    # Install Node.js dependencies
    if FRONTEND_DIR.exists():
        print("🔧 Installing Node.js dependencies...")
        try:
            # Check if npm is available (try multiple ways)
            npm_found = False
            npm_paths = [
                "npm",  # From PATH
                "npm.cmd",  # Windows specific
                os.path.join(os.environ.get("APPDATA", ""),
                             "npm", "npm.cmd"),  # Windows npm
                "/usr/local/bin/npm",  # macOS/Linux common
                "/usr/bin/npm",  # Linux
                "/opt/homebrew/bin/npm",  # macOS with Homebrew
            ]

            npm_cmd = None
            for npm_path in npm_paths:
                try:
                    if os.path.isfile(npm_path) or npm_path in ["npm", "npm.cmd"]:
                        result = subprocess.run(
                            [npm_path, "--version"], capture_output=True, text=True, timeout=10)
                        if result.returncode == 0:
                            npm_cmd = npm_path
                            npm_found = True
                            print(f"✅ Found npm at: {npm_path}")
                            print(f"   Version: {result.stdout.strip()}")
                            break
                except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                    continue

            if not npm_found:
                print("❌ npm not found in common locations")
                print("🔍 Searching for Node.js installation...")

                # Try to find npm in system
                common_paths = [
                    r"C:\Program Files\nodejs\npm.cmd",
                    r"C:\Program Files (x86)\nodejs\npm.cmd",
                    os.path.expanduser("~/.npm/npm.cmd"),
                    "/usr/local/bin/npm",
                    "/usr/bin/npm",
                    "/opt/homebrew/bin/npm",  # macOS with Homebrew
                ]

                for path in common_paths:
                    if os.path.exists(path):
                        print(f"📍 Found npm at: {path}")
                        npm_cmd = path
                        npm_found = True
                        break

                if not npm_found:
                    print(
                        "❌ Could not find npm. Please check your Node.js installation:")
                    print("1. Verify Node.js is installed: node --version")
                    print("2. Check npm: npm --version")
                    print("3. Restart your terminal/command prompt")
                    print("4. If using Windows, try running as Administrator")
                    print("5. Download from: https://nodejs.org/en/download/")
                    return False

            # Install dependencies using found npm
            print(f"📦 Using npm: {npm_cmd}")
            subprocess.run([npm_cmd, "install"], check=True, cwd=FRONTEND_DIR)
            print("✅ Node.js dependencies installed successfully")

        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Node.js dependencies: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error during Node.js installation: {e}")
            return False
    else:
        print("⚠️  Frontend directory not found, skipping Node.js dependencies")

    return True


def find_npm_command() -> Optional[str]:
    """Locate npm executable across platforms. Returns full path or None."""
    # Prefer PATH resolution
    for candidate in ["npm", "npm.cmd"]:
        path = shutil.which(candidate)
        if path:
            return path

    # Fallback common locations (Windows and Unix-like)
    common_paths = [
        r"C:\\Program Files\\nodejs\\npm.cmd",
        r"C:\\Program Files (x86)\\nodejs\\npm.cmd",
        os.path.join(os.environ.get("APPDATA", ""), "npm", "npm.cmd"),
        "/usr/local/bin/npm",
        "/usr/bin/npm",
        "/opt/homebrew/bin/npm",
    ]
    for path in common_paths:
        if path and os.path.exists(path):
            return path
    return None


def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path.cwd() / ".env"

    if not env_file.exists():
        print("❌ .env file not found!")
        print("Please create a .env file with your API keys:")
        print("- ENSEMBLE_DATA_API_KEY")
        print("- OPENAI_API_KEY")
        print("- SEATABLE_API_TOKEN")
        print("- SEATABLE_BASE_UUID (or SEATABLE_ID)")
        print("\n📋 To get access to TrendXL SeaTable database:")
        print("🔗 Join here: https://cloud.seatable.io/dtable/links/bc4b5e5624bf47b49d82")
        print("\nExample .env file content:")
        print("SEATABLE_BASE_UUID=a9d57cc5-bb91-4183-aeda-9e9954903d87")
        print("SEATABLE_API_TOKEN=your_token_here")
        print("# ... other variables")
        return False

    # Load environment variables for validation
    from dotenv import load_dotenv
    load_dotenv()

    # Check if required variables are set
    required_vars = ["ENSEMBLE_DATA_API_KEY",
                     "OPENAI_API_KEY", "SEATABLE_API_TOKEN"]
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    # Check SeaTable UUID (accept either variable name)
    seatable_uuid = os.getenv("SEATABLE_BASE_UUID") or os.getenv("SEATABLE_ID")
    if not seatable_uuid:
        missing_vars.append("SEATABLE_BASE_UUID (or SEATABLE_ID)")

    if missing_vars:
        print(
            f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("\nPlease add these to your .env file:")
        for var in missing_vars:
            print(f"  {var}=your_value_here")
        print("\n📋 To get access to TrendXL SeaTable database:")
        print("🔗 Join here: https://cloud.seatable.io/dtable/links/bc4b5e5624bf47b49d82")
        return False

    print("✅ Environment configuration looks good")
    print(f"✅ SeaTable UUID: {seatable_uuid}")
    return True


def run_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting FastAPI backend server...")
    # Stay in root directory and specify the correct module path

    # Find working Python executable (prioritize the working one we found)
    python_executables = [
        r"D:\PROGS.TIMO\python.exe",
        sys.executable,
        "python.exe",
        "python3.exe",
        "py.exe -3.12",
        "py.exe"
    ]

    python_exec = None
    for exec_candidate in python_executables:
        try:
            if " " in exec_candidate:
                cmd = exec_candidate.split() + \
                    ["-c", "import uvicorn; print('OK')"]
            else:
                cmd = [exec_candidate, "-c", "import uvicorn; print('OK')"]

            result = subprocess.run(
                cmd, check=True, capture_output=True, text=True)
            if "OK" in result.stdout:
                python_exec = exec_candidate
                break
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue

    if not python_exec:
        print("❌ No working Python executable found!")
        return

    try:
        if " " in python_exec:
            cmd = python_exec.split() + \
                ["-m", "uvicorn", "backend.main:app", "--host",
                    "0.0.0.0", "--port", "8000", "--reload"]
        else:
            cmd = [python_exec, "-m", "uvicorn", "backend.main:app",
                   "--host", "0.0.0.0", "--port", "8000", "--reload"]

        subprocess.run(cmd, check=True, cwd=Path.cwd())
    except KeyboardInterrupt:
        print("\n⏹️  Backend server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start backend server: {e}")


def run_frontend():
    """Start the React development server"""
    frontend_dir = Path.cwd() / "frontend"

    if not frontend_dir.exists():
        print(
            "❌ Frontend directory not found. Please ensure the frontend is properly set up.")
        return

    print("🚀 Starting React development server...")
    try:
        npm_cmd = find_npm_command()
        if not npm_cmd:
            print("❌ npm not found. Install Node.js and ensure npm is in PATH.")
            print("🔗 Download: https://nodejs.org/en/download/")
            return

        # Prefer explicit "run start" to avoid any shell built-in ambiguity on Windows
        subprocess.run([npm_cmd, "run", "start"], check=True, cwd=frontend_dir)
    except KeyboardInterrupt:
        print("\n⏹️  Frontend server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start frontend server: {e}")


def _delayed_run_frontend():
    """Start the frontend after a short delay to give backend time to boot.

    This function must be at module level so it is picklable by
    multiprocessing on Windows (spawn start method).
    """
    time.sleep(3)
    run_frontend()


def run_full_stack():
    """Run both backend and frontend in parallel"""
    import multiprocessing

    print("🚀 Starting TrendXL full-stack application...")
    print("Backend will be available at: http://localhost:8000")
    print("Frontend will be available at: http://localhost:3000")
    print("Press Ctrl+C to stop both servers\n")

    # Start backend in separate process
    backend_process = multiprocessing.Process(target=run_backend)
    frontend_process = multiprocessing.Process(target=_delayed_run_frontend)

    try:
        backend_process.start()
        frontend_process.start()

        # Wait for both processes
        backend_process.join()
        frontend_process.join()

    except KeyboardInterrupt:
        print("\n⏹️  Shutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.join()
        frontend_process.join()


def main():
    """Main application entry point"""
    print("🌟 Welcome to TrendXL - AI Trend Feed")
    print("=" * 60)
    print("🔗 Backend: http://localhost:8000")
    print("🔗 Frontend: http://localhost:3000")
    print("🔗 Health Check: http://localhost:8000/health")
    print("=" * 60)

    if len(sys.argv) < 2:
        print("Usage: python run.py [command]")
        print("\nCommands:")
        print("  install     - Install all dependencies")
        print("  backend     - Run backend server only")
        print("  frontend    - Run frontend server only")
        print("  dev         - Run full-stack development servers")
        print("  check       - Check environment setup")
        print("  diagnose    - Run detailed diagnostics")
        print("  docker      - Run with Docker (requires docker-compose)")
        print("  fix-python   - Fix Python compatibility issues")
        print("  check-node   - Diagnose Node.js/npm issues")
        print("\nExamples:")
        print("  python run.py install    # First time setup")
        print("  python run.py dev        # Start development servers")
        print("  python run.py check      # Verify configuration")
        return

    command = sys.argv[1].lower()

    if command == "install":
        if not install_dependencies():
            sys.exit(1)

    elif command == "check":
        if not check_env_file():
            sys.exit(1)
        print("✅ Environment check passed")

    elif command == "diagnose":
        print("🔍 Running detailed diagnostics...")
        try:
            subprocess.run([sys.executable, "diagnose_project.py"], check=True)
        except subprocess.CalledProcessError:
            print("❌ Diagnostics failed")
            sys.exit(1)
        except FileNotFoundError:
            print(
                "❌ Diagnostics script not found. Run 'python diagnose_project.py' directly")
            sys.exit(1)

    elif command == "docker":
        print("🐳 Starting TrendXL with Docker...")
        try:
            subprocess.run(["docker-compose", "up", "--build"], check=True)
        except subprocess.CalledProcessError:
            print("❌ Docker failed. Make sure Docker and docker-compose are installed")
            sys.exit(1)
        except FileNotFoundError:
            print("❌ docker-compose not found. Please install Docker and docker-compose")
            sys.exit(1)

    elif command == "fix-python":
        print("🔧 Running Python compatibility fixer...")
        try:
            subprocess.run(
                [sys.executable, "fix_python_compatibility.py"], check=True)
        except subprocess.CalledProcessError:
            print("❌ Compatibility fixer failed")
            sys.exit(1)
        except FileNotFoundError:
            print("❌ Compatibility fixer script not found")
            sys.exit(1)

    elif command == "check-node":
        print("🔍 Running Node.js diagnostic...")
        try:
            subprocess.run([sys.executable, "check_nodejs.py"], check=True)
        except subprocess.CalledProcessError:
            print("❌ Node.js diagnostic failed")
            sys.exit(1)
        except FileNotFoundError:
            print("❌ Node.js diagnostic script not found")
            sys.exit(1)

    elif command == "backend":
        if not check_env_file():
            sys.exit(1)
        run_backend()

    elif command == "frontend":
        run_frontend()

    elif command == "dev":
        if not check_env_file():
            sys.exit(1)
        run_full_stack()

    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python run.py' to see available commands")
        sys.exit(1)


if __name__ == "__main__":
    main()
