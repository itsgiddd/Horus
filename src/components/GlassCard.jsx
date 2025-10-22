import React from 'react';
import './GlassCard.css';

function GlassCard({
  children,
  className = '',
  variant = 'default', // 'default', 'strong', 'hover'
  onClick,
  style = {}
}) {
  const classNames = [
    'glass-card',
    variant === 'strong' ? 'glass-strong' : 'glass',
    variant === 'hover' ? 'hover-lift' : '',
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={classNames} onClick={onClick} style={style}>
      {children}
    </div>
  );
}

export default GlassCard;
