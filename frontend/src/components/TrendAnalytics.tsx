import React from 'react';
import {
  BarChart3,
  TrendingUp,
  TrendingDown,
  Activity,
  Eye,
  Heart,
  MessageCircle,
  Share2,
  Calendar,
  Clock,
  Zap,
  Target,
  Users
} from 'lucide-react';
import { TrendItem } from '../types';
import { formatNumber, getRelativeTime } from '../lib/api';
import SectionTitle from './ui/SectionTitle';
import Badge from './ui/Badge';

interface TrendAnalyticsProps {
  trends: TrendItem[];
  className?: string;
}

interface TrendMetrics {
  totalViews: number;
  totalLikes: number;
  totalComments: number;
  totalShares: number;
  avgEngagementRate: number;
  viralTrends: number;
  topCategory: string;
  trendingNow: number;
  growthPotential: number;
  competitiveOpportunity: number;
}

interface TimeSeriesData {
  date: string;
  views: number;
  engagement: number;
  trends: number;
}

const TrendAnalytics: React.FC<TrendAnalyticsProps> = ({ trends, className = '' }) => {
  // Calculate comprehensive trend metrics
  const metrics = React.useMemo((): TrendMetrics => {
    if (trends.length === 0) {
      return {
        totalViews: 0,
        totalLikes: 0,
        totalComments: 0,
        totalShares: 0,
        avgEngagementRate: 0,
        viralTrends: 0,
        topCategory: 'N/A',
        trendingNow: 0,
        growthPotential: 0,
        competitiveOpportunity: 0
      };
    }

    const totalViews = trends.reduce((sum, trend) => sum + (trend.statistics.play_count || 0), 0);
    const totalLikes = trends.reduce((sum, trend) => sum + (trend.statistics.digg_count || 0), 0);
    const totalComments = trends.reduce((sum, trend) => sum + (trend.statistics.comment_count || 0), 0);
    const totalShares = trends.reduce((sum, trend) => sum + (trend.statistics.share_count || 0), 0);
    
    const avgEngagementRate = trends.reduce((sum, trend) => sum + (trend.engagement_rate || 0), 0) / trends.length;
    
    // Calculate viral trends (engagement rate > 8%)
    const viralTrends = trends.filter(trend => (trend.engagement_rate || 0) > 8).length;
    
    // Find top category
    const categoryCount = trends.reduce((acc, trend) => {
      const category = trend.trend_category || 'Uncategorized';
      acc[category] = (acc[category] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);
    
    const topCategory = Object.entries(categoryCount)
      .sort(([,a], [,b]) => b - a)[0]?.[0] || 'N/A';
    
    // Calculate trending now (recent trends with high engagement)
    const now = Date.now();
    const recentThreshold = now - (7 * 24 * 60 * 60 * 1000); // 7 days ago
    const trendingNow = trends.filter(trend => 
      (trend.create_time * 1000) > recentThreshold && (trend.engagement_rate || 0) > 5
    ).length;
    
    // Calculate growth potential (based on relevance scores and trend potential)
    const growthPotential = trends.filter(trend => 
      (trend.relevance_score || 0) > 80 && 
      ['growing', 'stable'].includes(trend.trend_potential || '')
    ).length;
    
    // Calculate competitive opportunity (high views, moderate engagement = opportunity)
    const competitiveOpportunity = trends.filter(trend => 
      (trend.statistics.play_count || 0) > 100000 && 
      (trend.engagement_rate || 0) < 5
    ).length;

    return {
      totalViews,
      totalLikes,
      totalComments,
      totalShares,
      avgEngagementRate,
      viralTrends,
      topCategory,
      trendingNow,
      growthPotential,
      competitiveOpportunity
    };
  }, [trends]);

  // Generate time series data for visualization
  const timeSeriesData = React.useMemo((): TimeSeriesData[] => {
    if (trends.length === 0) return [];

    // Group trends by day
    const groupedByDay = trends.reduce((acc, trend) => {
      const date = new Date(trend.create_time * 1000);
      const dayKey = date.toISOString().split('T')[0];
      
      if (!acc[dayKey]) {
        acc[dayKey] = {
          views: 0,
          engagement: 0,
          count: 0
        };
      }
      
      acc[dayKey].views += trend.statistics.play_count || 0;
      acc[dayKey].engagement += trend.engagement_rate || 0;
      acc[dayKey].count += 1;
      
      return acc;
    }, {} as Record<string, { views: number; engagement: number; count: number }>);

    // Convert to array and calculate averages
    return Object.entries(groupedByDay)
      .map(([date, data]) => ({
        date,
        views: data.views,
        engagement: data.engagement / data.count,
        trends: data.count
      }))
      .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
      .slice(-7); // Last 7 days
  }, [trends]);

  // Performance categories
  const performanceCategories = React.useMemo(() => {
    const categories = trends.reduce((acc, trend) => {
      const category = trend.trend_category || 'Uncategorized';
      if (!acc[category]) {
        acc[category] = {
          count: 0,
          totalViews: 0,
          avgEngagement: 0,
          color: getRandomColor()
        };
      }
      
      acc[category].count += 1;
      acc[category].totalViews += trend.statistics.play_count || 0;
      acc[category].avgEngagement += trend.engagement_rate || 0;
      
      return acc;
    }, {} as Record<string, { count: number; totalViews: number; avgEngagement: number; color: string }>);

    // Calculate averages and sort by performance
    return Object.entries(categories)
      .map(([name, data]) => ({
        name,
        count: data.count,
        totalViews: data.totalViews,
        avgEngagement: data.avgEngagement / data.count,
        color: data.color,
        score: (data.totalViews / 1000000) + (data.avgEngagement * 10) // Composite score
      }))
      .sort((a, b) => b.score - a.score)
      .slice(0, 5);
  }, [trends]);

  function getRandomColor(): string {
    const colors = [
      'bg-blue-500', 'bg-emerald-500', 'bg-purple-500', 
      'bg-orange-500', 'bg-red-500', 'bg-cyan-500', 'bg-yellow-500'
    ];
    return colors[Math.floor(Math.random() * colors.length)];
  }

  // Get trend status
  const getTrendStatus = (value: number, thresholds: { high: number; medium: number }) => {
    if (value >= thresholds.high) return { status: 'High', color: 'text-emerald-400', icon: <TrendingUp className="w-4 h-4" /> };
    if (value >= thresholds.medium) return { status: 'Medium', color: 'text-yellow-400', icon: <Activity className="w-4 h-4" /> };
    return { status: 'Low', color: 'text-red-400', icon: <TrendingDown className="w-4 h-4" /> };
  };

  if (trends.length === 0) {
    return (
      <div className={`card ${className}`}>
        <SectionTitle
          title="Trend Analytics"
          subtitle="No trends data available"
          icon={<BarChart3 className="w-5 h-5" />}
        />
        <div className="text-center py-8 text-dark-400">
          <Activity className="w-12 h-12 mx-auto mb-4" />
          <p>Refresh trends to see analytics</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Key Performance Indicators */}
      <div className="card">
        <SectionTitle
          title="Trend Performance Overview"
          subtitle="Real-time performance metrics"
          icon={<BarChart3 className="w-5 h-5" />}
        />
        
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="bg-dark-700/30 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <Eye className="w-5 h-5 text-blue-400" />
              <Badge variant="neutral" size="sm">{trends.length} trends</Badge>
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {formatNumber(metrics.totalViews)}
            </div>
            <div className="text-sm text-dark-400">Total Views</div>
          </div>
          
          <div className="bg-dark-700/30 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <Heart className="w-5 h-5 text-red-400" />
              <div className="text-emerald-400 text-sm">
                {((metrics.totalLikes / metrics.totalViews) * 100).toFixed(1)}%
              </div>
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {formatNumber(metrics.totalLikes)}
            </div>
            <div className="text-sm text-dark-400">Total Likes</div>
          </div>
          
          <div className="bg-dark-700/30 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <MessageCircle className="w-5 h-5 text-cyan-400" />
              <Zap className="w-4 h-4 text-yellow-400" />
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {(metrics.avgEngagementRate * 100).toFixed(1)}%
            </div>
            <div className="text-sm text-dark-400">Avg Engagement</div>
          </div>
          
          <div className="bg-dark-700/30 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <Target className="w-5 h-5 text-purple-400" />
              <div className="text-emerald-400 text-sm">{metrics.viralTrends} viral</div>
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {metrics.trendingNow}
            </div>
            <div className="text-sm text-dark-400">Trending Now</div>
          </div>
        </div>

        {/* Trend Status Indicators */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            {
              label: 'Viral Potential',
              value: metrics.viralTrends,
              thresholds: { high: 3, medium: 1 }
            },
            {
              label: 'Growth Opportunity',
              value: metrics.growthPotential,
              thresholds: { high: 4, medium: 2 }
            },
            {
              label: 'Competition Gap',
              value: metrics.competitiveOpportunity,
              thresholds: { high: 2, medium: 1 }
            }
          ].map((item, index) => {
            const status = getTrendStatus(item.value, item.thresholds);
            return (
              <div key={index} className="bg-dark-700/20 rounded-lg p-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    {status.icon}
                    <span className="text-sm font-medium text-dark-300">{item.label}</span>
                  </div>
                  <div className={`font-bold ${status.color}`}>
                    {status.status}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Time Series Visualization */}
      {timeSeriesData.length > 0 && (
        <div className="card">
          <SectionTitle
            title="Trend Timeline"
            subtitle="Performance over the last 7 days"
            icon={<Calendar className="w-5 h-5" />}
          />
          
          <div className="space-y-4">
            {/* Engagement Rate Chart */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm font-medium text-dark-300">Daily Engagement Rate</span>
                <Badge variant="primary" size="sm">
                  {(metrics.avgEngagementRate * 100).toFixed(1)}% avg
                </Badge>
              </div>
              
              <div className="h-20 flex items-end justify-between gap-1">
                {timeSeriesData.map((data, index) => {
                  const height = Math.max((data.engagement * 1000), 10); // Scale engagement
                  return (
                    <div
                      key={index}
                      className="flex-1 bg-gradient-to-t from-emerald-600 to-emerald-400 rounded-t transition-all duration-300 hover:from-emerald-500 hover:to-emerald-300"
                      style={{
                        height: `${Math.min(height, 100)}%`,
                        minHeight: '8px'
                      }}
                      title={`${data.date}: ${(data.engagement * 100).toFixed(1)}% engagement`}
                    />
                  );
                })}
              </div>
              
              <div className="flex justify-between mt-2 text-xs text-dark-500">
                <span>{timeSeriesData[0]?.date}</span>
                <span>{timeSeriesData[timeSeriesData.length - 1]?.date}</span>
              </div>
            </div>

            {/* Views Chart */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm font-medium text-dark-300">Daily Views</span>
                <Badge variant="neutral" size="sm">
                  {formatNumber(metrics.totalViews)} total
                </Badge>
              </div>
              
              <div className="h-16 flex items-end justify-between gap-1 overflow-hidden">
                {timeSeriesData.map((data, index) => {
                  const maxViews = Math.max(...timeSeriesData.map(d => d.views));
                  const height = maxViews > 0 ? Math.min(Math.max((data.views / maxViews) * 100, 10), 100) : 10;
                  return (
                    <div
                      key={index}
                      className="flex-1 bg-gradient-to-t from-blue-600 to-blue-400 rounded-t transition-all duration-300 hover:from-blue-500 hover:to-blue-300"
                      style={{
                        height: `${height}%`,
                        minHeight: '4px'
                      }}
                      title={`${data.date}: ${formatNumber(data.views)} views`}
                    />
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Category Performance Analysis */}
      {performanceCategories.length > 0 && (
        <div className="card">
          <SectionTitle
            title="Category Performance"
            subtitle="Top performing content categories"
            icon={<Users className="w-5 h-5" />}
          />
          
          <div className="space-y-3">
            {performanceCategories.map((category, index) => (
              <div key={index} className="bg-dark-700/30 rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className={`w-3 h-3 rounded-full ${category.color}`} />
                    <span className="font-medium text-white">{category.name}</span>
                    <Badge variant="neutral" size="sm">
                      {category.count} trends
                    </Badge>
                  </div>
                  <div className="text-emerald-400 font-bold">
                    {(category.avgEngagement * 100).toFixed(1)}%
                  </div>
                </div>
                
                <div className="flex items-center justify-between text-sm text-dark-400">
                  <span>{formatNumber(category.totalViews)} views</span>
                  <div className="flex items-center gap-1">
                    <TrendingUp className="w-3 h-3" />
                    <span>Score: {category.score.toFixed(1)}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Actionable Insights */}
      <div className="card">
        <SectionTitle
          title="AI Recommendations"
          subtitle="Data-driven content strategy insights"
          icon={<Zap className="w-5 h-5" />}
        />
        
        <div className="space-y-3">
          {metrics.viralTrends > 2 && (
            <div className="flex items-start gap-3 bg-emerald-900/20 rounded-lg p-3 border-l-4 border-emerald-400">
              <TrendingUp className="w-5 h-5 text-emerald-400 mt-0.5 flex-shrink-0" />
              <div>
                <div className="font-medium text-emerald-300 mb-1">High Viral Potential</div>
                <div className="text-sm text-emerald-200">
                  {metrics.viralTrends} trends show viral characteristics. Focus on similar content styles.
                </div>
              </div>
            </div>
          )}
          
          {metrics.competitiveOpportunity > 0 && (
            <div className="flex items-start gap-3 bg-orange-900/20 rounded-lg p-3 border-l-4 border-orange-400">
              <Target className="w-5 h-5 text-orange-400 mt-0.5 flex-shrink-0" />
              <div>
                <div className="font-medium text-orange-300 mb-1">Competition Opportunity</div>
                <div className="text-sm text-orange-200">
                  {metrics.competitiveOpportunity} high-view trends have low engagement - opportunity to create better content.
                </div>
              </div>
            </div>
          )}
          
          {metrics.topCategory !== 'N/A' && (
            <div className="flex items-start gap-3 bg-blue-900/20 rounded-lg p-3 border-l-4 border-blue-400">
              <BarChart3 className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
              <div>
                <div className="font-medium text-blue-300 mb-1">Top Performing Category</div>
                <div className="text-sm text-blue-200">
                  "{metrics.topCategory}" is your strongest category. Consider focusing more content here.
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TrendAnalytics;
