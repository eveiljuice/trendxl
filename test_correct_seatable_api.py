#!/usr/bin/env python3
"""
Test SeaTable API with correct endpoints using real credentials
"""

import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()


class SeaTableAPITester:
    def __init__(self):
        self.base_url = "https://cloud.seatable.io"
        self.api_token = os.getenv("SEATABLE_API_TOKEN")
        self.base_uuid = os.getenv("SEATABLE_BASE_UUID")

        self.headers = {
            "Authorization": f"Token {self.api_token}",
            "Content-Type": "application/json"
        }

        print("🔧 SeaTable API v2.1 Tester")
        print("=" * 50)
        print(f"Base URL: {self.base_url}")
        print(
            f"API Token: {self.api_token[:10] if self.api_token else 'None'}...")
        print(f"Base UUID: {self.base_uuid}")
        print()

    def test_list_bases(self):
        """Test listing all bases (dtables)"""
        print("1️⃣ Testing: List all bases")

        url = f"{self.base_url}/api/v2.1/dtables/"
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                bases = response.json()
                print(f"   ✅ Found {len(bases)} bases")

                # Look for our base
                our_base = None
                for base in bases:
                    if isinstance(base, dict) and base.get('id') == self.base_uuid:
                        our_base = base
                        break

                if our_base:
                    print(
                        f"   ✅ Target base found: {our_base.get('name', 'Unknown')}")
                else:
                    print(f"   ⚠️  Target base NOT found in your account")
                    print("   Available bases:")
                    for base in bases[:5]:  # Show first 5
                        if isinstance(base, dict):
                            print(
                                f"      - {base.get('name', 'Unknown')} (ID: {base.get('id', 'Unknown')})")

                return True
            elif response.status_code == 401:
                print("   ❌ Invalid API token")
                return False
            else:
                print(f"   ❌ Unexpected status: {response.status_code}")
                print(f"   Response: {response.text}")
                return False

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return False

    def test_base_metadata(self):
        """Test getting base metadata"""
        print("\n2️⃣ Testing: Get base metadata")

        url = f"{self.base_url}/api/v2.1/dtables/{self.base_uuid}/"
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                metadata = response.json()
                print("   ✅ Base metadata retrieved")
                print(f"   📊 Keys: {list(metadata.keys())}")

                # Extract useful info
                if 'name' in metadata:
                    print(f"   📝 Base name: {metadata['name']}")
                if 'tables' in metadata:
                    tables = metadata['tables']
                    print(f"   📋 Tables: {len(tables)}")
                    for table in tables[:3]:  # Show first 3 tables
                        print(f"      - {table.get('name', 'Unknown')}")

                return True
            elif response.status_code == 404:
                print("   ❌ Base not found or no access")
                return False
            elif response.status_code == 401:
                print("   ❌ Invalid API token")
                return False
            else:
                print(f"   ❌ Unexpected status: {response.status_code}")
                return False

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return False

    def test_list_tables(self):
        """Test listing tables in the base"""
        print("\n3️⃣ Testing: List tables")

        url = f"{self.base_url}/api/v2.1/dtables/{self.base_uuid}/tables/"
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                tables_data = response.json()
                tables = tables_data.get('tables', [])
                print(f"   ✅ Found {len(tables)} tables")

                for table in tables:
                    print(
                        f"      - {table.get('name', 'Unknown')} (ID: {table.get('_id', 'Unknown')})")

                return True
            elif response.status_code == 404:
                print("   ❌ Base not found or no access")
                return False
            else:
                print(f"   ❌ Unexpected status: {response.status_code}")
                return False

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return False

    def test_list_rows(self, table_name="Users"):
        """Test listing rows from a table"""
        print(f"\n4️⃣ Testing: List rows from '{table_name}' table")

        # First get table ID
        tables_url = f"{self.base_url}/api/v2.1/dtables/{self.base_uuid}/tables/"
        try:
            response = requests.get(
                tables_url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                print(f"   ❌ Cannot get tables: {response.status_code}")
                return False

            tables_data = response.json()
            tables = tables_data.get('tables', [])

            table_id = None
            for table in tables:
                if table.get('name') == table_name:
                    table_id = table.get('_id')
                    break

            if not table_id:
                print(f"   ⚠️  Table '{table_name}' not found")
                return False

            # Now get rows
            rows_url = f"{self.base_url}/api/v2.1/dtables/{self.base_uuid}/tables/{table_id}/rows/"
            response = requests.get(rows_url, headers=self.headers, timeout=15)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                rows_data = response.json()
                rows = rows_data.get('rows', [])
                print(f"   ✅ Found {len(rows)} rows in '{table_name}'")

                if rows:
                    print("   📊 Sample row keys:")
                    if isinstance(rows[0], dict):
                        print(f"      {list(rows[0].keys())}")

                return True
            else:
                print(f"   ❌ Cannot get rows: {response.status_code}")
                return False

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all tests"""
        print("🔍 COMPREHENSIVE SEATABLE API v2.1 TEST")
        print("=" * 50)

        if not self.api_token:
            print("❌ SEATABLE_API_TOKEN not found in environment")
            return False

        if not self.base_uuid:
            print("❌ SEATABLE_BASE_UUID not found in environment")
            return False

        # Run tests
        tests = [
            ("List bases", self.test_list_bases),
            ("Base metadata", self.test_base_metadata),
            ("List tables", self.test_list_tables),
            ("List rows", lambda: self.test_list_rows("Users")),
        ]

        results = []
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ {test_name} failed with error: {str(e)}")
                results.append((test_name, False))

        # Summary
        print("\n" + "=" * 50)
        print("📋 TEST RESULTS SUMMARY")
        print("=" * 50)

        successful_tests = sum(1 for _, result in results if result)
        total_tests = len(results)

        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {status} {test_name}")

        print(f"\n📊 Overall: {successful_tests}/{total_tests} tests passed")

        if successful_tests == total_tests:
            print("🎉 All tests passed! SeaTable API v2.1 is working correctly.")
            return True
        else:
            print("⚠️  Some tests failed. Check the details above.")

            # Provide specific guidance
            failed_tests = [name for name, result in results if not result]
            if "List bases" in failed_tests:
                print("\n🔧 TROUBLESHOOTING:")
                print("   • Check if your API token is valid")
                print("   • Ensure you have access to SeaTable bases")
            elif "Base metadata" in failed_tests or "List tables" in failed_tests:
                print("\n🔧 TROUBLESHOOTING:")
                print("   • Verify SEATABLE_BASE_UUID is correct")
                print("   • Make sure you have access to the specific base")
                print("   • Check if the base still exists")

            return False


def main():
    tester = SeaTableAPITester()
    success = tester.run_comprehensive_test()

    if success:
        print("\n✅ SeaTable API v2.1 is working correctly!")
        print("You can now update your code to use the new endpoints.")
        return 0
    else:
        print("\n❌ SeaTable API tests failed.")
        return 1


if __name__ == "__main__":
    exit(main())
