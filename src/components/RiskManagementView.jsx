import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import GlassCard from './GlassCard';
import './RiskManagementView.css';

function RiskManagementView() {
  const riskMetrics = {
    riskScore: 42,
    var95: 2794.63,
    var99: 4471.40,
    maxDrawdown: -12.5,
    sharpeRatio: 1.85,
    sortinoRatio: 2.34,
    beta: 1.15,
    diversificationScore: 68,
  };

  const assetAllocation = [
    { name: 'Crypto', value: 60, color: '#00d4ff' },
    { name: 'Forex', value: 25, color: '#b967ff' },
    { name: 'Cash', value: 15, color: '#05ffa1' },
  ];

  const exposureData = [
    { asset: 'BTC', exposure: 38.7 },
    { asset: 'ETH', exposure: 20.4 },
    { asset: 'EUR/USD', exposure: 19.4 },
    { asset: 'SOL', exposure: 12.1 },
    { asset: 'Cash', exposure: 9.4 },
  ];

  const getRiskLevel = (score) => {
    if (score < 30) return { label: 'Low', color: 'var(--accent-success)' };
    if (score < 60) return { label: 'Medium', color: 'var(--accent-warning)' };
    return { label: 'High', color: 'var(--accent-danger)' };
  };

  const riskLevel = getRiskLevel(riskMetrics.riskScore);

  return (
    <div className="risk-management-view">
      <div className="risk-header">
        <h2>Risk Management</h2>
      </div>

      {/* Risk Score Card */}
      <GlassCard className="risk-score-card" variant="strong">
        <h3>Portfolio Risk Score</h3>
        <div className="risk-score-content">
          <div className="risk-score-gauge">
            <div className="gauge-value">{riskMetrics.riskScore}</div>
            <div className="gauge-label" style={{ color: riskLevel.color }}>
              {riskLevel.label} Risk
            </div>
            <div className="gauge-bar">
              <div
                className="gauge-fill"
                style={{ width: `${riskMetrics.riskScore}%`, background: riskLevel.color }}
              ></div>
            </div>
          </div>

          <div className="risk-factors">
            <div className="risk-factor">
              <span className="factor-label">Concentration Risk</span>
              <span className="factor-value">38%</span>
            </div>
            <div className="risk-factor">
              <span className="factor-label">Volatility Risk</span>
              <span className="factor-value">46%</span>
            </div>
            <div className="risk-factor">
              <span className="factor-label">Leverage Risk</span>
              <span className="factor-value">0%</span>
            </div>
          </div>
        </div>
      </GlassCard>

      {/* Metrics Grid */}
      <div className="risk-metrics-grid">
        <GlassCard className="metric-card hover-lift">
          <div className="metric-label">Value at Risk (95%)</div>
          <div className="metric-value">${riskMetrics.var95.toLocaleString()}</div>
          <div className="metric-subtext">Max loss (95% confidence)</div>
        </GlassCard>

        <GlassCard className="metric-card hover-lift">
          <div className="metric-label">Value at Risk (99%)</div>
          <div className="metric-value">${riskMetrics.var99.toLocaleString()}</div>
          <div className="metric-subtext">Max loss (99% confidence)</div>
        </GlassCard>

        <GlassCard className="metric-card hover-lift">
          <div className="metric-label">Max Drawdown</div>
          <div className="metric-value negative">{riskMetrics.maxDrawdown}%</div>
          <div className="metric-subtext">Historical peak to trough</div>
        </GlassCard>

        <GlassCard className="metric-card hover-lift">
          <div className="metric-label">Sharpe Ratio</div>
          <div className="metric-value positive">{riskMetrics.sharpeRatio}</div>
          <div className="metric-subtext">Risk-adjusted returns</div>
        </GlassCard>

        <GlassCard className="metric-card hover-lift">
          <div className="metric-label">Sortino Ratio</div>
          <div className="metric-value positive">{riskMetrics.sortinoRatio}</div>
          <div className="metric-subtext">Downside risk adjusted</div>
        </GlassCard>

        <GlassCard className="metric-card hover-lift">
          <div className="metric-label">Portfolio Beta</div>
          <div className="metric-value">{riskMetrics.beta}</div>
          <div className="metric-subtext">Market correlation</div>
        </GlassCard>
      </div>

      <div className="risk-charts">
        {/* Asset Allocation */}
        <GlassCard className="allocation-card" variant="strong">
          <h3>Asset Allocation</h3>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={assetAllocation}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {assetAllocation.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div className="allocation-legend">
              {assetAllocation.map((item, index) => (
                <div key={index} className="legend-item">
                  <span className="legend-color" style={{ background: item.color }}></span>
                  <span className="legend-label">{item.name}</span>
                  <span className="legend-value">{item.value}%</span>
                </div>
              ))}
            </div>
          </div>
        </GlassCard>

        {/* Position Exposure */}
        <GlassCard className="exposure-card" variant="strong">
          <h3>Position Exposure</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={exposureData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="asset" stroke="rgba(255,255,255,0.5)" />
              <YAxis stroke="rgba(255,255,255,0.5)" />
              <Tooltip
                contentStyle={{
                  background: 'rgba(15, 15, 25, 0.9)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  borderRadius: '8px',
                }}
              />
              <Bar dataKey="exposure" fill="#00d4ff" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </GlassCard>
      </div>

      {/* Diversification Score */}
      <GlassCard className="diversification-card" variant="strong">
        <h3>Diversification Analysis</h3>
        <div className="diversification-content">
          <div className="diversification-score">
            <div className="score-circle">
              <div className="score-number">{riskMetrics.diversificationScore}</div>
              <div className="score-label">Diversification Score</div>
            </div>
          </div>
          <div className="diversification-insights">
            <div className="insight-item">
              <span className="insight-icon">✓</span>
              <span className="insight-text">Good asset class diversity (Crypto + Forex)</span>
            </div>
            <div className="insight-item">
              <span className="insight-icon">⚠</span>
              <span className="insight-text">High concentration in BTC (38.7%)</span>
            </div>
            <div className="insight-item">
              <span className="insight-icon">✓</span>
              <span className="insight-text">Adequate cash buffer (15%)</span>
            </div>
          </div>
        </div>
      </GlassCard>
    </div>
  );
}

export default RiskManagementView;
