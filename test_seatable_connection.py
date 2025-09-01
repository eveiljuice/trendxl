#!/usr/bin/env python3
"""
SeaTable Connection Test Script
Tests all possible connection endpoints and identifies the issue
"""

import requests
import os
from dotenv import load_dotenv
import json
from urllib.parse import urljoin

# Load environment variables
load_dotenv()


class SeaTableTester:
    def __init__(self):
        self.base_url = os.getenv(
            "SEATABLE_BASE_URL", "https://cloud.seatable.io")
        self.api_token = os.getenv("SEATABLE_API_TOKEN")
        self.base_uuid = os.getenv(
            "SEATABLE_BASE_UUID") or os.getenv("SEATABLE_ID")

        self.headers = {
            "Authorization": f"Token {self.api_token}",
            "Content-Type": "application/json"
        }

        print("🔧 SeaTable Connection Test")
        print("=" * 50)
        print(f"Base URL: {self.base_url}")
        print(f"API Token: {self.api_token[:10]}...")
        print(f"Base UUID: {self.base_uuid}")
        print()

    def test_basic_connectivity(self):
        """Test basic internet connectivity and SeaTable availability"""
        print("1️⃣ Testing basic connectivity...")

        try:
            # Test basic HTTPS connectivity
            response = requests.get(self.base_url, timeout=10)
            print(f"✅ Base URL accessible: {response.status_code}")

            # Test API endpoint availability
            api_url = f"{self.base_url}/api/v2.1/"
            response = requests.get(api_url, timeout=10)
            print(f"✅ API endpoint accessible: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Connectivity issue: {str(e)}")
            return False

        return True

    def test_authentication(self):
        """Test API token authentication"""
        print("\n2️⃣ Testing authentication...")

        # Test workspace access
        workspace_url = f"{self.base_url}/api/v2.1/workspace/"
        try:
            response = requests.get(
                workspace_url, headers=self.headers, timeout=15)
            print(f"✅ Workspace access: {response.status_code}")

            if response.status_code == 200:
                workspace_data = response.json()
                print(
                    f"   📊 Found {len(workspace_data.get('table_list', []))} bases")

                # Check if our base exists in workspace
                base_found = any(base.get(
                    'id') == self.base_uuid for base in workspace_data.get('table_list', []))
                if base_found:
                    print("   ✅ Target base found in workspace")
                else:
                    print("   ⚠️  Target base NOT found in workspace")
                    print(
                        f"   Available bases: {[base.get('id') for base in workspace_data.get('table_list', [])]}")

            elif response.status_code == 401:
                print("   ❌ Authentication failed (401 Unauthorized)")
                return False
            elif response.status_code == 403:
                print("   ❌ Access forbidden (403 Forbidden)")
                return False
            else:
                print(f"   ⚠️  Unexpected status: {response.status_code}")
                print(f"   Response: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Workspace access failed: {str(e)}")
            return False

        return True

    def test_base_access(self):
        """Test direct base access using different endpoints"""
        print("\n3️⃣ Testing base access...")

        # Try different endpoint patterns
        endpoints = [
            # Old API pattern (v1)
            f"{self.base_url}/dtable-server/api/v1/dtables/{self.base_uuid}/",
            # New API pattern (v2.1)
            f"{self.base_url}/api/v2.1/dtables/{self.base_uuid}/",
            # Alternative patterns
            f"{self.base_url}/dtable-server/dtables/{self.base_uuid}/",
            f"{self.base_url}/api/v2.1/dtables/{self.base_uuid}/metadata/",
        ]

        for endpoint in endpoints:
            try:
                print(f"   Testing: {endpoint}")
                response = requests.get(
                    endpoint, headers=self.headers, timeout=15)

                if response.status_code == 200:
                    print(f"   ✅ SUCCESS: {response.status_code}")
                    try:
                        data = response.json()
                        if isinstance(data, dict):
                            keys = list(data.keys())[:5]  # Show first 5 keys
                            print(f"   📊 Response keys: {keys}")
                    except:
                        print(f"   📄 Response: {response.text[:200]}...")
                    return True

                elif response.status_code == 404:
                    print(f"   ❌ NOT FOUND: {response.status_code}")
                elif response.status_code == 401:
                    print(f"   ❌ UNAUTHORIZED: {response.status_code}")
                elif response.status_code == 403:
                    print(f"   ❌ FORBIDDEN: {response.status_code}")
                else:
                    print(
                        f"   ⚠️  STATUS: {response.status_code} - {response.text[:100]}")

            except requests.exceptions.RequestException as e:
                print(f"   ❌ ERROR: {str(e)}")

        return False

    def test_tables_access(self):
        """Test tables access"""
        print("\n4️⃣ Testing tables access...")

        # Try different table endpoint patterns
        table_endpoints = [
            f"{self.base_url}/dtable-server/api/v1/dtables/{self.base_uuid}/tables/",
            f"{self.base_url}/api/v2.1/dtables/{self.base_uuid}/tables/",
        ]

        for endpoint in table_endpoints:
            try:
                print(f"   Testing: {endpoint}")
                response = requests.get(
                    endpoint, headers=self.headers, timeout=15)

                if response.status_code == 200:
                    print(f"   ✅ SUCCESS: {response.status_code}")
                    try:
                        data = response.json()
                        tables = data.get('tables', [])
                        print(f"   📊 Found {len(tables)} tables")
                        for table in tables[:3]:  # Show first 3 tables
                            print(f"      - {table.get('name', 'Unknown')}")
                    except:
                        print(f"   📄 Response: {response.text[:200]}...")
                    return True

                elif response.status_code == 404:
                    print(f"   ❌ NOT FOUND: {response.status_code}")
                else:
                    print(f"   ⚠️  STATUS: {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"   ❌ ERROR: {str(e)}")

        return False

    def test_official_documentation_endpoints(self):
        """Test endpoints based on official SeaTable documentation"""
        print("\n5️⃣ Testing official documentation endpoints...")

        # According to SeaTable API docs, these should be the correct endpoints
        official_endpoints = [
            {
                "name": "List bases",
                "url": f"{self.base_url}/api/v2.1/dtables/",
                "method": "GET"
            },
            {
                "name": "Get base metadata",
                "url": f"{self.base_url}/api/v2.1/dtables/{self.base_uuid}/",
                "method": "GET"
            },
            {
                "name": "List tables",
                "url": f"{self.base_url}/api/v2.1/dtables/{self.base_uuid}/tables/",
                "method": "GET"
            },
            {
                "name": "List rows",
                "url": f"{self.base_url}/api/v2.1/dtables/{self.base_uuid}/rows/",
                "method": "GET"
            }
        ]

        success_count = 0

        for endpoint_info in official_endpoints:
            try:
                print(
                    f"   Testing {endpoint_info['name']}: {endpoint_info['url']}")
                response = requests.get(
                    endpoint_info['url'], headers=self.headers, timeout=15)

                if response.status_code == 200:
                    print(f"   ✅ SUCCESS: {response.status_code}")
                    success_count += 1
                elif response.status_code == 404:
                    print(f"   ❌ NOT FOUND: {response.status_code}")
                else:
                    print(f"   ⚠️  STATUS: {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"   ❌ ERROR: {str(e)}")

        print(
            f"\n   📊 Official endpoints success rate: {success_count}/{len(official_endpoints)}")
        return success_count > 0

    def diagnose_issues(self):
        """Run comprehensive diagnosis"""
        print("🔍 COMPREHENSIVE SEATABLE DIAGNOSIS")
        print("=" * 50)

        # Run all tests
        connectivity_ok = self.test_basic_connectivity()
        auth_ok = self.test_authentication()
        base_ok = self.test_base_access()
        tables_ok = self.test_tables_access()
        official_ok = self.test_official_documentation_endpoints()

        # Generate diagnosis
        print("\n" + "=" * 50)
        print("📋 DIAGNOSIS RESULTS")
        print("=" * 50)

        issues = []

        if not connectivity_ok:
            issues.append(
                "🌐 Network connectivity issue - cannot reach SeaTable servers")

        if not auth_ok:
            issues.append(
                "🔐 Authentication issue - API token is invalid or expired")

        if not base_ok:
            issues.append(
                "🏠 Base access issue - cannot access the specified base")

        if not tables_ok:
            issues.append(
                "📊 Tables access issue - cannot retrieve table information")

        if not official_ok:
            issues.append(
                "📚 API compatibility issue - endpoints don't match official documentation")

        if issues:
            print("🚨 IDENTIFIED ISSUES:")
            for i, issue in enumerate(issues, 1):
                print(f"   {i}. {issue}")

            print("\n🔧 RECOMMENDED SOLUTIONS:")

            if "Network connectivity" in str(issues):
                print("   • Check your internet connection")
                print("   • Verify firewall/proxy settings")
                print("   • Try accessing https://cloud.seatable.io in browser")

            if "Authentication" in str(issues):
                print("   • Verify SEATABLE_API_TOKEN in .env file")
                print("   • Regenerate API token in SeaTable account settings")
                print("   • Ensure token has proper permissions")

            if "Base access" in str(issues):
                print("   • Verify SEATABLE_BASE_UUID is correct")
                print("   • Ensure you have access to the base")
                print("   • Check if base still exists")

            if "API compatibility" in str(issues):
                print("   • Update SeaTable API endpoints in code")
                print("   • Check SeaTable API documentation for current endpoints")
                print("   • Consider using official SeaTable Python SDK")

        else:
            print("🎉 All tests passed! SeaTable connection should work correctly.")

        return len(issues) == 0


def main():
    try:
        tester = SeaTableTester()
        success = tester.diagnose_issues()

        if not success:
            print("\n❌ SeaTable connection has issues that need to be resolved.")
            return 1
        else:
            print("\n✅ SeaTable connection is working correctly!")
            return 0

    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
