import React from 'react';
import { clsx } from 'clsx';

interface LoadingProps {
  size?: 'sm' | 'md' | 'lg';
  text?: string;
  fullScreen?: boolean;
  timer?: number;
  estimatedTime?: number;
  currentStep?: string;
  loadingSteps?: string[];
  isDataReady?: boolean;
}

const Loading: React.FC<LoadingProps> = ({ 
  size = 'md', 
  text, 
  fullScreen = false,
  timer = 0,
  estimatedTime = 0,
  currentStep = '',
  loadingSteps = [],
  isDataReady = false
}) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  const spinner = (
    <div className={clsx('loading-spinner mx-auto', sizeClasses[size])} />
  );

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const content = (
    <div className="flex flex-col items-center justify-center gap-6">
      {/* Main Spinner and Status */}
      <div className="flex flex-col items-center justify-center text-center">
        <div className="flex items-center justify-center mb-3">
          {spinner}
        </div>
        {text && (
          <p className="text-dark-400 text-sm animate-pulse">{text}</p>
        )}
      </div>
      
      {/* Real-time Loading Progress */}
      {fullScreen && (
        <div className="w-96 max-w-md">
          {/* Current Step */}
          {currentStep && (
            <div className="text-center mb-4">
              <h3 className="text-lg font-semibold text-white mb-2">{currentStep}</h3>
              <div className="flex items-center justify-center gap-2">
                <span className="text-sm text-dark-400">
                  Elapsed: {formatTime(timer)}
                </span>
                {isDataReady && (
                  <span className="text-sm text-emerald-400 flex items-center gap-1">
                    ✓ Data Ready
                  </span>
                )}
              </div>
            </div>
          )}

          {/* Progress Steps */}
          {loadingSteps.length > 0 && (
            <div className="bg-dark-800/50 rounded-lg p-4 max-h-48 overflow-y-auto">
              <h4 className="text-sm font-medium text-dark-300 mb-3">Progress:</h4>
              <div className="space-y-2">
                {loadingSteps.slice(-6).map((step, index) => (
                  <div 
                    key={index}
                    className={`text-sm flex items-start gap-2 ${
                      step.startsWith('✓') ? 'text-emerald-400' :
                      step.startsWith('❌') ? 'text-red-400' :
                      step.startsWith('🎉') ? 'text-yellow-400' :
                      'text-dark-300'
                    }`}
                  >
                    <span className="flex-shrink-0 w-1 h-1 bg-current rounded-full mt-2"></span>
                    <span className="leading-relaxed">{step}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Status Bar */}
          <div className="mt-4 text-center">
            <div className="w-full bg-dark-700 rounded-full h-1 mb-2">
              <div 
                className={`h-1 rounded-full transition-all duration-1000 ease-out ${
                  isDataReady 
                    ? 'bg-gradient-to-r from-emerald-600 to-emerald-400' 
                    : 'bg-gradient-to-r from-primary-600 to-primary-400'
                }`}
                style={{ 
                  width: isDataReady ? '100%' : `${Math.min((timer / 10) * 100, 90)}%`
                }}
              />
            </div>
            <p className="text-xs text-dark-500">
              {isDataReady 
                ? 'Analysis complete - preparing results...' 
                : 'Loading comprehensive analytics and trends...'
              }
            </p>
          </div>
        </div>
      )}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-dark-900/80 backdrop-blur-sm z-50 flex items-center justify-center">
        {content}
      </div>
    );
  }

  return content;
};

export default Loading;
