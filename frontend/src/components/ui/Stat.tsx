import React from 'react';
import { clsx } from 'clsx';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { StatProps } from '../../types';

const Stat: React.FC<StatProps> = ({ label, value, icon, trend }) => {
  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-3 h-3 text-emerald-400" />;
      case 'down':
        return <TrendingDown className="w-3 h-3 text-red-400" />;
      case 'neutral':
      default:
        return <Minus className="w-3 h-3 text-gray-400" />;
    }
  };

  const getTrendColor = () => {
    switch (trend) {
      case 'up':
        return 'text-emerald-400';
      case 'down':
        return 'text-red-400';
      case 'neutral':
      default:
        return 'text-gray-400';
    }
  };

  return (
    <div className="stat-card hover:bg-dark-700/70 transition-colors duration-200">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          {icon && (
            <div className="text-primary-400">
              {icon}
            </div>
          )}
          <span className="text-sm text-dark-300 font-medium">{label}</span>
        </div>
        {trend && (
          <div className="flex items-center">
            {getTrendIcon()}
          </div>
        )}
      </div>
      <div className={clsx(
        'text-2xl font-bold',
        trend ? getTrendColor() : 'text-white'
      )}>
        {typeof value === 'number' ? value.toLocaleString() : value}
      </div>
    </div>
  );
};

export default Stat;
