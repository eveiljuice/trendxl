#!/usr/bin/env python3
"""
Simple Health Check for TrendXL Components
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))


def test_health():
    """Simple health check for all components"""
    print("🚀 TrendXL Health Check")
    print("=" * 30)

    results = {}

    # Test 1: Database
    try:
        from services.database_adapter import database_service
        results["Database"] = database_service.is_healthy()
        print(f"✅ Database: {'PASS' if results['Database'] else 'FAIL'}")
    except Exception as e:
        results["Database"] = False
        print(f"❌ Database: FAIL - {e}")

    # Test 2: Ensemble API
    try:
        from services.ensemble_service import EnsembleService
        ensemble = EnsembleService()
        results["Ensemble"] = ensemble.is_healthy()
        print(f"✅ Ensemble API: {'PASS' if results['Ensemble'] else 'FAIL'}")
    except Exception as e:
        results["Ensemble"] = False
        print(f"❌ Ensemble API: FAIL - {e}")

    # Test 3: GPT Service
    try:
        from services.gpt_service import GPTService
        gpt = GPTService()
        results["GPT"] = gpt.is_healthy()
        print(f"✅ GPT Service: {'PASS' if results['GPT'] else 'FAIL'}")
    except Exception as e:
        results["GPT"] = False
        print(f"❌ GPT Service: FAIL - {e}")

    # Summary
    print("\n" + "=" * 30)
    passed = sum(results.values())
    total = len(results)

    print(f"Results: {passed}/{total} components healthy")

    if passed == total:
        print("🎉 All components are healthy!")
        return True
    else:
        print("⚠️  Some components need attention")
        return False


if __name__ == "__main__":
    success = test_health()
    sys.exit(0 if success else 1)
