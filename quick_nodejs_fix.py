#!/usr/bin/env python3
"""
Quick Node.js Fix for TrendXL
Fast solution for common Node.js PATH issues
"""

import subprocess
import os
import sys


def quick_check():
    """Quick check for Node.js and npm"""
    print("🔍 Quick Node.js check...")

    node_ok = False
    npm_ok = False

    # Test node
    try:
        result = subprocess.run(["node", "--version"],
                                capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
            node_ok = True
    except:
        print("❌ Node.js not found")

    # Test npm
    try:
        result = subprocess.run(["npm", "--version"],
                                capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ npm: {result.stdout.strip()}")
            npm_ok = True
    except:
        print("❌ npm not found")

    return node_ok, npm_ok


def try_common_fixes():
    """Try common quick fixes"""
    print("\n🔧 Trying quick fixes...")

    # Fix 1: Try direct paths (Windows)
    if os.name == 'nt':
        common_paths = [
            r"C:\Program Files\nodejs\npm.cmd",
            r"C:\Program Files (x86)\nodejs\npm.cmd",
            os.path.expanduser(r"~\AppData\Roaming\npm\npm.cmd"),
        ]

        for npm_path in common_paths:
            if os.path.exists(npm_path):
                print(f"📍 Found npm at: {npm_path}")
                try:
                    result = subprocess.run(
                        [npm_path, "--version"], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        print(f"✅ npm works: {result.stdout.strip()}")
                        print(f"💡 Try using: {npm_path} install")
                        return True
                except:
                    continue

    # Fix 2: Check if we can run npm with full path
    try:
        # Try to find npm via where/which
        if os.name == 'nt':
            result = subprocess.run(
                ["where", "npm"], capture_output=True, text=True)
        else:
            result = subprocess.run(
                ["which", "npm"], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout.strip():
            npm_path = result.stdout.strip().split('\n')[0]
            print(f"📍 npm found at: {npm_path}")
            print("💡 npm exists but not in PATH")
            return True
    except:
        pass

    return False


def main():
    """Main quick fix function"""
    print("🚀 Quick Node.js Fix for TrendXL")
    print("=" * 35)

    # Quick check
    node_ok, npm_ok = quick_check()

    if node_ok and npm_ok:
        print("\n🎉 Node.js and npm are working!")
        print("Try running: python run.py install")
        return

    # Try fixes
    found_fix = try_common_fixes()

    # Provide solutions
    print("\n💡 Solutions:")

    if found_fix:
        print("1. npm found but not in PATH - use full path or restart terminal")
    else:
        print("1. Restart your terminal/command prompt")
        print("2. If using Windows, try running as Administrator")

    print("3. Run full diagnostic:")
    print("   python run.py check-node")

    print("4. Alternative - use Docker:")
    print("   python run.py docker")

    print("\n📖 For detailed help:")
    print("   Read NODEJS_TROUBLESHOOTING.md")


if __name__ == "__main__":
    main()
