import React, { useState, useCallback, useEffect, ChangeEvent } from 'react';
import { 
  Sparkles, 
  Search, 
  AlertCircle, 
  TrendingUp,
  Zap,
  Globe,
  Target
} from 'lucide-react';
import { 
  UserProfile, 
  ProfileAnalysis, 
  TrendItem, 
  LoadingState
} from './types';
import { 
  api, 
  validateTikTokUrl, 
  extractUsernameFromUrl 
} from './lib/api';
import ProfileCard from './components/ProfileCard';
import ProfileAnalytics from './components/ProfileAnalytics';
import NicheAnalyzer from './components/NicheAnalyzer';
import ParallaxTrendsSection from './components/ParallaxTrendsSection';

import TrendsChart from './components/TrendsChart';
import ErrorMessage from './components/ErrorMessage';
import SectionTitle from './components/ui/SectionTitle';
import Loading from './components/ui/Loading';
import Badge from './components/ui/Badge';

function App() {
  // State
  const [tiktokUrl, setTiktokUrl] = useState('');
  const [currentUser, setCurrentUser] = useState<UserProfile | null>(null);
  const [currentAnalysis, setCurrentAnalysis] = useState<ProfileAnalysis | null>(null);
  const [trends, setTrends] = useState<TrendItem[]>([]);
  const [loading, setLoading] = useState<LoadingState>({
    analyzing: false,
    refreshing: false,
    loading: false
  });
  const [error, setError] = useState<string | null>(null);
  const [urlError, setUrlError] = useState<string | null>(null);

  // Simple logging for development (no UI display)
  const logAction = useCallback((message: string) => {
    console.log(`[TrendXL] ${message}`);
  }, []);

  // Handle URL validation
  const handleUrlChange = (value: string) => {
    setTiktokUrl(value);
    setUrlError(null);
    setShowResults(false); // Reset results when URL changes
    
    if (value && !validateTikTokUrl(value)) {
      setUrlError('Please enter a valid TikTok profile URL');
    }
  };

  // Timer state for loading
  const [loadingTimer, setLoadingTimer] = useState(0);
  const [estimatedTime, setEstimatedTime] = useState(0);
  const [loadingSteps, setLoadingSteps] = useState<string[]>([]);
  const [currentStep, setCurrentStep] = useState('');
  const [isDataReady, setIsDataReady] = useState(false);
  const [showResults, setShowResults] = useState(false);

  // Analyze TikTok profile with comprehensive data loading
  const analyzeProfile = async () => {
    if (!tiktokUrl.trim()) {
      setUrlError('Please enter a TikTok URL');
      return;
    }

    if (!validateTikTokUrl(tiktokUrl)) {
      setUrlError('Please enter a valid TikTok profile URL');
      return;
    }

    const username = extractUsernameFromUrl(tiktokUrl);
    logAction(`Starting analysis for profile: ${username || tiktokUrl}`);
    
    // Reset states
    setLoading((prev: LoadingState) => ({ ...prev, analyzing: true }));
    setError(null);
    setLoadingTimer(0);
    setEstimatedTime(0);
    setIsDataReady(false);
    setShowResults(false);
    setLoadingSteps([]);
    setCurrentStep('');

    const startTime = Date.now();
    
    // Real-time timer that tracks actual loading time
    const timerInterval = setInterval(() => {
      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      setLoadingTimer(elapsed);
    }, 1000);

    try {
      // Step 1: Analyze profile
      setCurrentStep('Analyzing TikTok profile...');
      setLoadingSteps(prev => [...prev, 'Profile analysis started']);
      
      const response = await api.analyzeProfile(tiktokUrl);
      
      if (response.success && response.user_profile?.username) {
        setCurrentUser(response.user_profile);
        setCurrentAnalysis(response.profile_analysis);
        setLoadingSteps(prev => [...prev, `✓ Profile analyzed: @${response.user_profile.username}`]);
        logAction(`Successfully analyzed @${response.user_profile.username}`);
        
        // Step 2: Load trends and all metrics
        setCurrentStep('Loading personalized trends...');
        setLoadingSteps(prev => [...prev, 'Fetching trending content']);
        
        await loadTrendsAndMetrics(response.user_profile.username);
        
        // Step 3: Finalizing data
        setCurrentStep('Preparing analytics dashboard...');
        setLoadingSteps(prev => [...prev, '✓ All metrics loaded', '✓ Dashboard ready']);
        
        // Mark data as ready
        setIsDataReady(true);
        
        // Wait a minimum time for good UX (at least 5 seconds total)
        const elapsed = Date.now() - startTime;
        const minLoadTime = 5000; // 5 seconds minimum
        
        if (elapsed < minLoadTime) {
          setCurrentStep('Finalizing...');
          await new Promise(resolve => setTimeout(resolve, minLoadTime - elapsed));
        }
        
        // Final step - show results
        setEstimatedTime(Math.floor((Date.now() - startTime) / 1000));
        setCurrentStep('Complete!');
        setLoadingSteps(prev => [...prev, '🎉 Analysis complete']);
        
        // Small delay before showing results for smooth transition
        setTimeout(() => {
          setShowResults(true);
          clearInterval(timerInterval);
          setLoading((prev: LoadingState) => ({ ...prev, analyzing: false }));
        }, 1000);
        
      } else {
        throw new Error(response.message || 'Failed to analyze profile');
      }
    } catch (err: any) {
      clearInterval(timerInterval);
      const errorMessage = err.message || 'Failed to analyze profile';
      setError(errorMessage);
      setCurrentStep('Error occurred');
      setLoadingSteps(prev => [...prev, `❌ Error: ${errorMessage}`]);
      logAction(`Error: ${errorMessage}`);
      setLoading((prev: LoadingState) => ({ ...prev, analyzing: false }));
    }
  };

  // Load trends and all metrics synchronously
  const loadTrendsAndMetrics = async (username: string) => {
    try {
      // Load saved trends first
      setLoadingSteps(prev => [...prev, 'Checking saved trends...']);
      const savedResponse = await api.getSavedTrends(username, 20);
      
      if (savedResponse.success && savedResponse.trends.length > 0) {
        setTrends(savedResponse.trends);
        setLoadingSteps(prev => [...prev, `✓ Loaded ${savedResponse.trends.length} saved trends`]);
        logAction(`Loaded ${savedResponse.trends.length} saved trends`);
      } else {
        // If no saved trends, refresh new ones
        setLoadingSteps(prev => [...prev, 'Generating new personalized trends...']);
        const refreshResponse = await api.refreshTrends(username, 10);
        
        if (refreshResponse.success) {
          setTrends(refreshResponse.trends);
          setLoadingSteps(prev => [...prev, `✓ Generated ${refreshResponse.trends.length} relevant trends`]);
          logAction(`Found ${refreshResponse.trends.length} relevant trends`);
        }
      }
      
      // Simulate additional processing time for comprehensive analysis
      setLoadingSteps(prev => [...prev, 'Calculating engagement metrics...']);
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setLoadingSteps(prev => [...prev, 'Processing analytics data...']);
      await new Promise(resolve => setTimeout(resolve, 1000));
      
    } catch (err: any) {
      setLoadingSteps(prev => [...prev, `❌ Error loading trends: ${err.message}`]);
      logAction(`Failed to load trends: ${err.message}`);
      throw err; // Re-throw to handle in main function
    }
  };

  // Refresh trends
  const refreshTrends = async () => {
    if (!currentUser) return;

    logAction(`Refreshing trends for @${currentUser.username}`);
    setLoading((prev: LoadingState) => ({ ...prev, refreshing: true }));
    setError(null);

    try {
      const response = await api.refreshTrends(currentUser.username, 10);
      
      if (response.success) {
        setTrends(response.trends);
        logAction(`Found ${response.trends.length} relevant trends for @${currentUser.username}`);
      } else {
        throw new Error(response.message || 'Failed to refresh trends');
      }
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to refresh trends';
      setError(errorMessage);
      logAction(`Error: ${errorMessage}`);
    } finally {
      setLoading((prev: LoadingState) => ({ ...prev, refreshing: false }));
    }
  };



  // Check backend health on mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        await api.healthCheck();
      } catch (err) {
        console.warn('Backend health check failed:', err);
      }
    };
    
    checkHealth();
  }, []);

  return (
    <div className="min-h-screen gradient-bg">
      {/* Header */}
      <header className="border-b border-dark-700 backdrop-blur-glass sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary-600 rounded-lg">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold gradient-text">TrendXL</h1>
                <p className="text-sm text-dark-400">AI Trend Feed</p>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <Badge variant="success" size="sm">
                <Zap className="w-3 h-3 mr-1" />
                AI Powered
              </Badge>
              <Badge variant="primary" size="sm">
                <Globe className="w-3 h-3 mr-1" />
                Live Data
              </Badge>
              {showResults && currentUser && (
                <button
                  onClick={() => {
                    setShowResults(false);
                    setCurrentUser(null);
                    setCurrentAnalysis(null);
                    setTrends([]);
                    setTiktokUrl('');
                    setError(null);
                  }}
                  className="btn btn-ghost text-xs px-2 py-1"
                >
                  Analyze Another
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Profile Analysis Section */}
        {!currentUser || !showResults ? (
          <div className="max-w-2xl mx-auto">
            <div className="text-center mb-8">
              <Target className="w-16 h-16 text-primary-400 mx-auto mb-4" />
              <h2 className="text-3xl font-bold text-white mb-2">
                Discover Your TikTok Trends
              </h2>
              <p className="text-dark-400 text-lg">
                Paste a TikTok profile URL to get AI-powered trend recommendations
              </p>
            </div>

            <div className="card">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-dark-300 mb-2">
                    TikTok Profile URL
                  </label>
                  <input
                    type="url"
                    value={tiktokUrl}
                    onChange={(e: ChangeEvent<HTMLInputElement>) => handleUrlChange(e.target.value)}
                    placeholder="https://www.tiktok.com/@username"
                    className={`input ${urlError ? 'border-red-500 focus:ring-red-500' : ''}`}
                    disabled={loading.analyzing}
                  />
                  {urlError && (
                    <div className="flex items-center gap-2 mt-2 text-red-400 text-sm">
                      <AlertCircle className="w-4 h-4" />
                      <span>{urlError}</span>
                    </div>
                  )}
                </div>

                <button
                  onClick={analyzeProfile}
                  disabled={loading.analyzing || !!urlError}
                  className="btn btn-primary w-full flex items-center justify-center gap-2"
                >
                  <Search className={`w-4 h-4 ${loading.analyzing ? 'animate-pulse' : ''}`} />
                  {loading.analyzing ? 'Analyzing Profile...' : 'Analyze Profile'}
                </button>

                {error && (
                  <ErrorMessage 
                    error={error} 
                    onRetry={() => {
                      setError(null);
                      if (tiktokUrl) analyzeProfile();
                    }}
                  />
                )}
              </div>
            </div>
          </div>
        ) : (
          /* Main Dashboard */
          <div className="space-y-8">
            {/* Profile Section - Moved to Center */}
            <div className="max-w-4xl mx-auto">
              <ProfileCard
                profile={currentUser}
                analysis={currentAnalysis!}
                onRefreshTrends={refreshTrends}
                loading={loading.refreshing}
              />
            </div>

            {/* Advanced Analytics Section */}
            {currentUser && currentAnalysis && (
              <div className="max-w-6xl mx-auto">
                <ProfileAnalytics
                  profile={currentUser}
                  analysis={currentAnalysis}
                  trends={trends}
                />
              </div>
            )}

            {/* Deep Niche Analysis */}
            {currentUser && currentAnalysis && trends.length > 0 && (
              <div className="max-w-6xl mx-auto">
                <NicheAnalyzer
                  profile={currentUser}
                  analysis={currentAnalysis}
                  trends={trends}
                />
              </div>
            )}

            {/* Trends Analytics Chart */}
            {trends.length > 0 && (
              <div className="max-w-6xl mx-auto">
                <TrendsChart trends={trends} />
              </div>
            )}

            {/* Trends Feed - Full Width */}
            <div className="max-w-6xl mx-auto">
              <SectionTitle
                title="Trending Now"
                subtitle={`Personalized trends for @${currentUser.username}`}
                icon={<TrendingUp className="w-5 h-5" />}
                action={
                  <div className="flex items-center gap-2">
                    <Badge variant="primary" size="sm">
                      {trends.length} trends
                    </Badge>
                  </div>
                }
              />

              {loading.refreshing ? (
                <div className="flex items-center justify-center py-12">
                  <Loading size="lg" text="Finding relevant trends..." />
                </div>
              ) : trends.length === 0 ? (
                <div className="text-center py-12">
                  <TrendingUp className="w-16 h-16 text-dark-600 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-white mb-2">
                    No trends found yet
                  </h3>
                  <p className="text-dark-400 mb-4">
                    All trends and metrics will load automatically
                  </p>
                </div>
              ) : (
                <ParallaxTrendsSection 
                  trends={trends} 
                  title="Trending Now"
                />
              )}

              {error && (
                <ErrorMessage 
                  error={error} 
                  onRetry={() => {
                    setError(null);
                    if (currentUser) refreshTrends();
                  }}
                />
              )}
            </div>
          </div>
        )}
      </main>

      {/* Loading Overlay */}
      {loading.analyzing && (
        <Loading 
          fullScreen 
          text="Analyzing TikTok profile with AI..." 
          size="lg"
          timer={loadingTimer}
          estimatedTime={estimatedTime}
          currentStep={currentStep}
          loadingSteps={loadingSteps}
          isDataReady={isDataReady}
        />
      )}
    </div>
  );
}

export default App;
