#!/usr/bin/env python3
"""
Test TrendXL Proxy Connection
"""

import requests
import time


def test_proxy_connection():
    """Test the proxy connection between frontend and backend"""

    print("🧪 Testing TrendXL Proxy Connection")
    print("=" * 40)

    # Test 1: Backend direct access
    print("\n1. Testing Backend Direct Access...")
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check: PASS")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Backend health check: FAIL ({response.status_code})")
    except Exception as e:
        print(f"❌ Backend health check: FAIL - {e}")

    # Test 2: Frontend access
    print("\n2. Testing Frontend Access...")
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend access: PASS")
        else:
            print(f"❌ Frontend access: FAIL ({response.status_code})")
    except Exception as e:
        print(f"❌ Frontend access: FAIL - {e}")

    # Test 3: API through proxy (simulate frontend request)
    print("\n3. Testing API through Proxy...")
    try:
        # This simulates what happens when frontend makes a request
        response = requests.post(
            "http://localhost:3000/api/v1/analyze-profile",
            json={"tiktok_url": "https://www.tiktok.com/@test"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"✅ Proxy API test: Status {response.status_code}")
        if response.status_code == 200:
            print("   Proxy working correctly!")
        else:
            print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Proxy API test: FAIL - {e}")

    print("\n" + "=" * 40)
    print("🌐 Access URLs:")
    print("   Frontend: http://localhost:3000")
    print("   Backend:  http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")


if __name__ == "__main__":
    test_proxy_connection()
