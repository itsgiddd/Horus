/**
 * HORUS Configuration Constants
 * Centralized configuration for the application
 */

// API Configuration
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000',
  TIMEOUT: 30000, // 30 seconds
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000, // 1 second
};

// WebSocket Configuration
export const WS_CONFIG = {
  URL: import.meta.env.VITE_WS_URL || 'ws://127.0.0.1:5000',
  RECONNECT_INTERVAL: 5000,
  MAX_RECONNECT_ATTEMPTS: 5,
};

// Chart Configuration
export const CHART_CONFIG = {
  DEFAULT_SYMBOL: 'EUR/USD',
  DEFAULT_TIMEFRAME: '1h',
  DEFAULT_CANDLE_LIMIT: 200,
  THEME: {
    BACKGROUND: 'transparent',
    TEXT_COLOR: '#d1d4dc',
    GRID_COLOR: 'rgba(255, 255, 255, 0.05)',
    UP_COLOR: '#26a69a',
    DOWN_COLOR: '#ef5350',
    PREDICTION_UP: 'rgba(138, 43, 226, 0.4)',
    PREDICTION_DOWN: 'rgba(226, 43, 138, 0.4)',
    CROSSHAIR_COLOR: 'rgba(138, 43, 226, 0.5)',
    ACCENT_COLOR: '#8a2be2',
  },
};

// Supported Trading Pairs
export const TRADING_PAIRS = {
  CRYPTO: [
    { value: 'BTC', label: 'Bitcoin (BTC)', type: 'crypto' },
    { value: 'ETH', label: 'Ethereum (ETH)', type: 'crypto' },
    { value: 'SOL', label: 'Solana (SOL)', type: 'crypto' },
  ],
  FOREX_MAJOR: [
    { value: 'EUR/USD', label: 'EUR/USD', type: 'forex' },
    { value: 'GBP/USD', label: 'GBP/USD', type: 'forex' },
    { value: 'USD/JPY', label: 'USD/JPY', type: 'forex' },
    { value: 'AUD/USD', label: 'AUD/USD', type: 'forex' },
    { value: 'USD/CAD', label: 'USD/CAD', type: 'forex' },
    { value: 'NZD/USD', label: 'NZD/USD', type: 'forex' },
    { value: 'USD/CHF', label: 'USD/CHF', type: 'forex' },
  ],
  FOREX_EXOTIC: [
    { value: 'USD/CNY', label: 'USD/CNY (Chinese Yuan)', type: 'forex' },
    { value: 'USD/HKD', label: 'USD/HKD (Hong Kong Dollar)', type: 'forex' },
    { value: 'USD/SGD', label: 'USD/SGD (Singapore Dollar)', type: 'forex' },
    { value: 'USD/SEK', label: 'USD/SEK (Swedish Krona)', type: 'forex' },
    { value: 'USD/NOK', label: 'USD/NOK (Norwegian Krone)', type: 'forex' },
    { value: 'USD/DKK', label: 'USD/DKK (Danish Krone)', type: 'forex' },
    { value: 'USD/ZAR', label: 'USD/ZAR (South African Rand)', type: 'forex' },
    { value: 'USD/MXN', label: 'USD/MXN (Mexican Peso)', type: 'forex' },
    { value: 'USD/TRY', label: 'USD/TRY (Turkish Lira)', type: 'forex' },
    { value: 'USD/INR', label: 'USD/INR (Indian Rupee)', type: 'forex' },
    { value: 'USD/KRW', label: 'USD/KRW (South Korean Won)', type: 'forex' },
    { value: 'USD/BRL', label: 'USD/BRL (Brazilian Real)', type: 'forex' },
    { value: 'USD/PLN', label: 'USD/PLN (Polish Zloty)', type: 'forex' },
    { value: 'USD/THB', label: 'USD/THB (Thai Baht)', type: 'forex' },
    { value: 'USD/IDR', label: 'USD/IDR (Indonesian Rupiah)', type: 'forex' },
    { value: 'USD/CZK', label: 'USD/CZK (Czech Koruna)', type: 'forex' },
    { value: 'USD/HUF', label: 'USD/HUF (Hungarian Forint)', type: 'forex' },
    { value: 'USD/ILS', label: 'USD/ILS (Israeli Shekel)', type: 'forex' },
    { value: 'USD/CLP', label: 'USD/CLP (Chilean Peso)', type: 'forex' },
    { value: 'USD/PHP', label: 'USD/PHP (Philippine Peso)', type: 'forex' },
    { value: 'USD/AED', label: 'USD/AED (UAE Dirham)', type: 'forex' },
    { value: 'USD/SAR', label: 'USD/SAR (Saudi Riyal)', type: 'forex' },
    { value: 'USD/MYR', label: 'USD/MYR (Malaysian Ringgit)', type: 'forex' },
    { value: 'USD/RON', label: 'USD/RON (Romanian Leu)', type: 'forex' },
  ],
};

// Timeframes
export const TIMEFRAMES = [
  { value: '15m', label: '15 Minutes', seconds: 900 },
  { value: '1h', label: '1 Hour', seconds: 3600 },
  { value: '4h', label: '4 Hours', seconds: 14400 },
  { value: '1d', label: '1 Day', seconds: 86400 },
];

// Prediction Configuration
export const PREDICTION_CONFIG = {
  MIN_CONFIDENCE_DISPLAY: 50, // Only show predictions with 50%+ confidence
  EXHAUSTION_THRESHOLD: 4, // Number of pushes before exhaustion
  PATTERN_DISPLAY_LIMIT: 3, // Max patterns to show in UI
};

// Animation Durations (ms)
export const ANIMATION = {
  FAST: 150,
  NORMAL: 300,
  SLOW: 500,
  VERY_SLOW: 800,
};

// Storage Keys
export const STORAGE_KEYS = {
  SETUP_COMPLETE: 'horus_setup_complete',
  API_CONFIG: 'horus_api_config',
  USER_PREFERENCES: 'horus_user_preferences',
  THEME: 'horus_theme',
};

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Unable to connect to the server. Please ensure the backend is running.',
  TIMEOUT: 'Request timed out. Please try again.',
  INVALID_RESPONSE: 'Received invalid response from server.',
  NO_DATA: 'No data available for the selected symbol and timeframe.',
  PREDICTION_FAILED: 'Failed to generate prediction. Please try again.',
  UNAUTHORIZED: 'API authentication failed. Please check your API credentials.',
};

// Success Messages
export const SUCCESS_MESSAGES = {
  PREDICTION_GENERATED: 'AI prediction generated successfully!',
  SETTINGS_SAVED: 'Settings saved successfully!',
  API_CONNECTED: 'Connected to API successfully!',
};

// HTTP Status Codes
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  NOT_FOUND: 404,
  INTERNAL_SERVER: 500,
  SERVICE_UNAVAILABLE: 503,
};

// UI Constants
export const UI = {
  TOAST_DURATION: 4000,
  SKELETON_LOADING_MIN: 500, // Minimum time to show skeleton
  DEBOUNCE_DELAY: 300,
  MAX_PATTERN_NAME_LENGTH: 15,
};
