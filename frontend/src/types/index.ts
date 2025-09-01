// API Types for TrendXL Application

export interface UserProfile {
  username: string;
  display_name: string;
  follower_count: number;
  following_count: number;
  video_count: number;
  likes_count: number;
  bio: string;
  avatar_url: string;
  verified: boolean;
  sec_uid: string;
  uid: string;
  region: string;
  language: string;
  api_source?: 'ensemble' | 'database' | 'database_fallback' | 'mock';
}

export interface ProfileAnalysis {
  niche: string;
  interests: string[];
  keywords: string[];
  hashtags: string[];
  target_audience: string;
  content_style: string;
  region_focus: string;
}

export interface VideoStatistics {
  play_count: number; // Views
  digg_count: number; // Likes
  comment_count: number; // Comments
  share_count: number; // Shares
  download_count: number; // Downloads
  collect_count: number; // Favourited
  whatsapp_share_count: number; // Whatsapp Shares
}

export interface VideoInfo {
  duration: number; // Duration
  cover: string;
  download_addr: string;
  play_addr?: string;
  video_type?: string; // Video Type
}

export interface MusicInfo {
  title: string;
  author: string;
  mid: string;
  sound_type?: string; // Sound Type
}

export interface AuthorInfo {
  unique_id: string;
  nickname: string;
  follower_count: number;
  avatar_thumb: string;
  verified?: boolean; // Статус верификации
  total_favorited?: number; // Общее количество лайков пользователя
}

export interface TrendItem {
  aweme_id: string;
  desc: string; // Video's caption
  create_time: number;
  author: AuthorInfo;
  statistics: VideoStatistics; // Views, Likes, Comments, Shares, Downloads, Favourited, Whatsapp Shares
  video: VideoInfo; // Duration, Video Type
  music: MusicInfo; // Sound Type
  text_extra: Array<{ hashtag_name?: string; [key: string]: any }>; // hashtags
  engagement_rate: number; // Engagement
  region?: string; // Region
  sentiment?: string; // Sentiment
  audience?: string; // Audience
  tiktok_url: string;
  // GPT filtering results
  relevance_score?: number;
  relevance_reason?: string;
  trend_category?: string;
  audience_match?: boolean;
  trend_potential?: string;
  keyword?: string;
  hashtag?: string;
}

export interface AnalysisResponse {
  success: boolean;
  user_profile: UserProfile;
  profile_analysis: ProfileAnalysis;
  message: string;
}

export interface TrendsResponse {
  success: boolean;
  trends: TrendItem[];
  total_count: number;
  message: string;
}

export interface TikTokProfileRequest {
  tiktok_url: string;
}

export interface RefreshTrendsRequest {
  username: string;
  max_results?: number;
}

export interface HealthStatus {
  status: string;
  services: {
    ensemble: boolean;
    gpt: boolean;
    seatable: boolean;
  };
}

export interface ErrorResponse {
  success: false;
  error: string;
  message: string;
}

// API Error Response Types
export interface APIErrorData {
  detail?: string;
  message?: string;
  error?: string;
  [key: string]: any;
}

export interface FastAPIValidationError {
  detail: Array<{
    loc: (string | number)[];
    msg: string;
    type: string;
  }>;
}

export interface StandardErrorResponse {
  detail: string;
}

// Union type for all possible error response formats
export type ServerErrorData = APIErrorData | FastAPIValidationError | StandardErrorResponse | string | null | undefined;

// UI State Types
export interface AppState {
  currentUser: UserProfile | null;
  currentAnalysis: ProfileAnalysis | null;
  trends: TrendItem[];
  loading: boolean;
  error: string | null;
}

export interface LoadingState {
  analyzing: boolean;
  refreshing: boolean;
  loading: boolean;
}

// Component Props Types
export interface ProfileCardProps {
  profile: UserProfile;
  analysis: ProfileAnalysis;
  onRefreshTrends: () => void;
  loading?: boolean;
}

export interface TrendCardProps {
  trend: TrendItem;
  onPlay?: (trend: TrendItem) => void;
  showRelevanceScore?: boolean;
}

export interface StatProps {
  label: string;
  value: string | number;
  icon?: React.ReactNode;
  trend?: 'up' | 'down' | 'neutral';
}

export interface BadgeProps {
  children: React.ReactNode;
  variant?: 'primary' | 'success' | 'warning' | 'danger' | 'neutral';
  size?: 'sm' | 'md' | 'lg';
}

export interface SectionTitleProps {
  title: string;
  subtitle?: string;
  icon?: React.ReactNode;
  action?: React.ReactNode;
}

export interface InteractionLogProps {
  username: string;
  actions: InteractionAction[];
}

export interface InteractionAction {
  id: string;
  type: 'analysis' | 'refresh' | 'view';
  message: string;
  timestamp: Date;
  status: 'success' | 'error' | 'pending';
}

// Utility Types
export type TrendSortBy = 'relevance' | 'engagement' | 'views' | 'recent';
export type TrendFilter = 'all' | 'high-relevance' | 'viral' | 'recent';

export interface TrendFilters {
  sortBy: TrendSortBy;
  filter: TrendFilter;
  category?: string;
  minEngagement?: number;
  maxResults?: number;
}

// Analytics Types
export interface EngagementMetrics {
  total_views: number;
  total_likes: number;
  total_comments: number;
  total_shares: number;
  avg_engagement_rate: number;
  trend_count: number;
}

export interface TrendAnalytics {
  user_metrics: EngagementMetrics;
  top_categories: Array<{ category: string; count: number }>;
  performance_trends: Array<{ date: string; engagement: number }>;
  viral_potential: number;
}

// API Client Types
export interface APIClientConfig {
  baseURL: string;
  timeout: number;
}

export interface APIError extends Error {
  status?: number;
  code?: string;
  details?: any;
}

// Form Types
export interface ProfileAnalysisForm {
  tiktokUrl: string;
  analyzing: boolean;
  error?: string;
}

export interface TrendsRefreshForm {
  refreshing: boolean;
  maxResults: number;
  error?: string;
}
