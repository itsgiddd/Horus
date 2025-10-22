import React from 'react';
import GlassCard from './GlassCard';
import './HistoryView.css';

function HistoryView() {
  return (
    <div className="history-view">
      <div className="history-header">
        <h2>Trade History</h2>
      </div>

      <GlassCard variant="strong">
        <div className="coming-soon">
          <div className="coming-soon-icon">📜</div>
          <h3>Trade History Coming Soon</h3>
          <p>
            View your complete trading history, performance analytics, and detailed trade reports.
            This feature is currently in development.
          </p>
        </div>
      </GlassCard>
    </div>
  );
}

export default HistoryView;
