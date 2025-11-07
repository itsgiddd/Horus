/**
 * Global App Context
 * Centralized state management for the HORUS application
 */

import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import { CHART_CONFIG, STORAGE_KEYS } from '../config/constants';

const AppContext = createContext();

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};

export const AppProvider = ({ children }) => {
  // App state
  const [currentView, setCurrentView] = useState('charts');
  const [showSetup, setShowSetup] = useState(false);

  // Chart state
  const [selectedSymbol, setSelectedSymbol] = useState(CHART_CONFIG.DEFAULT_SYMBOL);
  const [selectedTimeframe, setSelectedTimeframe] = useState(CHART_CONFIG.DEFAULT_TIMEFRAME);

  // Prediction state
  const [predictionData, setPredictionData] = useState(null);
  const [isPredicting, setIsPredicting] = useState(false);

  // Pattern and analysis state
  const [patterns, setPatterns] = useState([]);
  const [pushAnalysis, setPushAnalysis] = useState(null);

  // Backend health state
  const [backendHealth, setBackendHealth] = useState(null);
  const [lastHealthCheck, setLastHealthCheck] = useState(null);

  // User preferences
  const [preferences, setPreferences] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEYS.USER_PREFERENCES);
    return saved ? JSON.parse(saved) : {
      autoRefresh: true,
      refreshInterval: 60000, // 1 minute
      showPatterns: true,
      showPushAnalysis: true,
      notifications: true,
    };
  });

  // Check setup status on mount
  useEffect(() => {
    const setupComplete = localStorage.getItem(STORAGE_KEYS.SETUP_COMPLETE);
    if (!setupComplete) {
      setShowSetup(true);
    }
  }, []);

  // Save preferences to localStorage
  useEffect(() => {
    localStorage.setItem(STORAGE_KEYS.USER_PREFERENCES, JSON.stringify(preferences));
  }, [preferences]);

  // Update symbol
  const updateSymbol = useCallback((symbol) => {
    setSelectedSymbol(symbol);
    // Clear prediction data when symbol changes
    setPredictionData(null);
  }, []);

  // Update timeframe
  const updateTimeframe = useCallback((timeframe) => {
    setSelectedTimeframe(timeframe);
    // Clear prediction data when timeframe changes
    setPredictionData(null);
  }, []);

  // Update prediction data
  const updatePrediction = useCallback((data) => {
    setPredictionData(data);
  }, []);

  // Update patterns
  const updatePatterns = useCallback((newPatterns) => {
    setPatterns(newPatterns);
  }, []);

  // Update push analysis
  const updatePushAnalysis = useCallback((analysis) => {
    setPushAnalysis(analysis);
  }, []);

  // Update backend health
  const updateBackendHealth = useCallback((health) => {
    setBackendHealth(health);
    setLastHealthCheck(new Date().toISOString());
  }, []);

  // Update preference
  const updatePreference = useCallback((key, value) => {
    setPreferences((prev) => ({
      ...prev,
      [key]: value,
    }));
  }, []);

  // Complete setup
  const completeSetup = useCallback(() => {
    localStorage.setItem(STORAGE_KEYS.SETUP_COMPLETE, 'true');
    setShowSetup(false);
  }, []);

  // Reset app state (for testing or troubleshooting)
  const resetAppState = useCallback(() => {
    setPredictionData(null);
    setPatterns([]);
    setPushAnalysis(null);
  }, []);

  const value = {
    // View state
    currentView,
    setCurrentView,
    showSetup,
    setShowSetup,

    // Chart state
    selectedSymbol,
    selectedTimeframe,
    updateSymbol,
    updateTimeframe,

    // Prediction state
    predictionData,
    updatePrediction,
    isPredicting,
    setIsPredicting,

    // Analysis state
    patterns,
    updatePatterns,
    pushAnalysis,
    updatePushAnalysis,

    // Backend health
    backendHealth,
    updateBackendHealth,
    lastHealthCheck,

    // Preferences
    preferences,
    updatePreference,

    // Actions
    completeSetup,
    resetAppState,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export default AppContext;
