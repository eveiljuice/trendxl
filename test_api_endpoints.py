#!/usr/bin/env python3
"""
Test TrendXL API Endpoints
"""

import requests
import json


def test_api_endpoints():
    """Test all TrendXL API endpoints"""

    print("🚀 Testing TrendXL API Endpoints")
    print("=" * 50)

    base_url = "http://localhost:8000"

    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health check: PASS")
            print(f"   Status: {health_data.get('status', 'Unknown')}")
            services = health_data.get('services', {})
            for service, status in services.items():
                status_icon = "✅" if status else "❌"
                print(
                    f"   {status_icon} {service}: {'PASS' if status else 'FAIL'}")
        else:
            print(f"❌ Health check: FAIL ({response.status_code})")
    except Exception as e:
        print(f"❌ Health check: ERROR - {e}")

    # Test 2: Profile Analysis (mock test)
    print("\n2. Testing Profile Analysis Endpoint...")
    try:
        test_payload = {
            "tiktok_url": "https://www.tiktok.com/@zachking"
        }
        response = requests.post(
            f"{base_url}/api/v1/analyze-profile",
            json=test_payload,
            timeout=30
        )
        print(f"✅ Profile analysis: Status {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("   Profile analysis successful!")
                user_profile = result.get('user_profile', {})
                analysis = result.get('profile_analysis', {})
                print(f"   Username: @{user_profile.get('username', 'N/A')}")
                print(f"   Niche: {analysis.get('niche', 'N/A')}")
            else:
                print(f"   Error: {result.get('message', 'Unknown error')}")
        else:
            print(f"   Response: {response.text[:200]}...")
    except requests.exceptions.Timeout:
        print("⏳ Profile analysis: TIMEOUT (expected for full analysis)")
    except Exception as e:
        print(f"❌ Profile analysis: ERROR - {e}")

    # Test 3: Refresh Trends (mock test)
    print("\n3. Testing Refresh Trends Endpoint...")
    try:
        test_payload = {
            "username": "testuser",
            "max_results": 3
        }
        response = requests.post(
            f"{base_url}/api/v1/refresh-trends",
            json=test_payload,
            timeout=30
        )
        print(f"✅ Refresh trends: Status {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   Found {result.get('total_count', 0)} trends")
            else:
                print(f"   Error: {result.get('message', 'Unknown error')}")
        else:
            print(f"   Response: {response.text[:200]}...")
    except requests.exceptions.Timeout:
        print("⏳ Refresh trends: TIMEOUT (expected for trend analysis)")
    except Exception as e:
        print(f"❌ Refresh trends: ERROR - {e}")

    # Test 4: API Documentation
    print("\n4. Testing API Documentation...")
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✅ API Documentation: Available")
            print("   Visit: http://localhost:8000/docs")
        else:
            print(f"❌ API Documentation: FAIL ({response.status_code})")
    except Exception as e:
        print(f"❌ API Documentation: ERROR - {e}")

    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")
    print("\n📋 Next Steps:")
    print("1. Open browser: http://localhost:3000")
    print("2. Enter TikTok URL: https://www.tiktok.com/@zachking")
    print("3. Click 'Analyze Profile'")
    print("4. Wait for AI analysis to complete")
    print("5. Click 'Refresh Trends' to see personalized recommendations")

    print("\n🔧 Troubleshooting:")
    print("- If proxy errors persist, restart both servers")
    print("- Check browser console for detailed error messages")
    print("- Verify all API keys are configured in .env file")


if __name__ == "__main__":
    test_api_endpoints()
