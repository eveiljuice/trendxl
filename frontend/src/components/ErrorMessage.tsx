import React from 'react';
import { 
  AlertTriangle, 
  ExternalLink, 
  RefreshCw,
  Key,
  Eye,
  HelpCircle
} from 'lucide-react';

interface ErrorMessageProps {
  error: string;
  onRetry?: () => void;
  className?: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ 
  error, 
  onRetry, 
  className = '' 
}) => {
  const getErrorDetails = (errorMessage: string) => {
    // Parse common error patterns
    if (errorMessage.includes('502') && errorMessage.includes('missing username')) {
      return {
        type: 'api_data',
        title: 'TikTok Profile Data Issue',
        description: 'The TikTok API couldn\'t retrieve complete profile data.',
        suggestions: [
          'Make sure the TikTok profile exists and is public',
          'Try a different profile (like @daviddobrik) to test',
          'Check if the username is spelled correctly'
        ],
        debugUrl: `/api/debug/test-profile/`
      };
    }
    
    if (errorMessage.includes('404') || errorMessage.includes('not found')) {
      return {
        type: 'not_found',
        title: 'Profile Not Found',
        description: 'The TikTok profile couldn\'t be found.',
        suggestions: [
          'Verify the profile URL is correct',
          'Make sure the profile is public',
          'Try without the @ symbol in the username'
        ]
      };
    }
    
    if (errorMessage.includes('403') || errorMessage.includes('Authentication')) {
      return {
        type: 'auth',
        title: 'API Authentication Issue',
        description: 'There\'s an issue with the API keys.',
        suggestions: [
          'Check if API keys are properly configured',
          'Contact support if the issue persists'
        ],
        debugUrl: '/api/debug/api-keys'
      };
    }
    
    if (errorMessage.includes('429') || errorMessage.includes('rate limit')) {
      return {
        type: 'rate_limit',
        title: 'Rate Limit Reached',
        description: 'Too many requests. Please wait before trying again.',
        suggestions: [
          'Wait a few minutes and try again',
          'Try with a different profile'
        ]
      };
    }
    
    if (errorMessage.includes('Network error')) {
      const isNetlify = typeof window !== 'undefined' && window.location.hostname.includes('netlify');
      return {
        type: 'network',
        title: isNetlify ? 'Backend API Unavailable' : 'Connection Issue',
        description: isNetlify
          ? '🚀 TrendXL deployed on Netlify. Backend API is not available. For full functionality, run locally with Docker.'
          : 'Cannot connect to the server.',
        suggestions: isNetlify ? [
          'Clone the repository locally',
          'Run with Docker: docker-compose up --build',
          'Access at http://localhost:3000',
          'Full functionality requires backend API'
        ] : [
          'Check your internet connection',
          'Make sure the server is running',
          'Try refreshing the page'
        ]
      };
    }
    
    // Generic error
    return {
      type: 'generic',
      title: 'Something went wrong',
      description: errorMessage,
      suggestions: [
        'Try again in a few moments',
        'Check the console for more details'
      ]
    };
  };

  const errorDetails = getErrorDetails(error);
  
  const getIconForType = (type: string) => {
    switch (type) {
      case 'api_data':
        return <Eye className="w-5 h-5" />;
      case 'not_found':
        return <HelpCircle className="w-5 h-5" />;
      case 'auth':
        return <Key className="w-5 h-5" />;
      case 'rate_limit':
        return <RefreshCw className="w-5 h-5" />;
      case 'network':
        return <ExternalLink className="w-5 h-5" />;
      default:
        return <AlertTriangle className="w-5 h-5" />;
    }
  };
  
  const getColorForType = (type: string) => {
    switch (type) {
      case 'api_data':
        return 'border-blue-500 bg-blue-900/20';
      case 'not_found':
        return 'border-yellow-500 bg-yellow-900/20';
      case 'auth':
        return 'border-purple-500 bg-purple-900/20';
      case 'rate_limit':
        return 'border-orange-500 bg-orange-900/20';
      case 'network':
        return 'border-red-500 bg-red-900/20';
      default:
        return 'border-red-500 bg-red-900/20';
    }
  };

  return (
    <div className={`rounded-lg border-l-4 p-4 ${getColorForType(errorDetails.type)} ${className}`}>
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 text-white">
          {getIconForType(errorDetails.type)}
        </div>
        
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-white mb-2">
            {errorDetails.title}
          </h3>
          
          <p className="text-gray-300 mb-3">
            {errorDetails.description}
          </p>
          
          {errorDetails.suggestions && errorDetails.suggestions.length > 0 && (
            <div className="mb-4">
              <h4 className="text-sm font-medium text-white mb-2">
                Try these solutions:
              </h4>
              <ul className="space-y-1">
                {errorDetails.suggestions.map((suggestion, index) => (
                  <li key={index} className="text-sm text-gray-300 flex items-start gap-2">
                    <span className="text-green-400 mt-1">•</span>
                    <span>{suggestion}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          <div className="flex items-center gap-3">
            {onRetry && (
              <button
                onClick={onRetry}
                className="btn btn-secondary btn-sm flex items-center gap-2"
              >
                <RefreshCw className="w-4 h-4" />
                Try Again
              </button>
            )}
            
            {errorDetails.debugUrl && (
              <a
                href={errorDetails.debugUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-blue-400 hover:text-blue-300 flex items-center gap-1"
              >
                <ExternalLink className="w-4 h-4" />
                Debug Info
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;
