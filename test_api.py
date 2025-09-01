#!/usr/bin/env python3
"""
Тестирование API endpoints TrendXL с SQLite
"""

import requests
import json


def test_api():
    """Тестирование основных API endpoints"""
    print('🧪 Тестирование API endpoints TrendXL...')
    print('=' * 50)

    # 1. Health check
    print('\n1️⃣ Health Check:')
    try:
        response = requests.get('http://localhost:8000/api/health', timeout=10)
        if response.status_code == 200:
            health = response.json()
            print('   ✅ Status:', health['status'])
            print('   📊 Services:')
            for service, status in health['services'].items():
                status_icon = '✅' if status else '❌'
                print(f'      {status_icon} {service}: {status}')
        else:
            print('   ❌ Failed:', response.status_code)
    except Exception as e:
        print('   ❌ Error:', str(e))

    # 2. Get all trends
    print('\n2️⃣ Getting all trends:')
    try:
        response = requests.get(
            'http://localhost:8000/api/v1/trends?limit=5', timeout=10)
        if response.status_code == 200:
            trends_data = response.json()
            print('   ✅ Found', trends_data['total_count'], 'trends')
            if trends_data['trends']:
                trend = trends_data['trends'][0]
                print('   📈 Sample trend keys:', list(trend.keys()))
                print('   👤 Author:', trend['author']['nickname'])
                print('   📊 Views:', trend['statistics']['play_count'])
                print('   🎯 Relevance:', trend.get('relevance_score', 'N/A'))
        else:
            print('   ❌ Failed:', response.status_code)
    except Exception as e:
        print('   ❌ Error:', str(e))

    # 3. Try to get a user profile
    print('\n3️⃣ Getting user profile:')
    try:
        response = requests.get(
            'http://localhost:8000/api/v1/profile/testuser', timeout=10)
        if response.status_code == 200:
            user_data = response.json()
            print('   ✅ User found:', user_data['user_profile']['username'])
            print('   🎯 Niche:', user_data['profile_analysis']['niche'])
            print('   📊 Followers:',
                  user_data['user_profile']['follower_count'])
        elif response.status_code == 404:
            print('   ℹ️  No users found (this is normal for fresh database)')
        else:
            print('   ❌ Failed:', response.status_code)
    except Exception as e:
        print('   ❌ Error:', str(e))

    print('\n' + '=' * 50)
    print('🎉 API тестирование завершено!')
    print('\n📋 Доступные endpoints:')
    print('   GET  /api/health - Health check')
    print('   POST /api/v1/analyze-profile - Analyze TikTok profile')
    print('   GET  /api/v1/profile/{username} - Get user profile')
    print('   POST /api/v1/refresh-trends - Refresh trends')
    print('   GET  /api/v1/trends/{username} - Get user trends')
    print('   GET  /api/v1/trends - Get all trends')


if __name__ == "__main__":
    test_api()
