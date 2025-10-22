import React, { useState, useEffect, useRef } from 'react';
import { createChart } from 'lightweight-charts';
import GlassCard from './GlassCard';
import './ChartsView.css';

function ChartsView() {
  const [selectedSymbol, setSelectedSymbol] = useState('BTCUSD');
  const [timeframe, setTimeframe] = useState('1H');
  const [prediction, setPrediction] = useState(null);
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);
  const candleSeriesRef = useRef(null);
  const predictionSeriesRef = useRef(null);

  const symbols = [
    { value: 'BTCUSD', label: 'BTC/USD' },
    { value: 'ETHUSD', label: 'ETH/USD' },
    { value: 'EURUSD', label: 'EUR/USD' },
    { value: 'GBPUSD', label: 'GBP/USD' },
    { value: 'SOLUSD', label: 'SOL/USD' },
  ];

  const timeframes = [
    { value: '1', label: '1m' },
    { value: '5', label: '5m' },
    { value: '15', label: '15m' },
    { value: '1H', label: '1H' },
    { value: '4H', label: '4H' },
    { value: '1D', label: '1D' },
  ];

  // Initialize chart
  useEffect(() => {
    if (!chartContainerRef.current) return;

    // Create chart
    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: chartContainerRef.current.clientHeight,
      layout: {
        background: { color: '#1a1d26' },
        textColor: '#9ca3af',
      },
      grid: {
        vertLines: { color: '#2a2d38' },
        horzLines: { color: '#2a2d38' },
      },
      crosshair: {
        mode: 1,
      },
      rightPriceScale: {
        borderColor: '#373a45',
      },
      timeScale: {
        borderColor: '#373a45',
        timeVisible: true,
        secondsVisible: false,
      },
    });

    // Add candlestick series
    const candleSeries = chart.addCandlestickSeries({
      upColor: '#10b981',
      downColor: '#ef4444',
      borderUpColor: '#10b981',
      borderDownColor: '#ef4444',
      wickUpColor: '#10b981',
      wickDownColor: '#ef4444',
    });

    // Add prediction line series
    const predictionSeries = chart.addLineSeries({
      color: '#3b82f6',
      lineWidth: 2,
      lineStyle: 2, // Dashed line
      lastValueVisible: true,
      priceLineVisible: false,
    });

    chartRef.current = chart;
    candleSeriesRef.current = candleSeries;
    predictionSeriesRef.current = predictionSeries;

    // Load initial data
    loadChartData();

    // Handle resize
    const handleResize = () => {
      chart.applyOptions({
        width: chartContainerRef.current.clientWidth,
        height: chartContainerRef.current.clientHeight,
      });
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, []);

  // Update chart when symbol or timeframe changes
  useEffect(() => {
    if (chartRef.current && candleSeriesRef.current) {
      loadChartData();
    }
  }, [selectedSymbol, timeframe]);

  const loadChartData = () => {
    // Generate realistic historical data
    const data = generateHistoricalData(100);
    candleSeriesRef.current.setData(data);

    // Generate AI prediction
    const predictionData = generatePrediction(data);
    predictionSeriesRef.current.setData(predictionData.line);
    setPrediction(predictionData.insight);

    // Fit content
    chartRef.current.timeScale().fitContent();
  };

  const generateHistoricalData = (count) => {
    const data = [];
    const basePrice = selectedSymbol === 'BTCUSD' ? 43000 :
                     selectedSymbol === 'ETHUSD' ? 2300 :
                     selectedSymbol === 'EURUSD' ? 1.08 :
                     selectedSymbol === 'GBPUSD' ? 1.26 : 100;

    const now = Date.now() / 1000;
    const timeInterval = timeframe === '1' ? 60 :
                        timeframe === '5' ? 300 :
                        timeframe === '15' ? 900 :
                        timeframe === '1H' ? 3600 :
                        timeframe === '4H' ? 14400 : 86400;

    let currentPrice = basePrice;

    for (let i = count; i >= 0; i--) {
      const time = now - (i * timeInterval);
      const volatility = basePrice * 0.002;
      const trend = Math.sin(i / 10) * volatility;
      const noise = (Math.random() - 0.5) * volatility * 2;

      currentPrice += trend + noise;

      const open = currentPrice;
      const close = currentPrice + (Math.random() - 0.5) * volatility;
      const high = Math.max(open, close) + Math.random() * volatility;
      const low = Math.min(open, close) - Math.random() * volatility;

      data.push({
        time: Math.floor(time),
        open: parseFloat(open.toFixed(selectedSymbol.includes('USD') && !selectedSymbol.includes('BTC') && !selectedSymbol.includes('ETH') && !selectedSymbol.includes('SOL') ? 5 : 2)),
        high: parseFloat(high.toFixed(selectedSymbol.includes('USD') && !selectedSymbol.includes('BTC') && !selectedSymbol.includes('ETH') && !selectedSymbol.includes('SOL') ? 5 : 2)),
        low: parseFloat(low.toFixed(selectedSymbol.includes('USD') && !selectedSymbol.includes('BTC') && !selectedSymbol.includes('ETH') && !selectedSymbol.includes('SOL') ? 5 : 2)),
        close: parseFloat(close.toFixed(selectedSymbol.includes('USD') && !selectedSymbol.includes('BTC') && !selectedSymbol.includes('ETH') && !selectedSymbol.includes('SOL') ? 5 : 2)),
      });

      currentPrice = close;
    }

    return data;
  };

  const generatePrediction = (historicalData) => {
    if (historicalData.length === 0) return { line: [], insight: null };

    // Get last 20 candles for prediction
    const recentData = historicalData.slice(-20);
    const lastCandle = historicalData[historicalData.length - 1];
    const lastPrice = lastCandle.close;

    // Simple trend analysis
    const prices = recentData.map(d => d.close);
    const avgPrice = prices.reduce((a, b) => a + b, 0) / prices.length;
    const trend = lastPrice > avgPrice ? 1 : -1;

    // Calculate momentum
    const recentPriceChange = ((lastPrice - recentData[0].close) / recentData[0].close) * 100;
    const momentum = Math.abs(recentPriceChange);

    // Generate prediction line (next 10 periods)
    const predictionLine = [];
    const timeInterval = lastCandle.time - historicalData[historicalData.length - 2].time;
    let predictedPrice = lastPrice;

    for (let i = 1; i <= 10; i++) {
      const noise = (Math.random() - 0.5) * lastPrice * 0.001;
      const trendMove = trend * lastPrice * 0.002 * i;
      predictedPrice = lastPrice + trendMove + noise;

      predictionLine.push({
        time: lastCandle.time + (i * timeInterval),
        value: parseFloat(predictedPrice.toFixed(selectedSymbol.includes('USD') && !selectedSymbol.includes('BTC') && !selectedSymbol.includes('ETH') && !selectedSymbol.includes('SOL') ? 5 : 2)),
      });
    }

    // Calculate confidence based on trend strength
    const confidence = Math.min(50 + momentum * 5, 95);

    // Determine signal
    const signal = trend > 0 ? 'BUY' : 'SELL';
    const priceTarget = predictionLine[predictionLine.length - 1].value;
    const priceChange = ((priceTarget - lastPrice) / lastPrice) * 100;

    const insight = {
      signal,
      confidence: Math.round(confidence),
      priceTarget,
      priceChange: parseFloat(priceChange.toFixed(2)),
      recommendation: momentum > 2 ? 'Strong' : momentum > 1 ? 'Moderate' : 'Weak',
    };

    return { line: predictionLine, insight };
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
              className="chart-select"
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
                  key={tf.value}
                  className={`timeframe-btn ${timeframe === tf.value ? 'active' : ''}`}
                  onClick={() => setTimeframe(tf.value)}
                >
                  {tf.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="chart-main">
        <GlassCard className="chart-card" variant="strong">
          <div ref={chartContainerRef} className="chart-container"></div>
        </GlassCard>
      </div>

      {prediction && (
        <div className="chart-sidebar">
          <GlassCard className="prediction-card">
            <div className="prediction-header">
              <h4>AI Prediction</h4>
              <span className={`prediction-badge ${prediction.signal.toLowerCase()}`}>
                {prediction.signal}
              </span>
            </div>

            <div className="prediction-body">
              <div className="prediction-stat">
                <span className="stat-label">Confidence</span>
                <div className="confidence-meter">
                  <div
                    className="confidence-bar"
                    style={{ width: `${prediction.confidence}%` }}
                  ></div>
                </div>
                <span className="stat-value">{prediction.confidence}%</span>
              </div>

              <div className="prediction-stat">
                <span className="stat-label">Price Target</span>
                <span className="stat-value">${prediction.priceTarget.toLocaleString()}</span>
              </div>

              <div className="prediction-stat">
                <span className="stat-label">Expected Change</span>
                <span className={`stat-value ${prediction.priceChange >= 0 ? 'positive' : 'negative'}`}>
                  {prediction.priceChange >= 0 ? '+' : ''}{prediction.priceChange}%
                </span>
              </div>

              <div className="prediction-stat">
                <span className="stat-label">Signal Strength</span>
                <span className="stat-value">{prediction.recommendation}</span>
              </div>
            </div>

            <div className="prediction-footer">
              <small>Prediction based on recent price action and momentum indicators</small>
            </div>
          </GlassCard>

          <GlassCard className="indicators-card">
            <h4>Technical Indicators</h4>
            <div className="indicators-list">
              <div className="indicator-row">
                <span className="indicator-name">RSI (14)</span>
                <span className="indicator-value">58.4</span>
              </div>
              <div className="indicator-row">
                <span className="indicator-name">MACD</span>
                <span className="indicator-value positive">+1.2</span>
              </div>
              <div className="indicator-row">
                <span className="indicator-name">SMA (20)</span>
                <span className="indicator-value">
                  ${selectedSymbol === 'BTCUSD' ? '42,850' :
                    selectedSymbol === 'ETHUSD' ? '2,280' : '1.0840'}
                </span>
              </div>
              <div className="indicator-row">
                <span className="indicator-name">Volume</span>
                <span className="indicator-value">High</span>
              </div>
            </div>
          </GlassCard>
        </div>
      )}
    </div>
  );
}

export default ChartsView;
