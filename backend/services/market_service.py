import os
from datetime import datetime, timedelta
import pandas as pd
import ta
import logging
import random
import math

logger = logging.getLogger(__name__)


class MarketService:
    """Service for generating and processing market data - fully self-contained"""

    def __init__(self):
        # No API keys needed - everything is generated locally
        self.crypto_symbols = ['BTC', 'ETH', 'SOL', 'ADA', 'XRP', 'DOT', 'LINK', 'MATIC', 'AVAX', 'UNI']
        self.forex_pairs = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'USD/CAD', 'NZD/USD']

        # Initialize price state for realistic price movement
        self.price_state = {}
        self._initialize_price_state()

    def _initialize_price_state(self):
        """Initialize base prices and trends for realistic simulation"""
        base_prices = {
            'BTC': 43250.50,
            'ETH': 2280.75,
            'SOL': 98.45,
            'ADA': 0.52,
            'XRP': 0.61,
            'DOT': 7.23,
            'LINK': 14.52,
            'MATIC': 0.89,
            'AVAX': 36.78,
            'UNI': 6.42,
            'EUR/USD': 1.0845,
            'GBP/USD': 1.2670,
            'USD/JPY': 148.50,
            'AUD/USD': 0.6542,
            'USD/CAD': 1.3521,
            'NZD/USD': 0.6123,
        }

        for symbol, base_price in base_prices.items():
            self.price_state[symbol] = {
                'base_price': base_price,
                'current_price': base_price,
                'trend': random.choice([-1, 0, 1]),  # -1: down, 0: sideways, 1: up
                'volatility': self._get_symbol_volatility(symbol),
                'last_update': datetime.utcnow()
            }

    def _get_symbol_volatility(self, symbol):
        """Get realistic volatility for each symbol type"""
        if 'BTC' in symbol or 'ETH' in symbol:
            return 0.02  # 2% volatility
        elif '/' in symbol:
            return 0.003  # 0.3% volatility for forex
        else:
            return 0.04  # 4% volatility for altcoins

    def get_current_price(self, symbol):
        """Get current price for a symbol - generated locally"""
        if symbol not in self.price_state:
            self._initialize_symbol_price(symbol)

        # Update price with realistic movement
        state = self.price_state[symbol]
        time_delta = (datetime.utcnow() - state['last_update']).total_seconds() / 60

        # Generate price movement
        trend_move = state['trend'] * state['volatility'] * time_delta * 0.1
        random_move = random.gauss(0, state['volatility'] * 0.5)

        # Update current price
        new_price = state['current_price'] * (1 + trend_move + random_move)
        state['current_price'] = new_price
        state['last_update'] = datetime.utcnow()

        # Occasionally change trend
        if random.random() < 0.05:
            state['trend'] = random.choice([-1, 0, 1])

        # Calculate 24h change
        change_24h = ((state['current_price'] - state['base_price']) / state['base_price']) * 100

        return {
            'symbol': symbol,
            'price': round(new_price, 2 if '/' in symbol else 2),
            'change_24h': round(change_24h, 2),
            'volume_24h': round(random.uniform(1000000, 50000000), 2),
            'timestamp': datetime.utcnow().isoformat()
        }

    def _initialize_symbol_price(self, symbol):
        """Initialize price state for a new symbol"""
        base_price = 100.0  # Default
        if symbol not in self.price_state:
            self.price_state[symbol] = {
                'base_price': base_price,
                'current_price': base_price,
                'trend': 0,
                'volatility': 0.02,
                'last_update': datetime.utcnow()
            }

    def get_multiple_prices(self, symbols):
        """Get prices for multiple symbols"""
        prices = {}
        for symbol in symbols:
            prices[symbol] = self.get_current_price(symbol)
        return prices

    def get_historical_data(self, symbol, timeframe='1h', limit=100):
        """Generate realistic historical OHLCV data"""
        if symbol not in self.price_state:
            self._initialize_symbol_price(symbol)

        state = self.price_state[symbol]
        history = []

        # Determine timeframe in seconds
        timeframe_map = {
            '1m': 60,
            '5m': 300,
            '15m': 900,
            '30m': 1800,
            '1h': 3600,
            '4h': 14400,
            '1d': 86400
        }
        interval_seconds = timeframe_map.get(timeframe, 3600)

        # Generate historical data with realistic trends
        base_price = state['base_price']
        current_price = base_price

        for i in range(limit, 0, -1):
            timestamp = datetime.utcnow() - timedelta(seconds=interval_seconds * i)

            # Add trend and noise
            trend_component = math.sin(i / 20) * state['volatility'] * base_price
            noise = random.gauss(0, state['volatility'] * base_price * 0.5)

            open_price = current_price
            close_price = open_price + trend_component + noise
            high_price = max(open_price, close_price) * (1 + random.uniform(0, state['volatility']))
            low_price = min(open_price, close_price) * (1 - random.uniform(0, state['volatility']))

            volume = random.uniform(100000, 5000000)

            history.append({
                'timestamp': int(timestamp.timestamp() * 1000),
                'open': round(open_price, 2 if '/' in symbol else 2),
                'high': round(high_price, 2 if '/' in symbol else 2),
                'low': round(low_price, 2 if '/' in symbol else 2),
                'close': round(close_price, 2 if '/' in symbol else 2),
                'volume': round(volume, 2)
            })

            current_price = close_price

        # Update state to current price
        state['current_price'] = current_price

        return history

    def calculate_indicators(self, symbol):
        """Calculate technical indicators using local data"""
        try:
            # Get historical data
            history = self.get_historical_data(symbol, limit=200)

            # Convert to DataFrame
            df = pd.DataFrame(history)
            df['close'] = df['close'].astype(float)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            df['volume'] = df['volume'].astype(float)

            # Calculate indicators
            indicators = {}

            # Moving Averages
            indicators['sma_20'] = float(ta.trend.sma_indicator(df['close'], window=20).iloc[-1])
            indicators['sma_50'] = float(ta.trend.sma_indicator(df['close'], window=50).iloc[-1])
            indicators['ema_12'] = float(ta.trend.ema_indicator(df['close'], window=12).iloc[-1])
            indicators['ema_26'] = float(ta.trend.ema_indicator(df['close'], window=26).iloc[-1])

            # RSI
            indicators['rsi'] = float(ta.momentum.rsi(df['close'], window=14).iloc[-1])

            # MACD
            macd = ta.trend.MACD(df['close'])
            indicators['macd'] = float(macd.macd().iloc[-1])
            indicators['macd_signal'] = float(macd.macd_signal().iloc[-1])
            indicators['macd_diff'] = float(macd.macd_diff().iloc[-1])

            # Bollinger Bands
            bb = ta.volatility.BollingerBands(df['close'])
            indicators['bb_upper'] = float(bb.bollinger_hband().iloc[-1])
            indicators['bb_middle'] = float(bb.bollinger_mavg().iloc[-1])
            indicators['bb_lower'] = float(bb.bollinger_lband().iloc[-1])

            # Stochastic Oscillator
            stoch = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close'])
            indicators['stoch_k'] = float(stoch.stoch().iloc[-1])
            indicators['stoch_d'] = float(stoch.stoch_signal().iloc[-1])

            # ATR (Average True Range)
            indicators['atr'] = float(ta.volatility.average_true_range(df['high'], df['low'], df['close']).iloc[-1])

            # Volume indicators
            indicators['volume'] = float(df['volume'].iloc[-1])
            indicators['volume_sma'] = float(df['volume'].rolling(window=20).mean().iloc[-1])

            # Current price
            indicators['current_price'] = float(df['close'].iloc[-1])

            return indicators

        except Exception as e:
            logger.error(f'Error calculating indicators: {e}')
            return {
                'current_price': self.get_current_price(symbol)['price'],
                'rsi': 50,
                'macd': 0,
                'macd_signal': 0,
                'macd_diff': 0
            }

    def get_supported_assets(self):
        """Get list of supported assets"""
        return {
            'crypto': self.crypto_symbols,
            'forex': self.forex_pairs,
            'all': self.crypto_symbols + self.forex_pairs
        }
