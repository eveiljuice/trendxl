import React, { useMemo } from 'react';
import {
  Activity,
  TrendingUp,
  Heart,
  MessageCircle,
  Share2,
  Eye,
  Target,
  Zap,
  BarChart3,
  ArrowRight,
  Info,
  Lightbulb
} from 'lucide-react';
import { TrendItem } from '../types';
import SectionTitle from './ui/SectionTitle';
import Badge from './ui/Badge';

interface MetricsCorrelationAnalysisProps {
  trends: TrendItem[];
}

interface CorrelationInsight {
  metric1: string;
  metric2: string;
  correlation: number;
  strength: 'strong' | 'moderate' | 'weak';
  insight: string;
  actionable_advice: string;
  icon1: React.ReactNode;
  icon2: React.ReactNode;
}

interface MetricImportance {
  metric: string;
  importance_score: number;
  impact_on_success: number;
  optimization_potential: number;
  current_performance: number;
  benchmark: number;
  recommendations: string[];
  icon: React.ReactNode;
}

const MetricsCorrelationAnalysis: React.FC<MetricsCorrelationAnalysisProps> = ({ trends }) => {
  // Calculate correlation insights
  const correlationInsights = useMemo((): CorrelationInsight[] => {
    if (trends.length < 5) return [];

    // Extract metrics for correlation analysis
    const metrics = trends.map(trend => ({
      views: trend.statistics.play_count,
      likes: trend.statistics.digg_count,
      comments: trend.statistics.comment_count,
      shares: trend.statistics.share_count,
      engagement_rate: trend.engagement_rate,
      relevance_score: trend.relevance_score || 0
    }));

    // Calculate correlation coefficients
    const calculateCorrelation = (x: number[], y: number[]): number => {
      const n = x.length;
      const sumX = x.reduce((a, b) => a + b, 0);
      const sumY = y.reduce((a, b) => a + b, 0);
      const sumXY = x.reduce((sum, xi, i) => sum + xi * y[i], 0);
      const sumX2 = x.reduce((sum, xi) => sum + xi * xi, 0);
      const sumY2 = y.reduce((sum, yi) => sum + yi * yi, 0);

      const numerator = n * sumXY - sumX * sumY;
      const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));
      
      return denominator === 0 ? 0 : numerator / denominator;
    };

    const getCorrelationStrength = (correlation: number): 'strong' | 'moderate' | 'weak' => {
      const abs = Math.abs(correlation);
      if (abs >= 0.7) return 'strong';
      if (abs >= 0.4) return 'moderate';
      return 'weak';
    };

    const views = metrics.map(m => m.views);
    const likes = metrics.map(m => m.likes);
    const comments = metrics.map(m => m.comments);
    const shares = metrics.map(m => m.shares);
    const engagement = metrics.map(m => m.engagement_rate);
    const relevance = metrics.map(m => m.relevance_score);

    return [
      {
        metric1: 'Views',
        metric2: 'Engagement Rate',
        correlation: calculateCorrelation(views, engagement),
        strength: getCorrelationStrength(calculateCorrelation(views, engagement)),
        insight: 'Higher view counts correlate with engagement rates, indicating content quality drives both metrics.',
        actionable_advice: 'Focus on creating compelling hooks and maintaining viewer interest throughout the video.',
        icon1: <Eye className="w-4 h-4" />,
        icon2: <Activity className="w-4 h-4" />
      },
      {
        metric1: 'Likes',
        metric2: 'Comments',
        correlation: calculateCorrelation(likes, comments),
        strength: getCorrelationStrength(calculateCorrelation(likes, comments)),
        insight: 'Likes and comments show strong positive correlation, suggesting content that resonates emotionally.',
        actionable_advice: 'Include discussion prompts and controversial but respectful topics to boost both metrics.',
        icon1: <Heart className="w-4 h-4" />,
        icon2: <MessageCircle className="w-4 h-4" />
      },
      {
        metric1: 'Relevance Score',
        metric2: 'Shares',
        correlation: calculateCorrelation(relevance, shares),
        strength: getCorrelationStrength(calculateCorrelation(relevance, shares)),
        insight: 'Content relevance directly impacts share behavior, showing audience value perception.',
        actionable_advice: 'Align content closely with trending topics and audience interests for maximum shareability.',
        icon1: <Target className="w-4 h-4" />,
        icon2: <Share2 className="w-4 h-4" />
      },
      {
        metric1: 'Comments',
        metric2: 'Shares',
        correlation: calculateCorrelation(comments, shares),
        strength: getCorrelationStrength(calculateCorrelation(comments, shares)),
        insight: 'Videos that spark discussion are more likely to be shared, amplifying organic reach.',
        actionable_advice: 'Create content that invites opinions, questions, or personal experiences sharing.',
        icon1: <MessageCircle className="w-4 h-4" />,
        icon2: <Share2 className="w-4 h-4" />
      }
    ].filter(insight => Math.abs(insight.correlation) > 0.2); // Only show meaningful correlations
  }, [trends]);

  // Calculate metric importance
  const metricImportance = useMemo((): MetricImportance[] => {
    if (trends.length === 0) return [];

    // Calculate averages and performance metrics
    const avgViews = trends.reduce((sum, trend) => sum + trend.statistics.play_count, 0) / trends.length;
    const avgLikes = trends.reduce((sum, trend) => sum + trend.statistics.digg_count, 0) / trends.length;
    const avgComments = trends.reduce((sum, trend) => sum + trend.statistics.comment_count, 0) / trends.length;
    const avgShares = trends.reduce((sum, trend) => sum + trend.statistics.share_count, 0) / trends.length;
    const avgEngagement = trends.reduce((sum, trend) => sum + trend.engagement_rate, 0) / trends.length;

    // Industry benchmarks (example values - would come from API in real app)
    const benchmarks = {
      engagement_rate: 0.06, // 6% is good for TikTok
      likes_to_views_ratio: 0.05, // 5% like rate
      comments_to_views_ratio: 0.01, // 1% comment rate
      shares_to_views_ratio: 0.005 // 0.5% share rate
    };

    return [
      {
        metric: 'Engagement Rate',
        importance_score: 95,
        impact_on_success: 90,
        optimization_potential: avgEngagement < benchmarks.engagement_rate ? 85 : 40,
        current_performance: (avgEngagement / benchmarks.engagement_rate) * 100,
        benchmark: benchmarks.engagement_rate * 100,
        recommendations: [
          'Use strong hooks in first 3 seconds',
          'Include trending sounds and effects',
          'Ask questions to encourage interaction',
          'Post during peak audience hours'
        ],
        icon: <Activity className="w-5 h-5" />
      },
      {
        metric: 'View-to-Like Ratio',
        importance_score: 80,
        impact_on_success: 75,
        optimization_potential: (avgLikes / avgViews) < benchmarks.likes_to_views_ratio ? 70 : 30,
        current_performance: ((avgLikes / avgViews) / benchmarks.likes_to_views_ratio) * 100,
        benchmark: benchmarks.likes_to_views_ratio * 100,
        recommendations: [
          'Create emotionally resonant content',
          'Use clear calls-to-action for likes',
          'Deliver valuable or entertaining content',
          'Maintain consistent quality standards'
        ],
        icon: <Heart className="w-5 h-5" />
      },
      {
        metric: 'Comment Engagement',
        importance_score: 85,
        impact_on_success: 80,
        optimization_potential: (avgComments / avgViews) < benchmarks.comments_to_views_ratio ? 75 : 35,
        current_performance: ((avgComments / avgViews) / benchmarks.comments_to_views_ratio) * 100,
        benchmark: benchmarks.comments_to_views_ratio * 100,
        recommendations: [
          'End videos with discussion questions',
          'Share controversial but respectful opinions',
          'Respond to comments to boost algorithm',
          'Create content that sparks debate'
        ],
        icon: <MessageCircle className="w-5 h-5" />
      },
      {
        metric: 'Share Rate',
        importance_score: 90,
        impact_on_success: 95,
        optimization_potential: (avgShares / avgViews) < benchmarks.shares_to_views_ratio ? 80 : 25,
        current_performance: ((avgShares / avgViews) / benchmarks.shares_to_views_ratio) * 100,
        benchmark: benchmarks.shares_to_views_ratio * 100,
        recommendations: [
          'Create highly relatable content',
          'Use trending formats and challenges',
          'Make content worth sharing with friends',
          'Include shareable moments or quotes'
        ],
        icon: <Share2 className="w-5 h-5" />
      }
    ].sort((a, b) => b.importance_score - a.importance_score);
  }, [trends]);

  const getCorrelationColor = (strength: string) => {
    switch (strength) {
      case 'strong': return 'text-emerald-400 border-emerald-400';
      case 'moderate': return 'text-yellow-400 border-yellow-400';
      case 'weak': return 'text-red-400 border-red-400';
      default: return 'text-gray-400 border-gray-400';
    }
  };

  const getPerformanceColor = (score: number) => {
    if (score >= 100) return 'text-emerald-400';
    if (score >= 80) return 'text-yellow-400';
    if (score >= 60) return 'text-orange-400';
    return 'text-red-400';
  };

  const getOptimizationUrgency = (potential: number) => {
    if (potential >= 70) return { level: 'High', color: 'bg-red-900/20 border-red-400 text-red-300' };
    if (potential >= 50) return { level: 'Medium', color: 'bg-yellow-900/20 border-yellow-400 text-yellow-300' };
    return { level: 'Low', color: 'bg-emerald-900/20 border-emerald-400 text-emerald-300' };
  };

  if (trends.length < 3) {
    return (
      <div className="card">
        <SectionTitle
          title="Metrics Correlation Analysis"
          subtitle="Need more trend data for correlation analysis"
          icon={<BarChart3 className="w-5 h-5" />}
        />
        <div className="text-center py-8">
          <Info className="w-12 h-12 text-dark-600 mx-auto mb-4" />
          <p className="text-dark-400">
            Correlation analysis requires at least 3 trends. 
            Refresh trends to get more data for comprehensive insights.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Metric Importance Ranking */}
      <div className="card">
        <SectionTitle
          title="Metric Importance Analysis"
          subtitle="Which metrics matter most for your success"
          icon={<Target className="w-5 h-5" />}
        />

        <div className="space-y-4">
          {metricImportance.map((metric, index) => {
            const urgency = getOptimizationUrgency(metric.optimization_potential);
            
            return (
              <div key={index} className="bg-dark-700/30 rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="text-primary-400">{metric.icon}</div>
                    <div>
                      <h4 className="font-semibold text-white">{metric.metric}</h4>
                      <div className="flex items-center gap-4 text-sm">
                        <span className="text-dark-400">
                          Importance: <span className="text-primary-400 font-medium">{metric.importance_score}/100</span>
                        </span>
                        <span className="text-dark-400">
                          Impact: <span className="text-emerald-400 font-medium">{metric.impact_on_success}/100</span>
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <div className={`text-lg font-bold ${getPerformanceColor(metric.current_performance)}`}>
                      {metric.current_performance.toFixed(1)}%
                    </div>
                    <div className="text-sm text-dark-400">vs benchmark</div>
                  </div>
                </div>

                {/* Performance Bar */}
                <div className="mb-3">
                  <div className="flex justify-between text-sm text-dark-400 mb-1">
                    <span>Current Performance</span>
                    <span>Benchmark: {metric.benchmark.toFixed(2)}%</span>
                  </div>
                  <div className="w-full bg-dark-600 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${
                        metric.current_performance >= 100 ? 'bg-emerald-500' :
                        metric.current_performance >= 80 ? 'bg-yellow-500' :
                        'bg-red-500'
                      }`}
                      style={{ width: `${Math.min(metric.current_performance, 100)}%` }}
                    />
                  </div>
                </div>

                {/* Optimization Urgency */}
                <div className={`rounded-lg p-3 border-l-4 ${urgency.color} mb-3`}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium">Optimization Priority</span>
                    <Badge variant={urgency.level === 'High' ? 'danger' : urgency.level === 'Medium' ? 'warning' : 'success'} size="sm">
                      {urgency.level}
                    </Badge>
                  </div>
                  <div className="text-sm opacity-90">
                    Improvement potential: {metric.optimization_potential.toFixed(0)}%
                  </div>
                </div>

                {/* Recommendations */}
                <div>
                  <h5 className="text-sm font-medium text-white mb-2">Optimization Recommendations:</h5>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {metric.recommendations.map((rec, idx) => (
                      <div key={idx} className="flex items-center gap-2 text-sm text-dark-300 bg-dark-800/50 rounded px-3 py-2">
                        <Zap className="w-3 h-3 text-yellow-400 flex-shrink-0" />
                        <span>{rec}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Correlation Insights */}
      <div className="card">
        <SectionTitle
          title="Metrics Correlation Insights"
          subtitle="Understanding relationships between your performance metrics"
          icon={<Activity className="w-5 h-5" />}
        />

        {correlationInsights.length === 0 ? (
          <div className="text-center py-8">
            <Info className="w-12 h-12 text-dark-600 mx-auto mb-4" />
            <p className="text-dark-400">
              No significant correlations found. This might indicate inconsistent performance patterns.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {correlationInsights.map((insight, index) => (
              <div key={index} className={`border-l-4 rounded-lg p-4 bg-dark-700/30 ${getCorrelationColor(insight.strength)}`}>
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="flex items-center gap-2 text-white">
                      <div className="flex items-center gap-1">
                        {insight.icon1}
                        <span className="font-medium">{insight.metric1}</span>
                      </div>
                      <ArrowRight className="w-4 h-4 text-dark-400" />
                      <div className="flex items-center gap-1">
                        {insight.icon2}
                        <span className="font-medium">{insight.metric2}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <div className={`text-lg font-bold ${getCorrelationColor(insight.strength).split(' ')[0]}`}>
                      {(insight.correlation * 100).toFixed(0)}%
                    </div>
                    <Badge 
                      variant={insight.strength === 'strong' ? 'success' : insight.strength === 'moderate' ? 'warning' : 'danger'}
                      size="sm"
                    >
                      {insight.strength}
                    </Badge>
                  </div>
                </div>

                <div className="space-y-2">
                  <p className="text-dark-200 text-sm leading-relaxed">
                    <strong>Insight:</strong> {insight.insight}
                  </p>
                  <div className="bg-dark-800/50 rounded-lg p-3">
                    <div className="flex items-start gap-2">
                      <Lightbulb className="w-4 h-4 text-yellow-400 mt-0.5 flex-shrink-0" />
                      <div>
                        <div className="text-sm font-medium text-yellow-300 mb-1">Actionable Advice:</div>
                        <div className="text-sm text-yellow-200">{insight.actionable_advice}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Summary and Next Steps */}
      <div className="card">
        <SectionTitle
          title="Strategic Recommendations"
          subtitle="Priority actions based on correlation analysis"
          icon={<TrendingUp className="w-5 h-5" />}
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-emerald-900/20 rounded-lg p-4 border border-emerald-800">
            <div className="flex items-center gap-2 mb-3">
              <Target className="w-5 h-5 text-emerald-400" />
              <h4 className="font-semibold text-emerald-300">Focus Areas</h4>
            </div>
            <div className="space-y-2">
              {metricImportance.slice(0, 2).map((metric, idx) => (
                <div key={idx} className="text-sm text-emerald-200">
                  • Optimize {metric.metric.toLowerCase()} ({metric.optimization_potential.toFixed(0)}% potential)
                </div>
              ))}
            </div>
          </div>

          <div className="bg-blue-900/20 rounded-lg p-4 border border-blue-800">
            <div className="flex items-center gap-2 mb-3">
              <Zap className="w-5 h-5 text-blue-400" />
              <h4 className="font-semibold text-blue-300">Quick Wins</h4>
            </div>
            <div className="space-y-2 text-sm text-blue-200">
              <div>• Improve content hooks for better engagement</div>
              <div>• Use trending sounds and hashtags</div>
              <div>• Post during peak audience hours</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MetricsCorrelationAnalysis;
