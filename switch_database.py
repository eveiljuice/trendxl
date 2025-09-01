#!/usr/bin/env python3
"""
Database Mode Switcher
Easily switch between SQLite (testing) and SeaTable (production) modes
"""

import os
import shutil
from pathlib import Path

def switch_to_sqlite():
    """Switch to SQLite mode"""
    print("🔄 Switching to SQLite mode (local testing)...")

    env_file = Path(".env")
    sqlite_env = Path(".env.sqlite")

    if sqlite_env.exists():
        shutil.copy(sqlite_env, env_file)
        print("✅ Copied .env.sqlite to .env")
    else:
        print("❌ .env.sqlite not found. Run setup_sqlite.py first")

    print("✅ Switched to SQLite mode")
    print("💡 Restart your application to use SQLite database")

def switch_to_seatable():
    """Switch to SeaTable mode"""
    print("🔄 Switching to SeaTable mode (production)...")

    env_file = Path(".env")
    original_env = Path(".env.original")

    if original_env.exists():
        shutil.copy(original_env, env_file)
        print("✅ Restored original .env")
    else:
        print("⚠️  .env.original not found")
        print("   Make sure your .env file contains SeaTable credentials")

    print("✅ Switched to SeaTable mode")
    print("💡 Restart your application to use SeaTable database")

def show_current_mode():
    """Show current database mode"""
    use_sqlite = os.getenv('USE_SQLITE', 'false').lower() == 'true'

    if use_sqlite:
        print("🔵 Current mode: SQLite (local testing)")
        print("   Database: trendxl_local.db")
    else:
        print("🔴 Current mode: SeaTable (production)")
        print("   API: https://cloud.seatable.io")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python switch_database.py sqlite    # Switch to SQLite")
        print("  python switch_database.py seatable  # Switch to SeaTable")
        print("  python switch_database.py status    # Show current mode")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "sqlite":
        switch_to_sqlite()
    elif command == "seatable":
        switch_to_seatable()
    elif command == "status":
        show_current_mode()
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)
