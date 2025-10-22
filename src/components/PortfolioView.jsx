import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import GlassCard from './GlassCard';
import './PortfolioView.css';

function PortfolioView() {
  const [portfolioData, setPortfolioData] = useState({
    totalValue: 55892.50,
    cashBalance: 12018.50,
    invested: 43874.00,
    totalPnL: 5892.50,
    totalPnLPercent: 11.78,
    dayPnL: 342.25,
    dayPnLPercent: 0.62,
  });

  const [positions, setPositions] = useState([
    {
      symbol: 'BTC',
      name: 'Bitcoin',
      quantity: 0.5,
      entryPrice: 42000.0,
      currentPrice: 43250.50,
      value: 21625.25,
      pnl: 625.25,
      pnlPercent: 2.97,
    },
    {
      symbol: 'ETH',
      name: 'Ethereum',
      quantity: 5.0,
      entryPrice: 2200.0,
      currentPrice: 2280.75,
      value: 11403.75,
      pnl: 403.75,
      pnlPercent: 3.67,
    },
    {
      symbol: 'EUR/USD',
      name: 'Euro / US Dollar',
      quantity: 10000,
      entryPrice: 1.0820,
      currentPrice: 1.0845,
      value: 10845.0,
      pnl: 250.0,
      pnlPercent: 2.36,
    },
  ]);

  // Mock performance data
  const performanceData = [
    { date: '01/15', value: 50000 },
    { date: '01/20', value: 51200 },
    { date: '01/25', value: 50800 },
    { date: '02/01', value: 52500 },
    { date: '02/05', value: 53800 },
    { date: '02/10', value: 54200 },
    { date: '02/15', value: 55892 },
  ];

  return (
    <div className="portfolio-view">
      <div className="portfolio-header">
        <h2>Portfolio</h2>
      </div>

      {/* Summary Cards */}
      <div className="portfolio-summary">
        <GlassCard className="summary-card hover-lift">
          <div className="summary-label">Total Value</div>
          <div className="summary-value">${portfolioData.totalValue.toLocaleString()}</div>
          <div className={`summary-change ${portfolioData.totalPnLPercent >= 0 ? 'positive' : 'negative'}`}>
            {portfolioData.totalPnLPercent >= 0 ? '▲' : '▼'} {Math.abs(portfolioData.totalPnLPercent)}%
          </div>
        </GlassCard>

        <GlassCard className="summary-card hover-lift">
          <div className="summary-label">Cash Balance</div>
          <div className="summary-value">${portfolioData.cashBalance.toLocaleString()}</div>
          <div className="summary-subtext">Available</div>
        </GlassCard>

        <GlassCard className="summary-card hover-lift">
          <div className="summary-label">Invested</div>
          <div className="summary-value">${portfolioData.invested.toLocaleString()}</div>
          <div className="summary-subtext">{positions.length} Positions</div>
        </GlassCard>

        <GlassCard className="summary-card hover-lift">
          <div className="summary-label">Total P&L</div>
          <div className="summary-value positive">${portfolioData.totalPnL.toLocaleString()}</div>
          <div className="summary-change positive">
            +{portfolioData.totalPnLPercent}%
          </div>
        </GlassCard>
      </div>

      {/* Performance Chart */}
      <GlassCard className="performance-chart" variant="strong">
        <h3>Portfolio Performance</h3>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={performanceData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey="date" stroke="rgba(255,255,255,0.5)" />
            <YAxis stroke="rgba(255,255,255,0.5)" />
            <Tooltip
              contentStyle={{
                background: 'rgba(15, 15, 25, 0.9)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '8px',
              }}
            />
            <Line type="monotone" dataKey="value" stroke="#00d4ff" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </GlassCard>

      {/* Positions Table */}
      <GlassCard className="positions-table" variant="strong">
        <h3>Positions</h3>
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Symbol</th>
                <th>Quantity</th>
                <th>Entry Price</th>
                <th>Current Price</th>
                <th>Value</th>
                <th>P&L</th>
                <th>P&L %</th>
              </tr>
            </thead>
            <tbody>
              {positions.map((position, index) => (
                <tr key={index}>
                  <td>
                    <div className="symbol-cell">
                      <span className="symbol-name">{position.symbol}</span>
                      <span className="symbol-fullname">{position.name}</span>
                    </div>
                  </td>
                  <td>{position.quantity}</td>
                  <td>${position.entryPrice.toLocaleString()}</td>
                  <td>${position.currentPrice.toLocaleString()}</td>
                  <td className="value-cell">${position.value.toLocaleString()}</td>
                  <td className={position.pnl >= 0 ? 'positive' : 'negative'}>
                    ${position.pnl.toLocaleString()}
                  </td>
                  <td className={position.pnlPercent >= 0 ? 'positive' : 'negative'}>
                    {position.pnlPercent >= 0 ? '+' : ''}{position.pnlPercent}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </GlassCard>
    </div>
  );
}

export default PortfolioView;
