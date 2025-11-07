/**
 * Advanced Chart Component
 * Professional chart with AI predictions, pattern detection, and push analysis
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { createChart } from 'lightweight-charts';
import { useApp } from '../contexts/AppContext';
import { useToast } from '../contexts/ToastContext';
import api, { handleAPIError } from '../services/api';
import { ChartSkeleton } from './LoadingSkeleton';
import { CHART_CONFIG, TRADING_PAIRS, TIMEFRAMES, UI, SUCCESS_MESSAGES } from '../config/constants';
import { truncate } from '../utils/helpers';
import './AdvancedChart.css';

function AdvancedChart() {
  // Refs
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);
  const candleSeriesRef = useRef(null);
  const predictionSeriesRef = useRef(null);

  // Context hooks
  const {
    selectedSymbol,
    selectedTimeframe,
    updateSymbol,
    updateTimeframe,
    patterns,
    updatePatterns,
    pushAnalysis,
    updatePushAnalysis,
    predictionData,
    updatePrediction,
    isPredicting,
    setIsPredicting,
  } = useApp();

  const toast = useToast();

  // Local state
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(false);
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

  // Fetch market data
  useEffect(() => {
    fetchMarketData();
  }, [selectedSymbol, selectedTimeframe]);

  /**
   * Fetch market data with professional error handling
   */
  const fetchMarketData = useCallback(async () => {
    setLoading(true);
    setPredictionGenerated(false);
    updatePrediction(null);

    if (predictionSeriesRef.current) {
      predictionSeriesRef.current.setData([]);
    }

    try {
      const data = await api.getHistoricalData(
        selectedSymbol,
        selectedTimeframe,
        CHART_CONFIG.DEFAULT_CANDLE_LIMIT
      );

      if (data?.history && Array.isArray(data.history)) {
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

        // Fetch patterns and push analysis in parallel
        fetchPatternAndPushAnalysis();
      }
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast.error(errorInfo.message);
      console.error('Market data fetch error:', error);
    } finally {
      setLoading(false);
    }
  }, [selectedSymbol, selectedTimeframe, toast, updatePrediction]);

  /**
   * Fetch pattern and push analysis in parallel
   */
  const fetchPatternAndPushAnalysis = useCallback(async () => {
    try {
      const { patterns: patternsData, pushAnalysis: pushData } = await api.getAllSignals(
        selectedSymbol,
        selectedTimeframe
      );

      if (patternsData?.patterns) {
        updatePatterns(patternsData.patterns);
        drawPatternMarkers(patternsData.patterns);
      }

      if (pushData?.analysis) {
        updatePushAnalysis(pushData.analysis);
        drawPushMarkers(pushData.analysis);
      }
    } catch (error) {
      console.error('Error fetching signals:', error);
      // Don't show toast for signals - they're supplementary data
    }
  }, [selectedSymbol, selectedTimeframe, updatePatterns, updatePushAnalysis]);

  /**
   * Generate AI prediction with professional error handling
   */
  const generatePrediction = useCallback(async () => {
    setIsPredicting(true);
    setPredictionGenerated(false);

    try {
      const predData = await api.getAdvancedPrediction(selectedSymbol, selectedTimeframe);

      if (predData?.prediction) {
        updatePrediction(predData.prediction);

        if (predData.prediction.predicted_candles) {
          displayPredictionCandles(predData.prediction.predicted_candles);
          setPredictionGenerated(true);
          toast.success(SUCCESS_MESSAGES.PREDICTION_GENERATED);
        }
      }
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast.error(errorInfo.message);
      console.error('Prediction generation error:', error);
    } finally {
      setIsPredicting(false);
    }
  }, [selectedSymbol, selectedTimeframe, setIsPredicting, updatePrediction, toast]);

  /**
   * Draw pattern markers on chart
   */
  const drawPatternMarkers = useCallback((patterns) => {
    if (!chartRef.current || !patterns.length || !chartData.length) return;

    patterns.slice(0, 5).forEach((pattern) => {
      const marker = {
        time: chartData[chartData.length - 1].time,
        position: pattern.bias === 'Bullish' ? 'belowBar' : 'aboveBar',
        color: pattern.bias === 'Bullish' ? CHART_CONFIG.THEME.UP_COLOR : CHART_CONFIG.THEME.DOWN_COLOR,
        shape: 'circle',
        text: truncate(pattern.type, UI.MAX_PATTERN_NAME_LENGTH),
      };

      if (candleSeriesRef.current) {
        const existingMarkers = candleSeriesRef.current.markers() || [];
        candleSeriesRef.current.setMarkers([...existingMarkers, marker]);
      }
    });
  }, [chartData]);

  /**
   * Draw push markers on chart
   */
  const drawPushMarkers = useCallback((analysis) => {
    if (!chartRef.current || !analysis || !analysis.push_details || !chartData.length) return;

    analysis.push_details.forEach((push, idx) => {
      if (idx < chartData.length) {
        const marker = {
          time: chartData[Math.min(push.end_idx || idx, chartData.length - 1)].time,
          position: push.direction === 'bullish' ? 'belowBar' : 'aboveBar',
          color: CHART_CONFIG.THEME.ACCENT_COLOR,
          shape: 'arrowUp',
          text: `Push ${idx + 1}`,
        };

        if (candleSeriesRef.current) {
          const existingMarkers = candleSeriesRef.current.markers() || [];
          candleSeriesRef.current.setMarkers([...existingMarkers, marker]);
        }
      }
    });
  }, [chartData]);

  /**
   * Display prediction candles on chart
   */
  const displayPredictionCandles = useCallback((candles) => {
    if (!predictionSeriesRef.current || !chartData.length || !candles?.length) return;

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

    predictionSeriesRef.current.setData(predictionData);
  }, [chartData]);

  // Show loading skeleton
  if (loading && chartData.length === 0) {
    return <ChartSkeleton />;
  }

  return (
    <div className="advanced-chart-container">
      <div className="chart-controls">
        <div className="symbol-controls">
          <select
            value={selectedSymbol}
            onChange={(e) => updateSymbol(e.target.value)}
            className="chart-select"
            disabled={loading || isPredicting}
          >
            <optgroup label="Cryptocurrencies">
              {TRADING_PAIRS.CRYPTO.map((pair) => (
                <option key={pair.value} value={pair.value}>
                  {pair.label}
                </option>
              ))}
            </optgroup>
            <optgroup label="Major USD Pairs">
              {TRADING_PAIRS.FOREX_MAJOR.map((pair) => (
                <option key={pair.value} value={pair.value}>
                  {pair.label}
                </option>
              ))}
            </optgroup>
            <optgroup label="Exotic USD Pairs">
              {TRADING_PAIRS.FOREX_EXOTIC.map((pair) => (
                <option key={pair.value} value={pair.value}>
                  {pair.label}
                </option>
              ))}
            </optgroup>
          </select>

          <select
            value={selectedTimeframe}
            onChange={(e) => updateTimeframe(e.target.value)}
            className="chart-select"
            disabled={loading || isPredicting}
          >
            {TIMEFRAMES.map((tf) => (
              <option key={tf.value} value={tf.value}>
                {tf.label}
              </option>
            ))}
          </select>
        </div>

        <button
          className="prediction-btn"
          onClick={generatePrediction}
          disabled={isPredicting || loading || chartData.length === 0}
        >
          {isPredicting ? (
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
