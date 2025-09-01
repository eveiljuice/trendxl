"""
Analytics API Routes
Handles advanced analytics and metrics operations
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional
import logging

from models.schemas import ErrorResponse
from services.ensemble_service import EnsembleService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/profile-metrics/{username}")
async def get_profile_metrics(
    username: str,
    posts_depth: int = Query(default=5, ge=1, le=10, description="Number of recent posts to analyze (1-10)")
):
    """
    Get comprehensive profile metrics including activity patterns,
    engagement trends, and performance analytics
    """
    try:
        ensemble_service = EnsembleService()
        logger.info(f"Getting advanced metrics for @{username}")
        
        metrics_data = await ensemble_service.get_advanced_user_metrics(username, posts_depth)
        
        if not metrics_data.get("metrics"):
            raise HTTPException(
                status_code=404, 
                detail=f"No metrics data available for @{username}"
            )
        
        return {
            "success": True,
            "username": username,
            "metrics": metrics_data["metrics"],
            "posts_analyzed": len(metrics_data.get("posts", [])),
            "analysis_timestamp": metrics_data.get("analysis_timestamp"),
            "message": f"Successfully calculated metrics for @{username}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting profile metrics for {username}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to calculate profile metrics: {str(e)}"
        )


@router.get("/trending-hashtags")
async def get_trending_hashtags(
    keywords: str = Query(..., description="Comma-separated list of keywords"),
    limit: int = Query(default=20, ge=1, le=50, description="Number of hashtags to return (1-50)")
):
    """
    Get trending hashtags related to specific keywords for trend discovery
    """
    try:
        ensemble_service = EnsembleService()
        keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
        
        if not keyword_list:
            raise HTTPException(status_code=400, detail="At least one keyword is required")
        
        logger.info(f"Getting trending hashtags for keywords: {keyword_list}")
        
        trending_hashtags = await ensemble_service.get_trending_hashtags(keyword_list, limit)
        
        return {
            "success": True,
            "keywords": keyword_list,
            "hashtags": trending_hashtags,
            "total_found": len(trending_hashtags),
            "message": f"Found {len(trending_hashtags)} trending hashtags"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting trending hashtags: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to get trending hashtags: {str(e)}"
        )


@router.get("/trend-analytics")
async def get_trend_analytics(
    username: str,
    max_trends: int = Query(default=50, ge=10, le=100, description="Maximum number of trends to analyze")
):
    """
    Get comprehensive trend analytics for a user including performance metrics,
    engagement patterns, and growth opportunities
    """
    try:
        from services.gpt_service import GPTService
        from services.database_adapter import database_service
        
        ensemble_service = EnsembleService()
        gpt_service = GPTService()
        
        logger.info(f"Getting trend analytics for @{username}")
        
        # Get user profile and analysis from database
        user_data = await database_service.get_user_profile(username)
        if not user_data:
            raise HTTPException(
                status_code=404, 
                detail=f"User profile not found for @{username}. Please analyze profile first."
            )
        
        # Extract profile analysis
        from models.schemas import ProfileAnalysis
        analysis_data = {
            "niche": user_data.get("Niche", ""),
            "interests": user_data.get("Interests", []),
            "keywords": user_data.get("Keywords", []),
            "hashtags": user_data.get("Hashtags", []),
            "target_audience": user_data.get("Target_Audience", ""),
            "content_style": user_data.get("Content_Style", ""),
            "region_focus": user_data.get("Region_Focus", "")
        }
        profile_analysis = ProfileAnalysis(**analysis_data)
        
        # Get trending content based on user's interests
        all_trends = []
        
        # Search by keywords
        for keyword in profile_analysis.keywords[:5]:  # Limit API calls
            keyword_trends = await ensemble_service.search_keyword_trends(
                [keyword], period="30", max_results=20
            )
            all_trends.extend(keyword_trends)
        
        # Search by hashtags  
        for hashtag in profile_analysis.hashtags[:5]:  # Limit API calls
            hashtag_trends = await ensemble_service.search_hashtag_trends(
                [hashtag], max_results=20
            )
            all_trends.extend(hashtag_trends)
        
        # Remove duplicates
        seen_ids = set()
        unique_trends = []
        for trend in all_trends:
            if trend.get("aweme_id") not in seen_ids:
                seen_ids.add(trend.get("aweme_id"))
                unique_trends.append(trend)
        
        # Limit to max_trends
        unique_trends = unique_trends[:max_trends]
        
        # Filter and rank trends using GPT
        if unique_trends:
            filtered_trends = await gpt_service.filter_and_rank_trends(
                unique_trends, profile_analysis, max_results=min(max_trends, 20)
            )
        else:
            filtered_trends = []
        
        # Calculate analytics from trends
        analytics = calculate_trend_analytics(filtered_trends)
        
        # Generate recommendations
        recommendations = generate_recommendations(analytics, profile_analysis)
        
        return {
            "success": True,
            "username": username,
            "niche": profile_analysis.niche,
            "analytics": analytics,
            "trends": filtered_trends,
            "recommendations": recommendations,
            "total_trends_analyzed": len(unique_trends),
            "relevant_trends_found": len(filtered_trends),
            "message": f"Generated trend analytics for @{username}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting trend analytics for {username}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to get trend analytics: {str(e)}"
        )


def calculate_trend_analytics(trends: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate comprehensive analytics from trend data"""
    if not trends:
        return {
            "overview": {
                "total_trends": 0,
                "total_views": 0,
                "total_engagement": 0,
                "avg_engagement_rate": 0
            },
            "performance": {
                "viral_potential": 0,
                "growth_opportunity": 0,
                "competition_level": 0
            },
            "categories": {},
            "time_analysis": {}
        }
    
    # Basic metrics
    total_views = sum(trend.get("statistics", {}).get("play_count", 0) for trend in trends)
    total_likes = sum(trend.get("statistics", {}).get("digg_count", 0) for trend in trends)
    total_engagement = sum(trend.get("engagement_rate", 0) for trend in trends)
    avg_engagement_rate = total_engagement / len(trends)
    
    # Performance analysis
    high_relevance_trends = len([t for t in trends if (t.get("relevance_score", 0) >= 80)])
    viral_potential = sum(1 for t in trends if t.get("statistics", {}).get("play_count", 0) > 1000000)
    growing_trends = len([t for t in trends if t.get("trend_potential") == "growing"])
    
    # Category analysis
    categories = {}
    for trend in trends:
        category = trend.get("trend_category", "Uncategorized")
        if category not in categories:
            categories[category] = {
                "count": 0,
                "avg_engagement": 0,
                "total_views": 0,
                "high_relevance": 0
            }
        
        categories[category]["count"] += 1
        categories[category]["avg_engagement"] += trend.get("engagement_rate", 0)
        categories[category]["total_views"] += trend.get("statistics", {}).get("play_count", 0)
        if trend.get("relevance_score", 0) >= 80:
            categories[category]["high_relevance"] += 1
    
    # Calculate category averages
    for category, data in categories.items():
        if data["count"] > 0:
            data["avg_engagement"] = data["avg_engagement"] / data["count"]
    
    # Time analysis (simplified)
    import time
    current_time = int(time.time())
    recent_trends = len([t for t in trends if (current_time - t.get("create_time", 0)) < (7 * 24 * 3600)])
    
    return {
        "overview": {
            "total_trends": len(trends),
            "total_views": total_views,
            "total_likes": total_likes,
            "avg_engagement_rate": avg_engagement_rate
        },
        "performance": {
            "high_relevance_trends": high_relevance_trends,
            "viral_potential": viral_potential,
            "growth_opportunity": growing_trends,
            "recent_trends": recent_trends
        },
        "categories": categories,
        "engagement_distribution": {
            "high": len([t for t in trends if t.get("engagement_rate", 0) > 8]),
            "medium": len([t for t in trends if 3 <= t.get("engagement_rate", 0) <= 8]),
            "low": len([t for t in trends if t.get("engagement_rate", 0) < 3])
        }
    }


