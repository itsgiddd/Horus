import React, { useState } from 'react';
import GlassCard from './GlassCard';
import './SignalsView.css';

function SignalsView() {
  const [signals] = useState([
    {
      id: 1,
      symbol: 'BTC/USD',
      signal: 'BUY',
      confidence: 85,
      price: 43250.50,
      timestamp: '2 mins ago',
      status: 'active',
      targetPrice: 44500,
      stopLoss: 42500,
    },
    {
      id: 2,
      symbol: 'ETH/USD',
      signal: 'SELL',
      confidence: 78,
      price: 2280.75,
      timestamp: '15 mins ago',
      status: 'completed',
      result: 'WIN',
      pnl: '+3.2%',
    },
    {
      id: 3,
      symbol: 'EUR/USD',
      signal: 'HOLD',
      confidence: 65,
      price: 1.0845,
      timestamp: '1 hour ago',
      status: 'completed',
      result: 'HOLD',
    },
    {
      id: 4,
      symbol: 'SOL/USD',
      signal: 'BUY',
      confidence: 92,
      price: 98.45,
      timestamp: '2 hours ago',
      status: 'completed',
      result: 'WIN',
      pnl: '+5.7%',
    },
    {
      id: 5,
      symbol: 'GBP/USD',
      signal: 'SELL',
      confidence: 71,
      price: 1.2670,
      timestamp: '3 hours ago',
      status: 'completed',
      result: 'LOSS',
      pnl: '-1.8%',
    },
  ]);

  const [performanceStats] = useState({
    totalSignals: 247,
    winRate: 73.2,
    avgProfit: 3.4,
    avgLoss: -1.8,
    profitFactor: 2.1,
    currentStreak: 5,
  });

  return (
    <div className="signals-view">
      <div className="signals-header">
        <h2>Trading Signals</h2>
      </div>

      {/* Performance Stats */}
      <div className="performance-stats">
        <GlassCard className="stat-card hover-lift">
          <div className="stat-label">Win Rate</div>
          <div className="stat-value">{performanceStats.winRate}%</div>
          <div className="stat-subtext">{performanceStats.totalSignals} Signals</div>
        </GlassCard>

        <GlassCard className="stat-card hover-lift">
          <div className="stat-label">Avg Profit</div>
          <div className="stat-value positive">+{performanceStats.avgProfit}%</div>
          <div className="stat-subtext">Per Winning Trade</div>
        </GlassCard>

        <GlassCard className="stat-card hover-lift">
          <div className="stat-label">Avg Loss</div>
          <div className="stat-value negative">{performanceStats.avgLoss}%</div>
          <div className="stat-subtext">Per Losing Trade</div>
        </GlassCard>

        <GlassCard className="stat-card hover-lift">
          <div className="stat-label">Profit Factor</div>
          <div className="stat-value">{performanceStats.profitFactor}</div>
          <div className="stat-subtext">Current Streak: {performanceStats.currentStreak}</div>
        </GlassCard>
      </div>

      {/* Signals List */}
      <GlassCard className="signals-list" variant="strong">
        <div className="signals-list-header">
          <h3>Signal History</h3>
          <div className="filter-buttons">
            <button className="filter-btn active">All</button>
            <button className="filter-btn">Active</button>
            <button className="filter-btn">Completed</button>
          </div>
        </div>

        <div className="signals-grid">
          {signals.map((signal) => (
            <div key={signal.id} className="signal-card glass">
              <div className="signal-card-header">
                <div className="signal-symbol">
                  <span className="symbol-name">{signal.symbol}</span>
                  <span className="signal-time">{signal.timestamp}</span>
                </div>
                <span className={`signal-badge ${signal.signal.toLowerCase()}`}>
                  {signal.signal}
                </span>
              </div>

              <div className="signal-card-body">
                <div className="signal-info">
                  <div className="info-item">
                    <span className="info-label">Price</span>
                    <span className="info-value">${signal.price.toLocaleString()}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Confidence</span>
                    <span className="info-value">{signal.confidence}%</span>
                  </div>
                  {signal.targetPrice && (
                    <div className="info-item">
                      <span className="info-label">Target</span>
                      <span className="info-value">${signal.targetPrice.toLocaleString()}</span>
                    </div>
                  )}
                  {signal.stopLoss && (
                    <div className="info-item">
                      <span className="info-label">Stop Loss</span>
                      <span className="info-value">${signal.stopLoss.toLocaleString()}</span>
                    </div>
                  )}
                </div>

                {signal.status === 'completed' && signal.result && (
                  <div className="signal-result">
                    <span className={`result-badge ${signal.result.toLowerCase()}`}>
                      {signal.result}
                    </span>
                    {signal.pnl && (
                      <span className={`pnl ${signal.pnl.startsWith('+') ? 'positive' : 'negative'}`}>
                        {signal.pnl}
                      </span>
                    )}
                  </div>
                )}

                {signal.status === 'active' && (
                  <div className="signal-actions">
                    <button className="action-btn close">Close Position</button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </GlassCard>
    </div>
  );
}

export default SignalsView;
