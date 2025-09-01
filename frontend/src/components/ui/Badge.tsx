import React from 'react';
import { clsx } from 'clsx';
import { BadgeProps } from '../../types';

const Badge: React.FC<BadgeProps> = ({ 
  children, 
  variant = 'neutral', 
  size = 'md',
  ...props 
}) => {
  const baseClasses = 'inline-flex items-center font-medium rounded-full border';
  
  const variantClasses = {
    primary: 'bg-primary-900/20 text-primary-400 border-primary-800',
    success: 'bg-emerald-900/20 text-emerald-400 border-emerald-800',
    warning: 'bg-amber-900/20 text-amber-400 border-amber-800',
    danger: 'bg-red-900/20 text-red-400 border-red-800',
    neutral: 'bg-dark-700/50 text-dark-300 border-dark-600',
  };
  
  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-0.5 text-xs',
    lg: 'px-3 py-1 text-sm',
  };
  
  return (
    <span
      className={clsx(
        baseClasses,
        variantClasses[variant],
        sizeClasses[size]
      )}
      {...props}
    >
      {children}
    </span>
  );
};

export default Badge;
