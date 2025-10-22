// API Service for backend communication
const API_BASE_URL = 'http://127.0.0.1:5000/api';

class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Market Data APIs
  async getCurrentPrice(symbol) {
    return this.request(`/market/price/${symbol}`);
  }

  async getMultiplePrices(symbols) {
    return this.request('/market/prices', {
      method: 'POST',
      body: JSON.stringify({ symbols }),
    });
  }

  async getHistoricalData(symbol, timeframe = '1h', limit = 100) {
    return this.request(`/market/history/${symbol}?timeframe=${timeframe}&limit=${limit}`);
  }

  async getIndicators(symbol) {
    return this.request(`/market/indicators/${symbol}`);
  }

  async getSupportedAssets() {
    return this.request('/market/supported-assets');
  }

  // Signal APIs
  async getCurrentSignals() {
    return this.request('/signals/current');
  }

  async generateSignal(symbol) {
    return this.request(`/signals/generate/${symbol}`, {
      method: 'POST',
    });
  }

  async getSignalHistory(limit = 50) {
    return this.request(`/signals/history?limit=${limit}`);
  }

  async getSignalPerformance() {
    return this.request('/signals/performance');
  }

  // Portfolio APIs
  async getPortfolioSummary() {
    return this.request('/portfolio/summary');
  }

  async getPositions() {
    return this.request('/portfolio/positions');
  }

  async getRiskMetrics() {
    return this.request('/portfolio/risk-metrics');
  }

  async getPerformance(timeframe = '30d') {
    return this.request(`/portfolio/performance?timeframe=${timeframe}`);
  }

  // Health check
  async healthCheck() {
    return this.request('/health');
  }
}

export default new ApiService();
