#!/usr/bin/env python3
"""
Python Compatibility Fixer for TrendXL
Helps resolve Python 3.13 compatibility issues with PyO3
"""

import sys
import subprocess
import os
from pathlib import Path


def check_python_version():
    """Check Python version and provide recommendations"""
    version = sys.version_info
    print(f"🔍 Detected Python {version.major}.{version.minor}.{version.micro}")

    if version.major == 3 and version.minor == 13:
        print("⚠️  Python 3.13 detected - some packages may need special handling")
        return "python313"
    elif version >= (3, 8):
        print("✅ Compatible Python version detected")
        return "compatible"
    else:
        print(f"❌ Python {version.major}.{version.minor} is not supported")
        print("Please upgrade to Python 3.8 or higher")
        return "incompatible"


def install_with_compatibility_mode():
    """Install packages with PyO3 compatibility mode"""
    print("🔧 Installing with PyO3 compatibility mode...")

    env = os.environ.copy()
    env['PYO3_USE_ABI3_FORWARD_COMPATIBILITY'] = '1'

    try:
        cmd = [sys.executable, "-m", "pip",
               "install", "-r", "requirements.txt"]
        subprocess.run(cmd, check=True, env=env)
        print("✅ Dependencies installed successfully with compatibility mode")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False


def suggest_alternatives():
    """Suggest alternative solutions"""
    print("\n💡 Alternative Solutions:")
    print("1. Use Docker (recommended):")
    print("   python run.py docker")
    print()
    print("2. Downgrade to Python 3.12:")
    print("   - Download Python 3.12 from python.org")
    print("   - Create new virtual environment with Python 3.12")
    print("   - Run installation again")
    print()
    print("3. Use pyenv to manage multiple Python versions:")
    print("   pyenv install 3.12")
    print("   pyenv local 3.12")
    print()
    print("4. Use conda environment:")
    print("   conda create -n trendxl python=3.12")
    print("   conda activate trendxl")


def main():
    """Main compatibility fixer"""
    print("🛠️  TrendXL Python Compatibility Fixer")
    print("=" * 40)

    python_status = check_python_version()

    if python_status == "incompatible":
        print("\n❌ Cannot proceed with incompatible Python version")
        sys.exit(1)

    elif python_status == "python313":
        print("\n🔧 Python 3.13 detected - attempting compatibility installation...")

        if install_with_compatibility_mode():
            print("\n✅ Installation completed successfully!")
            print("You can now run the application with:")
            print("  python run.py dev")
        else:
            print("\n❌ Installation failed despite compatibility mode")
            suggest_alternatives()
            sys.exit(1)

    else:
        print("\n✅ Python version is fully compatible")
        print("Proceeding with normal installation...")

        try:
            cmd = [sys.executable, "-m", "pip",
                   "install", "-r", "requirements.txt"]
            subprocess.run(cmd, check=True)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation failed: {e}")
            sys.exit(1)

    print("\n🎉 Ready to run TrendXL!")
    print("Next steps:")
    print("1. Configure your .env file")
    print("2. Run: python run.py dev")


if __name__ == "__main__":
    main()
