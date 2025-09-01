"""
OpenAI GPT Service
Handles profile analysis and trend filtering using GPT-4
"""

from typing import List, Dict, Any, Optional
from openai import OpenAI
import os
import json
import logging
from pydantic import BaseModel

# Import ProfileAnalysis from schemas to avoid duplication
from models.schemas import ProfileAnalysis

logger = logging.getLogger(__name__)


class TrendFilterResult(BaseModel):
    relevance_score: float
    relevance_reason: str
    category: str
    audience_match: bool
    trend_potential: str


class GPTService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4-turbo-preview"  # Updated model

    def is_healthy(self) -> bool:
        """Check if the service is healthy"""
        try:
            # Simple validation of API key format
            if not os.getenv("OPENAI_API_KEY"):
                logger.error("OPENAI_API_KEY not configured")
                return False

            # Test API connection (lightweight call)
            self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"OpenAI service health check failed: {str(e)}")
            return False

    async def analyze_profile(self, profile_data: Dict[str, Any], user_posts: List[Dict[str, Any]]) -> ProfileAnalysis:
        """
        GPT Agent 1: Analyze TikTok profile and determine interests, keywords, and hashtags for trend search
        """

        # Prepare profile summary
        profile_summary = self._prepare_profile_summary(
            profile_data, user_posts)

        from prompts.gpt_prompts import get_profile_analyzer_prompt
        system_prompt = get_profile_analyzer_prompt()

        user_prompt = f"""
        Analyze this TikTok profile and recent posts:
        
        PROFILE DATA:
        {profile_summary}
        
        Please provide a comprehensive analysis focusing on trend discovery opportunities.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )

            result = json.loads(response.choices[0].message.content)
            return ProfileAnalysis(**result)

        except Exception as e:
            logger.error(f"Error analyzing profile: {str(e)}")
            # Fallback analysis
            return self._fallback_profile_analysis(profile_data)

    async def analyze_sentiment_and_audience(
        self,
        trends: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Analyze sentiment and audience for trends (as per prompt.md requirements)
        """
        try:
            trends_summary = self._prepare_trends_for_sentiment_analysis(
                trends[:10])

            system_prompt = """
            You are a TikTok content sentiment and audience analyzer. Analyze the provided trends and determine:
            1. Sentiment: positive, negative, neutral, mixed
            2. Audience: primary demographic and interests
            
            Return JSON array with sentiment and audience for each trend:
            [
                {
                    "aweme_id": "trend_id",
                    "sentiment": "positive|negative|neutral|mixed",
                    "audience": "demographic description"
                }
            ]
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": trends_summary}
                ],
                temperature=0.2,
                max_tokens=1500
            )

            sentiment_results = json.loads(response.choices[0].message.content)

            # Merge sentiment/audience data with original trends
            for trend in trends:
                sentiment_data = next(
                    (s for s in sentiment_results if s["aweme_id"]
                     == trend["aweme_id"]),
                    {"sentiment": "neutral", "audience": "General audience"}
                )
                trend["sentiment"] = sentiment_data["sentiment"]
                trend["audience"] = sentiment_data["audience"]

            return trends

        except Exception as e:
            logger.error(f"Error analyzing sentiment and audience: {str(e)}")
            # Fallback: add default values
            for trend in trends:
                trend["sentiment"] = "neutral"
                trend["audience"] = "General audience"
            return trends

    async def filter_and_rank_trends(
        self,
        trends: List[Dict[str, Any]],
        profile_analysis: ProfileAnalysis,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        GPT Agent 2: Filter and rank trends based on profile analysis
        """

        # Prepare trends summary for GPT
        trends_summary = self._prepare_trends_summary(
            trends[:20])  # Analyze top 20 trends

        from prompts.gpt_prompts import get_trend_filter_prompt
        system_prompt = get_trend_filter_prompt()

        user_prompt = f"""
        USER PROFILE ANALYSIS:
        - Niche: {profile_analysis.niche}
        - Interests: {', '.join(profile_analysis.interests)}
        - Target Audience: {profile_analysis.target_audience}
        - Content Style: {profile_analysis.content_style}
        - Region Focus: {profile_analysis.region_focus}
        
        TRENDS TO ANALYZE:
        {trends_summary}
        
        Please filter and rank these trends based on relevance to this user profile.
        Return only the most relevant trends with scores above 70.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=2000
            )

            filter_results = json.loads(response.choices[0].message.content)

            # Merge filter results with original trend data
            filtered_trends = []
            for filter_result in filter_results:
                # Find matching trend
                matching_trend = next(
                    (t for t in trends if t["aweme_id"]
                     == filter_result["aweme_id"]),
                    None
                )
                if matching_trend and filter_result["relevance_score"] >= 70:
                    matching_trend.update({
                        "relevance_score": filter_result["relevance_score"],
                        "relevance_reason": filter_result["relevance_reason"],
                        "trend_category": filter_result["category"],
                        "audience_match": filter_result["audience_match"],
                        "trend_potential": filter_result["trend_potential"]
                    })
                    filtered_trends.append(matching_trend)

            # Sort by relevance score and engagement
            filtered_trends.sort(
                key=lambda x: (x["relevance_score"], x["engagement_rate"]),
                reverse=True
            )

            return filtered_trends[:max_results]

        except Exception as e:
            logger.error(f"Error filtering trends: {str(e)}")
            # Fallback: return top trends by engagement
            return trends[:max_results]

    def _prepare_profile_summary(self, profile_data: Dict[str, Any], user_posts: List[Dict[str, Any]]) -> str:
        """Prepare a concise profile summary for GPT analysis"""

        # Extract hashtags from posts
        all_hashtags = []
        post_descriptions = []

        for post in user_posts[:10]:  # Analyze last 10 posts
            post_descriptions.append(post.get("desc", ""))
            for tag in post.get("text_extra", []):
                if tag.get("hashtag_name"):
                    all_hashtags.append(tag["hashtag_name"])

        hashtags_summary = list(set(all_hashtags))[
            :20]  # Top 20 unique hashtags

        summary = f"""
        Username: @{profile_data.get('username', '')}
        Display Name: {profile_data.get('display_name', '')}
        Bio: {profile_data.get('bio', 'No bio')}
        Followers: {profile_data.get('follower_count', 0):,}
        Following: {profile_data.get('following_count', 0):,}
        Videos: {profile_data.get('video_count', 0):,}
        Total Likes: {profile_data.get('likes_count', 0):,}
        Verified: {profile_data.get('verified', False)}
        Region: {profile_data.get('region', 'Unknown')}
        
        Recent Post Descriptions:
        {chr(10).join(post_descriptions[:5])}
        
        Commonly Used Hashtags:
        {', '.join(hashtags_summary)}
        """

        return summary

    def _prepare_trends_summary(self, trends: List[Dict[str, Any]]) -> str:
        """Prepare trends summary for GPT analysis"""
        trends_text = []

        for i, trend in enumerate(trends, 1):
            stats = trend.get("statistics", {})
            trend_text = f"""
            Trend #{i}:
            ID: {trend.get('aweme_id', '')}
            Description: {trend.get('desc', '')[:200]}...
            Author: @{trend.get('author', {}).get('unique_id', '')}
            Views: {stats.get('play_count', 0):,}
            Likes: {stats.get('digg_count', 0):,}
            Comments: {stats.get('comment_count', 0):,}
            Shares: {stats.get('share_count', 0):,}
            Engagement Rate: {trend.get('engagement_rate', 0):.2f}%
            Duration: {trend.get('video', {}).get('duration', 0)}ms
            Music: {trend.get('music', {}).get('title', 'N/A')}
            """
            trends_text.append(trend_text)

        return "\n".join(trends_text)

    def _prepare_trends_for_sentiment_analysis(self, trends: List[Dict[str, Any]]) -> str:
        """Prepare trends summary for sentiment and audience analysis"""
        trends_text = []

        for i, trend in enumerate(trends, 1):
            trend_text = f"""
            Trend #{i}:
            ID: {trend.get('aweme_id', '')}
            Description: {trend.get('desc', '')[:300]}...
            Author: @{trend.get('author', {}).get('unique_id', '')}
            Music: {trend.get('music', {}).get('title', 'N/A')}
            """
            trends_text.append(trend_text)

        return "\n".join(trends_text)

    def _fallback_profile_analysis(self, profile_data: Dict[str, Any]) -> ProfileAnalysis:
        """Fallback analysis when GPT fails"""
        bio = profile_data.get('bio', '').lower()

        # Simple keyword-based niche detection
        niche_keywords = {
            'beauty': ['beauty', 'makeup', 'skincare', 'cosmetics'],
            'fitness': ['fitness', 'workout', 'gym', 'health'],
            'comedy': ['funny', 'comedy', 'humor', 'jokes'],
            'food': ['food', 'cooking', 'recipe', 'chef'],
            'tech': ['tech', 'technology', 'gadgets', 'ai'],
            'lifestyle': ['lifestyle', 'daily', 'life', 'vlog']
        }

        detected_niche = 'lifestyle'  # default
        for niche, keywords in niche_keywords.items():
            if any(keyword in bio for keyword in keywords):
                detected_niche = niche
                break

        return ProfileAnalysis(
            niche=detected_niche,
            interests=[detected_niche, 'trending', 'viral'],
            keywords=[detected_niche, 'trending', 'popular'],
            hashtags=[detected_niche, 'fyp', 'viral'],
            target_audience='General audience',
            content_style='Mixed content',
            region_focus=profile_data.get('region', 'Global')
        )
