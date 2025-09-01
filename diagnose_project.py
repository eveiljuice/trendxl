#!/usr/bin/env python3
"""
TrendXL Project Diagnostic Script
Comprehensive analysis of project configuration and dependencies
"""

import os
import sys
import subprocess
import importlib
import json
from pathlib import Path


class ProjectDiagnostics:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.project_root = Path.cwd()

    def log_issue(self, category, message, severity="error"):
        """Log an issue with category and severity"""
        if severity == "error":
            self.issues.append(f"❌ [{category}] {message}")
        else:
            self.warnings.append(f"⚠️  [{category}] {message}")

    def check_python_version(self):
        """Check Python version compatibility"""
        print("🔍 Checking Python version...")
        version = sys.version_info
        if version.major == 3 and version.minor >= 8:
            print(
                f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        else:
            self.log_issue(
                "Python", f"Python {version.major}.{version.minor} detected. Minimum required: 3.8")

    def check_dependencies(self):
        """Check if required Python packages are installed"""
        print("\n🔍 Checking Python dependencies...")

        required_packages = {
            'fastapi': '0.104.1',
            'uvicorn': '0.24.0',
            'ensembledata': '0.2.6',
            'openai': '1.3.0',
            'requests': '2.31.0',
            'pydantic': '2.0.0',
            'python-dotenv': '1.0.0',
            'seatable-api': '2.6.0',
            'httpx': '0.25.0',
            'python-multipart': '0.0.6'
        }

        missing_packages = []
        version_issues = []

        for package, expected_version in required_packages.items():
            try:
                if package == 'seatable-api':
                    import seatable_api as pkg
                else:
                    pkg = importlib.import_module(package.replace('-', '_'))

                if hasattr(pkg, '__version__'):
                    installed_version = pkg.__version__
                    print(f"✅ {package} {installed_version}")
                else:
                    print(f"✅ {package} (version unknown)")
            except ImportError:
                missing_packages.append(package)
                self.log_issue("Dependencies", f"Missing package: {package}")

        if missing_packages:
            print(f"❌ Missing packages: {', '.join(missing_packages)}")

    def check_env_file(self):
        """Check .env file configuration"""
        print("\n🔍 Checking environment configuration...")

        env_file = self.project_root / ".env"
        if not env_file.exists():
            self.log_issue("Environment", ".env file not found")
            return

        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()

        required_vars = {
            'ENSEMBLE_DATA_API_KEY': 'Ensemble Data API Key',
            'OPENAI_API_KEY': 'OpenAI API Key',
            'SEATABLE_API_TOKEN': 'SeaTable API Token'
        }

        for var, description in required_vars.items():
            value = os.getenv(var)
            if not value:
                self.log_issue("Environment", f"Missing {description}: {var}")
            elif value.startswith(('your_', 'test_')) or 'placeholder' in value.lower():
                self.log_issue(
                    "Environment", f"Placeholder value detected for {var}", "warning")
            else:
                print(f"✅ {description} configured")

        # Check SeaTable UUID
        seatable_uuid = os.getenv(
            "SEATABLE_BASE_UUID") or os.getenv("SEATABLE_ID")
        if not seatable_uuid:
            self.log_issue(
                "Environment", "Missing SeaTable Base UUID (SEATABLE_BASE_UUID or SEATABLE_ID)")
        else:
            print("✅ SeaTable Base UUID configured")

    def check_node_js(self):
        """Check Node.js and npm availability"""
        print("\n🔍 Checking Node.js environment...")

        try:
            node_result = subprocess.run(
                ['node', '--version'], capture_output=True, text=True, timeout=10)
            if node_result.returncode == 0:
                node_version = node_result.stdout.strip()
                print(f"✅ Node.js {node_version}")
            else:
                self.log_issue("Node.js", "Node.js not found or not working")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_issue("Node.js", "Node.js not installed or not in PATH")

        try:
            npm_result = subprocess.run(
                ['npm', '--version'], capture_output=True, text=True, timeout=10)
            if npm_result.returncode == 0:
                npm_version = npm_result.stdout.strip()
                print(f"✅ npm {npm_version}")
            else:
                self.log_issue("Node.js", "npm not found or not working")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_issue("Node.js", "npm not installed or not in PATH")

    def check_frontend_dependencies(self):
        """Check if frontend dependencies are installed"""
        print("\n🔍 Checking frontend dependencies...")

        frontend_dir = self.project_root / "frontend"
        package_json = frontend_dir / "package.json"
        node_modules = frontend_dir / "node_modules"

        if not package_json.exists():
            self.log_issue(
                "Frontend", "package.json not found in frontend directory")
            return

        if not node_modules.exists():
            self.log_issue(
                "Frontend", "node_modules not found - run 'npm install' in frontend directory")
            return

        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                package_data = json.load(f)

            dependencies = package_data.get('dependencies', {})
            dev_dependencies = package_data.get('devDependencies', {})

            print(
                f"✅ Frontend dependencies configured ({len(dependencies)} deps, {len(dev_dependencies)} dev deps)")

        except json.JSONDecodeError:
            self.log_issue("Frontend", "Invalid package.json format")
        except Exception as e:
            self.log_issue("Frontend", f"Error reading package.json: {str(e)}")

    def check_project_structure(self):
        """Check if all required files and directories exist"""
        print("\n🔍 Checking project structure...")

        required_files = [
            'backend/main.py',
            'backend/routers/analysis.py',
            'backend/routers/trends.py',
            'backend/services/ensemble_service.py',
            'backend/services/gpt_service.py',
            'backend/services/seatable_service.py',
            'backend/models/schemas.py',
            'frontend/src/App.tsx',
            'frontend/src/index.tsx',
            'requirements.txt',
            'setup_seatable.py'
        ]

        required_dirs = [
            'backend',
            'backend/routers',
            'backend/services',
            'backend/models',
            'backend/prompts',
            'frontend',
            'frontend/src',
            'frontend/public'
        ]

        for file_path in required_files:
            if not (self.project_root / file_path).exists():
                self.log_issue(
                    "Structure", f"Missing required file: {file_path}")

        for dir_path in required_dirs:
            if not (self.project_root / dir_path).is_dir():
                self.log_issue(
                    "Structure", f"Missing required directory: {dir_path}")

        if not self.issues:
            print("✅ Project structure is complete")

    def check_service_imports(self):
        """Check if backend services can be imported without errors"""
        print("\n🔍 Testing backend service imports...")

        services = [
            ('backend.services.ensemble_service', 'EnsembleService'),
            ('backend.services.gpt_service', 'GPTService'),
            ('backend.services.seatable_service', 'SeaTableService')
        ]

        for module_name, class_name in services:
            try:
                module = importlib.import_module(module_name)
                service_class = getattr(module, class_name)
                print(f"✅ {class_name} can be imported")
            except ImportError as e:
                self.log_issue(
                    "Services", f"Cannot import {class_name}: {str(e)}")
            except AttributeError as e:
                self.log_issue(
                    "Services", f"Cannot find class {class_name}: {str(e)}")
            except Exception as e:
                self.log_issue(
                    "Services", f"Error importing {class_name}: {str(e)}")

    def check_api_endpoints(self):
        """Check if API endpoints are properly defined"""
        print("\n🔍 Checking API endpoints...")

        try:
            sys.path.insert(0, str(self.project_root / 'backend'))
            from main import app

            routes = []
            for route in app.routes:
                if hasattr(route, 'methods') and hasattr(route, 'path'):
                    routes.append(f"{list(route.methods)[0]} {route.path}")

            if routes:
                print(f"✅ Found {len(routes)} API routes")
                for route in routes[:5]:  # Show first 5 routes
                    print(f"   - {route}")
                if len(routes) > 5:
                    print(f"   ... and {len(routes) - 5} more")
            else:
                self.log_issue("API", "No API routes found")

        except Exception as e:
            self.log_issue("API", f"Cannot load FastAPI app: {str(e)}")

    def generate_report(self):
        """Generate final diagnostic report"""
        print("\n" + "=" * 60)
        print("📋 TRENDXL PROJECT DIAGNOSTIC REPORT")
        print("=" * 60)

        if not self.issues and not self.warnings:
            print("🎉 No issues found! Project should work correctly.")
            return

        if self.issues:
            print(f"\n🚨 CRITICAL ISSUES ({len(self.issues)}):")
            for issue in self.issues:
                print(f"   {issue}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   {warning}")

        print("\n🔧 RECOMMENDATIONS:")
        if any("Dependencies" in issue for issue in self.issues):
            print("   • Install missing Python packages: pip install -r requirements.txt")
        if any("Environment" in issue for issue in self.issues):
            print("   • Configure .env file with proper API keys")
            print(
                "   • Join SeaTable database: https://cloud.seatable.io/dtable/links/bc4b5e5624bf47b49d82")
        if any("Node.js" in issue for issue in self.issues):
            print("   • Install Node.js and npm from https://nodejs.org")
        if any("Frontend" in issue for issue in self.issues):
            print("   • Run 'npm install' in frontend directory")
        if any("Python" in issue for issue in self.issues):
            print("   • Upgrade Python to version 3.8 or higher")

    def run_diagnostics(self):
        """Run all diagnostic checks"""
        print("🌟 TrendXL Project Diagnostics")
        print("=" * 40)

        self.check_python_version()
        self.check_dependencies()
        self.check_env_file()
        self.check_node_js()
        self.check_frontend_dependencies()
        self.check_project_structure()
        self.check_service_imports()
        self.check_api_endpoints()

        self.generate_report()


def main():
    diagnostics = ProjectDiagnostics()
    diagnostics.run_diagnostics()


if __name__ == "__main__":
    main()
