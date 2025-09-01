"""
Trends API Routes
Handles trend discovery and retrieval operations
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
import logging

from models.schemas import (
    RefreshTrendsRequest,
    TrendsResponse,
    TrendItem,
    ErrorResponse,
    VideoStatistics,
    VideoInfo,
    MusicInfo,
    AuthorInfo,
    ProfileAnalysis
)
from services.ensemble_service import EnsembleService
from services.gpt_service import GPTService
from services.database_adapter import database_service

logger = logging.getLogger(__name__)
router = APIRouter()

# Service instances will be initialized in route handlers


@router.post("/refresh-trends", response_model=TrendsResponse)
async def refresh_trends(request: RefreshTrendsRequest):
    """
    Refresh trends for a specific user based on their profile analysis

    This endpoint:
    1. Gets user profile and analysis from database
    2. Searches for trends using keywords/hashtags from profile analysis
    3. Filters and ranks trends using GPT based on relevance
    4. Saves filtered trends to database
    5. Returns top relevant trends
    """
    try:
        # Initialize services
        ensemble_service = EnsembleService()
        gpt_service = GPTService()

        logger.info(f"Refreshing trends for user: {request.username}")

        # Step 1: Get user profile and analysis only if previously saved from real API flow
        user_data = await database_service.get_user_profile(request.username)
        if not user_data:
            raise HTTPException(
                status_code=404, detail=f"User profile not found for @{request.username}")

        # Extract profile analysis data
        profile_analysis = ProfileAnalysis(
            niche=user_data.get("Niche", ""),
            interests=user_data.get("Interests", []),
            keywords=user_data.get("Keywords", []),
            hashtags=user_data.get("Hashtags", []),
            target_audience=user_data.get("Target_Audience", ""),
            content_style=user_data.get("Content_Style", ""),
            region_focus=user_data.get("Region_Focus", "")
        )

        logger.info(
            f"Profile analysis - Niche: {profile_analysis.niche}, Keywords: {profile_analysis.keywords}")

        # Step 2: Search for trends using hashtags and keywords (all live from Ensemble)
        all_trends = []

        # Search by hashtags (if available)
        if profile_analysis.hashtags:
            hashtag_trends = await ensemble_service.search_hashtag_trends(
                hashtags=profile_analysis.hashtags[:5],  # Top 5 hashtags
                max_results=25
            )
            all_trends.extend(hashtag_trends)
            logger.info(f"Found {len(hashtag_trends)} hashtag trends")

        # Search by keywords (if available)
        if profile_analysis.keywords:
            keyword_trends = await ensemble_service.search_keyword_trends(
                keywords=profile_analysis.keywords[:5],  # Top 5 keywords
                period="180",  # Last 6 months
                max_results=25
            )
            all_trends.extend(keyword_trends)
            logger.info(f"Found {len(keyword_trends)} keyword trends")

        # Remove duplicates based on aweme_id
        seen_ids = set()
        unique_trends = []
        for trend in all_trends:
            if trend["aweme_id"] not in seen_ids:
                seen_ids.add(trend["aweme_id"])
                unique_trends.append(trend)

        logger.info(f"Total unique trends found: {len(unique_trends)}")

        if not unique_trends:
            return TrendsResponse(
                success=True,
                trends=[],
                total_count=0,
                message=f"No trends found for @{request.username}. Try analyzing the profile again."
            )

        # Step 3: Analyze sentiment and audience (prompt.md requirements)
        try:
            trends_with_sentiment = await gpt_service.analyze_sentiment_and_audience(unique_trends)
            logger.info(
                f"Added sentiment and audience analysis to {len(trends_with_sentiment)} trends")
        except Exception as sentiment_error:
            logger.error(f"Sentiment analysis failed: {str(sentiment_error)}")
            trends_with_sentiment = unique_trends  # Continue without sentiment analysis

        # Step 4: Filter and rank trends using GPT (no mocks)
        try:
            filtered_trends = await gpt_service.filter_and_rank_trends(
                trends=trends_with_sentiment,
                profile_analysis=profile_analysis,
                max_results=request.max_results
            )
            logger.info(
                f"GPT filtered trends to {len(filtered_trends)} relevant items")
        except Exception as filter_error:
            logger.error(f"GPT trend filtering failed: {str(filter_error)}")
            # Fallback: use top trends by engagement rate
            sorted_trends = sorted(trends_with_sentiment,
                                   key=lambda x: x.get('engagement_rate', 0),
                                   reverse=True)
            filtered_trends = sorted_trends[:request.max_results or 10]
            logger.info(
                f"Using fallback filtering - returning top {len(filtered_trends)} trends by engagement")

        # Step 4: Save filtered trends to database
        save_success = await database_service.save_trends(filtered_trends, request.username)
        if save_success:
            logger.info(
                f"Successfully saved {len(filtered_trends)} trends to database")

        # Step 5: Convert to response format
        trend_items = []
        for trend in filtered_trends:
            # Create TikTok URL
            author_username = trend.get("author", {}).get("unique_id", "")
            aweme_id = trend.get("aweme_id", "")
            tiktok_url = f"https://www.tiktok.com/@{author_username}/video/{aweme_id}" if author_username and aweme_id else ""

            trend_item = TrendItem(
                aweme_id=trend.get("aweme_id", ""),
                desc=trend.get("desc", ""),
                create_time=trend.get("create_time", 0),
                author=AuthorInfo(
                    unique_id=trend.get("author", {}).get("unique_id", ""),
                    nickname=trend.get("author", {}).get("nickname", ""),
                    follower_count=trend.get(
                        "author", {}).get("follower_count", 0),
                    avatar_thumb=trend.get(
                        "author", {}).get("avatar_thumb", "")
                ),
                statistics=VideoStatistics(
                    digg_count=trend.get(
                        "statistics", {}).get("digg_count", 0),
                    comment_count=trend.get(
                        "statistics", {}).get("comment_count", 0),
                    play_count=trend.get(
                        "statistics", {}).get("play_count", 0),
                    share_count=trend.get(
                        "statistics", {}).get("share_count", 0),
                    download_count=trend.get(
                        "statistics", {}).get("download_count", 0),
                    collect_count=trend.get(
                        "statistics", {}).get("collect_count", 0),
                    forward_count=trend.get(
                        "statistics", {}).get("forward_count", 0),
                    whatsapp_share_count=trend.get(
                        "statistics", {}).get("whatsapp_share_count", 0)
                ),
                video=VideoInfo(
                    duration=trend.get("video", {}).get("duration", 0),
                    height=trend.get("video", {}).get("height", 0),
                    width=trend.get("video", {}).get("width", 0),
                    cover=trend.get("video", {}).get("cover", ""),
                    download_addr=trend.get(
                        "video", {}).get("download_addr", "")
                ),
                music=MusicInfo(
                    title=trend.get("music", {}).get("title", ""),
                    author=trend.get("music", {}).get("author", ""),
                    mid=trend.get("music", {}).get("mid", "")
                ),
                text_extra=trend.get("text_extra", []),
                engagement_rate=trend.get("engagement_rate", 0.0),
                relevance_score=trend.get("relevance_score"),
                relevance_reason=trend.get("relevance_reason"),
                trend_category=trend.get("trend_category"),
                audience_match=trend.get("audience_match"),
                trend_potential=trend.get("trend_potential"),
                keyword=trend.get("keyword"),
                hashtag=trend.get("hashtag"),
                tiktok_url=tiktok_url,
                sentiment=trend.get("sentiment", "Neutral"),
                audience=trend.get("audience", "General")
            )
            trend_items.append(trend_item)

        return TrendsResponse(
            success=True,
            trends=trend_items,
            total_count=len(trend_items),
            message=f"Found {len(trend_items)} relevant trends for @{request.username}"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error refreshing trends for {request.username}: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to refresh trends: {str(e)}")


@router.get("/trends/{username}", response_model=TrendsResponse)
async def get_saved_trends(
    username: str,
    limit: int = Query(default=20, ge=1, le=100,
                       description="Maximum number of trends to return")
):
    """
    Get previously saved trends for a user from database
    """
    try:
        logger.info(f"Retrieving saved trends for user: {username}")

        # Get trends from database
        saved_trends = await database_service.get_user_trends(username, limit=limit)

        if not saved_trends:
            return TrendsResponse(
                success=True,
                trends=[],
                total_count=0,
                message=f"No saved trends found for @{username}"
            )

        # Convert to response format
        trend_items = []
        for trend in saved_trends:
            trend_item = TrendItem(
                aweme_id=trend.get("Aweme_ID", ""),
                desc=trend.get("Description", ""),
                create_time=0,  # Convert from ISO string if needed
                author=AuthorInfo(
                    unique_id=trend.get("Author_Username", ""),
                    nickname=trend.get("Author_Nickname", ""),
                    follower_count=trend.get("Author_Followers", 0),
                    avatar_thumb=""
                ),
                statistics=VideoStatistics(
                    digg_count=trend.get("Likes", 0),
                    comment_count=trend.get("Comments", 0),
                    play_count=trend.get("Views", 0),
                    share_count=trend.get("Shares", 0),
                    download_count=trend.get("Downloads", 0),
                    collect_count=trend.get("Favourited", 0),
                    whatsapp_share_count=trend.get("Whatsapp_Shares", 0)
                ),
                video=VideoInfo(
                    duration=trend.get("Duration", 0),
                    height=0,
                    width=0,
                    cover=trend.get("Video_Cover", ""),
                    download_addr=trend.get("Video_URL", "")
                ),
                music=MusicInfo(
                    title=trend.get("Music_Title", ""),
                    author=trend.get("Music_Author", ""),
                    mid=trend.get("Music_ID", "")
                ),
                text_extra=[],  # Hashtags are stored separately
                engagement_rate=trend.get("Engagement_Rate", 0.0),
                relevance_score=trend.get("Relevance_Score"),
                relevance_reason=trend.get("Relevance_Reason"),
                trend_category=trend.get("Trend_Category"),
                audience_match=trend.get("Audience_Match"),
                trend_potential=trend.get("Trend_Potential"),
                keyword=trend.get("Keyword"),
                hashtag=trend.get("Hashtag"),
                tiktok_url=trend.get("TikTok_URL", ""),
                sentiment=trend.get("Sentiment", "Neutral"),
                audience=trend.get("Audience", "General")
            )
            trend_items.append(trend_item)

        return TrendsResponse(
            success=True,
            trends=trend_items,
            total_count=len(trend_items),
            message=f"Retrieved {len(trend_items)} saved trends for @{username}"
        )

    except Exception as e:
        logger.error(f"Error retrieving trends for {username}: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve trends: {str(e)}")


@router.get("/trends", response_model=TrendsResponse)
async def get_all_recent_trends(
    limit: int = Query(default=50, ge=1, le=200,
                       description="Maximum number of trends to return")
):
    """
    Get all recent trends across all users
    """
    try:
        logger.info(f"Retrieving all recent trends (limit: {limit})")

        # Get all recent trends from database
        all_trends = await database_service.get_all_trends(limit=limit)

        if not all_trends:
            return TrendsResponse(
                success=True,
                trends=[],
                total_count=0,
                message="No recent trends found"
            )

        # Convert to response format (similar to get_saved_trends)
        trend_items = []
        for trend in all_trends:
            trend_item = TrendItem(
                aweme_id=trend.get("Aweme_ID", ""),
                desc=trend.get("Description", ""),
                create_time=0,
                author=AuthorInfo(
                    unique_id=trend.get("Author_Username", ""),
                    nickname=trend.get("Author_Nickname", ""),
                    follower_count=trend.get("Author_Followers", 0),
                    avatar_thumb=""
                ),
                statistics=VideoStatistics(
                    digg_count=trend.get("Likes", 0),
                    comment_count=trend.get("Comments", 0),
                    play_count=trend.get("Views", 0),
                    share_count=trend.get("Shares", 0),
                    download_count=trend.get("Downloads", 0),
                    collect_count=trend.get("Favourited", 0),
                    whatsapp_share_count=trend.get("Whatsapp_Shares", 0)
                ),
                video=VideoInfo(
                    duration=trend.get("Duration", 0),
                    height=0,
                    width=0,
                    cover=trend.get("Video_Cover", ""),
                    download_addr=trend.get("Video_URL", "")
                ),
                music=MusicInfo(
                    title=trend.get("Music_Title", ""),
                    author=trend.get("Music_Author", ""),
                    mid=trend.get("Music_ID", "")
                ),
                text_extra=[],
                engagement_rate=trend.get("Engagement_Rate", 0.0),
                relevance_score=trend.get("Relevance_Score"),
                relevance_reason=trend.get("Relevance_Reason"),
                trend_category=trend.get("Trend_Category"),
                audience_match=trend.get("Audience_Match"),
                trend_potential=trend.get("Trend_Potential"),
                tiktok_url=trend.get("TikTok_URL", ""),
                sentiment=trend.get("Sentiment", "Neutral"),
                audience=trend.get("Audience", "General")
            )
            trend_items.append(trend_item)

        return TrendsResponse(
            success=True,
            trends=trend_items,
            total_count=len(trend_items),
            message=f"Retrieved {len(trend_items)} recent trends"
        )

    except Exception as e:
        logger.error(f"Error retrieving all trends: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve trends: {str(e)}")
