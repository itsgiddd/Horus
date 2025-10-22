import React, { useState, useEffect, useRef } from 'react';
import GlassCard from './GlassCard';
import './ChartsView.css';

function ChartsView() {
  const [selectedSymbol, setSelectedSymbol] = useState('BTCUSD');
  const [timeframe, setTimeframe] = useState('1H');
  const chartContainerRef = useRef(null);

  const symbols = [
    { value: 'BTCUSD', label: 'BTC/USD' },
    { value: 'ETHUSD', label: 'ETH/USD' },
    { value: 'EURUSD', label: 'EUR/USD' },
    { value: 'GBPUSD', label: 'GBP/USD' },
    { value: 'SOLUSD', label: 'SOL/USD' },
  ];

  const timeframes = ['1', '5', '15', '30', '1H', '4H', '1D', '1W'];

  useEffect(() => {
    // Load TradingView widget
    loadTradingViewWidget();
  }, [selectedSymbol, timeframe]);

  const loadTradingViewWidget = () => {
    if (!chartContainerRef.current) return;

    // Clear previous widget
    chartContainerRef.current.innerHTML = '';

    // Create script for TradingView widget
    const script = document.createElement('script');
    script.src = 'https://s3.tradingview.com/tv.js';
    script.async = true;
    script.onload = () => {
      if (window.TradingView) {
        new window.TradingView.widget({
          autosize: true,
          symbol: selectedSymbol,
          interval: timeframe,
          timezone: 'Etc/UTC',
          theme: 'dark',
          style: '1',
          locale: 'en',
          toolbar_bg: 'rgba(15, 15, 25, 0.7)',
          enable_publishing: false,
          hide_top_toolbar: false,
          hide_legend: false,
          save_image: false,
          container_id: 'tradingview-widget',
          backgroundColor: 'rgba(15, 15, 25, 0.3)',
          gridColor: 'rgba(255, 255, 255, 0.06)',
          hide_side_toolbar: false,
          allow_symbol_change: true,
          studies: [
            'MASimple@tv-basicstudies',
            'RSI@tv-basicstudies',
            'MACD@tv-basicstudies',
          ],
        });
      }
    };

    const widgetContainer = document.createElement('div');
    widgetContainer.id = 'tradingview-widget';
    widgetContainer.style.height = '100%';
    widgetContainer.style.width = '100%';

    chartContainerRef.current.appendChild(widgetContainer);
    document.head.appendChild(script);
  };

  return (
    <div className="charts-view">
      <div className="charts-header">
        <div className="chart-controls">
          <div className="control-group">
            <label>Symbol</label>
            <select
              value={selectedSymbol}
              onChange={(e) => setSelectedSymbol(e.target.value)}
              className="glass-select"
            >
              {symbols.map((sym) => (
                <option key={sym.value} value={sym.value}>
                  {sym.label}
                </option>
              ))}
            </select>
          </div>

          <div className="control-group">
            <label>Timeframe</label>
            <div className="timeframe-buttons">
              {timeframes.map((tf) => (
                <button
                  key={tf}
                  className={`timeframe-btn ${timeframe === tf ? 'active' : ''}`}
                  onClick={() => setTimeframe(tf)}
                >
                  {tf}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="chart-container-wrapper">
        <GlassCard className="chart-card" variant="strong">
          <div ref={chartContainerRef} className="tradingview-chart"></div>
        </GlassCard>
      </div>

      <div className="chart-info">
        <GlassCard className="indicator-panel">
          <h4>Technical Indicators</h4>
          <div className="indicators-grid">
            <div className="indicator-item">
              <span className="indicator-label">RSI (14)</span>
              <span className="indicator-value">65.4</span>
            </div>
            <div className="indicator-item">
              <span className="indicator-label">MACD</span>
              <span className="indicator-value positive">+2.3</span>
            </div>
            <div className="indicator-item">
              <span className="indicator-label">SMA (20)</span>
              <span className="indicator-value">43,120</span>
            </div>
            <div className="indicator-item">
              <span className="indicator-label">Volume</span>
              <span className="indicator-value">2.4M</span>
            </div>
          </div>
        </GlassCard>

        <GlassCard className="ai-insight">
          <h4>AI Insight</h4>
          <div className="insight-content">
            <div className="insight-signal buy">
              <span className="signal-label">Signal</span>
              <span className="signal-badge">BUY</span>
            </div>
            <div className="insight-confidence">
              <span className="confidence-label">Confidence</span>
              <div className="confidence-bar">
                <div className="confidence-fill" style={{ width: '78%' }}></div>
              </div>
              <span className="confidence-value">78%</span>
            </div>
            <p className="insight-text">
              Strong bullish momentum with RSI in healthy range. MACD crossover indicates potential upward movement.
            </p>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}

export default ChartsView;
