"""
Pydantic models for request/response schemas
"""

from pydantic import BaseModel, HttpUrl, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class TikTokProfileRequest(BaseModel):
    """Request model for TikTok profile analysis"""
    tiktok_url: str = Field(..., description="TikTok profile URL")


class UserProfile(BaseModel):
    """User profile data model"""
    username: str
    display_name: str
    follower_count: int
    following_count: int
    video_count: int
    likes_count: int
    bio: str
    avatar_url: str
    verified: bool
    sec_uid: str
    uid: str
    region: str
    language: str


class ProfileAnalysis(BaseModel):
    """Profile analysis result from GPT"""
    niche: str
    interests: List[str]
    keywords: List[str]
    hashtags: List[str]
    target_audience: str
    content_style: str
    region_focus: str


class VideoStatistics(BaseModel):
    """Video engagement statistics"""
    digg_count: int = 0  # likes
    comment_count: int = 0
    play_count: int = 0  # views
    share_count: int = 0
    download_count: int = 0
    collect_count: int = 0  # favourited
    forward_count: int = 0
    whatsapp_share_count: int = 0


class VideoInfo(BaseModel):
    """Video metadata"""
    duration: int
    height: int
    width: int
    cover: str
    download_addr: str


class MusicInfo(BaseModel):
    """Music/audio information"""
    title: str
    author: str
    mid: str


class AuthorInfo(BaseModel):
    """Video author information"""
    unique_id: str
    nickname: str
    follower_count: int
    avatar_thumb: str


class TrendItem(BaseModel):
    """Individual trend item"""
    aweme_id: str
    desc: str
    create_time: int
    author: AuthorInfo
    statistics: VideoStatistics
    video: VideoInfo
    music: MusicInfo
    text_extra: List[Dict[str, Any]]
    engagement_rate: float
    relevance_score: Optional[float] = None
    relevance_reason: Optional[str] = None
    trend_category: Optional[str] = None
    audience_match: Optional[bool] = None
    trend_potential: Optional[str] = None
    keyword: Optional[str] = None
    hashtag: Optional[str] = None
    tiktok_url: str
    sentiment: Optional[str] = None
    audience: Optional[str] = None


class AnalysisResponse(BaseModel):
    """Response for profile analysis"""
    success: bool
    user_profile: UserProfile
    profile_analysis: ProfileAnalysis
    message: str


class TrendsResponse(BaseModel):
    """Response for trends retrieval"""
    success: bool
    trends: List[TrendItem]
    total_count: int
    message: str


class RefreshTrendsRequest(BaseModel):
    """Request for refreshing trends"""
    username: str = Field(..., description="TikTok username")
    max_results: int = Field(default=10, ge=1, le=50,
                             description="Maximum number of trends to return")


class HealthStatus(BaseModel):
    """Health check response"""
    status: str
    services: Dict[str, bool]


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str
    message: str

# SQLite-specific models are not needed as we use direct database operations
