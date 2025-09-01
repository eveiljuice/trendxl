import React from 'react';
import { TrendingUp, TrendingDown, Activity, BarChart3 } from 'lucide-react';
import { TrendItem } from '../types';
import SectionTitle from './ui/SectionTitle';
import Badge from './ui/Badge';

interface TrendsChartProps {
  trends: TrendItem[];
}

const TrendsChart: React.FC<TrendsChartProps> = ({ trends }) => {
  // Calculate analytics from trends data
  const analytics = React.useMemo(() => {
    if (trends.length === 0) return null;

    const totalViews = trends.reduce((sum, trend) => sum + trend.statistics.play_count, 0);
    const totalLikes = trends.reduce((sum, trend) => sum + trend.statistics.digg_count, 0);
    const totalComments = trends.reduce((sum, trend) => sum + trend.statistics.comment_count, 0);
    const totalShares = trends.reduce((sum, trend) => sum + trend.statistics.share_count, 0);

    const avgEngagementRate = trends.reduce((sum, trend) => sum + trend.engagement_rate, 0) / trends.length;

    // Group by categories
    const categoryCount = trends.reduce((acc, trend) => {
      const category = trend.trend_category || 'Uncategorized';
      acc[category] = (acc[category] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const topCategories = Object.entries(categoryCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 5);

    return {
      totalViews,
      totalLikes,
      totalComments,
      totalShares,
      avgEngagementRate,
      topCategories,
      trendCount: trends.length
    };
  }, [trends]);

  if (!analytics) return null;

  // Format large numbers
  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`;
    }
    if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K`;
    }
    return num.toString();
  };

  return (
    <div className="card">
      <SectionTitle
        title="Trend Analytics"
        subtitle="Performance insights from your trends"
        icon={<BarChart3 className="w-5 h-5" />}
      />

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="stat-card">
          <div className="flex items-center gap-2 mb-2">
            <Activity className="w-4 h-4 text-primary-400" />
            <span className="text-sm text-dark-400">Total Views</span>
          </div>
          <div className="text-2xl font-bold text-white">
            {formatNumber(analytics.totalViews)}
          </div>
        </div>

        <div className="stat-card">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-4 h-4 text-red-400" />
            <span className="text-sm text-dark-400">Total Likes</span>
          </div>
          <div className="text-2xl font-bold text-white">
            {formatNumber(analytics.totalLikes)}
          </div>
        </div>

        <div className="stat-card">
          <div className="flex items-center gap-2 mb-2">
            <TrendingDown className="w-4 h-4 text-blue-400" />
            <span className="text-sm text-dark-400">Comments</span>
          </div>
          <div className="text-2xl font-bold text-white">
            {formatNumber(analytics.totalComments)}
          </div>
        </div>

        <div className="stat-card">
          <div className="flex items-center gap-2 mb-2">
            <BarChart3 className="w-4 h-4 text-green-400" />
            <span className="text-sm text-dark-400">Avg Engagement</span>
          </div>
          <div className="text-2xl font-bold text-white">
            {(analytics.avgEngagementRate * 100).toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Category Distribution */}
      {analytics.topCategories.length > 0 && (
        <div className="mb-6">
          <h4 className="text-sm font-medium text-dark-300 mb-3">Top Categories</h4>
          <div className="space-y-2">
            {analytics.topCategories.map(([category, count]) => (
              <div key={category} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Badge variant="primary" size="sm">
                    {category}
                  </Badge>
                  <span className="text-sm text-dark-400">
                    {count} trend{count !== 1 ? 's' : ''}
                  </span>
                </div>
                <div className="flex-1 ml-4">
                  <div className="w-full bg-dark-700 rounded-full h-2 overflow-hidden">
                    <div
                      className="bg-primary-500 h-2 rounded-full transition-all duration-300"
                      style={{
                        width: `${Math.min(Math.max((count / analytics.trendCount) * 100, 2), 100)}%`
                      }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Simple Engagement Chart */}
      {trends.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-dark-300 mb-3">Engagement Trend</h4>
          <div className="h-32 flex items-end justify-between gap-1 overflow-hidden">
            {trends.slice(0, 10).map((trend, index) => {
              const height = Math.min(Math.max((trend.engagement_rate * 100), 10), 100); // Min 10%, max 100%
              return (
                <div
                  key={trend.aweme_id}
                  className="flex-1 bg-gradient-to-t from-primary-600 to-primary-400 rounded-t transition-all duration-300 hover:from-primary-500 hover:to-primary-300"
                  style={{
                    height: `${height}%`,
                    minHeight: '8px'
                  }}
                  title={`${trend.desc.slice(0, 50)}... (${(trend.engagement_rate * 100).toFixed(1)}% engagement)`}
                />
              );
            })}
          </div>
          <div className="flex justify-between mt-2 text-xs text-dark-500">
            <span>Recent</span>
            <span>Latest</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default TrendsChart;
