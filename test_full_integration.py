#!/usr/bin/env python3
"""
Full Integration Test for TrendXL
Tests all components: API services, database, GPT analysis
"""

import asyncio
import sys
import os
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))


async def test_full_integration():
    """Test complete TrendXL integration"""
    print("🚀 Starting TrendXL Full Integration Test")
    print("=" * 50)

    try:
        # Test 1: Import all modules
        print("\n📦 Testing imports...")
        from services.ensemble_service import EnsembleService
        from services.gpt_service import GPTService
        from services.database_adapter import database_service
        from routers.analysis import router as analysis_router
        from routers.trends import router as trends_router
        from models.schemas import UserProfile, ProfileAnalysis
        print("✅ All modules imported successfully")

        # Test 2: Database health
        print("\n🗄️  Testing database...")
        db_healthy = database_service.is_healthy()
        print(f"✅ Database health: {db_healthy}")
        print(f"   Database type: {database_service.service_type}")

        # Test 3: Ensemble API service
        print("\n🔗 Testing Ensemble API...")
        ensemble_service = EnsembleService()
        ensemble_healthy = ensemble_service.is_healthy()
        print(f"✅ Ensemble API health: {ensemble_healthy}")

        # Test 4: GPT service
        print("\n🤖 Testing GPT service...")
        gpt_service = GPTService()
        gpt_healthy = gpt_service.is_healthy()
        print(f"✅ GPT service health: {gpt_healthy}")

        # Test 5: Full profile analysis workflow
        print("\n🔍 Testing profile analysis workflow...")
        test_username = "zachking"  # Popular TikTok creator

        # Get profile
        profile_data = await ensemble_service.get_user_profile(test_username)
        print(f"✅ Retrieved profile: @{profile_data['username']}")

        # Get posts for analysis
        user_posts = await ensemble_service.get_user_posts(test_username, depth=2)
        print(f"✅ Retrieved {len(user_posts)} posts for analysis")

        # Analyze with GPT
        profile_analysis = await gpt_service.analyze_profile(profile_data, user_posts)
        print(f"✅ GPT analysis completed:")
        print(f"   - Niche: {profile_analysis.niche}")
        print(
            f"   - Interests: {', '.join(profile_analysis.interests[:3])}...")
        print(f"   - Keywords: {', '.join(profile_analysis.keywords[:3])}...")

        # Test 6: Trend discovery
        print("\n📈 Testing trend discovery...")

        trends = []
        # Search trends by keywords
        if profile_analysis.keywords:
            trends = await ensemble_service.search_keyword_trends(
                keywords=profile_analysis.keywords[:2],
                period="180",
                max_results=5
            )
            print(f"✅ Found {len(trends)} trends by keywords")

            # Filter trends with GPT
            filtered_trends = await gpt_service.filter_and_rank_trends(
                trends=trends,
                profile_analysis=profile_analysis,
                max_results=3
            )
            print(f"✅ Filtered to {len(filtered_trends)} relevant trends")

            # Show top trend
            if filtered_trends:
                top_trend = filtered_trends[0]
                print(f"   📊 Top trend: {top_trend['desc'][:50]}...")
                print(f"   👤 Author: @{top_trend['author']['unique_id']}")
                print(f"   📊 Engagement: {top_trend['engagement_rate']:.1f}%")
                if top_trend.get('relevance_score'):
                    print(f"   🎯 Relevance: {top_trend['relevance_score']}%")

        # Test 7: Database operations
        print("\n💾 Testing database operations...")

        # Create user profile
        user_id = await database_service.create_user_profile(profile_data, profile_analysis.dict())
        print(f"✅ Created user profile in database: {user_id}")

        # Retrieve user profile
        retrieved_profile = await database_service.get_user_profile(test_username)
        if retrieved_profile:
            print("✅ Retrieved user profile from database")
            print(f"   - Niche: {retrieved_profile.get('Niche', 'N/A')}")
        else:
            print("⚠️  Could not retrieve user profile from database")

        # Test 8: Summary
        print("\n🎉 Integration Test Summary")
        print("=" * 30)

        services_status = {
            "Database": db_healthy,
            "Ensemble API": ensemble_healthy,
            "GPT Service": gpt_healthy,
            "Profile Analysis": True,
            "Trend Discovery": len(trends) > 0,
            "Database Operations": retrieved_profile is not None
        }

        all_passed = all(services_status.values())

        for service, status in services_status.items():
            status_icon = "✅" if status else "❌"
            print(f"{status_icon} {service}: {'PASS' if status else 'FAIL'}")

        print("\n" + "=" * 50)
        if all_passed:
            print("🎉 ALL TESTS PASSED! TrendXL MVP is ready for production!")
        else:
            print("⚠️  Some tests failed. Check the logs above for details.")

        return all_passed

    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_full_integration())
    sys.exit(0 if success else 1)
