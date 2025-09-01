"""
Debug API Routes
Provides debugging endpoints for API connectivity and service health
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging
import os

from services.ensemble_service import EnsembleService
from services.gpt_service import GPTService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/test-ensemble")
async def test_ensemble_api():
    """
    Test Ensemble Data API connectivity with a known working profile
    """
    try:
        ensemble_service = EnsembleService()

        # Test with a well-known TikTok profile
        test_username = "daviddobrik"  # Known public profile

        logger.info(f"Testing Ensemble API with profile: @{test_username}")

        # Test the API call
        result = ensemble_service.client.tiktok.user_info_from_username(
            username=test_username
        )

        response_info = {
            "success": True,
            "test_username": test_username,
            "api_responded": result is not None,
            "units_charged": getattr(result, 'units_charged', 'N/A'),
            "has_data": result.data is not None if result else False,
        }

        if result and result.data:
            user_data = result.data.get("user", {})
            response_info.update({
                "has_user_field": "user" in result.data,
                "user_data_keys": list(user_data.keys()) if user_data else [],
                "unique_id": user_data.get("unique_id", ""),
                "nickname": user_data.get("nickname", ""),
                "follower_count": user_data.get("follower_count", 0),
                "has_username": bool(user_data.get("unique_id", "").strip()),
            })
        else:
            response_info["error"] = "No data returned from API"

        return response_info

    except Exception as e:
        logger.error(f"Ensemble API test failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "test_username": test_username,
            "suggestion": "Check your ENSEMBLE_DATA_API_KEY in .env file"
        }


@router.get("/test-gpt")
async def test_gpt_api():
    """
    Test OpenAI GPT API connectivity
    """
    try:
        gpt_service = GPTService()

        # Simple test call
        test_response = gpt_service.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'API test successful' in exactly 3 words."}
            ],
            max_tokens=10,
            temperature=0
        )

        return {
            "success": True,
            "response": test_response.choices[0].message.content,
            "model": test_response.model,
            "usage": {
                "prompt_tokens": test_response.usage.prompt_tokens,
                "completion_tokens": test_response.usage.completion_tokens,
                "total_tokens": test_response.usage.total_tokens
            }
        }

    except Exception as e:
        logger.error(f"GPT API test failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "suggestion": "Check your OPENAI_API_KEY in .env file"
        }


@router.get("/api-keys")
async def check_api_keys():
    """
    Check if required API keys are configured
    """
    return {
        "ensemble_data_key": {
            "configured": bool(os.getenv("ENSEMBLE_DATA_API_KEY")),
            "key_prefix": os.getenv("ENSEMBLE_DATA_API_KEY", "")[:10] + "..." if os.getenv("ENSEMBLE_DATA_API_KEY") else "Not configured"
        },
        "openai_key": {
            "configured": bool(os.getenv("OPENAI_API_KEY")),
            "key_prefix": os.getenv("OPENAI_API_KEY", "")[:10] + "..." if os.getenv("OPENAI_API_KEY") else "Not configured"
        },
        "database_type": "SQLite (SeaTable not required)"
    }


@router.post("/test-profile/{username}")
async def test_profile_fetch(username: str):
    """
    Test fetching a specific profile with detailed debugging
    """
    try:
        ensemble_service = EnsembleService()

        logger.info(f"Testing profile fetch for @{username}")

        # Use the enhanced method with debugging
        profile_data = await ensemble_service.get_user_profile_strict(username)

        return {
            "success": True,
            "username": username,
            "profile_data": profile_data,
            "message": f"Successfully fetched profile for @{username}"
        }

    except HTTPException as e:
        return {
            "success": False,
            "username": username,
            "error": e.detail,
            "status_code": e.status_code,
            "message": f"HTTP error fetching profile for @{username}"
        }
    except Exception as e:
        logger.error(f"Error testing profile fetch for @{username}: {str(e)}")
        return {
            "success": False,
            "username": username,
            "error": str(e),
            "error_type": type(e).__name__,
            "message": f"Unexpected error fetching profile for @{username}"
        }
