#!/usr/bin/env python3
"""
Node.js Diagnostic Script for TrendXL
Helps identify Node.js and npm installation issues
"""

import subprocess
import os
import sys
from pathlib import Path


def check_node_installation():
    """Check Node.js installation status"""
    print("🔍 Checking Node.js installation...")

    node_found = False
    npm_found = False
    node_version = None
    npm_version = None

    # Check node
    try:
        result = subprocess.run(["node", "--version"],
                                capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            node_version = result.stdout.strip()
            node_found = True
            print(f"✅ Node.js found: {node_version}")
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        print("❌ Node.js not found in PATH")

    # Check npm
    try:
        result = subprocess.run(["npm", "--version"],
                                capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            npm_version = result.stdout.strip()
            npm_found = True
            print(f"✅ npm found: {npm_version}")
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        print("❌ npm not found in PATH")

    return node_found, npm_found, node_version, npm_version


def find_nodejs_paths():
    """Find potential Node.js installation paths"""
    print("\n🔍 Searching for Node.js installations...")

    found_paths = []

    # Common installation paths
    search_paths = [
        # Windows paths
        r"C:\Program Files\nodejs",
        r"C:\Program Files (x86)\nodejs",
        r"C:\Users\{}\AppData\Roaming\npm".format(
            os.environ.get("USERNAME", "")),
        r"C:\Users\{}\AppData\Local\Programs\Node.js".format(
            os.environ.get("USERNAME", "")),

        # macOS/Linux paths
        "/usr/local/bin",
        "/usr/bin",
        "/opt/homebrew/bin",  # macOS Homebrew
        "/usr/local/lib/node_modules/npm/bin",
        "/usr/lib/node_modules/npm/bin",

        # User-specific paths
        os.path.expanduser("~/.npm"),
        os.path.expanduser("~/.nvm"),
        os.path.expanduser("~/node_modules/.bin"),
    ]

    for path in search_paths:
        if os.path.exists(path):
            # Check for node executable
            node_path = os.path.join(path, "node")
            npm_path = os.path.join(path, "npm")

            if not os.path.exists(node_path):
                node_path = os.path.join(path, "node.exe")  # Windows
            if not os.path.exists(npm_path):
                npm_path = os.path.join(path, "npm.cmd")   # Windows

            if os.path.exists(node_path) or os.path.exists(npm_path):
                found_paths.append(path)
                print(f"📍 Found Node.js related path: {path}")

                # Test executables
                if os.path.exists(node_path):
                    try:
                        result = subprocess.run(
                            [node_path, "--version"], capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            print(
                                f"   ✅ node executable: {result.stdout.strip()}")
                    except:
                        pass

                if os.path.exists(npm_path):
                    try:
                        result = subprocess.run(
                            [npm_path, "--version"], capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            print(
                                f"   ✅ npm executable: {result.stdout.strip()}")
                    except:
                        pass

    if not found_paths:
        print("❌ No Node.js installations found in common locations")

    return found_paths


def check_path_variables():
    """Check PATH environment variables"""
    print("\n🔍 Checking PATH environment...")

    path_var = os.environ.get("PATH", "")
    path_dirs = path_var.split(os.pathsep) if path_var else []

    node_in_path = False
    npm_in_path = False

    print("Current PATH directories containing 'node' or 'npm':")
    for dir_path in path_dirs:
        if 'node' in dir_path.lower() or 'npm' in dir_path.lower():
            print(f"📁 {dir_path}")

            # Check if actually contains node/npm
            node_path = os.path.join(dir_path, "node")
            npm_path = os.path.join(dir_path, "npm")

            if not os.path.exists(node_path):
                node_path = os.path.join(dir_path, "node.exe")
            if not os.path.exists(npm_path):
                npm_path = os.path.join(dir_path, "npm.cmd")

            if os.path.exists(node_path):
                node_in_path = True
                print(f"   ✅ Contains node executable")
            if os.path.exists(npm_path):
                npm_in_path = True
                print(f"   ✅ Contains npm executable")

    if not node_in_path or not npm_in_path:
        print("\n⚠️  Node.js/npm not found in PATH")
        print("This might be the issue!")

    return node_in_path, npm_in_path


def suggest_solutions():
    """Provide solutions based on findings"""
    print("\n💡 Solutions:")

    print("\n1. Restart your terminal/command prompt")
    print("   Sometimes PATH updates after restart")

    print("\n2. Check Node.js installation")
    print("   Visit: https://nodejs.org/en/download/")
    print("   Download and install the LTS version")

    print("\n3. Verify installation")
    print("   node --version")
    print("   npm --version")

    print("\n4. If using Windows:")
    print("   - Try running as Administrator")
    print("   - Check if antivirus blocks npm")
    print("   - Reinstall Node.js")

    print("\n5. Alternative: Use Docker")
    print("   python run.py docker")


def main():
    """Main diagnostic function"""
    print("🩺 Node.js Diagnostic Tool for TrendXL")
    print("=" * 40)

    # Check basic installation
    node_found, npm_found, node_ver, npm_ver = check_node_installation()

    # If both found, everything should work
    if node_found and npm_found:
        print("\n🎉 Node.js is properly installed!")
        print("The issue might be elsewhere. Try:")
        print("1. Restart your terminal")
        print("2. Run: python run.py install")
        print("3. If still failing, run: python run.py diagnose")
        return

    # If not found, search for installations
    found_paths = find_nodejs_paths()

    # Check PATH
    node_in_path, npm_in_path = check_path_variables()

    # Provide solutions
    suggest_solutions()

    print("
          📞 For more help: "    print(" - Check QUICK_START.md for troubleshooting")
    print("- Run: python run.py diagnose")
    print("- Visit: https://nodejs.org/en/download/")


if __name__ == "__main__":
    main()
