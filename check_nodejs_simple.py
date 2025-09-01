#!/usr/bin/env python3
"""
Simple Node.js Diagnostic for TrendXL
"""

import subprocess
import os
import sys

def check_node():
    """Check if node is available"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Node.js found: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    print("❌ Node.js not found in PATH")
    return False

def check_npm():
    """Check if npm is available"""
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ npm found: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    print("❌ npm not found in PATH")
    return False

def find_npm_paths():
    """Find npm in common locations"""
    print("\n🔍 Searching for npm...")

    paths_to_check = [
        r"C:\Program Files\nodejs\npm.cmd",
        r"C:\Program Files (x86)\nodejs\npm.cmd",
    ]

    for path in paths_to_check:
        if os.path.exists(path):
            print(f"📍 Found npm at: {path}")
            try:
                result = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"   ✅ Version: {result.stdout.strip()}")
                    print(f"   💡 Try using: {path} install")
                    return True
            except:
                pass

    print("❌ npm not found in common locations")
    return False

def main():
    print("🩺 Node.js Quick Check")
    print("=" * 25)

    node_ok = check_node()
    npm_ok = check_npm()

    if node_ok and npm_ok:
        print("\n🎉 Node.js and npm are working!")
        print("Try: python run.py install")
        return

    print("\n🔧 Trying to find npm...")
    found_npm = find_npm_paths()

    print("\n💡 Solutions:")
    print("1. Restart your terminal/command prompt")
    print("2. If using Windows, try running as Administrator")
    print("3. Check if antivirus is blocking npm")
    print("4. Reinstall Node.js from https://nodejs.org")

    if found_npm:
        print("5. npm found but not in PATH - use the full path shown above")

    print("\n🐳 Alternative: Use Docker")
    print("   python run.py docker")

if __name__ == "__main__":
    main()
