import React, { useState, useEffect, useRef } from 'react';
import { createChart } from 'lightweight-charts';
import './AdvancedChart.css';

function AdvancedChart({ symbol = 'EUR/USD', timeframe = '1h' }) {
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);
  const candleSeriesRef = useRef(null);
  const predictionSeriesRef = useRef(null);

  const [currentSymbol, setCurrentSymbol] = useState(symbol);
  const [currentTimeframe, setCurrentTimeframe] = useState(timeframe);
  const [chartData, setChartData] = useState([]);
  const [predictionCandles, setPredictionCandles] = useState([]);
  const [patterns, setPatterns] = useState([]);
  const [pushAnalysis, setPushAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [predicting, setPredicting] = useState(false);
  const [predictionGenerated, setPredictionGenerated] = useState(false);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: chartContainerRef.current.clientHeight,
      layout: {
        background: { color: 'transparent' },
        textColor: '#d1d4dc',
      },
      grid: {
        vertLines: { color: 'rgba(255, 255, 255, 0.05)' },
        horzLines: { color: 'rgba(255, 255, 255, 0.05)' },
      },
      crosshair: {
        mode: 0,
        vertLine: {
          color: 'rgba(138, 43, 226, 0.5)',
          width: 1,
          style: 1,
          labelBackgroundColor: '#8a2be2',
        },
        horzLine: {
          color: 'rgba(138, 43, 226, 0.5)',
          width: 1,
          style: 1,
          labelBackgroundColor: '#8a2be2',
        },
      },
      rightPriceScale: {
        borderColor: 'rgba(255, 255, 255, 0.1)',
      },
      timeScale: {
        borderColor: 'rgba(255, 255, 255, 0.1)',
        timeVisible: true,
        secondsVisible: false,
      },
    });

    const candleSeries = chart.addCandlestickSeries({
      upColor: '#26a69a',
      downColor: '#ef5350',
      borderUpColor: '#26a69a',
      borderDownColor: '#ef5350',
      wickUpColor: '#26a69a',
      wickDownColor: '#ef5350',
    });

    const predictionSeries = chart.addCandlestickSeries({
      upColor: 'rgba(138, 43, 226, 0.4)',
      downColor: 'rgba(226, 43, 138, 0.4)',
      borderUpColor: 'rgba(138, 43, 226, 0.8)',
      borderDownColor: 'rgba(226, 43, 138, 0.8)',
      wickUpColor: 'rgba(138, 43, 226, 0.6)',
      wickDownColor: 'rgba(226, 43, 138, 0.6)',
    });

    chartRef.current = chart;
    candleSeriesRef.current = candleSeries;
    predictionSeriesRef.current = predictionSeries;

    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({
          width: chartContainerRef.current.clientWidth,
          height: chartContainerRef.current.clientHeight,
        });
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, []);

  useEffect(() => {
    fetchMarketData();
  }, [currentSymbol, currentTimeframe]);

  const fetchMarketData = async () => {
    setLoading(true);
    setPredictionGenerated(false);
    setPredictionCandles([]);
    if (predictionSeriesRef.current) {
      predictionSeriesRef.current.setData([]);
    }
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/market/history/${currentSymbol}?timeframe=${currentTimeframe}&limit=200`
      );
      const data = await response.json();

      if (data.history) {
        const formattedData = data.history.map(candle => ({
          time: candle.timestamp / 1000,
          open: candle.open,
          high: candle.high,
          low: candle.low,
          close: candle.close,
        }));

        setChartData(formattedData);
        if (candleSeriesRef.current) {
          candleSeriesRef.current.setData(formattedData);
        }

        fetchPatternAndPushAnalysis();
      }
    } catch (error) {
      console.error('Error fetching market data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchPatternAndPushAnalysis = async () => {
    try {
      const [patternsRes, pushRes] = await Promise.all([
        fetch(`http://127.0.0.1:5000/api/signals/patterns/${currentSymbol}?timeframe=${currentTimeframe}`),
        fetch(`http://127.0.0.1:5000/api/signals/push-analysis/${currentSymbol}?timeframe=${currentTimeframe}`),
      ]);

      if (patternsRes.ok) {
        const patternsData = await patternsRes.json();
        setPatterns(patternsData.patterns || []);
        drawPatternMarkers(patternsData.patterns || []);
      }

      if (pushRes.ok) {
        const pushData = await pushRes.json();
        setPushAnalysis(pushData.analysis);
        drawPushMarkers(pushData.analysis);
      }
    } catch (error) {
      console.error('Error fetching pattern and push analysis:', error);
    }
  };

  const generatePrediction = async () => {
    setPredicting(true);
    setPredictionGenerated(false);
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/signals/advanced-prediction/${currentSymbol}?timeframe=${currentTimeframe}`,
        { method: 'POST' }
      );

      if (response.ok) {
        const predData = await response.json();
        if (predData.prediction && predData.prediction.predicted_candles) {
          displayPredictionCandles(predData.prediction.predicted_candles);
          setPredictionGenerated(true);
        }
      }
    } catch (error) {
      console.error('Error generating prediction:', error);
    } finally {
      setPredicting(false);
    }
  };

  const drawPatternMarkers = (patterns) => {
    if (!chartRef.current || !patterns.length) return;

    patterns.slice(0, 5).forEach((pattern, idx) => {
      const marker = {
        time: chartData[chartData.length - 1]?.time || Date.now() / 1000,
        position: pattern.bias === 'Bullish' ? 'belowBar' : 'aboveBar',
        color: pattern.bias === 'Bullish' ? '#26a69a' : '#ef5350',
        shape: 'circle',
        text: pattern.type.substring(0, 15),
      };

      if (candleSeriesRef.current) {
        const existingMarkers = candleSeriesRef.current.markers();
        candleSeriesRef.current.setMarkers([...existingMarkers, marker]);
      }
    });
  };

  const drawPushMarkers = (analysis) => {
    if (!chartRef.current || !analysis || !analysis.push_details) return;

    analysis.push_details.forEach((push, idx) => {
      if (idx < chartData.length) {
        const marker = {
          time: chartData[Math.min(push.end_idx || idx, chartData.length - 1)]?.time || Date.now() / 1000,
          position: push.direction === 'bullish' ? 'belowBar' : 'aboveBar',
          color: '#8a2be2',
          shape: 'arrowUp',
          text: `Push ${idx + 1}`,
        };

        if (candleSeriesRef.current) {
          const existingMarkers = candleSeriesRef.current.markers();
          candleSeriesRef.current.setMarkers([...existingMarkers, marker]);
        }
      }
    });
  };

  const displayPredictionCandles = (candles) => {
    if (!predictionSeriesRef.current || !chartData.length) return;

    const lastTime = chartData[chartData.length - 1].time;
    const timeInterval = chartData.length > 1
      ? chartData[chartData.length - 1].time - chartData[chartData.length - 2].time
      : 3600;

    const predictionData = candles.map((candle, idx) => ({
      time: lastTime + ((idx + 1) * timeInterval),
      open: candle.open,
      high: candle.high,
      low: candle.low,
      close: candle.close,
    }));

    setPredictionCandles(predictionData);
    predictionSeriesRef.current.setData(predictionData);
  };

  return (
    <div className="advanced-chart-container">
      <div className="chart-controls">
        <div className="symbol-controls">
          <select
            value={currentSymbol}
            onChange={(e) => setCurrentSymbol(e.target.value)}
            className="chart-select"
          >
            <option value="EUR/USD">EUR/USD</option>
            <option value="GBP/USD">GBP/USD</option>
            <option value="USD/JPY">USD/JPY</option>
            <option value="BTC">Bitcoin</option>
            <option value="ETH">Ethereum</option>
            <option value="SOL">Solana</option>
          </select>

          <select
            value={currentTimeframe}
            onChange={(e) => setCurrentTimeframe(e.target.value)}
            className="chart-select"
          >
            <option value="15m">15 Minutes</option>
            <option value="1h">1 Hour</option>
            <option value="4h">4 Hours</option>
            <option value="1d">1 Day</option>
          </select>
        </div>

        <button
          className="prediction-btn"
          onClick={generatePrediction}
          disabled={predicting || loading || chartData.length === 0}
        >
          {predicting ? (
            <>
              <div className="btn-spinner"></div>
              Generating...
            </>
          ) : predictionGenerated ? (
            'Regenerate Prediction'
          ) : (
            'Generate AI Prediction'
          )}
        </button>
      </div>

      {loading && (
        <div className="chart-loading-overlay">
          <div className="loading-spinner"></div>
          <span>Loading chart data...</span>
        </div>
      )}

      <div ref={chartContainerRef} className="chart-canvas"></div>

      {pushAnalysis && (
        <div className="push-analysis-overlay">
          <div className={`push-indicator ${pushAnalysis.warning_level.toLowerCase()}`}>
            <div className="push-count">
              Push {pushAnalysis.active_pushes}/{pushAnalysis.exhaustion_threshold}
            </div>
            <div className="exhaustion-bar">
              <div
                className="exhaustion-fill"
                style={{ width: `${pushAnalysis.exhaustion_level}%` }}
              ></div>
            </div>
            <div className="warning-text">
              {pushAnalysis.should_exit ? 'EXIT - Market Exhausted!' : `${pushAnalysis.remaining_safe_pushes} pushes remaining`}
            </div>
          </div>
        </div>
      )}

      {patterns.length > 0 && (
        <div className="patterns-legend">
          <h5>Detected Patterns</h5>
          {patterns.slice(0, 3).map((pattern, idx) => (
            <div key={idx} className={`pattern-item ${pattern.bias.toLowerCase()}`}>
              <span className="pattern-name">{pattern.type}</span>
              <span className="pattern-confidence">{pattern.confidence.toFixed(1)}%</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default AdvancedChart;
