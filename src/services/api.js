/**
 * Professional API Service Layer
 * Centralized API communication with error handling, retry logic, and request management
 */

import { API_CONFIG, ERROR_MESSAGES, HTTP_STATUS } from '../config/constants';

/**
 * Custom API Error class for better error handling
 */
export class APIError extends Error {
  constructor(message, status, data = null) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.data = data;
    this.timestamp = new Date().toISOString();
  }
}

/**
 * Sleep utility for retry delays
 */
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Enhanced fetch wrapper with timeout support
 */
const fetchWithTimeout = async (url, options = {}) => {
  const { timeout = API_CONFIG.TIMEOUT } = options;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    return response;
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === 'AbortError') {
      throw new APIError(ERROR_MESSAGES.TIMEOUT, 408);
    }
    throw error;
  }
};

/**
 * Core API request handler with retry logic
 */
const apiRequest = async (endpoint, options = {}, retries = API_CONFIG.RETRY_ATTEMPTS) => {
  const url = `${API_CONFIG.BASE_URL}${endpoint}`;

  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  let lastError;

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const response = await fetchWithTimeout(url, defaultOptions);

      // Handle different HTTP status codes
      if (response.ok) {
        const data = await response.json();
        return data;
      }

      // Handle specific error status codes
      switch (response.status) {
        case HTTP_STATUS.UNAUTHORIZED:
          throw new APIError(ERROR_MESSAGES.UNAUTHORIZED, response.status);

        case HTTP_STATUS.NOT_FOUND:
          throw new APIError(`Resource not found: ${endpoint}`, response.status);

        case HTTP_STATUS.SERVICE_UNAVAILABLE:
          throw new APIError(ERROR_MESSAGES.NETWORK_ERROR, response.status);

        default:
          const errorData = await response.json().catch(() => ({}));
          throw new APIError(
            errorData.error || ERROR_MESSAGES.INVALID_RESPONSE,
            response.status,
            errorData
          );
      }
    } catch (error) {
      lastError = error;

      // Don't retry on certain errors
      if (error instanceof APIError && error.status === HTTP_STATUS.UNAUTHORIZED) {
        throw error;
      }

      // Retry on network errors or server errors
      if (attempt < retries) {
        const delay = API_CONFIG.RETRY_DELAY * Math.pow(2, attempt); // Exponential backoff
        await sleep(delay);
        continue;
      }

      throw error;
    }
  }

  throw lastError || new APIError(ERROR_MESSAGES.NETWORK_ERROR, 0);
};

/**
 * API Service Class - Enterprise-grade API wrapper
 */
class ApiService {
  constructor() {
    this.baseUrl = API_CONFIG.BASE_URL;
  }

  // Market Data APIs
  async getCurrentPrice(symbol) {
    return await apiRequest(`/api/market/price/${symbol}`);
  }

  async getMultiplePrices(symbols) {
    return await apiRequest('/api/market/prices', {
      method: 'POST',
      body: JSON.stringify({ symbols }),
    });
  }

  async getHistoricalData(symbol, timeframe = '1h', limit = 200) {
    try {
      return await apiRequest(
        `/api/market/history/${symbol}?timeframe=${timeframe}&limit=${limit}`
      );
    } catch (error) {
      console.error('Market history fetch error:', error);
      throw new APIError(ERROR_MESSAGES.NO_DATA, error.status || 0, error);
    }
  }

  async getIndicators(symbol, timeframe = '1h') {
    return await apiRequest(`/api/market/indicators/${symbol}?timeframe=${timeframe}`);
  }

  async getSupportedAssets() {
    return await apiRequest('/api/market/supported-assets');
  }

  // Signal & Prediction APIs
  async getCurrentSignals() {
    return await apiRequest('/api/signals/current');
  }

  async generateSignal(symbol) {
    return await apiRequest(`/api/signals/generate/${symbol}`, {
      method: 'POST',
    });
  }

  async getPrediction(symbol, timeframe = '1h') {
    return await apiRequest(
      `/api/signals/prediction/${symbol}?timeframe=${timeframe}`,
      { method: 'POST' }
    );
  }

  async getAdvancedPrediction(symbol, timeframe = '1h') {
    try {
      return await apiRequest(
        `/api/signals/advanced-prediction/${symbol}?timeframe=${timeframe}`,
        { method: 'POST' }
      );
    } catch (error) {
      console.error('Advanced prediction error:', error);
      throw new APIError(ERROR_MESSAGES.PREDICTION_FAILED, error.status || 0, error);
    }
  }

  async getPatterns(symbol, timeframe = '1h') {
    return await apiRequest(
      `/api/signals/patterns/${symbol}?timeframe=${timeframe}`
    );
  }

  async getPushAnalysis(symbol, timeframe = '1h') {
    return await apiRequest(
      `/api/signals/push-analysis/${symbol}?timeframe=${timeframe}`
    );
  }

  async getSignalHistory(limit = 50) {
    return await apiRequest(`/api/signals/history?limit=${limit}`);
  }

  async getSignalPerformance() {
    return await apiRequest('/api/signals/performance');
  }

  /**
   * Get all signals at once (optimized parallel request)
   */
  async getAllSignals(symbol, timeframe = '1h') {
    try {
      const [patterns, pushAnalysis] = await Promise.all([
        this.getPatterns(symbol, timeframe),
        this.getPushAnalysis(symbol, timeframe),
      ]);

      return { patterns, pushAnalysis };
    } catch (error) {
      console.error('Error fetching signals:', error);
      // Return partial data if available
      return {
        patterns: { patterns: [] },
        pushAnalysis: { analysis: null },
      };
    }
  }

  // Portfolio APIs
  async getPortfolioSummary() {
    return await apiRequest('/api/portfolio/summary');
  }

  async getPositions() {
    return await apiRequest('/api/portfolio/positions');
  }

  async getRiskMetrics() {
    return await apiRequest('/api/portfolio/risk-metrics');
  }

  async getPerformance(timeframe = '30d') {
    return await apiRequest(`/api/portfolio/performance?timeframe=${timeframe}`);
  }

  // Settings APIs
  async saveApiConfig(config) {
    return await apiRequest('/api/settings/api-config', {
      method: 'POST',
      body: JSON.stringify(config),
    });
  }

  async getConfig() {
    return await apiRequest('/api/settings/config');
  }

  // Health check
  async healthCheck() {
    try {
      const response = await fetchWithTimeout(
        `${API_CONFIG.BASE_URL}/health`,
        { timeout: 5000 }
      );
      return response.ok;
    } catch (error) {
      return false;
    }
  }

  async getStatus() {
    return await apiRequest('/api/status');
  }
}

/**
 * Utility function to handle API errors consistently
 */
export const handleAPIError = (error, defaultMessage = ERROR_MESSAGES.NETWORK_ERROR) => {
  if (error instanceof APIError) {
    return {
      message: error.message,
      status: error.status,
      data: error.data,
    };
  }

  if (error.name === 'TypeError' && error.message.includes('fetch')) {
    return {
      message: ERROR_MESSAGES.NETWORK_ERROR,
      status: 0,
      data: null,
    };
  }

  return {
    message: error.message || defaultMessage,
    status: 0,
    data: null,
  };
};

export default new ApiService();
