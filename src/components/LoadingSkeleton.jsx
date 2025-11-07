/**
 * Professional Loading Skeleton Components
 * Beautiful skeleton screens for better UX during loading states
 */

import React from 'react';
import '../styles/LoadingSkeleton.css';

/**
 * Chart Loading Skeleton
 */
export const ChartSkeleton = () => {
  return (
    <div className="skeleton-chart">
      <div className="skeleton-chart-header">
        <div className="skeleton skeleton-text skeleton-text-lg"></div>
        <div className="skeleton skeleton-text skeleton-text-sm"></div>
      </div>
      <div className="skeleton-chart-body">
        <div className="skeleton-chart-bars">
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="skeleton-bar"
              style={{
                height: `${Math.random() * 60 + 40}%`,
                animationDelay: `${i * 0.05}s`,
              }}
            ></div>
          ))}
        </div>
      </div>
      <div className="skeleton-chart-footer">
        <div className="skeleton skeleton-button"></div>
        <div className="skeleton skeleton-button"></div>
      </div>
    </div>
  );
};

/**
 * Card Loading Skeleton
 */
export const CardSkeleton = ({ lines = 3 }) => {
  return (
    <div className="skeleton-card">
      <div className="skeleton skeleton-title"></div>
      {[...Array(lines)].map((_, i) => (
        <div
          key={i}
          className="skeleton skeleton-text"
          style={{ width: `${100 - i * 15}%` }}
        ></div>
      ))}
    </div>
  );
};

/**
 * Prediction Panel Skeleton
 */
export const PredictionSkeleton = () => {
  return (
    <div className="skeleton-prediction">
      <div className="skeleton-prediction-header">
        <div className="skeleton skeleton-circle"></div>
        <div className="skeleton skeleton-text skeleton-text-lg"></div>
      </div>
      <div className="skeleton-prediction-body">
        <div className="skeleton skeleton-meter"></div>
        <div className="skeleton skeleton-text skeleton-text-md"></div>
        <div className="skeleton skeleton-text skeleton-text-sm"></div>
      </div>
    </div>
  );
};

/**
 * List Loading Skeleton
 */
export const ListSkeleton = ({ items = 5 }) => {
  return (
    <div className="skeleton-list">
      {[...Array(items)].map((_, i) => (
        <div key={i} className="skeleton-list-item">
          <div className="skeleton skeleton-circle-sm"></div>
          <div className="skeleton-list-content">
            <div className="skeleton skeleton-text skeleton-text-md"></div>
            <div className="skeleton skeleton-text skeleton-text-sm"></div>
          </div>
        </div>
      ))}
    </div>
  );
};

/**
 * Table Loading Skeleton
 */
export const TableSkeleton = ({ rows = 5, columns = 4 }) => {
  return (
    <div className="skeleton-table">
      <div className="skeleton-table-header">
        {[...Array(columns)].map((_, i) => (
          <div key={i} className="skeleton skeleton-text skeleton-text-sm"></div>
        ))}
      </div>
      {[...Array(rows)].map((_, rowIndex) => (
        <div key={rowIndex} className="skeleton-table-row">
          {[...Array(columns)].map((_, colIndex) => (
            <div key={colIndex} className="skeleton skeleton-text"></div>
          ))}
        </div>
      ))}
    </div>
  );
};

/**
 * Full Page Loading Skeleton
 */
export const PageSkeleton = () => {
  return (
    <div className="skeleton-page">
      <div className="skeleton-page-header">
        <div className="skeleton skeleton-logo"></div>
        <div className="skeleton-nav">
          <div className="skeleton skeleton-button"></div>
          <div className="skeleton skeleton-button"></div>
          <div className="skeleton skeleton-button"></div>
        </div>
      </div>
      <div className="skeleton-page-main">
        <ChartSkeleton />
      </div>
    </div>
  );
};

/**
 * Generic Skeleton Box
 */
export const Skeleton = ({ width, height, circle, className = '' }) => {
  const style = {
    width: width || '100%',
    height: height || '20px',
    borderRadius: circle ? '50%' : '8px',
  };

  return <div className={`skeleton ${className}`} style={style}></div>;
};

export default {
  ChartSkeleton,
  CardSkeleton,
  PredictionSkeleton,
  ListSkeleton,
  TableSkeleton,
  PageSkeleton,
  Skeleton,
};
