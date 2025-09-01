"""
Profile Analysis API Routes
Handles TikTok profile analysis operations
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging

from models.schemas import (
    TikTokProfileRequest,
    AnalysisResponse,
    ErrorResponse,
    UserProfile,
    ProfileAnalysis
)
from services.ensemble_service import EnsembleService
from services.gpt_service import GPTService
from services.database_adapter import database_service

logger = logging.getLogger(__name__)
router = APIRouter()

# Service instances will be initialized in route handlers


@router.post("/analyze-profile", response_model=AnalysisResponse)
async def analyze_tiktok_profile(request: TikTokProfileRequest):
    """
    Analyze TikTok profile and create user profile with niche adaptation

    This endpoint:
    1. Extracts username from TikTok URL
    2. Fetches user profile data from TikTok
    3. Fetches recent user posts
    4. Uses GPT to analyze profile and determine interests/keywords
    5. Saves user profile and analysis to database (SQLite or SeaTable)
    """
    try:
        # Initialize services
        ensemble_service = EnsembleService()
        gpt_service = GPTService()

        logger.info(f"Starting profile analysis for URL: {request.tiktok_url}")

        # Step 1: Extract username from URL
        username = ensemble_service.extract_username_from_url(
            request.tiktok_url)
        logger.info(f"Extracted username: {username}")

        # Step 2: Get user profile STRICTLY from TikTok (no mocks/fallbacks)
        profile_data = await ensemble_service.get_user_profile_strict(username)

        # Validate that API returned a real username
        if not profile_data.get("username"):
            logger.error(
                f"Ensemble API returned empty username for @{username}")
            raise HTTPException(
                status_code=502, detail="Incomplete user data from TikTok API (missing username)")
        logger.info(f"Retrieved profile data for {username}")

        # Step 3: Get recent user posts for content analysis
        # Get 30 recent posts
        user_posts = await ensemble_service.get_user_posts(username, depth=3)
        logger.info(f"Retrieved {len(user_posts)} posts for analysis")

        # Step 4: Use GPT to analyze profile and determine niche/interests
        try:
            profile_analysis = await gpt_service.analyze_profile(profile_data, user_posts)
            logger.info(
                f"Completed GPT analysis - Niche: {profile_analysis.niche}")
        except Exception as gpt_error:
            logger.error(
                f"GPT analysis failed for @{username}: {str(gpt_error)}")
            # Use fallback analysis if GPT fails
            profile_analysis = gpt_service._fallback_profile_analysis(
                profile_data)
            logger.info(
                f"Using fallback analysis - Niche: {profile_analysis.niche}")

        # Step 5: Save user profile and analysis to database
        user_id = await database_service.create_user_profile(
            profile_data,
            profile_analysis.dict()
        )
        logger.info(f"Saved user profile to database with ID: {user_id}")

        # Prepare response
        user_profile = UserProfile(**profile_data)

        return AnalysisResponse(
            success=True,
            user_profile=user_profile,
            profile_analysis=profile_analysis,
            message=f"Successfully analyzed profile for @{username}. Detected niche: {profile_analysis.niche}"
        )

    except ValueError as e:
        logger.error(f"Validation error in profile analysis: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in profile analysis: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to analyze profile: {str(e)}")


@router.get("/profile/{username}", response_model=AnalysisResponse)
async def get_user_profile(username: str):
    """
    Get existing user profile and analysis from database
    """
    try:
        logger.info(f"Retrieving profile for username: {username}")

        # Get user profile from database
        user_data = await database_service.get_user_profile(username)

        if not user_data:
            raise HTTPException(
                status_code=404, detail=f"User profile not found for @{username}")

        # Extract profile data (SeaTable-compatible format)
        profile_data = {
            "username": user_data.get("Username", ""),
            "display_name": user_data.get("Display_Name", ""),
            "follower_count": user_data.get("Follower_Count", 0),
            "following_count": user_data.get("Following_Count", 0),
            "video_count": user_data.get("Video_Count", 0),
            "likes_count": user_data.get("Likes_Count", 0),
            "bio": user_data.get("Bio", ""),
            "avatar_url": user_data.get("Avatar_URL", ""),
            "verified": user_data.get("Verified", False),
            "sec_uid": user_data.get("Sec_UID", ""),
            "uid": user_data.get("UID", ""),
            "region": user_data.get("Region", ""),
            "language": user_data.get("Language", "")
        }

        # Extract analysis data (SeaTable-compatible format)
        analysis_data = {
            "niche": user_data.get("Niche", ""),
            "interests": user_data.get("Interests", []),
            "keywords": user_data.get("Keywords", []),
            "hashtags": user_data.get("Hashtags", []),
            "target_audience": user_data.get("Target_Audience", ""),
            "content_style": user_data.get("Content_Style", ""),
            "region_focus": user_data.get("Region_Focus", "")
        }

        user_profile = UserProfile(**profile_data)
        profile_analysis = ProfileAnalysis(**analysis_data)

        return AnalysisResponse(
            success=True,
            user_profile=user_profile,
            profile_analysis=profile_analysis,
            message=f"Retrieved profile for @{username}"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving profile for {username}: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve profile: {str(e)}")


@router.post("/reanalyze-profile/{username}")
async def reanalyze_profile(username: str):
    """
    Re-analyze existing user profile with fresh data
    """
    try:
        # Initialize services
        ensemble_service = EnsembleService()
        gpt_service = GPTService()

        logger.info(f"Re-analyzing profile for username: {username}")

        # Get fresh profile data from TikTok
        profile_data = await ensemble_service.get_user_profile(username)

        # Get fresh user posts
        user_posts = await ensemble_service.get_user_posts(username, depth=3)

        # Re-analyze with GPT
        profile_analysis = await gpt_service.analyze_profile(profile_data, user_posts)

        # Update in database
        user_id = await database_service.create_user_profile(
            profile_data,
            profile_analysis.dict()
        )

        user_profile = UserProfile(**profile_data)

        return AnalysisResponse(
            success=True,
            user_profile=user_profile,
            profile_analysis=profile_analysis,
            message=f"Successfully re-analyzed profile for @{username}"
        )

    except Exception as e:
        logger.error(f"Error re-analyzing profile for {username}: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to re-analyze profile: {str(e)}")
