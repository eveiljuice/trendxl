import React from 'react';
import { 
  User, 
  Users, 
  Video, 
  Heart, 
  MapPin, 
  Globe, 
  CheckCircle, 
  RefreshCw,
  TrendingUp
} from 'lucide-react';
import { ProfileCardProps } from '../types';
import { formatNumber } from '../lib/api';
import Stat from './ui/Stat';
import Badge from './ui/Badge';
import SectionTitle from './ui/SectionTitle';
import ApiStatusBanner from './ui/ApiStatusBanner';

const ProfileCard: React.FC<ProfileCardProps> = ({ 
  profile, 
  analysis, 
  onRefreshTrends, 
  loading = false 
}) => {
  // Determine API status from profile data
  const getApiStatus = () => {
    if (profile.api_source === 'ensemble') return 'ensemble';
    if (profile.api_source === 'database' || profile.api_source === 'database_fallback') return 'database';
    if (profile.api_source === 'mock') return 'mock';
    return 'ensemble'; // Default to ensemble if undefined
  };

  return (
    <div className="card">
      {/* API Status Banner */}
      <ApiStatusBanner 
        status={getApiStatus()}
        className="mb-6"
      />

      {/* Profile Header */}
      <div className="flex flex-col md:flex-row items-center md:items-start gap-6 mb-8">
        <div className="relative">
          <img
            src={profile.avatar_url || '/default-avatar.png'}
            alt={profile.display_name}
            className="w-20 h-20 md:w-16 md:h-16 rounded-full object-cover border-2 border-dark-600"
          />
          {profile.verified && (
            <CheckCircle className="absolute -bottom-1 -right-1 w-5 h-5 text-blue-500 bg-dark-800 rounded-full" />
          )}
        </div>
        
        <div className="flex-1 text-center md:text-left">
          <div className="flex flex-col md:flex-row items-center md:items-center gap-2 mb-2">
            <h3 className="text-2xl font-bold text-white">{profile.display_name}</h3>
            <Badge variant="neutral" size="sm">
              @{profile.username}
            </Badge>
          </div>
          
          {profile.bio && (
            <p className="text-dark-300 text-sm mb-4 max-w-2xl">{profile.bio}</p>
          )}
          
          <div className="flex flex-wrap items-center justify-center md:justify-start gap-4 text-sm text-dark-400">
            {profile.region && (
              <div className="flex items-center gap-1">
                <MapPin className="w-4 h-4" />
                <span>{profile.region}</span>
              </div>
            )}
            {profile.language && (
              <div className="flex items-center gap-1">
                <Globe className="w-4 h-4" />
                <span>{profile.language}</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Profile Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <Stat
          label="Followers"
          value={formatNumber(profile.follower_count || 0)}
          icon={<Users className="w-4 h-4" />}
        />
        <Stat
          label="Following"
          value={formatNumber(profile.following_count || 0)}
          icon={<User className="w-4 h-4" />}
        />
        <Stat
          label="Videos"
          value={formatNumber(profile.video_count || 0)}
          icon={<Video className="w-4 h-4" />}
        />
        <Stat
          label="Total Likes"
          value={formatNumber(profile.likes_count || 0)}
          icon={<Heart className="w-4 h-4" />}
        />
      </div>

      {/* Analysis Results */}
      <div className="space-y-6 mb-6">
        <SectionTitle
          title="Profile Analysis"
          subtitle="AI-generated insights"
          icon={<TrendingUp className="w-5 h-5" />}
        />
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Niche and Categories */}
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-dark-300 block mb-2">
                Detected Niche
              </label>
              <Badge variant="primary" size="lg">
                {analysis.niche || 'Not analyzed'}
              </Badge>
            </div>
            
            <div>
              <label className="text-sm font-medium text-dark-300 block mb-2">
                Core Interests
              </label>
              <div className="flex flex-wrap gap-2">
                {analysis.interests.length > 0 ? (
                  analysis.interests.slice(0, 4).map((interest, index) => (
                    <Badge key={index} variant="neutral" size="sm">
                      {interest}
                    </Badge>
                  ))
                ) : (
                  <span className="text-dark-400 text-sm">No interests detected</span>
                )}
              </div>
            </div>
          </div>

          {/* Keywords */}
          <div>
            <label className="text-sm font-medium text-dark-300 block mb-2">
              Trending Keywords
            </label>
            <div className="flex flex-wrap gap-2">
              {analysis.keywords.length > 0 ? (
                analysis.keywords.slice(0, 6).map((keyword, index) => (
                  <Badge key={index} variant="success" size="sm">
                    #{keyword}
                  </Badge>
                ))
              ) : (
                <span className="text-dark-400 text-sm">No keywords detected</span>
              )}
            </div>
          </div>

          {/* Audience & Style */}
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-dark-300 block mb-1">
                Target Audience
              </label>
              <p className="text-sm text-white bg-dark-700/50 rounded-lg p-3">
                {analysis.target_audience || 'Not analyzed'}
              </p>
            </div>
            
            <div>
              <label className="text-sm font-medium text-dark-300 block mb-1">
                Content Style
              </label>
              <p className="text-sm text-white bg-dark-700/50 rounded-lg p-3">
                {analysis.content_style || 'Not analyzed'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Action Button */}
      <button
        onClick={onRefreshTrends}
        disabled={loading}
        className="btn btn-primary w-full flex items-center justify-center gap-2"
      >
        <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
        {loading ? 'Refreshing Trends...' : 'Refresh Trends'}
      </button>
    </div>
  );
};

export default ProfileCard;
