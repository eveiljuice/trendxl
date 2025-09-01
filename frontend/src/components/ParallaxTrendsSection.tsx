import React, { useState, useRef, useEffect } from 'react';
import {
  Play,
  Pause,
  Volume2,
  VolumeX,
  Heart,
  MessageCircle,
  Share2,
  Download,
  Star,
  Eye,
  ExternalLink,
  ChevronLeft,
  ChevronRight,
  X,
  User
} from 'lucide-react';
import { TrendItem } from '../types';
import Badge from './ui/Badge';
import { formatNumber, formatDuration } from '../lib/utils';

interface ParallaxTrendsSectionProps {
  trends: TrendItem[];
  title?: string;
}

interface TrendPlayerProps {
  trend: TrendItem;
  onClose: () => void;
}

const TrendPlayer: React.FC<TrendPlayerProps> = ({ trend, onClose }) => {
  console.log('[TrendPlayer] Rendering TrendPlayer for trend:', trend.aweme_id);
  
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(true);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  const togglePlay = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play().catch(console.error);
      }
      setIsPlaying(!isPlaying);
    }
  };

  const toggleMute = () => {
    if (videoRef.current) {
      videoRef.current.muted = !isMuted;
      setIsMuted(!isMuted);
    }
  };

  const handleTimeUpdate = () => {
    if (videoRef.current) {
      setCurrentTime(videoRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (videoRef.current) {
      setDuration(videoRef.current.duration);
    }
  };

  const handleSeek = (e: React.MouseEvent<HTMLDivElement>) => {
    if (videoRef.current && duration > 0) {
      const rect = e.currentTarget.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const newTime = (clickX / rect.width) * duration;
      videoRef.current.currentTime = newTime;
      setCurrentTime(newTime);
    }
  };

  // Handle ESC key and prevent body scroll
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    // Prevent body scroll when modal is open
    document.body.style.overflow = 'hidden';
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.body.style.overflow = 'unset';
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [onClose]);

  useEffect(() => {
    const video = videoRef.current;
    if (video) {
      video.addEventListener('timeupdate', handleTimeUpdate);
      video.addEventListener('loadedmetadata', handleLoadedMetadata);
      
      // Auto-play video when loaded (muted)
      video.play().catch(console.error);
      setIsPlaying(true);
      
      return () => {
        video.removeEventListener('timeupdate', handleTimeUpdate);
        video.removeEventListener('loadedmetadata', handleLoadedMetadata);
      };
    }
  }, []);

  const progress = duration > 0 ? (currentTime / duration) * 100 : 0;

  return (
    <div 
      className="trend-modal-overlay fixed inset-0 bg-black/90 backdrop-blur-sm flex items-center justify-center"
      onClick={(e) => {
        // Close modal when clicking outside
        if (e.target === e.currentTarget) {
          onClose();
        }
      }}
    >
      <div className="relative w-full max-w-4xl mx-4 bg-dark-800 rounded-xl overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-4 bg-dark-900/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full overflow-hidden bg-dark-700">
              {trend.author.avatar_thumb ? (
                <img
                  src={trend.author.avatar_thumb}
                  alt={trend.author.nickname}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.currentTarget.style.display = 'none';
                  }}
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <User className="w-6 h-6 text-dark-400" />
                </div>
              )}
            </div>
            <div>
              <h3 className="text-white font-semibold">{trend.author.nickname}</h3>
              <p className="text-dark-400 text-sm">@{trend.author.unique_id}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-dark-700 rounded-lg transition-colors"
          >
            <X className="w-6 h-6 text-white" />
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 p-6">
          {/* Video Player */}
          <div className="relative aspect-[9/16] max-h-[70vh] bg-black rounded-lg overflow-hidden">
            <video
              ref={videoRef}
              className="w-full h-full object-cover"
              muted={isMuted}
              loop
              playsInline
              poster={trend.video.cover}
              onError={() => {
                console.error('Video failed to load');
              }}
            >
              {trend.video.play_addr && (
                <source src={trend.video.play_addr} type="video/mp4" />
              )}
              {trend.video.download_addr && (
                <source src={trend.video.download_addr} type="video/mp4" />
              )}
            </video>

            {/* Video Controls Overlay */}
            <div className="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity duration-200">
              <button
                onClick={togglePlay}
                className="bg-black/50 hover:bg-black/70 rounded-full p-4 transition-colors"
              >
                {isPlaying ? (
                  <Pause className="w-8 h-8 text-white" />
                ) : (
                  <Play className="w-8 h-8 text-white" />
                )}
              </button>
            </div>

            {/* Bottom Controls */}
            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
              {/* Progress Bar */}
              <div
                className="w-full h-1 bg-white/20 rounded-full mb-3 cursor-pointer"
                onClick={handleSeek}
              >
                <div
                  className="h-full bg-white rounded-full transition-all duration-200"
                  style={{ width: `${progress}%` }}
                />
              </div>

              {/* Control Buttons */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <button
                    onClick={togglePlay}
                    className="text-white hover:text-primary-400 transition-colors"
                  >
                    {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
                  </button>
                  <button
                    onClick={toggleMute}
                    className="text-white hover:text-primary-400 transition-colors"
                  >
                    {isMuted ? <VolumeX className="w-5 h-5" /> : <Volume2 className="w-5 h-5" />}
                  </button>
                  <span className="text-white text-sm">
                    {formatDuration(currentTime * 1000)} / {formatDuration(duration * 1000)}
                  </span>
                </div>
                <a
                  href={trend.tiktok_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-white hover:text-primary-400 transition-colors"
                >
                  <ExternalLink className="w-5 h-5" />
                </a>
              </div>
            </div>
          </div>

          {/* Trend Info */}
          <div className="space-y-6">
            {/* Description */}
            <div>
              <p className="text-white text-lg leading-relaxed">{trend.desc}</p>
            </div>

            {/* Hashtags */}
            {trend.text_extra && trend.text_extra.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {trend.text_extra
                  .filter(item => item.hashtag_name)
                  .map((item, index) => (
                    <Badge key={index} variant="primary" size="sm">
                      #{item.hashtag_name}
                    </Badge>
                  ))}
              </div>
            )}

            {/* Primary Stats */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-dark-700/50 rounded-lg p-4 text-center">
                <div className="flex items-center justify-center gap-2 mb-2">
                  <Eye className="w-5 h-5 text-blue-400" />
                  <span className="text-white font-semibold">Views</span>
                </div>
                <div className="text-2xl font-bold text-blue-400">
                  {formatNumber(trend.statistics.play_count)}
                </div>
              </div>
              <div className="bg-dark-700/50 rounded-lg p-4 text-center">
                <div className="flex items-center justify-center gap-2 mb-2">
                  <Heart className="w-5 h-5 text-red-400" />
                  <span className="text-white font-semibold">Likes</span>
                </div>
                <div className="text-2xl font-bold text-red-400">
                  {formatNumber(trend.statistics.digg_count)}
                </div>
              </div>
            </div>

            {/* Secondary Stats */}
            <div className="grid grid-cols-3 gap-3">
              <div className="bg-dark-700/30 rounded-lg p-3 text-center">
                <MessageCircle className="w-4 h-4 text-green-400 mx-auto mb-1" />
                <div className="text-sm font-semibold text-white">
                  {formatNumber(trend.statistics.comment_count)}
                </div>
                <div className="text-xs text-dark-400">Comments</div>
              </div>
              <div className="bg-dark-700/30 rounded-lg p-3 text-center">
                <Share2 className="w-4 h-4 text-purple-400 mx-auto mb-1" />
                <div className="text-sm font-semibold text-white">
                  {formatNumber(trend.statistics.share_count)}
                </div>
                <div className="text-xs text-dark-400">Shares</div>
              </div>
              <div className="bg-dark-700/30 rounded-lg p-3 text-center">
                <Download className="w-4 h-4 text-orange-400 mx-auto mb-1" />
                <div className="text-sm font-semibold text-white">
                  {formatNumber(trend.statistics.download_count)}
                </div>
                <div className="text-xs text-dark-400">Downloads</div>
              </div>
            </div>

            {/* Additional Metrics */}
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-dark-700/30 rounded-lg p-3 text-center">
                <Star className="w-4 h-4 text-yellow-400 mx-auto mb-1" />
                <div className="text-sm font-semibold text-white">
                  {formatNumber(trend.statistics.collect_count)}
                </div>
                <div className="text-xs text-dark-400">Favourited</div>
              </div>
              <div className="bg-dark-700/30 rounded-lg p-3 text-center">
                <MessageCircle className="w-4 h-4 text-green-500 mx-auto mb-1" />
                <div className="text-sm font-semibold text-white">
                  {formatNumber(trend.statistics.whatsapp_share_count)}
                </div>
                <div className="text-xs text-dark-400">WhatsApp</div>
              </div>
            </div>

            {/* Meta Information */}
            <div className="space-y-3 pt-4 border-t border-dark-700">
              <div className="flex items-center justify-between text-sm">
                <span className="text-dark-400">Engagement Rate</span>
                <span className="text-emerald-400 font-semibold">
                  {(trend.engagement_rate * 100).toFixed(1)}%
                </span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-dark-400">Duration</span>
                <span className="text-white font-semibold">
                  {Math.floor(trend.video.duration / 1000)}s
                </span>
              </div>
              {trend.region && (
                <div className="flex items-center justify-between text-sm">
                  <span className="text-dark-400">Region</span>
                  <span className="text-white font-semibold">{trend.region}</span>
                </div>
              )}
              {trend.sentiment && (
                <div className="flex items-center justify-between text-sm">
                  <span className="text-dark-400">Sentiment</span>
                  <Badge 
                    variant={trend.sentiment === 'positive' ? 'success' : trend.sentiment === 'negative' ? 'danger' : 'neutral'} 
                    size="sm"
                  >
                    {trend.sentiment}
                  </Badge>
                </div>
              )}
              {trend.audience && (
                <div className="flex items-center justify-between text-sm">
                  <span className="text-dark-400">Target Audience</span>
                  <span className="text-white font-semibold text-right max-w-xs truncate">
                    {trend.audience}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const ParallaxTrendsSection: React.FC<ParallaxTrendsSectionProps> = ({ 
  trends, 
  title = "Trending Content" 
}) => {
  const scrollRef = useRef<HTMLDivElement>(null);
  const [selectedTrend, setSelectedTrend] = useState<TrendItem | null>(null);
  const [scrollPosition, setScrollPosition] = useState(0);
  const [isVideoLoading, setIsVideoLoading] = useState(false);

  const handleScroll = () => {
    if (scrollRef.current) {
      setScrollPosition(scrollRef.current.scrollLeft);
    }
  };

  const scrollLeft = () => {
    if (scrollRef.current) {
      scrollRef.current.scrollBy({ left: -400, behavior: 'smooth' });
    }
  };

  const scrollRight = () => {
    if (scrollRef.current) {
      scrollRef.current.scrollBy({ left: 400, behavior: 'smooth' });
    }
  };

  const handleTrendClick = (trend: TrendItem, event?: React.MouseEvent) => {
    console.log('[ParallaxTrends] Click detected for trend:', trend.aweme_id);
    
    // Prevent multiple clicks while video is loading
    if (isVideoLoading) {
      console.log('[ParallaxTrends] Video is loading, preventing click');
      return;
    }
    
    // Stop event propagation to prevent conflicts
    if (event) {
      event.stopPropagation();
      event.preventDefault();
      console.log('[ParallaxTrends] Event propagation stopped');
    }

    console.log('[ParallaxTrends] Current selectedTrend:', selectedTrend?.aweme_id);

    // Close current video if different trend is clicked
    if (selectedTrend && selectedTrend.aweme_id !== trend.aweme_id) {
      console.log('[ParallaxTrends] Closing current video and opening new one');
      setSelectedTrend(null);
      // Small delay before opening new video for smooth transition
      setTimeout(() => {
        console.log('[ParallaxTrends] Setting new trend after delay:', trend.aweme_id);
        setSelectedTrend(trend);
      }, 150);
    } else {
      console.log('[ParallaxTrends] Setting trend directly:', trend.aweme_id);
      setSelectedTrend(trend);
    }
  };

  const closeTrendPlayer = () => {
    setIsVideoLoading(false);
    setSelectedTrend(null);
  };

  // Log when selectedTrend changes
  useEffect(() => {
    if (selectedTrend) {
      console.log('[ParallaxTrends] Rendering TrendPlayer for:', selectedTrend.aweme_id);
    } else {
      console.log('[ParallaxTrends] No selectedTrend, not rendering modal');
    }
  }, [selectedTrend]);

  // Create parallax layers based on scroll position
  const getParallaxOffset = (index: number) => {
    const baseOffset = scrollPosition * 0.1;
    const layerOffset = (index % 3) * 0.05;
    return baseOffset + layerOffset * scrollPosition;
  };

  if (trends.length === 0) {
    return (
      <div className="w-full py-12 text-center">
        <div className="text-dark-400 text-lg">No trends available</div>
      </div>
    );
  }

  return (
    <div className="relative w-full py-8 overflow-hidden">
      {/* Section Header */}
      <div className="flex items-center justify-between mb-8 px-6">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">{title}</h2>
          <p className="text-dark-400">Discover trending content tailored for you</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={scrollLeft}
            className="p-3 bg-dark-700 hover:bg-dark-600 rounded-full transition-colors"
          >
            <ChevronLeft className="w-6 h-6 text-white" />
          </button>
          <button
            onClick={scrollRight}
            className="p-3 bg-dark-700 hover:bg-dark-600 rounded-full transition-colors"
          >
            <ChevronRight className="w-6 h-6 text-white" />
          </button>
        </div>
      </div>

      {/* Parallax Scrolling Container */}
      <div
        ref={scrollRef}
        onScroll={handleScroll}
        className="flex gap-6 overflow-x-auto parallax-container pb-4 px-6"
      >
        {trends.map((trend, index) => (
          <div
            key={trend.aweme_id}
            className="relative flex-shrink-0 group cursor-pointer"
            onClick={(e) => handleTrendClick(trend, e)}
            style={{
              transform: `translateX(${getParallaxOffset(index)}px)`,
              transition: 'transform 0.1s ease-out',
              zIndex: selectedTrend?.aweme_id === trend.aweme_id ? 10 : 1
            }}
          >
            {/* Main Trend Card */}
            <div className={`parallax-card relative w-80 h-96 bg-gradient-to-br from-dark-800 to-dark-900 rounded-2xl overflow-hidden shadow-2xl group-hover:shadow-3xl transition-all duration-300 group-hover:scale-105 ${selectedTrend?.aweme_id === trend.aweme_id ? 'active' : ''}`}>
              {/* Background Video/Image */}
              <div className="absolute inset-0">
                <img
                  src={trend.video.cover || '/api/placeholder/320/384'}
                  alt={trend.desc}
                  className="w-full h-full object-cover opacity-60 group-hover:opacity-80 transition-opacity duration-300"
                  onError={(e) => {
                    e.currentTarget.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIwIiBoZWlnaHQ9IjM4NCIgdmlld0JveD0iMCAwIDMyMCAzODQiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMjAiIGhlaWdodD0iMzg0IiBmaWxsPSIjMzc0MTUxIi8+CjxwYXRoIGQ9Ik0xNDQgMTcyTDE3NiAxOTJMMTQ0IDIxMlYxNzJaIiBmaWxsPSIjNkI3Mjg0Ii8+Cjx0ZXh0IHg9IjE2MCIgeT0iMjQwIiBmb250LWZhbWlseT0ic2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzZCNzI4NCIgdGV4dC1hbmNob3I9Im1pZGRsZSI+VmlkZW8gUHJldmlldzwvdGV4dD4KPC9zdmc+';
                    e.currentTarget.classList.add('image-loading');
                  }}
                  onLoad={(e) => {
                    e.currentTarget.classList.remove('image-loading');
                  }}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />
              </div>

              {/* Content Overlay */}
              <div className="relative h-full flex flex-col justify-between p-6">
                {/* Top Section - Author Info */}
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-full overflow-hidden bg-dark-700 border-2 border-white/20">
                    {trend.author.avatar_thumb ? (
                      <img
                        src={trend.author.avatar_thumb}
                        alt={trend.author.nickname}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          e.currentTarget.style.display = 'none';
                        }}
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center">
                        <User className="w-6 h-6 text-dark-400" />
                      </div>
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-white font-semibold truncate">
                      {trend.author.nickname}
                    </div>
                    <div className="text-white/70 text-sm truncate">
                      @{trend.author.unique_id}
                    </div>
                  </div>
                </div>

                {/* Center Section - Play Button */}
                <div className="flex items-center justify-center">
                                  <div className="play-button w-16 h-16 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center group-hover:bg-white/30 transition-colors duration-300">
                  <Play className="w-8 h-8 text-white ml-1" />
                </div>
                </div>

                {/* Bottom Section - Stats and Info */}
                <div className="space-y-3">
                  <p className="text-white text-sm line-clamp-2 leading-relaxed">
                    {trend.desc}
                  </p>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4 text-white/80 text-sm">
                      <div className="flex items-center gap-1">
                        <Eye className="w-4 h-4" />
                        <span>{formatNumber(trend.statistics.play_count)}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Heart className="w-4 h-4 text-red-400" />
                        <span>{formatNumber(trend.statistics.digg_count)}</span>
                      </div>
                    </div>
                    <div className="text-white/60 text-xs">
                      {Math.floor(trend.video.duration / 1000)}s
                    </div>
                  </div>

                  {/* Engagement Indicator */}
                  <div className="w-full bg-white/20 rounded-full h-1">
                    <div
                      className="h-full bg-gradient-to-r from-emerald-400 to-blue-400 rounded-full"
                      style={{ width: `${Math.min(trend.engagement_rate * 100, 100)}%` }}
                    />
                  </div>
                </div>
              </div>

              {/* Hover Overlay */}
              <div className="absolute inset-0 bg-primary-500/0 group-hover:bg-primary-500/10 transition-colors duration-300 pointer-events-none" />
            </div>

            {/* Parallax Background Elements */}
            <div
              className="absolute -top-4 -left-4 w-20 h-20 bg-primary-500/10 rounded-full blur-xl"
              style={{
                transform: `translate(${getParallaxOffset(index) * 0.5}px, ${getParallaxOffset(index) * 0.3}px)`
              }}
            />
            <div
              className="absolute -bottom-4 -right-4 w-16 h-16 bg-emerald-500/10 rounded-full blur-xl"
              style={{
                transform: `translate(${getParallaxOffset(index) * -0.3}px, ${getParallaxOffset(index) * -0.2}px)`
              }}
            />
          </div>
        ))}
      </div>

      {/* Trend Player Modal */}
      {selectedTrend && (
        <TrendPlayer trend={selectedTrend} onClose={closeTrendPlayer} />
      )}


    </div>
  );
};

export default ParallaxTrendsSection;
