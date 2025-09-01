import React, { useState, useEffect, useMemo, useCallback } from 'react';
import {
  Target,
  TrendingUp,
  Hash,
  Users,
  Star,
  BarChart3,
  Lightbulb,
  PlayCircle,
  Clock,
  Heart,
  Eye,
  Award,
  ArrowRight,
  ChevronDown,
  ChevronRight
} from 'lucide-react';
import { UserProfile, ProfileAnalysis, TrendItem } from '../types';
import SectionTitle from './ui/SectionTitle';
import Badge from './ui/Badge';
import MetricsCorrelationAnalysis from './MetricsCorrelationAnalysis';

interface NicheAnalyzerProps {
  profile: UserProfile;
  analysis: ProfileAnalysis;
  trends: TrendItem[];
}

interface KeywordAnalysis {
  keyword: string;
  relevance_score: number;
  trend_potential: number;
  competition_level: 'low' | 'medium' | 'high';
  search_volume: number;
  engagement_correlation: number;
  seasonal_trends: Array<{ month: string; popularity: number }>;
  related_hashtags: string[];
  success_examples: Array<{
    video_id: string;
    description: string;
    views: number;
    engagement_rate: number;
  }>;
}

interface NicheInsights {
  primary_niche: string;
  niche_saturation: number;
  growth_opportunity: number;
  key_demographics: {
    age_groups: Array<{ range: string; percentage: number }>;
    interests: string[];
    peak_activity_hours: number[];
    geographic_hotspots: string[];
  };
  content_gaps: Array<{
    topic: string;
    opportunity_score: number;
    explanation: string;
    suggested_approach: string;
  }>;
  competitive_analysis: {
    top_creators: Array<{
      username: string;
      followers: number;
      avg_views: number;
      content_style: string;
      unique_selling_point: string;
    }>;
    market_position: 'leader' | 'challenger' | 'follower' | 'niche_player';
    differentiation_opportunities: string[];
  };
}

interface VideoIdeaRecommendation {
  id: string;
  title: string;
  concept: string;
  target_keywords: string[];
  estimated_reach: number;
  difficulty_score: number;
  trending_factor: number;
  optimal_timing: {
    best_days: string[];
    best_hours: number[];
    seasonal_relevance: string;
  };
  content_structure: {
    hook_suggestions: string[];
    key_elements: string[];
    call_to_action: string;
    optimal_duration: string;
  };
  success_probability: number;
  supporting_data: {
    similar_video_performance: Array<{
      views: number;
      engagement_rate: number;
      description: string;
    }>;
    trend_evidence: string[];
    audience_interest_indicators: string[];
  };
}

