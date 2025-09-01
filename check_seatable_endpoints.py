#!/usr/bin/env python3
"""
Script to discover current SeaTable API endpoints
"""

import requests
import json
from urllib.parse import urljoin

BASE_URL = "https://cloud.seatable.io"


def test_endpoint(endpoint, headers=None, method="GET", data=None):
    """Test an endpoint and return detailed response info"""
    url = urljoin(BASE_URL, endpoint.lstrip('/'))
    print(f"\n🔍 Testing: {method} {url}")

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(
                url, headers=headers, json=data, timeout=10)

        print(f"   Status: {response.status_code}")

        # Try to parse JSON
        try:
            json_data = response.json()
            print(f"   Response type: JSON")
            print(
                f"   Keys: {list(json_data.keys()) if isinstance(json_data, dict) else 'Array/List'}")
            if isinstance(json_data, dict) and len(str(json_data)) < 500:
                print(f"   Content: {json_data}")
        except:
            print(f"   Response type: HTML/Text")
            print(f"   Content length: {len(response.text)} chars")
            # Show first 200 chars
            print(f"   Preview: {response.text[:200]}...")

        return {
            'status': response.status_code,
            'url': url,
            'method': method,
            'success': response.status_code == 200,
            'json': response.headers.get('content-type', '').startswith('application/json')
        }

    except Exception as e:
        print(f"   Error: {str(e)}")
        return {
            'status': None,
            'url': url,
            'method': method,
            'success': False,
            'error': str(e)
        }


def main():
    print("🔍 SeaTable API Endpoint Discovery")
    print("=" * 50)
    print(f"Base URL: {BASE_URL}")

    # Test basic endpoints without auth
    print("\n📋 TESTING PUBLIC ENDPOINTS:")

    public_endpoints = [
        "/",
        "/api/v2.1/",
        "/api/v2/",
        "/api/v1/",
        "/dtable-server/api/v1/",
    ]

    for endpoint in public_endpoints:
        result = test_endpoint(endpoint)

    # Test with auth headers (using dummy token to see auth behavior)
    print("\n🔐 TESTING WITH AUTH HEADERS:")

    auth_headers = {
        "Authorization": "Token dummy_token_for_testing",
        "Content-Type": "application/json"
    }

    auth_endpoints = [
        "/api/v2.1/workspace/",
        "/api/v2.1/dtables/",
        "/dtable-server/api/v1/dtables/",
    ]

    for endpoint in auth_endpoints:
        result = test_endpoint(endpoint, headers=auth_headers)

    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print("Based on the responses above, SeaTable appears to use different API endpoints.")
    print("The correct endpoints seem to be under /api/v2.1/ rather than the old /dtable-server/api/v1/")

    print("\n🔧 RECOMMENDATIONS:")
    print("1. Update all SeaTable API calls to use /api/v2.1/ endpoints")
    print("2. Verify your API token is valid")
    print("3. Confirm the base UUID exists and you have access to it")
    print("4. Check SeaTable's official API documentation for current endpoints")


if __name__ == "__main__":
    main()
