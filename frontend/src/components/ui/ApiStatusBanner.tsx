import React from 'react';
import { clsx } from 'clsx';
import { Database, Zap, Layers, AlertTriangle, CheckCircle } from 'lucide-react';

interface ApiStatusBannerProps {
  status: 'ensemble' | 'database' | 'mock';
  className?: string;
}

const ApiStatusBanner: React.FC<ApiStatusBannerProps> = ({
  status,
  className
}) => {
  const getStatusConfig = (status: string) => {
    switch (status) {
      case 'ensemble':
        return {
          icon: <Layers className="w-4 h-4" />,
          label: 'AI Ensemble',
          description: 'Using multiple AI services for optimal results',
          variant: 'success' as const,
          bgColor: 'bg-emerald-900/20',
          borderColor: 'border-emerald-800',
          textColor: 'text-emerald-400'
        };
      case 'database':
        return {
          icon: <Database className="w-4 h-4" />,
          label: 'Database Mode',
          description: 'Using cached data from local database',
          variant: 'primary' as const,
          bgColor: 'bg-primary-900/20',
          borderColor: 'border-primary-800',
          textColor: 'text-primary-400'
        };
      case 'mock':
        return {
          icon: <AlertTriangle className="w-4 h-4" />,
          label: 'Demo Mode',
          description: 'Using sample data for demonstration',
          variant: 'warning' as const,
          bgColor: 'bg-amber-900/20',
          borderColor: 'border-amber-800',
          textColor: 'text-amber-400'
        };
      default:
        return {
          icon: <CheckCircle className="w-4 h-4" />,
          label: 'Unknown',
          description: 'Status unknown',
          variant: 'neutral' as const,
          bgColor: 'bg-dark-700/50',
          borderColor: 'border-dark-600',
          textColor: 'text-dark-300'
        };
    }
  };

  const config = getStatusConfig(status);

  return (
    <div className={clsx(
      'rounded-lg border p-3 transition-all duration-200',
      config.bgColor,
      config.borderColor,
      className
    )}>
      <div className="flex items-center gap-3">
        <div className={clsx('p-1 rounded-md', config.bgColor, config.borderColor)}>
          {config.icon}
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className={clsx('text-sm font-medium', config.textColor)}>
              {config.label}
            </span>
            <div className={clsx(
              'w-2 h-2 rounded-full',
              status === 'ensemble' && 'bg-emerald-400',
              status === 'database' && 'bg-primary-400',
              status === 'mock' && 'bg-amber-400'
            )} />
          </div>
          <p className="text-xs text-dark-400">
            {config.description}
          </p>
        </div>
      </div>
    </div>
  );
};

export default ApiStatusBanner;
