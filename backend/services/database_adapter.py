"""
SQLite Database Service for TrendXL
SQLite-only database service implementation
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import SQLite service
try:
    from .sqlite_service import SQLiteService
    SQLITE_AVAILABLE = True
except ImportError:
    SQLITE_AVAILABLE = False
    print("❌ SQLite service not available")


class DatabaseService:
    """
    SQLite-only database service for TrendXL
    """

    def __init__(self):
        self._service = None

        if not SQLITE_AVAILABLE:
            raise ImportError("SQLite service not available")
        print("🔄 Using SQLite database")
        db_path = os.getenv('SQLITE_DB_PATH', 'trendxl.db')
        self._service = SQLiteService(db_path=db_path)

    def __getattr__(self, name):
        """Delegate all method calls to the actual service"""
        if hasattr(self._service, name):
            return getattr(self._service, name)
        else:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'")

    @property
    def service_type(self):
        """Return current service type"""
        return "SQLite"

    @property
    def is_sqlite(self):
        """Check if using SQLite"""
        return True

    def get_user_profile_sync(self, username: str) -> Optional[Dict[str, Any]]:
        """Synchronous passthrough for internal fallbacks"""
        if hasattr(self._service, 'get_user_profile_sync'):
            return self._service.get_user_profile_sync(username)
        else:
            print("get_user_profile_sync not implemented")
            return None


# Create singleton instance
database_service = DatabaseService()
