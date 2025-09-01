import React from 'react';
import {
  TrendingUp,
  TrendingDown,
  Activity,
  Users,
  Heart,
  MessageCircle,
  Calendar,
  Clock,
  Target,
  Star,
  BarChart3
} from 'lucide-react';
import { UserProfile, TrendItem, ProfileAnalysis } from '../types';
import { formatNumber } from '../lib/api';
import SectionTitle from './ui/SectionTitle';
import Stat from './ui/Stat';
import Badge from './ui/Badge';

interface AdvancedMetricsProps {
  profile: UserProfile;
  analysis: ProfileAnalysis;
  trends: TrendItem[];
  userPosts?: any[];
}

interface MetricCard {
  title: string;
  value: number | string;
  change?: number;
  trend?: 'up' | 'down' | 'stable';
  icon: React.ReactNode;
  color: string;
}

const AdvancedMetrics: React.FC<AdvancedMetricsProps> = ({
  profile,
  analysis,
  trends,
  userPosts = []
}) => {
  // Calculate advanced metrics
  const metrics = React.useMemo(() => {
    // Basic calculations
    const followerCount = profile.follower_count || 0;
    const videosCount = profile.video_count || 0;
    const totalLikes = profile.likes_count || 0;
    
    // Engagement calculations
    const avgLikesPerVideo = videosCount > 0 ? totalLikes / videosCount : 0;
    const followerToVideoRatio = videosCount > 0 ? followerCount / videosCount : 0;
    const likesPerFollower = followerCount > 0 ? totalLikes / followerCount : 0;
    
    // Trending content metrics
    const trendCount = trends.length;
    const avgTrendEngagement = trends.length > 0 
      ? trends.reduce((sum, trend) => sum + trend.engagement_rate, 0) / trends.length 
      : 0;
    
    const totalTrendViews = trends.reduce((sum, trend) => sum + trend.statistics.play_count, 0);
    const highEngagementTrends = trends.filter(trend => trend.engagement_rate > 5).length;
    
    // Calculate activity score (synthetic metric based on various factors)
    const activityScore = Math.min(100, 
      (videosCount * 2) + 
      (followerCount / 1000) + 
      (totalLikes / 10000) + 
      (trendCount * 5)
    );
    
    // Calculate growth potential score
    const growthPotential = Math.min(100,
      (avgTrendEngagement * 10) + 
      (highEngagementTrends * 5) + 
      (likesPerFollower * 20)
    );

    return {
      followerCount,
      videosCount,
      totalLikes,
      avgLikesPerVideo,
      followerToVideoRatio,
      likesPerFollower,
      trendCount,
      avgTrendEngagement,
      totalTrendViews,
      highEngagementTrends,
      activityScore,
      growthPotential
    };
  }, [profile, trends]);

  // Performance metrics cards
  const performanceMetrics: MetricCard[] = [
    {
      title: 'Activity Score',
      value: `${metrics.activityScore.toFixed(1)}/100`,
      trend: metrics.activityScore > 50 ? 'up' : metrics.activityScore > 25 ? 'stable' : 'down',
      icon: <Activity className="w-4 h-4" />,
      color: 'text-blue-400'
    },
    {
      title: 'Growth Potential',
      value: `${metrics.growthPotential.toFixed(1)}/100`,
      trend: metrics.growthPotential > 60 ? 'up' : metrics.growthPotential > 30 ? 'stable' : 'down',
      icon: <TrendingUp className="w-4 h-4" />,
      color: 'text-emerald-400'
    },
    {
      title: 'Avg Likes/Video',
      value: formatNumber(metrics.avgLikesPerVideo),
      trend: metrics.avgLikesPerVideo > 1000 ? 'up' : 'stable',
      icon: <Heart className="w-4 h-4" />,
      color: 'text-red-400'
    },
    {
      title: 'Follower Efficiency',
      value: `${(metrics.likesPerFollower * 100).toFixed(1)}%`,
      trend: metrics.likesPerFollower > 0.1 ? 'up' : 'stable',
      icon: <Target className="w-4 h-4" />,
      color: 'text-purple-400'
    }
  ];

  // Trend analysis metrics
  const trendMetrics: MetricCard[] = [
    {
      title: 'Relevant Trends',
      value: metrics.trendCount,
      icon: <BarChart3 className="w-4 h-4" />,
      color: 'text-orange-400'
    },
    {
      title: 'Avg Trend Engagement',
      value: `${(metrics.avgTrendEngagement * 100).toFixed(1)}%`,
      trend: metrics.avgTrendEngagement > 0.05 ? 'up' : 'stable',
      icon: <MessageCircle className="w-4 h-4" />,
      color: 'text-cyan-400'
    },
    {
      title: 'High Engagement Trends',
      value: metrics.highEngagementTrends,
      icon: <Star className="w-4 h-4" />,
      color: 'text-yellow-400'
    },
    {
      title: 'Total Trend Views',
      value: formatNumber(metrics.totalTrendViews),
      icon: <Users className="w-4 h-4" />,
      color: 'text-indigo-400'
    }
  ];

  const getTrendIcon = (trend?: 'up' | 'down' | 'stable') => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-3 h-3 text-emerald-400" />;
      case 'down':
        return <TrendingDown className="w-3 h-3 text-red-400" />;
      default:
        return <Activity className="w-3 h-3 text-yellow-400" />;
    }
  };

  // Niche-specific insights
  const getNicheInsights = (): string[] => {
    const insights: string[] = [];

    if (metrics.avgTrendEngagement > 0.08) {
      insights.push("High engagement potential in your niche");
    }
    
    if (metrics.highEngagementTrends > 3) {
      insights.push("Multiple viral opportunities identified");
    }
    
    if (metrics.likesPerFollower > 0.15) {
      insights.push("Strong audience loyalty indicators");
    }
    
    if (metrics.followerToVideoRatio > 1000) {
      insights.push("High follower-to-content ratio - consistent posting recommended");
    }

    return insights;
  };

  return (
    <div className="space-y-6">
      {/* Performance Metrics */}
      <div className="card">
        <SectionTitle
          title="Performance Analytics"
          subtitle="Comprehensive profile performance metrics"
          icon={<BarChart3 className="w-5 h-5" />}
        />
        
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {performanceMetrics.map((metric, index) => (
            <div key={index} className="bg-dark-700/30 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <div className={`${metric.color}`}>
                  {metric.icon}
                </div>
                {metric.trend && getTrendIcon(metric.trend)}
              </div>
              <div className="text-2xl font-bold text-white mb-1">
                {metric.value}
              </div>
              <div className="text-sm text-dark-400">
                {metric.title}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Trend Analysis Metrics */}
      <div className="card">
        <SectionTitle
          title="Trend Analysis"
          subtitle="Performance of relevant trending content"
          icon={<TrendingUp className="w-5 h-5" />}
        />
        
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {trendMetrics.map((metric, index) => (
            <div key={index} className="bg-dark-700/30 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <div className={`${metric.color}`}>
                  {metric.icon}
                </div>
                {metric.trend && getTrendIcon(metric.trend)}
              </div>
              <div className="text-2xl font-bold text-white mb-1">
                {metric.value}
              </div>
              <div className="text-sm text-dark-400">
                {metric.title}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Engagement Distribution */}
      <div className="card">
        <SectionTitle
          title="Engagement Distribution"
          subtitle="How your content resonates with audiences"
          icon={<Heart className="w-5 h-5" />}
        />
        
        <div className="space-y-4">
          {/* Engagement Rate Visualization */}
          <div className="bg-dark-700/30 rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-medium text-dark-300">Average Engagement Rate</span>
              <Badge variant="primary" size="sm">
                {(metrics.avgTrendEngagement * 100).toFixed(1)}%
              </Badge>
            </div>
            <div className="w-full bg-dark-600 rounded-full h-3 overflow-hidden">
              <div 
                className="bg-gradient-to-r from-primary-500 to-emerald-500 h-3 rounded-full transition-all duration-500"
                style={{ width: `${Math.min(Math.max(metrics.avgTrendEngagement * 100, 5), 100)}%` }}
              />
            </div>
          </div>

          {/* Activity Timeline */}
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-dark-700/30 rounded-lg p-3 text-center">
              <div className="text-lg font-bold text-emerald-400 mb-1">
                {metrics.videosCount}
              </div>
              <div className="text-xs text-dark-400">Total Videos</div>
            </div>
            <div className="bg-dark-700/30 rounded-lg p-3 text-center">
              <div className="text-lg font-bold text-blue-400 mb-1">
                {formatNumber(metrics.followerCount)}
              </div>
              <div className="text-xs text-dark-400">Followers</div>
            </div>
            <div className="bg-dark-700/30 rounded-lg p-3 text-center">
              <div className="text-lg font-bold text-red-400 mb-1">
                {formatNumber(metrics.totalLikes)}
              </div>
              <div className="text-xs text-dark-400">Total Likes</div>
            </div>
          </div>
        </div>
      </div>

      {/* Niche-Specific Insights */}
      {getNicheInsights().length > 0 && (
        <div className="card">
          <SectionTitle
            title="AI Insights"
            subtitle={`Insights specific to ${analysis.niche} niche`}
            icon={<Target className="w-5 h-5" />}
          />
          
          <div className="space-y-3">
            {getNicheInsights().map((insight, index) => (
              <div key={index} className="flex items-start gap-3 bg-dark-700/30 rounded-lg p-3">
                <div className="w-2 h-2 bg-emerald-400 rounded-full mt-2 flex-shrink-0" />
                <span className="text-sm text-dark-200 leading-relaxed">
                  {insight}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Quick Stats Summary */}
      <div className="card">
        <SectionTitle
          title="Quick Summary"
          subtitle="Key performance indicators at a glance"
          icon={<Clock className="w-5 h-5" />}
        />
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-3">
            <Stat
              label="Content Consistency"
              value={metrics.followerToVideoRatio > 500 ? "High" : metrics.followerToVideoRatio > 100 ? "Medium" : "Low"}
              icon={<Calendar className="w-4 h-4" />}
            />
            <Stat
              label="Audience Loyalty"
              value={metrics.likesPerFollower > 0.1 ? "Strong" : metrics.likesPerFollower > 0.05 ? "Moderate" : "Developing"}
              icon={<Users className="w-4 h-4" />}
            />
          </div>
          
          <div className="space-y-3">
            <Stat
              label="Viral Potential"
              value={metrics.highEngagementTrends > 2 ? "High" : metrics.highEngagementTrends > 0 ? "Medium" : "Low"}
              icon={<Star className="w-4 h-4" />}
            />
            <Stat
              label="Trend Alignment"
              value={metrics.trendCount > 5 ? "Excellent" : metrics.trendCount > 2 ? "Good" : "Needs Improvement"}
              icon={<Target className="w-4 h-4" />}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdvancedMetrics;