const NicheAnalyzer: React.FC<NicheAnalyzerProps> = ({
  profile,
  analysis,
  trends
}) => {
  const [keywordAnalyses, setKeywordAnalyses] = useState<KeywordAnalysis[]>([]);
  const [nicheInsights, setNicheInsights] = useState<NicheInsights | null>(null);
  const [videoRecommendations, setVideoRecommendations] = useState<VideoIdeaRecommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({});
  const [selectedKeyword, setSelectedKeyword] = useState<string | null>(null);

  // Comprehensive niche analysis
  const analyzeNiche = useMemo(() => {
    if (!analysis || !trends.length) return null;

    // Extract and analyze keywords from profile and trends
    const allKeywords = [
      ...analysis.keywords,
      ...analysis.hashtags,
      ...trends.flatMap(trend => 
        trend.text_extra?.map(item => item.hashtag_name).filter(Boolean) || []
      )
    ].filter((keyword): keyword is string => typeof keyword === 'string' && keyword.length > 0);

    // Calculate keyword frequency and importance
    const keywordFreq = allKeywords.reduce((acc, keyword) => {
      if (keyword) {
        acc[keyword] = (acc[keyword] || 0) + 1;
      }
      return acc;
    }, {} as Record<string, number>);

    // Analyze content themes
    const contentThemes = trends.reduce((themes, trend) => {
      const description = trend.desc.toLowerCase();
      
      // Detect themes based on content
      if (description.includes('lifestyle') || description.includes('daily')) themes.lifestyle++;
      if (description.includes('tutorial') || description.includes('how')) themes.educational++;
      if (description.includes('funny') || description.includes('comedy')) themes.entertainment++;
      if (description.includes('review') || description.includes('opinion')) themes.review++;
      if (description.includes('challenge') || description.includes('trend')) themes.trending++;
      
      return themes;
    }, { lifestyle: 0, educational: 0, entertainment: 0, review: 0, trending: 0 });

    // Calculate engagement patterns
    const avgEngagement = trends.reduce((sum, trend) => sum + trend.engagement_rate, 0) / trends.length;
    const highPerformingTrends = trends.filter(trend => trend.engagement_rate > avgEngagement * 1.2);

    return {
      keywordFrequency: keywordFreq,
      contentThemes,
      avgEngagement,
      highPerformingTrends,
      totalTrends: trends.length,
      nicheStrength: analysis.niche ? 1 : 0.5,
    };
  }, [analysis, trends]);

  // Generate detailed keyword analysis
  const generateKeywordAnalysis = useCallback((keyword: string): KeywordAnalysis => {
    const relatedTrends = trends.filter(trend => 
      trend.desc.toLowerCase().includes(keyword.toLowerCase()) ||
      trend.text_extra?.some(item => 
        item.hashtag_name?.toLowerCase().includes(keyword.toLowerCase())
      )
    );

    const avgViews = relatedTrends.length > 0 
      ? relatedTrends.reduce((sum, trend) => sum + trend.statistics.play_count, 0) / relatedTrends.length
      : 0;

    const avgEngagement = relatedTrends.length > 0
      ? relatedTrends.reduce((sum, trend) => sum + trend.engagement_rate, 0) / relatedTrends.length
      : 0;

    // Simulate competition analysis (in real app, this would come from API)
    const competitionLevel = avgViews > 1000000 ? 'high' : avgViews > 100000 ? 'medium' : 'low';

    return {
      keyword,
      relevance_score: Math.min(95, (relatedTrends.length * 10) + (avgEngagement * 100)),
      trend_potential: Math.min(90, avgViews / 10000),
      competition_level: competitionLevel,
      search_volume: Math.floor(avgViews * 0.1),
      engagement_correlation: avgEngagement,
      seasonal_trends: [], // Would be populated from API
      related_hashtags: relatedTrends.flatMap(trend =>
        trend.text_extra?.map(item => item.hashtag_name).filter((name): name is string => Boolean(name)) || []
      ).slice(0, 5),
      success_examples: relatedTrends.slice(0, 3).map(trend => ({
        video_id: trend.aweme_id,
        description: trend.desc.slice(0, 100) + '...',
        views: trend.statistics.play_count,
        engagement_rate: trend.engagement_rate
      }))
    };
  }, [trends]);

  // Generate video idea recommendations
  const generateVideoRecommendations = useCallback((): VideoIdeaRecommendation[] => {
    if (!analyzeNiche || !analysis) return [];

    const recommendations: VideoIdeaRecommendation[] = [];
    const niche = analysis.niche.toLowerCase();
    const topKeywords = Object.entries(analyzeNiche.keywordFrequency)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 5)
      .map(([keyword]) => keyword);

    // Generate different types of video ideas based on niche analysis
    const ideaTemplates = [
      {
        type: 'trending',
        title: `${niche} Trend Challenge`,
        concept: `Create a unique take on current ${niche} trends`,
        difficulty: 3,
        reach_multiplier: 1.5
      },
      {
        type: 'educational',
        title: `${niche} Tips & Tricks`,
        concept: `Share valuable insights about ${niche}`,
        difficulty: 2,
        reach_multiplier: 1.2
      },
      {
        type: 'behind_scenes',
        title: `Behind the Scenes: ${niche}`,
        concept: `Show the process behind your ${niche} content`,
        difficulty: 1,
        reach_multiplier: 1.0
      },
      {
        type: 'collaboration',
        title: `${niche} Creator Collab`,
        concept: `Collaborate with other ${niche} creators`,
        difficulty: 4,
        reach_multiplier: 2.0
      },
      {
        type: 'reaction',
        title: `Reacting to ${niche} Trends`,
        concept: `React to and analyze current ${niche} trends`,
        difficulty: 2,
        reach_multiplier: 1.3
      }
    ];

    ideaTemplates.forEach((template, index) => {
      const baseReach = profile.follower_count * 0.05; // 5% base reach
      const estimatedReach = Math.floor(baseReach * template.reach_multiplier);
      
      recommendations.push({
        id: `idea_${index}`,
        title: template.title,
        concept: template.concept,
        target_keywords: topKeywords.slice(0, 3),
        estimated_reach: estimatedReach,
        difficulty_score: template.difficulty,
        trending_factor: Math.random() * 0.3 + 0.7, // 70-100%
        optimal_timing: {
          best_days: ['Tuesday', 'Wednesday', 'Thursday'],
          best_hours: [19, 20, 21], // Peak engagement hours
          seasonal_relevance: 'Year-round'
        },
        content_structure: {
          hook_suggestions: [
            `"You won't believe what happened in ${niche}..."`,
            `"The ${niche} secret nobody talks about"`,
            `"This ${niche} trend is everywhere"`
          ],
          key_elements: [
            'Strong opening hook',
            'Clear value proposition',
            'Visual engagement elements',
            'Community interaction'
          ],
          call_to_action: 'Follow for more insights',
          optimal_duration: '15-30 seconds'
        },
        success_probability: Math.min(95, 60 + (template.reach_multiplier * 10) + (5 - template.difficulty) * 5),
        supporting_data: {
          similar_video_performance: analyzeNiche.highPerformingTrends.slice(0, 2).map(trend => ({
            views: trend.statistics.play_count,
            engagement_rate: trend.engagement_rate,
            description: trend.desc.slice(0, 50) + '...'
          })),
          trend_evidence: [
            `${analyzeNiche.totalTrends} similar trends analyzed`,
            `Average engagement: ${(analyzeNiche.avgEngagement * 100).toFixed(1)}%`,
            `High-performing content identified`
          ],
          audience_interest_indicators: topKeywords.slice(0, 3)
        }
      });
    });

    return recommendations.sort((a, b) => b.success_probability - a.success_probability);
  }, [analyzeNiche, analysis, profile]);

  // Load comprehensive analysis
  useEffect(() => {
    if (analysis && trends.length > 0) {
      setLoading(true);
      
      // Generate keyword analyses
      const keywordsSet = new Set([...analysis.keywords, ...analysis.hashtags]);
      const keywords = Array.from(keywordsSet).slice(0, 8);
      const analyses = keywords.map(generateKeywordAnalysis);
      setKeywordAnalyses(analyses);

      // Generate video recommendations
      const recommendations = generateVideoRecommendations();
      setVideoRecommendations(recommendations);

      // Generate niche insights (mock data - would come from API)
      setNicheInsights({
        primary_niche: analysis.niche,
        niche_saturation: Math.random() * 40 + 30, // 30-70%
        growth_opportunity: Math.random() * 30 + 60, // 60-90%
        key_demographics: {
          age_groups: [
            { range: '18-24', percentage: 35 },
            { range: '25-34', percentage: 40 },
            { range: '35-44', percentage: 20 },
            { range: '45+', percentage: 5 }
          ],
          interests: analysis.interests.slice(0, 6),
          peak_activity_hours: [19, 20, 21, 22],
          geographic_hotspots: ['US', 'UK', 'Canada', 'Australia']
        },
        content_gaps: [
          {
            topic: `Advanced ${analysis.niche} techniques`,
            opportunity_score: 85,
            explanation: 'Limited content covering advanced topics in your niche',
            suggested_approach: 'Create in-depth tutorial series'
          },
          {
            topic: `${analysis.niche} for beginners`,
            opportunity_score: 78,
            explanation: 'High demand for beginner-friendly content',
            suggested_approach: 'Step-by-step guide format'
          }
        ],
        competitive_analysis: {
          top_creators: [], // Would be populated from API
          market_position: 'challenger',
          differentiation_opportunities: [
            'Unique perspective on trending topics',
            'Higher production quality',
            'More frequent posting schedule'
          ]
        }
      });

      setLoading(false);
    }
  }, [analysis, trends, generateKeywordAnalysis, generateVideoRecommendations]);

  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const getImportanceColor = (score: number) => {
    if (score >= 80) return 'text-emerald-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getCompetitionColor = (level: string) => {
    switch (level) {
      case 'low': return 'text-emerald-400';
      case 'medium': return 'text-yellow-400';
      case 'high': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  if (loading) {
    return (
      <div className="card">
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <BarChart3 className="w-8 h-8 animate-pulse text-primary-400 mx-auto mb-4" />
            <p className="text-dark-400">Analyzing niche and generating insights...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Niche Overview */}
      {nicheInsights && (
        <div className="card">
          <SectionTitle
            title="Niche Intelligence"
            subtitle={`Deep analysis of ${nicheInsights.primary_niche} niche`}
            icon={<Target className="w-5 h-5" />}
          />

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-dark-700/30 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <BarChart3 className="w-5 h-5 text-blue-400" />
                <span className="text-sm font-medium text-dark-300">Market Saturation</span>
              </div>
              <div className="text-2xl font-bold text-white mb-1">
                {nicheInsights.niche_saturation.toFixed(1)}%
              </div>
              <div className="w-full bg-dark-600 rounded-full h-2">
                <div 
                  className="bg-blue-500 h-2 rounded-full"
                  style={{ width: `${nicheInsights.niche_saturation}%` }}
                />
              </div>
            </div>

            <div className="bg-dark-700/30 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="w-5 h-5 text-emerald-400" />
                <span className="text-sm font-medium text-dark-300">Growth Opportunity</span>
              </div>
              <div className="text-2xl font-bold text-white mb-1">
                {nicheInsights.growth_opportunity.toFixed(1)}%
              </div>
              <div className="w-full bg-dark-600 rounded-full h-2">
                <div 
                  className="bg-emerald-500 h-2 rounded-full"
                  style={{ width: `${nicheInsights.growth_opportunity}%` }}
                />
              </div>
            </div>

            <div className="bg-dark-700/30 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <Award className="w-5 h-5 text-purple-400" />
                <span className="text-sm font-medium text-dark-300">Market Position</span>
              </div>
              <div className="text-lg font-bold text-white mb-1 capitalize">
                {nicheInsights.competitive_analysis.market_position.replace('_', ' ')}
              </div>
              <Badge variant="primary" size="sm">
                Competitive Analysis
              </Badge>
            </div>
          </div>

          {/* Demographics */}
          <div className="mb-6">
            <h4 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
              <Users className="w-5 h-5" />
              Target Demographics
            </h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {nicheInsights.key_demographics.age_groups.map((group, index) => (
                <div key={index} className="bg-dark-800/50 rounded-lg p-3 text-center">
                  <div className="text-lg font-bold text-primary-400">{group.percentage}%</div>
                  <div className="text-sm text-dark-400">{group.range}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Content Gaps */}
          <div>
            <button
              onClick={() => toggleSection('content_gaps')}
              className="flex items-center gap-2 text-lg font-semibold text-white mb-3 hover:text-primary-400 transition-colors"
            >
              <Lightbulb className="w-5 h-5" />
              Content Opportunities
              {expandedSections.content_gaps ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
            </button>
            
            {expandedSections.content_gaps && (
              <div className="space-y-3">
                {nicheInsights.content_gaps.map((gap, index) => (
                  <div key={index} className="bg-dark-800/50 rounded-lg p-4 border-l-4 border-emerald-400">
                    <div className="flex items-start justify-between mb-2">
                      <h5 className="font-medium text-white">{gap.topic}</h5>
                      <Badge variant="success" size="sm">
                        {gap.opportunity_score}% opportunity
                      </Badge>
                    </div>
                    <p className="text-sm text-dark-300 mb-2">{gap.explanation}</p>
                    <p className="text-sm text-emerald-400">
                      <strong>Suggested approach:</strong> {gap.suggested_approach}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Keyword Analysis */}
      <div className="card">
        <SectionTitle
          title="Keyword Intelligence"
          subtitle="Comprehensive analysis of your niche keywords"
          icon={<Hash className="w-5 h-5" />}
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {keywordAnalyses.map((keyword, index) => (
            <div
              key={index}
              className={`bg-dark-700/30 rounded-lg p-4 cursor-pointer transition-all duration-200 hover:bg-dark-700/50 ${
                selectedKeyword === keyword.keyword ? 'ring-2 ring-primary-500' : ''
              }`}
              onClick={() => setSelectedKeyword(selectedKeyword === keyword.keyword ? null : keyword.keyword)}
            >
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-medium text-white">#{keyword.keyword}</h4>
                <Badge 
                  variant={keyword.competition_level === 'low' ? 'success' : keyword.competition_level === 'medium' ? 'warning' : 'danger'}
                  size="sm"
                >
                  {keyword.competition_level} competition
                </Badge>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-dark-400">Relevance Score</span>
                  <span className={`text-sm font-medium ${getImportanceColor(keyword.relevance_score)}`}>
                    {keyword.relevance_score.toFixed(1)}/100
                  </span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-dark-400">Trend Potential</span>
                  <span className={`text-sm font-medium ${getImportanceColor(keyword.trend_potential)}`}>
                    {keyword.trend_potential.toFixed(1)}/100
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm text-dark-400">Engagement Correlation</span>
                  <span className="text-sm font-medium text-primary-400">
                    {(keyword.engagement_correlation * 100).toFixed(1)}%
                  </span>
                </div>
              </div>

              {selectedKeyword === keyword.keyword && keyword.success_examples.length > 0 && (
                <div className="mt-4 pt-4 border-t border-dark-600">
                  <h5 className="text-sm font-medium text-white mb-2">Success Examples:</h5>
                  <div className="space-y-2">
                    {keyword.success_examples.map((example, idx) => (
                      <div key={idx} className="text-xs text-dark-300 bg-dark-800/50 rounded p-2">
                        <div className="flex items-center gap-2 mb-1">
                          <Eye className="w-3 h-3" />
                          <span>{(example.views / 1000000).toFixed(1)}M views</span>
                          <Heart className="w-3 h-3 text-red-400" />
                          <span>{(example.engagement_rate * 100).toFixed(1)}%</span>
                        </div>
                        <p className="text-dark-400">{example.description}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Video Idea Recommendations */}
      <div className="card">
        <SectionTitle
          title="AI-Generated Video Ideas"
          subtitle="Data-driven content recommendations for maximum impact"
          icon={<Lightbulb className="w-5 h-5" />}
        />

        <div className="space-y-4">
          {videoRecommendations.map((idea, index) => (
            <div key={idea.id} className="bg-dark-700/30 rounded-lg p-6 border-l-4 border-primary-500">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <PlayCircle className="w-6 h-6 text-primary-400" />
                    <h4 className="text-lg font-semibold text-white">{idea.title}</h4>
                    <Badge variant="success" size="sm">
                      {idea.success_probability.toFixed(0)}% success probability
                    </Badge>
                  </div>
                  <p className="text-dark-300 mb-3">{idea.concept}</p>
                  
                  <div className="flex flex-wrap gap-2 mb-3">
                    {idea.target_keywords.map((keyword, idx) => (
                      <Badge key={idx} variant="primary" size="sm">
                        #{keyword}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div className="text-right">
                  <div className="text-2xl font-bold text-emerald-400">
                    {(idea.estimated_reach / 1000).toFixed(0)}K
                  </div>
                  <div className="text-sm text-dark-400">Est. Reach</div>
                </div>
              </div>

              {/* Metrics Row */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                <div className="text-center">
                  <div className="flex items-center justify-center gap-1 mb-1">
                    <Star className="w-4 h-4 text-yellow-400" />
                    <span className="text-sm text-dark-400">Difficulty</span>
                  </div>
                  <div className="text-lg font-semibold text-white">
                    {idea.difficulty_score}/5
                  </div>
                </div>

                <div className="text-center">
                  <div className="flex items-center justify-center gap-1 mb-1">
                    <TrendingUp className="w-4 h-4 text-emerald-400" />
                    <span className="text-sm text-dark-400">Trending</span>
                  </div>
                  <div className="text-lg font-semibold text-white">
                    {(idea.trending_factor * 100).toFixed(0)}%
                  </div>
                </div>

                <div className="text-center">
                  <div className="flex items-center justify-center gap-1 mb-1">
                    <Clock className="w-4 h-4 text-blue-400" />
                    <span className="text-sm text-dark-400">Duration</span>
                  </div>
                  <div className="text-sm font-semibold text-white">
                    {idea.content_structure.optimal_duration}
                  </div>
                </div>

                <div className="text-center">
                  <div className="flex items-center justify-center gap-1 mb-1">
                    <Users className="w-4 h-4 text-purple-400" />
                    <span className="text-sm text-dark-400">Best Days</span>
                  </div>
                  <div className="text-xs font-semibold text-white">
                    {idea.optimal_timing.best_days.slice(0, 2).join(', ')}
                  </div>
                </div>
              </div>

              {/* Expandable Details */}
              <button
                onClick={() => toggleSection(`idea_${idea.id}`)}
                className="flex items-center gap-2 text-sm text-primary-400 hover:text-primary-300 transition-colors"
              >
                <span>View detailed strategy</span>
                {expandedSections[`idea_${idea.id}`] ? <ChevronDown className="w-4 h-4" /> : <ArrowRight className="w-4 h-4" />}
              </button>

              {expandedSections[`idea_${idea.id}`] && (
                <div className="mt-4 pt-4 border-t border-dark-600 space-y-4">
                  {/* Hook Suggestions */}
                  <div>
                    <h5 className="text-sm font-semibold text-white mb-2">Hook Suggestions:</h5>
                    <div className="space-y-1">
                      {idea.content_structure.hook_suggestions.map((hook, idx) => (
                        <div key={idx} className="text-sm text-dark-300 bg-dark-800/50 rounded px-3 py-1">
                          {hook}
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Key Elements */}
                  <div>
                    <h5 className="text-sm font-semibold text-white mb-2">Key Elements:</h5>
                    <div className="flex flex-wrap gap-2">
                      {idea.content_structure.key_elements.map((element, idx) => (
                        <Badge key={idx} variant="neutral" size="sm">
                          {element}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  {/* Supporting Data */}
                  <div>
                    <h5 className="text-sm font-semibold text-white mb-2">Supporting Evidence:</h5>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h6 className="text-xs font-medium text-dark-400 mb-1">Similar Video Performance:</h6>
                        {idea.supporting_data.similar_video_performance.map((perf, idx) => (
                          <div key={idx} className="text-xs text-dark-300 mb-1">
                            <span className="text-emerald-400">{(perf.views / 1000000).toFixed(1)}M views</span>
                            <span className="text-yellow-400 ml-2">{(perf.engagement_rate * 100).toFixed(1)}%</span>
                            <p className="text-dark-400">{perf.description}</p>
                          </div>
                        ))}
                      </div>
                      
                      <div>
                        <h6 className="text-xs font-medium text-dark-400 mb-1">Trend Evidence:</h6>
                        {idea.supporting_data.trend_evidence.map((evidence, idx) => (
                          <div key={idx} className="text-xs text-dark-300 mb-1">
                            • {evidence}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Metrics Correlation Analysis */}
      <MetricsCorrelationAnalysis trends={trends} />

      {/* Key Metrics Summary */}
      <div className="card">
        <SectionTitle
          title="Analysis Summary"
          subtitle="Key insights and recommended actions"
          icon={<BarChart3 className="w-5 h-5" />}
        />

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="bg-emerald-900/20 rounded-lg p-4 border border-emerald-800">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="w-5 h-5 text-emerald-400" />
              <span className="text-sm font-medium text-emerald-300">Most Important Metric</span>
            </div>
            <div className="text-lg font-bold text-white mb-1">Engagement Rate</div>
            <p className="text-sm text-emerald-200">
              Focus on creating content that drives meaningful interactions. 
              Your current average of {analyzeNiche ? (analyzeNiche.avgEngagement * 100).toFixed(1) : 0}% 
              shows strong potential.
            </p>
          </div>

          <div className="bg-blue-900/20 rounded-lg p-4 border border-blue-800">
            <div className="flex items-center gap-2 mb-2">
              <Target className="w-5 h-5 text-blue-400" />
              <span className="text-sm font-medium text-blue-300">Priority Keywords</span>
            </div>
            <div className="text-lg font-bold text-white mb-1">Top 3 Keywords</div>
            <div className="space-y-1">
              {keywordAnalyses.slice(0, 3).map((keyword, idx) => (
                <div key={idx} className="text-sm text-blue-200">
                  #{keyword.keyword} ({keyword.relevance_score.toFixed(0)} score)
                </div>
              ))}
            </div>
          </div>

          <div className="bg-purple-900/20 rounded-lg p-4 border border-purple-800">
            <div className="flex items-center gap-2 mb-2">
              <Lightbulb className="w-5 h-5 text-purple-400" />
              <span className="text-sm font-medium text-purple-300">Next Actions</span>
            </div>
            <div className="text-lg font-bold text-white mb-1">Immediate Steps</div>
            <div className="space-y-1 text-sm text-purple-200">
              <div>• Create content using top keywords</div>
              <div>• Focus on {videoRecommendations[0]?.optimal_timing.best_days[0]} posting</div>
              <div>• Develop {nicheInsights?.content_gaps[0]?.topic.toLowerCase()} content</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NicheAnalyzer;
