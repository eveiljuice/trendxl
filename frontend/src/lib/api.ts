/**
 * API Client for TrendXL Backend
 * Handles all HTTP requests to the FastAPI backend
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import {
  AnalysisResponse,
  TrendsResponse,
  TikTokProfileRequest,
  RefreshTrendsRequest,
  HealthStatus,
  APIError,
  ServerErrorData
} from '../types';

class APIClient {
  private client: AxiosInstance;

  constructor(baseURL: string = process.env.REACT_APP_API_URL || '/api/v1') {
    this.client = axios.create({
      baseURL,
      timeout: 60000, // 60 seconds for long-running operations
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        console.error('API Request Error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        console.log(`API Response: ${response.status} ${response.config.url}`);
        return response;
      },
      (error: AxiosError<ServerErrorData>) => {
        const apiError = this.handleError(error);
        console.error('API Response Error:', apiError);
        return Promise.reject(apiError);
      }
    );
  }

  private handleError(error: AxiosError<ServerErrorData>): APIError {
    const apiError = new Error() as APIError;
    
    if (error.response) {
      // Server responded with error status
      apiError.status = error.response.status;
      
      const errorData = error.response.data;
      
      // Handle different error response formats
      if (typeof errorData === 'string') {
        apiError.message = errorData;
      } else if (errorData && typeof errorData === 'object') {
        // Handle FastAPI validation errors
        if ('detail' in errorData && Array.isArray(errorData.detail)) {
          apiError.message = errorData.detail.map(err => err.msg).join(', ');
        }
        // Handle standard error responses with detail field
        else if ('detail' in errorData && typeof errorData.detail === 'string') {
          apiError.message = errorData.detail;
        }
        // Handle custom error responses with message field
        else if ('message' in errorData && typeof errorData.message === 'string') {
          apiError.message = errorData.message;
        }
        // Handle error field
        else if ('error' in errorData && typeof errorData.error === 'string') {
          apiError.message = errorData.error;
        }
        // Fallback for unknown error structure
        else {
          apiError.message = 'Server error';
        }
      } else {
        apiError.message = 'Server error';
      }
      
      apiError.details = errorData;
    } else if (error.request) {
      // Request made but no response received
      apiError.message = 'Network error - please check your connection';
      apiError.status = 0;
    } else {
      // Request setup error
      apiError.message = error.message || 'Request configuration error';
    }

    return apiError;
  }

  /**
   * Health Check
   */
  async healthCheck(): Promise<HealthStatus> {
    try {
      // Use environment-aware URL for health check
      const healthUrl = process.env.REACT_APP_API_URL 
        ? `${process.env.REACT_APP_API_URL.replace('/api/v1', '')}/api/health`
        : '/api/health';
      const response = await axios.get<HealthStatus>(healthUrl);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Profile Analysis Operations
   */
  async analyzeProfile(request: TikTokProfileRequest): Promise<AnalysisResponse> {
    try {
      const response = await this.client.post<AnalysisResponse>('/analyze-profile', request);
      // Strict contract: ensure real user data, surface backend message if invalid
      if (!response.data?.user_profile?.username) {
        const serverMsg = (response.data as any)?.message || 'Backend returned invalid profile payload';
        throw new Error(serverMsg);
      }
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async getUserProfile(username: string): Promise<AnalysisResponse> {
    try {
      const response = await this.client.get<AnalysisResponse>(`/profile/${username}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async reanalyzeProfile(username: string): Promise<AnalysisResponse> {
    try {
      const response = await this.client.post<AnalysisResponse>(`/reanalyze-profile/${username}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Trends Operations
   */
  async refreshTrends(request: RefreshTrendsRequest): Promise<TrendsResponse> {
    try {
      const response = await this.client.post<TrendsResponse>('/refresh-trends', request);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async getSavedTrends(username: string, limit: number = 20): Promise<TrendsResponse> {
    try {
      const response = await this.client.get<TrendsResponse>(`/trends/${username}`, {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async getAllTrends(limit: number = 50): Promise<TrendsResponse> {
    try {
      const response = await this.client.get<TrendsResponse>('/trends', {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  }
}

// Create singleton instance
const apiClient = new APIClient();

// Export individual functions for easier usage
export const api = {
  // Health
  healthCheck: () => apiClient.healthCheck(),

  // Profile Analysis
  analyzeProfile: (tiktokUrl: string) => 
    apiClient.analyzeProfile({ tiktok_url: tiktokUrl }),
  
  getUserProfile: (username: string) => 
    apiClient.getUserProfile(username),
  
  reanalyzeProfile: (username: string) => 
    apiClient.reanalyzeProfile(username),

  // Trends
  refreshTrends: (username: string, maxResults: number = 10) => 
    apiClient.refreshTrends({ username, max_results: maxResults }),
  
  getSavedTrends: (username: string, limit?: number) => 
    apiClient.getSavedTrends(username, limit),
  
  getAllTrends: (limit?: number) => 
    apiClient.getAllTrends(limit),
};

// Export utility functions
export const validateTikTokUrl = (url: string): boolean => {
  const tiktokUrlPattern = /^https?:\/\/(www\.)?(tiktok\.com|vm\.tiktok\.com)\//;
  return tiktokUrlPattern.test(url);
};

export const extractUsernameFromUrl = (url: string): string | null => {
  try {
    const match = url.match(/@([^/]+)/);
    return match ? match[1] : null;
  } catch {
    return null;
  }
};

export const formatNumber = (num: number): string => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
};

export const formatDuration = (ms: number): string => {
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  
  if (minutes > 0) {
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  }
  return `${remainingSeconds}s`;
};

export const calculateEngagementRate = (stats: {
  play_count: number;
  digg_count: number;
  comment_count: number;
  share_count: number;
}): number => {
  const { play_count, digg_count, comment_count, share_count } = stats;
  if (play_count === 0) return 0;
  
  const totalEngagement = digg_count + comment_count + share_count;
  return (totalEngagement / play_count) * 100;
};

export const getRelativeTime = (timestamp: number): string => {
  const now = Date.now();
  const diff = now - timestamp * 1000; // Convert to milliseconds
  
  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  
  if (days > 0) {
    return `${days}d ago`;
  } else if (hours > 0) {
    return `${hours}h ago`;
  } else if (minutes > 0) {
    return `${minutes}m ago`;
  } else {
    return 'Just now';
  }
};

export const getTrendPotentialColor = (potential?: string): string => {
  switch (potential?.toLowerCase()) {
    case 'growing':
      return 'text-emerald-400';
    case 'stable':
      return 'text-blue-400';
    case 'declining':
      return 'text-amber-400';
    default:
      return 'text-gray-400';
  }
};

export const getRelevanceScoreColor = (score?: number): string => {
  if (!score) return 'text-gray-400';
  
  if (score >= 90) return 'text-emerald-400';
  if (score >= 80) return 'text-blue-400';
  if (score >= 70) return 'text-amber-400';
  return 'text-red-400';
};

export const getSentimentColor = (sentiment?: string): string => {
  switch (sentiment?.toLowerCase()) {
    case 'positive':
      return 'text-emerald-400';
    case 'negative':
      return 'text-red-400';
    case 'neutral':
    default:
      return 'text-gray-400';
  }
};

export default apiClient;
