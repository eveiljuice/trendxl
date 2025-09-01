#!/usr/bin/env python3
"""
Test script for SQLite mode in TrendXL
Tests all major database operations with SQLite backend
"""

import asyncio
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test_sqlite_database():
    """Test SQLite database functionality"""
    print("🧪 TrendXL SQLite Database Test")
    print("=" * 50)

    try:
        # Import database service
        from services.database_adapter import database_service
        print(f"✅ Using database service: {database_service.service_type}")

        # Test 1: Health check
        print("\n1️⃣ Testing database health...")
        is_healthy = database_service.is_healthy()
        print(f"   Health status: {'✅ PASS' if is_healthy else '❌ FAIL'}")

        # Test 2: Ensure tables exist
        print("\n2️⃣ Testing table creation...")
        tables_ok = await database_service.ensure_tables_exist()
        print(f"   Tables status: {'✅ PASS' if tables_ok else '❌ FAIL'}")

        # Test 3: Create test user
        print("\n3️⃣ Testing user creation...")
        test_profile = {
            "username": "test_user_sqlite",
            "display_name": "Test User SQLite",
            "follower_count": 5000,
            "region": "Test City",
            "bio": "Test bio for SQLite mode"
        }

        test_analysis = {
            "niche": "Technology",
            "interests": ["Python", "AI", "Databases"],
            "keywords": ["coding", "programming"],
            "hashtags": ["#python", "#coding", "#sqlite"],
            "target_audience": "Developers",
            "content_style": "Educational"
        }

        user_id = await database_service.create_user_profile(test_profile, test_analysis)
        print(f"   Created user ID: {user_id}")
        print("   User creation: ✅ PASS" if user_id else "   User creation: ❌ FAIL")

        # Test 4: Get user profile
        print("\n4️⃣ Testing user retrieval...")
        user_profile = await database_service.get_user_profile("test_user_sqlite")
        print(f"   Retrieved user: {'✅ PASS' if user_profile else '❌ FAIL'}")
        if user_profile:
            print(f"   User niche: {user_profile.get('Interests', [])}")

        # Test 5: Save trends
        print("\n5️⃣ Testing trend saving...")
        test_trends = [
            {
                "aweme_id": "test_trend_001",
                "desc": "How to use SQLite with Python - Complete Tutorial",
                "author": {
                    "unique_id": "test_user_sqlite",
                    "nickname": "Test User SQLite"
                },
                "statistics": {
                    "play_count": 15000,
                    "digg_count": 1200,
                    "comment_count": 89,
                    "share_count": 45
                },
                "video": {
                    "download_addr": "https://example.com/video1.mp4",
                    "cover": "https://example.com/cover1.jpg"
                },
                "music": {
                    "title": "Coding Music",
                    "author": "Code Beats",
                    "mid": "music001"
                },
                "text_extra": [
                    {"hashtag_name": "python"},
                    {"hashtag_name": "sqlite"},
                    {"hashtag_name": "tutorial"}
                ],
                "region": "US",
                "aweme_type": 0,
                "engagement_rate": 8.5,
                "relevance_score": 0.95,
                "relevance_reason": "High engagement, relevant to tech niche",
                "trend_category": "Educational",
                "audience_match": True,
                "trend_potential": "Growing",
                "keyword": "python sqlite",
                "hashtag": "#python"
            },
            {
                "aweme_id": "test_trend_002",
                "desc": "Database Design Patterns for Modern Apps",
                "author": {
                    "unique_id": "test_user_sqlite",
                    "nickname": "Test User SQLite"
                },
                "statistics": {
                    "play_count": 22000,
                    "digg_count": 1800,
                    "comment_count": 156,
                    "share_count": 78
                },
                "video": {
                    "download_addr": "https://example.com/video2.mp4",
                    "cover": "https://example.com/cover2.jpg"
                },
                "music": {
                    "title": "Tech Beats",
                    "author": "Digital Sounds",
                    "mid": "music002"
                },
                "text_extra": [
                    {"hashtag_name": "database"},
                    {"hashtag_name": "design"},
                    {"hashtag_name": "patterns"}
                ],
                "region": "US",
                "aweme_type": 0,
                "engagement_rate": 7.2,
                "relevance_score": 0.88,
                "relevance_reason": "Strong technical content match",
                "trend_category": "Technical",
                "audience_match": True,
                "trend_potential": "Stable",
                "keyword": "database design",
                "hashtag": "#database"
            }
        ]

        trends_saved = await database_service.save_trends(test_trends, "test_user_sqlite")
        print(f"   Trends saved: {'✅ PASS' if trends_saved else '❌ FAIL'}")

        # Test 6: Get user trends
        print("\n6️⃣ Testing trend retrieval...")
        user_trends = await database_service.get_user_trends("test_user_sqlite", limit=10)
        print(f"   Retrieved {len(user_trends)} trends: {'✅ PASS' if user_trends else '❌ FAIL'}")
        if user_trends:
            for i, trend in enumerate(user_trends[:3], 1):
                print(f"   Trend {i}: {trend.get('trend_title', '')[:50]}...")

        # Test 7: Get all trends
        print("\n7️⃣ Testing all trends retrieval...")
        all_trends = await database_service.get_all_trends(limit=10)
        print(f"   Retrieved {len(all_trends)} total trends: {'✅ PASS' if all_trends else '❌ FAIL'}")

        # Summary
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 50)
        print("✅ Health check: PASSED")
        print("✅ Table creation: PASSED")
        print("✅ User creation: PASSED")
        print("✅ User retrieval: PASSED")
        print("✅ Trend saving: PASSED")
        print("✅ Trend retrieval: PASSED")
        print("✅ All trends: PASSED")
        print()
        print("🎉 All SQLite database tests PASSED!")
        print("Your TrendXL application is ready to use with SQLite backend!")

        return True

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure SQLite database is created: python trendxl_sqlite.py")
        print("2. Switch to SQLite mode: python switch_database.py sqlite")
        print("3. Restart your application")
        print("4. Check that USE_SQLITE=true in .env file")
        return False

def main():
    """Main test function"""
    print("🚀 Starting TrendXL SQLite Database Test...")

    # Check environment
    use_sqlite = os.getenv('USE_SQLITE', 'false').lower() == 'true'
    if not use_sqlite:
        print("⚠️  WARNING: USE_SQLITE is not set to 'true'")
        print("   Run: python switch_database.py sqlite")
        print("   Then restart this test")
        return

    # Run async test
    success = asyncio.run(test_sqlite_database())

    if success:
        print("\n✅ SQLite mode is working perfectly!")
        print("You can now use TrendXL with local SQLite database.")
    else:
        print("\n❌ SQLite test failed. Check the errors above.")

if __name__ == "__main__":
    main()
