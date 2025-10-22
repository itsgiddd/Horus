import React, { useState, useEffect } from 'react';
import GlassCard from './GlassCard';
import './Dashboard.css';

function Dashboard() {
  const [marketData, setMarketData] = useState({
    btc: { price: 43250.50, change: 2.5 },
    eth: { price: 2280.75, change: -1.2 },
    eurusd: { price: 1.0845, change: 0.3 },
    gbpusd: { price: 1.2670, change: -0.5 },
  });

  const [signals, setSignals] = useState([
    { pair: 'BTC/USD', signal: 'BUY', confidence: 78, time: '2 mins ago' },
    { pair: 'EUR/USD', signal: 'HOLD', confidence: 65, time: '5 mins ago' },
    { pair: 'ETH/USD', signal: 'SELL', confidence: 82, time: '8 mins ago' },
  ]);

  return (
    <div className="dashboard">
      {/* Header Stats */}
      <div className="dashboard-header">
        <GlassCard className="stat-card hover-lift">
          <h4>Portfolio Value</h4>
          <div className="stat-value">$45,892.50</div>
          <div className="stat-change positive">+5.2%</div>
        </GlassCard>

        <GlassCard className="stat-card hover-lift">
          <h4>24h Profit/Loss</h4>
          <div className="stat-value">$2,340.25</div>
          <div className="stat-change positive">+5.4%</div>
        </GlassCard>

        <GlassCard className="stat-card hover-lift">
          <h4>Active Signals</h4>
          <div className="stat-value">{signals.length}</div>
          <div className="stat-change neutral">Live</div>
        </GlassCard>

        <GlassCard className="stat-card hover-lift">
          <h4>Win Rate</h4>
          <div className="stat-value">73%</div>
          <div className="stat-change positive">+2% this week</div>
        </GlassCard>
      </div>

      {/* Main Content */}
      <div className="dashboard-content">
        {/* Market Overview */}
        <GlassCard className="market-overview" variant="strong">
          <h3>Market Overview</h3>
          <div className="market-grid">
            {Object.entries(marketData).map(([symbol, data]) => (
              <div key={symbol} className="market-item">
                <div className="market-symbol">{symbol.toUpperCase()}</div>
                <div className="market-price">${data.price.toLocaleString()}</div>
                <div className={`market-change ${data.change >= 0 ? 'positive' : 'negative'}`}>
                  {data.change >= 0 ? '▲' : '▼'} {Math.abs(data.change)}%
                </div>
              </div>
            ))}
          </div>
        </GlassCard>

        {/* Trading Signals */}
        <GlassCard className="signals-panel" variant="strong">
          <h3>AI Trading Signals</h3>
          <div className="signals-list">
            {signals.map((signal, index) => (
              <div key={index} className="signal-item fade-in">
                <div className="signal-header">
                  <span className="signal-pair">{signal.pair}</span>
                  <span className="signal-time">{signal.time}</span>
                </div>
                <div className="signal-body">
                  <span className={`signal-badge ${signal.signal.toLowerCase()}`}>
                    {signal.signal}
                  </span>
                  <div className="signal-confidence">
                    <div className="confidence-bar">
                      <div
                        className="confidence-fill"
                        style={{ width: `${signal.confidence}%` }}
                      />
                    </div>
                    <span className="confidence-text">{signal.confidence}%</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>

        {/* Chart Placeholder */}
        <GlassCard className="chart-panel" variant="strong">
          <h3>Price Chart</h3>
          <div className="chart-placeholder">
            <div className="chart-overlay">
              <div className="chart-icon">📈</div>
              <p>TradingView Chart Integration</p>
              <small>Connect your trading account to view live charts</small>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}

export default Dashboard;
