#!/usr/bin/env python3
"""
Quick Frontend Dependencies Installer
Installs Node.js dependencies for React frontend
"""

import subprocess
import os
from pathlib import Path

def install_frontend():
    """Install frontend dependencies"""
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    print("🔧 Installing frontend dependencies...")
    print(f"📁 Working directory: {frontend_dir}")
    
    try:
        # Check if npm is available
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        print("✅ npm found")
        
        # Install dependencies
        print("📦 Installing packages...")
        result = subprocess.run(
            ["npm", "install"], 
            cwd=frontend_dir, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Frontend dependencies installed successfully!")
            print("\n🚀 You can now run:")
            print("   python run.py dev")
            return True
        else:
            print(f"❌ npm install failed:")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js:")
        print("   Visit: https://nodejs.org/en/download/")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🌟 TrendXL Frontend Dependencies Installer")
    print("=" * 50)
    success = install_frontend()
    exit(0 if success else 1)
