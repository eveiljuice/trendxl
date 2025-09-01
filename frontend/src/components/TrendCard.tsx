import React, { useState } from 'react';
import { 
  Play, 
  Heart, 
  MessageCircle, 
  Share2, 
  Download, 
  Star, 
  ExternalLink,
  Music,
  Clock,
  TrendingUp,
  Users,
  Target,
  MapPin
} from 'lucide-react';
import { TrendCardProps } from '../types';
import { 
  formatNumber, 
  formatDuration, 
  getRelativeTime,
  getRelevanceScoreColor,
  getTrendPotentialColor,
  getSentimentColor
} from '../lib/api';
import Badge from './ui/Badge';
import Stat from './ui/Stat';

const TrendCard: React.FC<TrendCardProps> = ({ 
  trend, 
  onPlay, 
  showRelevanceScore = true 
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [videoError, setVideoError] = useState(false);

  const handlePlay = () => {
    setIsPlaying(!isPlaying);
    if (onPlay) {
      onPlay(trend);
    }
  };

  const handleVideoError = () => {
    setVideoError(true);
  };

  const engagementRate = trend.engagement_rate || 0;
  const hashtags = trend.text_extra
    ?.filter(item => item.hashtag_name)
    .map(item => item.hashtag_name)
    .slice(0, 5) || [];

  return (
    <div className="trend-card card h-full flex flex-col">
      {/* Video Section */}
      <div className="relative mb-4 flex-shrink-0">
        <div className="video-container aspect-[9/16] max-h-80 overflow-hidden">
          {!videoError && trend.video.cover ? (
            <img
              src={trend.video.cover}
              alt="Video thumbnail"
              className="w-full h-full object-cover"
              onError={handleVideoError}
            />
          ) : (
            <div className="w-full h-full bg-dark-700 flex items-center justify-center">
              <Play className="w-12 h-12 text-dark-500" />
            </div>
          )}
          
          {/* Video Preview on Hover */}
          {!videoError && trend.video.play_addr && (
            <video
              className="absolute inset-0 w-full h-full object-cover opacity-0 hover:opacity-100 transition-opacity duration-300"
              muted
              loop
              onMouseEnter={(e) => e.currentTarget.play().catch(() => {})}
              onMouseLeave={(e) => {
                e.currentTarget.pause();
                e.currentTarget.currentTime = 0;
              }}
            >
              <source src={trend.video.play_addr} type="video/mp4" />
            </video>
          )}
          
          <div className="video-overlay">
            <div className="flex items-center justify-between">
              <button
                onClick={handlePlay}
                className="bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-full p-3 transition-all duration-200"
              >
                <Play className="w-6 h-6 text-white" />
              </button>
              
              <div className="flex items-center gap-2">
                {trend.video.duration > 0 && (
                  <Badge variant="neutral" size="sm">
                    <Clock className="w-3 h-3 mr-1" />
                    {formatDuration(trend.video.duration)}
                  </Badge>
                )}
                
                <a
                  href={trend.tiktok_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-full p-2 transition-all duration-200"
                  title="Open on TikTok"
                >
                  <ExternalLink className="w-4 h-4 text-white" />
                </a>
              </div>
            </div>
          </div>
        </div>
        
        {/* Relevance Score */}
        {showRelevanceScore && trend.relevance_score && (
          <div className="absolute top-3 left-3">
            <Badge variant="primary" size="sm">
              <Target className="w-3 h-3 mr-1" />
              <span className={getRelevanceScoreColor(trend.relevance_score)}>
                {trend.relevance_score}%
              </span>
            </Badge>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="space-y-4 flex-1">
        {/* Author - Enhanced */}
        <div className="flex items-start gap-3">
          <div className="relative flex-shrink-0">
            <img
              src={trend.author.avatar_thumb || '/default-avatar.png'}
              alt={trend.author.nickname}
              className="w-12 h-12 rounded-full object-cover border-2 border-dark-600"
            />
            {trend.author.verified && (
              <div className="absolute -bottom-1 -right-1 bg-blue-500 rounded-full p-1">
                <Star className="w-3 h-3 text-white" />
              </div>
            )}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <p className="font-medium text-white truncate">{trend.author.nickname}</p>
              {trend.author.verified && (
                <Badge variant="primary" size="sm">Verified</Badge>
              )}
            </div>
            <p className="text-sm text-dark-400">
              @{trend.author.unique_id}
            </p>
            <div className="flex items-center gap-4 mt-1 text-xs text-dark-500">
              <span className="flex items-center gap-1">
                <Users className="w-3 h-3" />
                {formatNumber(trend.author.follower_count)} followers
              </span>
              {trend.author.total_favorited && (
                <span className="flex items-center gap-1">
                  <Heart className="w-3 h-3" />
                  {formatNumber(trend.author.total_favorited)} likes
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Description */}
        <div>
          <p className="text-white text-sm leading-relaxed line-clamp-3">
            {trend.desc}
          </p>
        </div>

        {/* Hashtags */}
        {hashtags.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {hashtags.map((hashtag, index) => (
              <Badge key={index} variant="neutral" size="sm">
                #{hashtag}
              </Badge>
            ))}
          </div>
        )}

        {/* Music Info */}
        {trend.music.title && (
          <div className="flex items-center gap-2 text-sm text-dark-400">
            <Music className="w-4 h-4" />
            <span className="truncate">
              {trend.music.title} - {trend.music.author}
            </span>
          </div>
        )}

        {/* All Metrics as per prompt.md */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
          <Stat
            label="Views"
            value={formatNumber(trend.statistics.play_count)}
            icon={<Play className="w-4 h-4" />}
          />
          <Stat
            label="Likes"
            value={formatNumber(trend.statistics.digg_count)}
            icon={<Heart className="w-4 h-4" />}
          />
          <Stat
            label="Comments"
            value={formatNumber(trend.statistics.comment_count)}
            icon={<MessageCircle className="w-4 h-4" />}
          />
          <Stat
            label="Shares"
            value={formatNumber(trend.statistics.share_count)}
            icon={<Share2 className="w-4 h-4" />}
          />
        </div>

        {/* Additional Required Metrics */}
        <div className="grid grid-cols-2 lg:grid-cols-3 gap-3 mb-4">
          <Stat
            label="Downloads"
            value={formatNumber(trend.statistics.download_count)}
            icon={<Download className="w-4 h-4" />}
          />
          <Stat
            label="Favourited"
            value={formatNumber(trend.statistics.collect_count)}
            icon={<Star className="w-4 h-4" />}
          />
          <Stat
            label="WhatsApp Shares"
            value={formatNumber(trend.statistics.whatsapp_share_count)}
            icon={<MessageCircle className="w-4 h-4" />}
          />
        </div>

        {/* Duration and Region */}
        <div className="grid grid-cols-2 gap-3 mb-4">
          <Stat
            label="Duration"
            value={`${Math.floor(trend.video.duration / 1000)}s`}
            icon={<Clock className="w-4 h-4" />}
          />
          {trend.region && (
            <Stat
              label="Region"
              value={trend.region}
              icon={<MapPin className="w-4 h-4" />}
            />
          )}
        </div>

        {/* Engagement, Sentiment, Audience */}
        <div className="grid grid-cols-3 gap-3 mb-4">
          <div className="text-center p-2 bg-dark-700/30 rounded-lg">
            <div className="text-lg font-bold text-emerald-400">
              {engagementRate.toFixed(1)}%
            </div>
            <div className="text-xs text-dark-400">Engagement</div>
          </div>
          
          <div className="text-center p-2 bg-dark-700/30 rounded-lg">
            <div className={`text-lg font-bold ${getSentimentColor(trend.sentiment)}`}>
              {trend.sentiment || 'N/A'}
            </div>
            <div className="text-xs text-dark-400">Sentiment</div>
          </div>
          
          <div className="text-center p-2 bg-dark-700/30 rounded-lg">
            <div className="text-lg font-bold text-blue-400">
              {trend.audience || 'General'}
            </div>
            <div className="text-xs text-dark-400">Audience</div>
          </div>
        </div>

        {/* Video Type and Sound Type */}
        <div className="grid grid-cols-2 gap-3 mb-4">
          {trend.video.video_type && (
            <div className="text-center p-2 bg-dark-700/30 rounded-lg">
              <div className="text-sm font-bold text-purple-400">
                {trend.video.video_type}
              </div>
              <div className="text-xs text-dark-400">Video Type</div>
            </div>
          )}
          
          {trend.music.sound_type && (
            <div className="text-center p-2 bg-dark-700/30 rounded-lg">
              <div className="text-sm font-bold text-orange-400">
                {trend.music.sound_type}
              </div>
              <div className="text-xs text-dark-400">Sound Type</div>
            </div>
          )}
        </div>

        {/* AI Analysis */}
        {trend.relevance_reason && (
          <div className="bg-dark-700/30 rounded-lg p-3">
            <h4 className="text-sm font-medium text-white mb-2 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-primary-400" />
              AI Analysis
            </h4>
            <p className="text-sm text-dark-300 leading-relaxed">
              {trend.relevance_reason}
            </p>
          </div>
        )}

        {/* Trend Metadata */}
        <div className="flex items-center justify-between text-xs text-dark-400 pt-2 border-t border-dark-700">
          <div className="flex items-center gap-4">
            {trend.trend_category && (
              <Badge variant="neutral" size="sm">
                {trend.trend_category}
              </Badge>
            )}
            
            {trend.trend_potential && (
              <div className="flex items-center gap-1">
                <TrendingUp className="w-3 h-3" />
                <span className={getTrendPotentialColor(trend.trend_potential)}>
                  {trend.trend_potential}
                </span>
              </div>
            )}
            
            {trend.audience_match && (
              <div className="flex items-center gap-1">
                <Users className="w-3 h-3 text-emerald-400" />
                <span className="text-emerald-400">Audience Match</span>
              </div>
            )}
          </div>
          
          <div>
            {getRelativeTime(trend.create_time)}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrendCard;
