#!/usr/bin/env python3
"""
TrendXL Database Switcher
Temporarily switches from SeaTable to SQLite for local testing
WITHOUT modifying original SeaTable code
"""

import os
import sys
from pathlib import Path


class DatabaseSwitcher:
    """Switcher between SeaTable and SQLite services"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "backend"
        self.services_dir = self.backend_dir / "services"

    def create_sqlite_adapter(self):
        """Create a database adapter that switches between services"""
        adapter_content = '''"""
Database Adapter for TrendXL
Automatically switches between SeaTable and SQLite based on configuration
"""

import os
from typing import Optional

# Import both services
try:
    from .seatable_service import SeaTableService
    SEATABLE_AVAILABLE = True
except ImportError:
    SEATABLE_AVAILABLE = False
    print("⚠️  SeaTable service not available")

try:
    from .sqlite_service import SQLiteService
    SQLITE_AVAILABLE = True
except ImportError:
    SQLITE_AVAILABLE = False
    print("⚠️  SQLite service not available")

class DatabaseService:
    """
    Universal database service that switches between SeaTable and SQLite
    based on USE_SQLITE environment variable
    """

    def __init__(self):
        self.use_sqlite = os.getenv('USE_SQLITE', 'false').lower() == 'true'
        self._service = None

        if self.use_sqlite:
            if not SQLITE_AVAILABLE:
                raise ImportError("SQLite service requested but not available")
            print("🔄 Using SQLite database (local testing mode)")
            self._service = SQLiteService()
        else:
            if not SEATABLE_AVAILABLE:
                raise ImportError("SeaTable service requested but not available")
            print("🔄 Using SeaTable database (production mode)")
            self._service = SeaTableService()

    def __getattr__(self, name):
        """Delegate all method calls to the actual service"""
        if hasattr(self._service, name):
            return getattr(self._service, name)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    @property
    def service_type(self):
        """Return current service type"""
        return "SQLite" if self.use_sqlite else "SeaTable"

    @property
    def is_sqlite(self):
        """Check if using SQLite"""
        return self.use_sqlite

    @property
    def is_seatable(self):
        """Check if using SeaTable"""
        return not self.use_sqlite

# Create singleton instance
database_service = DatabaseService()
'''

        adapter_file = self.services_dir / "database_adapter.py"
        with open(adapter_file, 'w', encoding='utf-8') as f:
            f.write(adapter_content)

        print(f"✅ Created database adapter: {adapter_file}")

    def update_imports_in_main_files(self):
        """Update imports in main service files to use the adapter"""

        # Files that need to be updated
        files_to_update = [
            self.backend_dir / "main.py",
            self.backend_dir / "routers" / "analysis.py",
            self.backend_dir / "routers" / "trends.py"
        ]

        for file_path in files_to_update:
            if file_path.exists():
                self._update_file_imports(file_path)

    def _update_file_imports(self, file_path):
        """Update imports in a specific file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Replace SeaTable imports with database adapter
            original_import = "from backend.services.seatable_service import SeaTableService"
            new_import = "from backend.services.database_adapter import database_service as SeaTableService"

            if original_import in content:
                content = content.replace(original_import, new_import)
                print(f"✅ Updated imports in: {file_path}")

                # Write back the updated content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            else:
                print(f"ℹ️  No SeaTable imports found in: {file_path}")

        except Exception as e:
            print(f"❌ Error updating {file_path}: {e}")

    def create_env_template(self):
        """Create environment template for SQLite switching"""
        env_content = '''
# TrendXL Environment Configuration
# Copy this file and fill in your actual API keys

# Database Mode Switcher
# Set to 'true' to use SQLite for local testing
# Set to 'false' to use SeaTable for production
USE_SQLITE=true

# Required API Keys (only needed when USE_SQLITE=false)
ENSEMBLE_DATA_API_KEY=hqtExYWR0e0CSdxz
OPENAI_API_KEY=your_openai_api_key_here
SEATABLE_API_TOKEN=2da25ba20620557122aab2d1c4872f39883918e1

# SeaTable Database Configuration
# Join the TrendXL SeaTable database: https://cloud.seatable.io/dtable/links/bc4b5e5624bf47b49d82
SEATABLE_BASE_UUID=a9d57cc5-bb91-4183-aeda-9e9954903d87

# Optional Configuration
DEBUG=true
HOST=0.0.0.0
PORT=8000
'''

        env_template = self.project_root / ".env.sqlite"
        with open(env_template, 'w', encoding='utf-8') as f:
            f.write(env_content.strip())

        print(f"✅ Created SQLite environment template: {env_template}")

    def create_switch_script(self):
        """Create a script to easily switch between database modes"""
        switch_script = '''#!/usr/bin/env python3
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
'''

        switch_file = self.project_root / "switch_database.py"
        with open(switch_file, 'w', encoding='utf-8') as f:
            f.write(switch_script)

        # Make it executable on Unix systems
        try:
            os.chmod(switch_file, 0o755)
        except:
            pass  # Ignore on Windows

        print(f"✅ Created database switcher: {switch_file}")

    def backup_original_env(self):
        """Backup original .env file"""
        env_file = self.project_root / ".env"
        backup_file = self.project_root / ".env.original"

        if env_file.exists() and not backup_file.exists():
            import shutil
            shutil.copy(env_file, backup_file)
            print(f"✅ Backed up original .env to {backup_file}")

    def run_setup(self):
        """Run complete SQLite setup"""
        print("🚀 TrendXL SQLite Setup")
        print("=" * 50)

        # Backup original environment
        self.backup_original_env()

        # Create SQLite database
        print("\n1️⃣ Creating SQLite database...")
        from trendxl_sqlite import TrendXLSQLite
        db_creator = TrendXLSQLite()
        db_creator.setup_database()

        # Create database adapter
        print("\n2️⃣ Creating database adapter...")
        self.create_sqlite_adapter()

        # Create environment template
        print("\n3️⃣ Creating environment templates...")
        self.create_env_template()

        # Create switch script
        print("\n4️⃣ Creating database switcher...")
        self.create_switch_script()

        print("\n" + "=" * 50)
        print("✅ SQLite setup completed!")
        print("\n📋 Next steps:")
        print("1. Run: python switch_database.py sqlite")
        print("2. Restart your TrendXL application")
        print("3. Test with local SQLite database")
        print("4. Switch back: python switch_database.py seatable")
        print("\n🎯 Your original SeaTable code remains untouched!")


def main():
    """Main function"""
    switcher = DatabaseSwitcher()
    switcher.run_setup()


if __name__ == "__main__":
    main()
