import React, { useState, useEffect } from 'react';
import {
  BarChart3,
  TrendingUp,
  Loader2,
  AlertTriangle,
  RefreshCw,
  Activity,
  Target,
  Zap
} from 'lucide-react';
import { UserProfile, ProfileAnalysis, TrendItem } from '../types';
import SectionTitle from './ui/SectionTitle';
import AdvancedMetrics from './AdvancedMetrics';
import TrendAnalytics from './TrendAnalytics';
import Badge from './ui/Badge';

interface ProfileAnalyticsProps {
  profile: UserProfile;
  analysis: ProfileAnalysis;
  trends: TrendItem[];
}

interface ProfileMetricsData {
  overview: {
    total_posts_analyzed: number;
    total_views: number;
    total_likes: number;
    total_comments: number;
    total_shares: number;
    avg_views_per_post: number;
    avg_likes_per_post: number;
    avg_engagement_rate: number;
  };
  performance: {
    consistency_score: number;
    viral_posts: number;
    high_engagement_posts: number;
    best_performing_post_views: number;
    engagement_variance: number;
  };
  content_analysis: {
    hashtag_diversity: number;
    top_hashtags: Array<[string, number]>;
    posting_patterns: {
      peak_posting_hour?: number;
      peak_posting_day?: string;
      posting_frequency?: number;
      hourly_distribution?: Record<string, number>;
      daily_distribution?: Record<string, number>;
    };
  };
  growth_indicators: {
    viral_potential: number;
    audience_loyalty: number;
    content_quality_score: number;
  };
}

interface TrendAnalyticsData {
  overview: {
    total_trends: number;
    total_views: number;
    total_likes: number;
    avg_engagement_rate: number;
  };
  performance: {
    high_relevance_trends: number;
    viral_potential: number;
    growth_opportunity: number;
    recent_trends: number;
  };
  categories: Record<string, {
    count: number;
    avg_engagement: number;
    total_views: number;
    high_relevance: number;
  }>;
  engagement_distribution: {
    high: number;
    medium: number;
    low: number;
  };
}

interface Recommendation {
  type: 'opportunity' | 'viral' | 'category' | 'growth' | 'improvement';
  title: string;
  message: string;
}

