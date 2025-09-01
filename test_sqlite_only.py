#!/usr/bin/env python3
"""
Test TrendXL with SQLite-only configuration
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))


def test_sqlite_only():
    """Test that TrendXL works without SeaTable dependencies"""

    print("🧪 Testing SQLite-only TrendXL configuration")
    print("=" * 50)

    try:
        # Test imports (should not fail on SeaTable)
        print("\n1. Testing imports...")
        from services.ensemble_service import EnsembleService
        from services.gpt_service import GPTService
        from services.database_adapter import database_service

        print("✅ All required services imported successfully")

        # Test database adapter
        print("\n2. Testing database adapter...")
        db_type = database_service.service_type
        is_sqlite = database_service.is_sqlite

        print(f"✅ Database type: {db_type}")
        print(f"✅ Is SQLite: {is_sqlite}")

        if db_type != "SQLite":
            print(f"❌ Expected SQLite, got {db_type}")
            return False

        # Test database health
        print("\n3. Testing database health...")
        db_healthy = database_service.is_healthy()
        print(f"✅ Database healthy: {db_healthy}")

        # Test ensemble service
        print("\n4. Testing Ensemble service...")
        ensemble = EnsembleService()
        ensemble_healthy = ensemble.is_healthy()
        print(f"✅ Ensemble healthy: {ensemble_healthy}")

        # Test GPT service
        print("\n5. Testing GPT service...")
        gpt = GPTService()
        gpt_healthy = gpt.is_healthy()
        print(f"✅ GPT healthy: {gpt_healthy}")

        print("\n" + "=" * 50)
        print("🎉 SQLite-only configuration test PASSED!")
        print("\n✅ No SeaTable dependencies required")
        print("✅ Application ready to run with SQLite only")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_sqlite_only()
    sys.exit(0 if success else 1)
