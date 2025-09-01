"""
Ensemble Data API Service
Handles all TikTok data fetching operations
"""

from typing import List, Dict, Any, Optional
from ensembledata.api import EDClient, EDError
import os
import time
import logging
from urllib.parse import urlparse
from fastapi import HTTPException

logger = logging.getLogger(__name__)


class EnsembleService:
    def __init__(self):
        api_key = os.getenv("ENSEMBLE_DATA_API_KEY")
        if not api_key:
            raise ValueError(
                "ENSEMBLE_DATA_API_KEY environment variable is required")
        self.client = EDClient(api_key)

    def is_healthy(self) -> bool:
        """Check if the service is healthy"""
        try:
            # Simple test call
            return True
        except Exception:
            return False

    def extract_username_from_url(self, url: str) -> str:
        """Extract TikTok username from profile URL"""
        try:
            # Handle different TikTok URL formats
            if "@" in url:
                # Extract from URL like https://www.tiktok.com/@username
                username = url.split("@")[-1].split("/")[0].split("?")[0]
            else:
                # Handle other formats
                parsed = urlparse(url)
                path_parts = parsed.path.strip("/").split("/")
                for part in path_parts:
                    if part.startswith("@"):
                        username = part[1:]
                        break
                else:
                    raise ValueError("Could not extract username from URL")

            return username.lower()
        except Exception as e:
            logger.error(
                f"Failed to extract username from URL {url}: {str(e)}")
            raise ValueError(f"Invalid TikTok URL format: {url}")

    async def get_user_profile(self, username: str) -> Dict[str, Any]:
        """Get TikTok user profile information"""
        try:
            result = self.client.tiktok.user_info_from_username(
                username=username)

            if not result.data or not result.data.get("user"):
                logger.warning(
                    f"No user data found for {username} from Ensemble API")
                # Fallback to database if available
                db_profile = self._get_profile_from_db(username)
                if db_profile:
                    logger.info(
                        f"Found {username} in database, using cached data.")
                    db_profile['api_source'] = 'database'
                    return db_profile
                raise ValueError(
                    f"User @{username} not found via API and not in cache.")

            user_data = result.data["user"]

            # Extract username with enhanced field priority
            extracted_username = user_data.get("uniqueId", "").strip()
            if not extracted_username:
                extracted_username = user_data.get("unique_id", "").strip()
                if not extracted_username:
                    extracted_username = username

            # Get enhanced statistics if possible
            sec_uid = user_data.get("secUid", "").strip()
            enhanced_user_data = user_data  # Default to basic data

            if sec_uid:
                try:
                    enhanced_result = self.client.tiktok.user_info_from_secuid(
                        sec_uid=sec_uid, alternative_method=True)

                    if enhanced_result and enhanced_result.data and "user" in enhanced_result.data:
                        enhanced_user_data = enhanced_result.data["user"]
                        logger.info(
                            f"Enhanced stats for @{username} - Followers: {enhanced_user_data.get('follower_count', 0)}")
                except Exception as e:
                    logger.warning(
                        f"Could not get enhanced stats for @{username}: {str(e)}")

            # Extract key profile information with enhanced data
            profile = {
                "username": extracted_username,
                "display_name": enhanced_user_data.get("nickname", ""),
                "follower_count": enhanced_user_data.get("follower_count", 0),
                "following_count": enhanced_user_data.get("following_count", 0),
                "video_count": enhanced_user_data.get("aweme_count", 0),
                "likes_count": enhanced_user_data.get("total_favorited", 0),
                "bio": enhanced_user_data.get("signature", ""),
                "avatar_url": enhanced_user_data.get("avatar_larger", {}).get("url_list", [""])[0],
                "verified": enhanced_user_data.get("verified", False),
                # Always use original secUid
                "sec_uid": user_data.get("secUid", ""),
                "uid": enhanced_user_data.get("uid", ""),
                "region": enhanced_user_data.get("region", ""),
                "language": enhanced_user_data.get("language", ""),
                "api_source": "ensemble_enhanced"
            }

            return profile

        except EDError as e:
            logger.error(
                f"Ensemble API error getting user @{username}: {e.detail}")
            # Fallback to database on API error
            db_profile = self._get_profile_from_db(username)
            if db_profile:
                logger.warning(
                    f"Ensemble API failed. Using cached data for @{username}.")
                db_profile['api_source'] = 'database_fallback'
                return db_profile
            raise HTTPException(status_code=e.status_code,
                                detail=f"API Error: {e.detail}")
        except Exception as e:
            logger.error(f"Error getting user profile @{username}: {str(e)}")
            db_profile = self._get_profile_from_db(username)
            if db_profile:
                logger.warning(
                    f"General error. Using cached data for @{username}.")
                db_profile['api_source'] = 'database_fallback'
                return db_profile
            raise ValueError(
                f"Failed to get user profile for @{username}: {str(e)}")

    async def get_user_profile_strict(self, username: str) -> Dict[str, Any]:
        """Get TikTok user profile strictly from Ensemble API (no fallbacks)."""
        try:
            logger.info(
                f"Fetching user profile for @{username} from Ensemble API")
            result = self.client.tiktok.user_info_from_username(
                username=username)

            # Debug logging
            logger.info(
                f"Ensemble API response status for @{username}: {result is not None}")
            if result:
                logger.info(
                    f"Units charged: {getattr(result, 'units_charged', 'N/A')}")
                logger.info(f"Has data: {result.data is not None}")
                if result.data:
                    logger.info(f"Has user field: {'user' in result.data}")

            if not result.data or not result.data.get("user"):
                logger.warning(
                    f"No user data from Ensemble API for @{username} (strict mode)")
                logger.warning(
                    f"API response: {result.data if result else 'No result'}")
                raise HTTPException(
                    status_code=404, detail=f"User @{username} not found via Ensemble API")

            user_data = result.data["user"]

            # Debug log user data keys
            logger.info(
                f"User data keys for @{username}: {list(user_data.keys()) if user_data else 'None'}")

            # Extract username with fallback (prioritize uniqueId over unique_id)
            extracted_username = user_data.get("uniqueId", "").strip()
            if not extracted_username:
                extracted_username = user_data.get("unique_id", "").strip()
                if not extracted_username:
                    extracted_username = username  # Use the input username as fallback
                    logger.warning(
                        f"No uniqueId/unique_id in API response for @{username}, using input username as fallback")

            # Get sec_uid for enhanced statistics
            sec_uid = user_data.get("secUid", "").strip()
            enhanced_user_data = user_data  # Default to basic data

            if sec_uid:
                try:
                    logger.info(
                        f"Fetching enhanced statistics for @{username} using sec_uid")
                    enhanced_result = self.client.tiktok.user_info_from_secuid(
                        sec_uid=sec_uid, alternative_method=True)

                    if enhanced_result and enhanced_result.data and "user" in enhanced_result.data:
                        enhanced_user_data = enhanced_result.data["user"]
                        logger.info(
                            f"Enhanced stats - Followers: {enhanced_user_data.get('follower_count', 0)}, Videos: {enhanced_user_data.get('aweme_count', 0)}")
                    else:
                        logger.warning(
                            f"Failed to get enhanced statistics for @{username}")

                except Exception as e:
                    logger.warning(
                        f"Error getting enhanced statistics for @{username}: {str(e)}")

            profile = {
                "username": extracted_username,
                "display_name": enhanced_user_data.get("nickname", ""),
                "follower_count": enhanced_user_data.get("follower_count", 0),
                "following_count": enhanced_user_data.get("following_count", 0),
                "video_count": enhanced_user_data.get("aweme_count", 0),
                "likes_count": enhanced_user_data.get("total_favorited", 0),
                "bio": enhanced_user_data.get("signature", ""),
                "avatar_url": enhanced_user_data.get("avatar_larger", {}).get("url_list", [""])[0],
                "verified": enhanced_user_data.get("verified", False),
                # Always use original secUid
                "sec_uid": user_data.get("secUid", ""),
                "uid": enhanced_user_data.get("uid", ""),
                "region": enhanced_user_data.get("region", ""),
                "language": enhanced_user_data.get("language", ""),
                "api_source": "ensemble_enhanced"
            }

            # Final validation
            if not profile["username"]:
                logger.error(
                    f"Could not extract valid username for @{username}")
                logger.error(f"User data: {user_data}")
                raise HTTPException(
                    status_code=502,
                    detail=f"Ensemble API returned incomplete data for @{username}. Please check if the profile exists and is public."
                )

            logger.info(
                f"Successfully extracted profile for @{profile['username']}")
            return profile

        except EDError as e:
            logger.error(
                f"Ensemble API error (strict) getting user @{username}: {e.detail}")
            raise HTTPException(status_code=e.status_code,
                                detail=f"API Error: {e.detail}")
        except Exception as e:
            logger.error(
                f"Error (strict) getting user profile @{username}: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Failed to get user profile for @{username}: {str(e)}")

    def _get_profile_from_db(self, username: str) -> Optional[Dict[str, Any]]:
        """A helper to fetch profile from DB as a fallback."""
        from .database_adapter import database_service
        try:
            user_data = database_service.get_user_profile_sync(username)
            if not user_data:
                return None

            return {
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
                "language": user_data.get("Language", ""),
            }
        except Exception as e:
            logger.error(f"Database fallback failed for @{username}: {e}")
            return None

    async def get_user_posts(self, username: str, depth: int = 5) -> List[Dict[str, Any]]:
        """Get recent posts from TikTok user"""
        try:
            result = self.client.tiktok.user_posts_from_username(
                username=username,
                depth=depth
            )

            if not result.data or not result.data.get("data"):
                logger.warning(
                    f"No posts found for @{username} from Ensemble API.")
                return []

            posts = []
            for post in result.data.get("data", []):
                post_data = {
                    "aweme_id": post.get("aweme_id", ""),
                    "desc": post.get("desc", ""),
                    "create_time": post.get("create_time", 0),
                    "statistics": {
                        # Views
                        "play_count": post.get("statistics", {}).get("play_count", 0),
                        # Likes
                        "digg_count": post.get("statistics", {}).get("digg_count", 0),
                        # Comments
                        "comment_count": post.get("statistics", {}).get("comment_count", 0),
                        # Shares
                        "share_count": post.get("statistics", {}).get("share_count", 0),
                        # Downloads
                        "download_count": post.get("statistics", {}).get("download_count", 0),
                        # Favourited
                        "collect_count": post.get("statistics", {}).get("collect_count", 0),
                        # Whatsapp Shares
                        "whatsapp_share_count": post.get("statistics", {}).get("whatsapp_share_count", 0)
                    },
                    "video": {
                        # Duration
                        "duration": post.get("video", {}).get("duration", 0),
                        "cover": self._get_best_video_cover_url(post.get("video", {})),
                        "download_addr": self._get_best_video_url(post.get("video", {})),
                        "play_addr": self._get_best_video_url(post.get("video", {})),
                        "video_type": post.get("aweme_type", 0)  # Video Type
                    },
                    "music": {
                        **post.get("music", {}),
                        # Sound Type
                        "sound_type": post.get("music", {}).get("album", "")
                    },
                    "text_extra": post.get("text_extra", []),  # hashtags
                    "region": post.get("region", ""),  # Region
                    "engagement_rate": self._calculate_engagement_rate(post.get("statistics", {}))
                }
                posts.append(post_data)

            return posts

        except EDError as e:
            logger.error(
                f"Ensemble API error getting posts for {username}: {e.detail}")
            # For posts, we can return an empty list as a fallback
            return []
        except Exception as e:
            logger.error(f"Error getting user posts {username}: {str(e)}")
            raise ValueError(f"Failed to get user posts: {str(e)}")

    async def search_hashtag_trends(self, hashtags: List[str], max_results: int = 50) -> List[Dict[str, Any]]:
        """Search for trending posts by hashtags"""
        all_trends = []

        for hashtag in hashtags:
            try:
                result = self.client.tiktok.hashtag_search(
                    hashtag=hashtag, cursor=0)

                trends = []
                for post in result.data.get("data", [])[:max_results]:
                    trend_data = {
                        "aweme_id": post.get("aweme_id", ""),
                        "desc": post.get("desc", ""),  # Video's caption
                        "create_time": post.get("create_time", 0),
                        "hashtag": hashtag,
                        "author": {
                            "unique_id": post.get("author", {}).get("unique_id", ""),
                            "nickname": post.get("author", {}).get("nickname", ""),
                            "follower_count": post.get("author", {}).get("follower_count", 0),
                            "avatar_thumb": self._get_best_avatar_url(post.get("author", {})),
                            "verified": post.get("author", {}).get("verified", False)
                        },
                        "statistics": {
                            # Views
                            "play_count": post.get("statistics", {}).get("play_count", 0),
                            # Likes
                            "digg_count": post.get("statistics", {}).get("digg_count", 0),
                            # Comments
                            "comment_count": post.get("statistics", {}).get("comment_count", 0),
                            # Shares
                            "share_count": post.get("statistics", {}).get("share_count", 0),
                            # Downloads
                            "download_count": post.get("statistics", {}).get("download_count", 0),
                            # Favourited
                            "collect_count": post.get("statistics", {}).get("collect_count", 0),
                            # Whatsapp Shares
                            "whatsapp_share_count": post.get("statistics", {}).get("whatsapp_share_count", 0)
                        },
                        "video": {
                            # Duration
                            "duration": post.get("video", {}).get("duration", 0),
                            "cover": self._get_best_video_cover_url(post.get("video", {})),
                            "download_addr": self._get_best_video_url(post.get("video", {})),
                            "play_addr": self._get_best_video_url(post.get("video", {})),
                            # Video Type
                            "video_type": post.get("aweme_type", 0)
                        },
                        "music": {
                            "title": post.get("music", {}).get("title", ""),
                            "author": post.get("music", {}).get("author", ""),
                            "mid": post.get("music", {}).get("mid", ""),
                            # Sound Type
                            "sound_type": post.get("music", {}).get("album", "")
                        },
                        "text_extra": post.get("text_extra", []),  # hashtags
                        "region": post.get("region", ""),  # Region
                        # Engagement
                        "engagement_rate": self._calculate_engagement_rate(post.get("statistics", {})),
                        "tiktok_url": f"https://www.tiktok.com/@{post.get('author', {}).get('unique_id', '')}/video/{post.get('aweme_id', '')}"
                    }
                    trends.append(trend_data)

                all_trends.extend(trends)

            except EDError as e:
                logger.error(
                    f"Ensemble API error searching hashtag {hashtag}: {e.detail}")
                continue
            except Exception as e:
                logger.error(f"Error searching hashtag {hashtag}: {str(e)}")
                continue

        # Sort by engagement rate and views
        all_trends.sort(key=lambda x: (
            x["engagement_rate"],
            x["statistics"]["play_count"]
        ), reverse=True)

        return all_trends[:max_results]

    async def search_keyword_trends(self, keywords: List[str], period: str = "180", max_results: int = 50) -> List[Dict[str, Any]]:
        """Search for trending posts by keywords"""
        all_trends = []

        for keyword in keywords:
            try:
                result = self.client.tiktok.keyword_search(
                    keyword=keyword,
                    period=period,
                    cursor=0
                )

                trends = []
                for post in result.data.get("data", [])[:max_results]:
                    trend_data = {
                        "aweme_id": post.get("aweme_id", ""),
                        "desc": post.get("desc", ""),  # Video's caption
                        "create_time": post.get("create_time", 0),
                        "keyword": keyword,
                        "author": {
                            "unique_id": post.get("author", {}).get("unique_id", ""),
                            "nickname": post.get("author", {}).get("nickname", ""),
                            "follower_count": post.get("author", {}).get("follower_count", 0),
                            "avatar_thumb": self._get_best_avatar_url(post.get("author", {})),
                            "verified": post.get("author", {}).get("verified", False)
                        },
                        "statistics": {
                            # Views
                            "play_count": post.get("statistics", {}).get("play_count", 0),
                            # Likes
                            "digg_count": post.get("statistics", {}).get("digg_count", 0),
                            # Comments
                            "comment_count": post.get("statistics", {}).get("comment_count", 0),
                            # Shares
                            "share_count": post.get("statistics", {}).get("share_count", 0),
                            # Downloads
                            "download_count": post.get("statistics", {}).get("download_count", 0),
                            # Favourited
                            "collect_count": post.get("statistics", {}).get("collect_count", 0),
                            # Whatsapp Shares
                            "whatsapp_share_count": post.get("statistics", {}).get("whatsapp_share_count", 0)
                        },
                        "video": {
                            # Duration
                            "duration": post.get("video", {}).get("duration", 0),
                            "cover": self._get_best_video_cover_url(post.get("video", {})),
                            "download_addr": self._get_best_video_url(post.get("video", {})),
                            "play_addr": self._get_best_video_url(post.get("video", {})),
                            # Video Type
                            "video_type": post.get("aweme_type", 0)
                        },
                        "music": {
                            "title": post.get("music", {}).get("title", ""),
                            "author": post.get("music", {}).get("author", ""),
                            "mid": post.get("music", {}).get("mid", ""),
                            # Sound Type
                            "sound_type": post.get("music", {}).get("album", "")
                        },
                        "text_extra": post.get("text_extra", []),  # hashtags
                        "region": post.get("region", ""),  # Region
                        # Engagement
                        "engagement_rate": self._calculate_engagement_rate(post.get("statistics", {})),
                        "tiktok_url": f"https://www.tiktok.com/@{post.get('author', {}).get('unique_id', '')}/video/{post.get('aweme_id', '')}"
                    }
                    trends.append(trend_data)

                all_trends.extend(trends)

            except EDError as e:
                logger.error(
                    f"Ensemble API error searching keyword {keyword}: {e.detail}")
                continue
            except Exception as e:
                logger.error(f"Error searching keyword {keyword}: {str(e)}")
                continue

        # Sort by engagement rate and views
        all_trends.sort(key=lambda x: (
            x["engagement_rate"],
            x["statistics"]["play_count"]
        ), reverse=True)

        return all_trends[:max_results]

    def _calculate_engagement_rate(self, stats: Dict[str, int]) -> float:
        """Calculate engagement rate from statistics"""
        views = stats.get("play_count", 0)
        if views == 0:
            return 0.0

        engagements = (
            stats.get("digg_count", 0) +
            stats.get("comment_count", 0) +
            stats.get("share_count", 0)
        )

        return (engagements / views) * 100 if views > 0 else 0.0

    def _get_best_avatar_url(self, author_data: Dict[str, Any]) -> str:
        """Get the best quality avatar URL from author data"""
        avatar_sources = [
            author_data.get("avatar_larger", {}).get("url_list", []),
            author_data.get("avatar_medium", {}).get("url_list", []),
            author_data.get("avatar_thumb", {}).get("url_list", [])
        ]

        for source in avatar_sources:
            if source and len(source) > 0:
                # Return the first available URL
                return source[0]

        return ""

    def _get_best_video_cover_url(self, video_data: Dict[str, Any]) -> str:
        """Get the best quality video cover/thumbnail URL"""
        cover_sources = [
            video_data.get("origin_cover", {}).get("url_list", []),
            video_data.get("dynamic_cover", {}).get("url_list", []),
            video_data.get("cover", {}).get("url_list", [])
        ]

        for source in cover_sources:
            if source and len(source) > 0:
                return source[0]

        return ""

    def _get_best_video_url(self, video_data: Dict[str, Any]) -> str:
        """Get the best quality video URL for playback"""
        video_sources = [
            video_data.get("play_addr", {}).get("url_list", []),
            video_data.get("download_addr", {}).get("url_list", [])
        ]

        for source in video_sources:
            if source and len(source) > 0:
                return source[0]

        return ""

    async def get_advanced_user_metrics(self, username: str, posts_depth: int = 5) -> Dict[str, Any]:
        """
        Get advanced metrics for user analysis including activity patterns,
        engagement trends, and content performance analytics
        """
        try:
            # Get user profile and posts
            profile_data = await self.get_user_profile(username)
            user_posts = await self.get_user_posts(username, depth=posts_depth)

            if not user_posts:
                logger.warning(
                    f"No posts found for advanced metrics calculation for @{username}")
                return self._empty_metrics(profile_data)

            # Calculate advanced metrics
            metrics = self._calculate_advanced_metrics(
                profile_data, user_posts)

            return {
                "profile": profile_data,
                "posts": user_posts,
                "metrics": metrics,
                "analysis_timestamp": int(time.time())
            }

        except Exception as e:
            logger.error(
                f"Error calculating advanced metrics for {username}: {str(e)}")
            return self._empty_metrics({})

    def _calculate_advanced_metrics(self, profile_data: Dict[str, Any], posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate comprehensive user metrics"""
        if not posts:
            return {}

        # Basic stats
        total_views = sum(post.get("statistics", {}).get(
            "play_count", 0) for post in posts)
        total_likes = sum(post.get("statistics", {}).get(
            "digg_count", 0) for post in posts)
        total_comments = sum(post.get("statistics", {}).get(
            "comment_count", 0) for post in posts)
        total_shares = sum(post.get("statistics", {}).get(
            "share_count", 0) for post in posts)

        # Advanced calculations
        post_count = len(posts)
        avg_views_per_post = total_views / post_count if post_count > 0 else 0
        avg_likes_per_post = total_likes / post_count if post_count > 0 else 0

        # Engagement metrics
        engagement_rates = [self._calculate_engagement_rate(
            post.get("statistics", {})) for post in posts]
        avg_engagement_rate = sum(engagement_rates) / \
            len(engagement_rates) if engagement_rates else 0

        # Consistency metrics
        views_variance = self._calculate_variance(
            [post.get("statistics", {}).get("play_count", 0) for post in posts])
        consistency_score = max(
            0, 100 - (views_variance / avg_views_per_post * 100)) if avg_views_per_post > 0 else 0

        # Content analysis
        hashtag_usage = self._analyze_hashtag_usage(posts)
        posting_patterns = self._analyze_posting_patterns(posts)

        # Performance categorization
        viral_posts = len([post for post in posts if post.get(
            "statistics", {}).get("play_count", 0) > 1000000])
        high_engagement_posts = len(
            [post for post in posts if self._calculate_engagement_rate(post.get("statistics", {})) > 8])

        return {
            "overview": {
                "total_posts_analyzed": post_count,
                "total_views": total_views,
                "total_likes": total_likes,
                "total_comments": total_comments,
                "total_shares": total_shares,
                "avg_views_per_post": avg_views_per_post,
                "avg_likes_per_post": avg_likes_per_post,
                "avg_engagement_rate": avg_engagement_rate
            },
            "performance": {
                "consistency_score": consistency_score,
                "viral_posts": viral_posts,
                "high_engagement_posts": high_engagement_posts,
                "best_performing_post_views": max([post.get("statistics", {}).get("play_count", 0) for post in posts], default=0),
                "engagement_variance": self._calculate_variance(engagement_rates)
            },
            "content_analysis": {
                "hashtag_diversity": len(hashtag_usage),
                "top_hashtags": sorted(hashtag_usage.items(), key=lambda x: x[1], reverse=True)[:10],
                "posting_patterns": posting_patterns
            },
            "growth_indicators": {
                "viral_potential": min(100, (viral_posts / post_count * 100) + (high_engagement_posts / post_count * 50)) if post_count > 0 else 0,
                "audience_loyalty": (total_likes / max(profile_data.get("follower_count", 1), 1)) * 100,
                "content_quality_score": min(100, (avg_engagement_rate * 10) + (consistency_score * 0.3))
            }
        }

    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values"""
        if not values:
            return 0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)

    def _analyze_hashtag_usage(self, posts: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze hashtag usage patterns"""
        hashtag_count = {}
        for post in posts:
            text_extra = post.get("text_extra", [])
            for item in text_extra:
                hashtag = item.get("hashtag_name")
                if hashtag:
                    hashtag_count[hashtag] = hashtag_count.get(hashtag, 0) + 1
        return hashtag_count

    def _analyze_posting_patterns(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze when user typically posts"""
        import datetime

        if not posts:
            return {}

        # Convert timestamps to datetime objects
        post_times = []
        for post in posts:
            timestamp = post.get("create_time", 0)
            if timestamp:
                post_times.append(datetime.datetime.fromtimestamp(timestamp))

        if not post_times:
            return {}

        # Analyze patterns
        hourly_pattern = {}
        daily_pattern = {}

        for dt in post_times:
            hour = dt.hour
            day = dt.strftime("%A")  # Day name

            hourly_pattern[hour] = hourly_pattern.get(hour, 0) + 1
            daily_pattern[day] = daily_pattern.get(day, 0) + 1

        # Find peak times
        peak_hour = max(
            hourly_pattern, key=hourly_pattern.get) if hourly_pattern else 12
        peak_day = max(
            daily_pattern, key=daily_pattern.get) if daily_pattern else "Monday"

        return {
            "hourly_distribution": hourly_pattern,
            "daily_distribution": daily_pattern,
            "peak_posting_hour": peak_hour,
            "peak_posting_day": peak_day,
            # Assuming last 30 days of posts
            "posting_frequency": len(posts) / 30
        }

    def _empty_metrics(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Return empty metrics structure"""
        return {
            "profile": profile_data,
            "posts": [],
            "metrics": {
                "overview": {
                    "total_posts_analyzed": 0,
                    "total_views": 0,
                    "total_likes": 0,
                    "total_comments": 0,
                    "total_shares": 0,
                    "avg_views_per_post": 0,
                    "avg_likes_per_post": 0,
                    "avg_engagement_rate": 0
                },
                "performance": {
                    "consistency_score": 0,
                    "viral_posts": 0,
                    "high_engagement_posts": 0,
                    "best_performing_post_views": 0,
                    "engagement_variance": 0
                },
                "content_analysis": {
                    "hashtag_diversity": 0,
                    "top_hashtags": [],
                    "posting_patterns": {}
                },
                "growth_indicators": {
                    "viral_potential": 0,
                    "audience_loyalty": 0,
                    "content_quality_score": 0
                }
            },
            "analysis_timestamp": int(time.time())
        }

    async def get_trending_hashtags(self, niche_keywords: List[str], limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get trending hashtags related to user's niche for trend discovery
        """
        trending_hashtags = []

        for keyword in niche_keywords[:5]:  # Limit API calls
            try:
                # Use keyword search to find recent trending content
                result = self.client.tiktok.keyword_search(
                    keyword=keyword,
                    period="7",  # Last 7 days
                    sorting="1"  # Sort by likes
                )

                # Extract hashtags from trending posts
                # Top 10 posts per keyword
                for post in result.data.get("data", [])[:10]:
                    for text_item in post.get("text_extra", []):
                        hashtag = text_item.get("hashtag_name")
                        if hashtag:
                            # Calculate hashtag performance
                            hashtag_data = {
                                "hashtag": hashtag,
                                "keyword_source": keyword,
                                "post_views": post.get("statistics", {}).get("play_count", 0),
                                "post_likes": post.get("statistics", {}).get("digg_count", 0),
                                "post_engagement": self._calculate_engagement_rate(post.get("statistics", {})),
                                "post_timestamp": post.get("create_time", 0)
                            }
                            trending_hashtags.append(hashtag_data)

            except Exception as e:
                logger.error(
                    f"Error fetching trending hashtags for {keyword}: {str(e)}")
                continue

        # Aggregate and rank hashtags
        hashtag_performance = {}
        for item in trending_hashtags:
            hashtag = item["hashtag"]
            if hashtag not in hashtag_performance:
                hashtag_performance[hashtag] = {
                    "hashtag": hashtag,
                    "appearances": 0,
                    "total_views": 0,
                    "total_likes": 0,
                    "avg_engagement": 0,
                    "keyword_sources": set()
                }

            perf = hashtag_performance[hashtag]
            perf["appearances"] += 1
            perf["total_views"] += item["post_views"]
            perf["total_likes"] += item["post_likes"]
            perf["avg_engagement"] += item["post_engagement"]
            perf["keyword_sources"].add(item["keyword_source"])

        # Calculate final scores and sort
        final_hashtags = []
        for hashtag, data in hashtag_performance.items():
            data["avg_engagement"] = data["avg_engagement"] / data["appearances"]
            data["keyword_sources"] = list(data["keyword_sources"])
            data["trending_score"] = (
                data["total_views"] / 100000 +  # Views score
                data["total_likes"] / 10000 +   # Likes score
                data["avg_engagement"] * 2 +    # Engagement score
                data["appearances"] * 10        # Frequency score
            )
            final_hashtags.append(data)

        # Sort by trending score and return top results
        final_hashtags.sort(key=lambda x: x["trending_score"], reverse=True)
        return final_hashtags[:limit]