const ProfileAnalytics: React.FC<ProfileAnalyticsProps> = ({
  profile,
  analysis,
  trends
}) => {
  const [profileMetrics, setProfileMetrics] = useState<ProfileMetricsData | null>(null);
  const [trendAnalytics, setTrendAnalytics] = useState<TrendAnalyticsData | null>(null);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  // Fetch profile metrics
  const fetchProfileMetrics = async () => {
    try {
      const response = await fetch(`/api/v1/analytics/profile-metrics/${profile.username}`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      if (data.success) {
        setProfileMetrics(data.metrics);
      } else {
        throw new Error(data.message || 'Failed to fetch profile metrics');
      }
    } catch (err) {
      console.error('Error fetching profile metrics:', err);
      throw err;
    }
  };

  // Fetch trend analytics
  const fetchTrendAnalytics = async () => {
    try {
      const response = await fetch(`/api/v1/analytics/trend-analytics?username=${profile.username}`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      if (data.success) {
        setTrendAnalytics(data.analytics);
        setRecommendations(data.recommendations || []);
      } else {
        throw new Error(data.message || 'Failed to fetch trend analytics');
      }
    } catch (err) {
      console.error('Error fetching trend analytics:', err);
      throw err;
    }
  };

  // Load analytics data
  const loadAnalytics = async () => {
    setLoading(true);
    setError(null);
    
    try {
      await Promise.all([
        fetchProfileMetrics(),
        fetchTrendAnalytics()
      ]);
      setLastUpdated(new Date());
    } catch (err: any) {
      setError(err.message || 'Failed to load analytics data');
    } finally {
      setLoading(false);
    }
  };

  // Load analytics on mount
  useEffect(() => {
    if (profile.username) {
      loadAnalytics();
    }
  }, [profile.username]);

  // Get analytics status
  const getAnalyticsStatus = () => {
    if (loading) return { status: 'loading', message: 'Loading analytics...' };
    if (error) return { status: 'error', message: error };
    if (!profileMetrics || !trendAnalytics) return { status: 'empty', message: 'No analytics data available' };
    return { status: 'success', message: 'Analytics loaded successfully' };
  };

  const status = getAnalyticsStatus();

  // Render loading state
  if (loading) {
    return (
      <div className="card">
        <SectionTitle
          title="Advanced Analytics"
          subtitle="Loading comprehensive profile insights..."
          icon={<BarChart3 className="w-5 h-5" />}
        />
        
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <Loader2 className="w-8 h-8 animate-spin text-primary-400 mx-auto mb-4" />
            <p className="text-dark-400">Analyzing profile and trends...</p>
          </div>
        </div>
      </div>
    );
  }

  // Render error state
  if (error && !profileMetrics && !trendAnalytics) {
    return (
      <div className="card">
        <SectionTitle
          title="Advanced Analytics"
          subtitle="Error loading analytics data"
          icon={<AlertTriangle className="w-5 h-5 text-red-400" />}
        />
        
        <div className="text-center py-8">
          <AlertTriangle className="w-12 h-12 text-red-400 mx-auto mb-4" />
          <p className="text-red-300 mb-4">{error}</p>
          <button
            onClick={loadAnalytics}
            className="btn btn-secondary flex items-center gap-2"
          >
            <RefreshCw className="w-4 h-4" />
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Analytics Header */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <SectionTitle
            title="Advanced Analytics"
            subtitle={`Comprehensive analysis for @${profile.username}`}
            icon={<BarChart3 className="w-5 h-5" />}
          />
          
          <div className="flex items-center gap-3">
            {lastUpdated && (
              <span className="text-sm text-dark-400">
                Updated {lastUpdated.toLocaleTimeString()}
              </span>
            )}
            <button
              onClick={loadAnalytics}
              disabled={loading}
              className="btn btn-secondary btn-sm flex items-center gap-2"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </button>
          </div>
        </div>

        {/* Quick Overview Cards */}
        {profileMetrics && (
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-dark-700/30 rounded-lg p-4 text-center">
              <Activity className="w-6 h-6 text-blue-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white mb-1">
                {profileMetrics.growth_indicators.content_quality_score.toFixed(1)}
              </div>
              <div className="text-sm text-dark-400">Content Quality</div>
            </div>
            
            <div className="bg-dark-700/30 rounded-lg p-4 text-center">
              <TrendingUp className="w-6 h-6 text-emerald-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white mb-1">
                {profileMetrics.growth_indicators.viral_potential.toFixed(1)}%
              </div>
              <div className="text-sm text-dark-400">Viral Potential</div>
            </div>
            
            <div className="bg-dark-700/30 rounded-lg p-4 text-center">
              <Target className="w-6 h-6 text-purple-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white mb-1">
                {profileMetrics.performance.consistency_score.toFixed(1)}
              </div>
              <div className="text-sm text-dark-400">Consistency</div>
            </div>
            
            <div className="bg-dark-700/30 rounded-lg p-4 text-center">
              <Zap className="w-6 h-6 text-yellow-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white mb-1">
                {trendAnalytics?.performance?.high_relevance_trends || 0}
              </div>
              <div className="text-sm text-dark-400">Relevant Trends</div>
            </div>
          </div>
        )}

        {/* Status Badge */}
        <div className="mt-4">
          <Badge 
            variant={status.status === 'success' ? 'success' : status.status === 'error' ? 'danger' : 'neutral'}
            size="sm"
          >
            {status.message}
          </Badge>
        </div>
      </div>

      {/* AI Recommendations */}
      {recommendations.length > 0 && (
        <div className="card">
          <SectionTitle
            title="AI Recommendations"
            subtitle="Strategic insights based on your analytics"
            icon={<Zap className="w-5 h-5" />}
          />
          
          <div className="space-y-3">
            {recommendations.map((rec, index) => (
              <div
                key={index}
                className={`p-4 rounded-lg border-l-4 ${
                  rec.type === 'viral' ? 'bg-red-900/20 border-red-400' :
                  rec.type === 'opportunity' ? 'bg-emerald-900/20 border-emerald-400' :
                  rec.type === 'growth' ? 'bg-blue-900/20 border-blue-400' :
                  rec.type === 'category' ? 'bg-purple-900/20 border-purple-400' :
                  'bg-orange-900/20 border-orange-400'
                }`}
              >
                <div className="flex items-start gap-3">
                  <div className={`mt-1 ${
                    rec.type === 'viral' ? 'text-red-400' :
                    rec.type === 'opportunity' ? 'text-emerald-400' :
                    rec.type === 'growth' ? 'text-blue-400' :
                    rec.type === 'category' ? 'text-purple-400' :
                    'text-orange-400'
                  }`}>
                    {rec.type === 'viral' && <TrendingUp className="w-5 h-5" />}
                    {rec.type === 'opportunity' && <Target className="w-5 h-5" />}
                    {rec.type === 'growth' && <Activity className="w-5 h-5" />}
                    {rec.type === 'category' && <BarChart3 className="w-5 h-5" />}
                    {rec.type === 'improvement' && <Zap className="w-5 h-5" />}
                  </div>
                  
                  <div className="flex-1">
                    <div className={`font-medium mb-1 ${
                      rec.type === 'viral' ? 'text-red-300' :
                      rec.type === 'opportunity' ? 'text-emerald-300' :
                      rec.type === 'growth' ? 'text-blue-300' :
                      rec.type === 'category' ? 'text-purple-300' :
                      'text-orange-300'
                    }`}>
                      {rec.title}
                    </div>
                    <div className={`text-sm ${
                      rec.type === 'viral' ? 'text-red-200' :
                      rec.type === 'opportunity' ? 'text-emerald-200' :
                      rec.type === 'growth' ? 'text-blue-200' :
                      rec.type === 'category' ? 'text-purple-200' :
                      'text-orange-200'
                    }`}>
                      {rec.message}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Advanced Metrics Component */}
      {profileMetrics && (
        <AdvancedMetrics
          profile={profile}
          analysis={analysis}
          trends={trends}
          userPosts={[]} // This would come from API if needed
        />
      )}

      {/* Trend Analytics Component */}
      <TrendAnalytics 
        trends={trends}
      />

      {/* Footer */}
      {lastUpdated && (
        <div className="text-center text-sm text-dark-500">
          Analytics last updated: {lastUpdated.toLocaleString()}
        </div>
      )}
    </div>
  );
};

export default ProfileAnalytics;
