import React from 'react';
import { SectionTitleProps } from '../../types';

const SectionTitle: React.FC<SectionTitleProps> = ({ 
  title, 
  subtitle, 
  icon, 
  action 
}) => {
  return (
    <div className="flex items-center justify-between mb-6">
      <div className="flex items-center gap-3">
        {icon && (
          <div className="text-primary-400">
            {icon}
          </div>
        )}
        <div>
          <h2 className="text-2xl font-bold text-white">{title}</h2>
          {subtitle && (
            <p className="text-dark-400 mt-1">{subtitle}</p>
          )}
        </div>
      </div>
      {action && (
        <div>
          {action}
        </div>
      )}
    </div>
  );
};

export default SectionTitle;