def generate_recommendations(analytics: Dict[str, Any], profile_analysis) -> List[Dict[str, str]]:
    """Generate actionable recommendations based on analytics"""
    recommendations = []
    
    # Performance-based recommendations
    if analytics["performance"]["high_relevance_trends"] > 3:
        recommendations.append({
            "type": "opportunity",
            "title": "High Relevance Content Opportunity",
            "message": f"Found {analytics['performance']['high_relevance_trends']} highly relevant trends. Focus on creating content in these areas for maximum impact."
        })
    
    if analytics["performance"]["viral_potential"] > 2:
        recommendations.append({
            "type": "viral",
            "title": "Viral Content Potential",
            "message": f"{analytics['performance']['viral_potential']} trends show viral potential. Study their characteristics and adapt for your niche."
        })
    
    # Category-based recommendations
    top_category = None
    if analytics["categories"]:
        top_category = max(analytics["categories"].items(), key=lambda x: x[1]["avg_engagement"])
        recommendations.append({
            "type": "category",
            "title": "Top Performing Category",
            "message": f"'{top_category[0]}' shows highest engagement ({top_category[1]['avg_engagement']:.1f}%). Consider focusing more content here."
        })
    
    # Growth recommendations
    if analytics["performance"]["growth_opportunity"] > 0:
        recommendations.append({
            "type": "growth",
            "title": "Growth Trending Content",
            "message": f"{analytics['performance']['growth_opportunity']} trends are currently growing. Act fast to capitalize on these opportunities."
        })
    
    # Engagement recommendations
    engagement_dist = analytics["engagement_distribution"]
    if engagement_dist["low"] > engagement_dist["high"]:
        recommendations.append({
            "type": "improvement",
            "title": "Engagement Optimization Needed",
            "message": "Many relevant trends have low engagement. Look for gaps in content quality or timing that you can improve upon."
        })
    
    return recommendations
