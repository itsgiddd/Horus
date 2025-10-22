import requests
import os
from datetime import datetime, timedelta
import pandas as pd
import ta
import logging

logger = logging.getLogger(__name__)


class MarketService:
    """Service for fetching and processing market data"""

    def __init__(self):
        self.crypto_api_key = os.getenv('CRYPTOCOMPARE_API_KEY', 'demo')
        self.base_url_crypto = 'https://min-api.cryptocompare.com/data'
        self.coingecko_url = 'https://api.coingecko.com/api/v3'

        # Supported assets
        self.crypto_symbols = ['BTC', 'ETH', 'SOL', 'ADA', 'XRP', 'DOT', 'LINK', 'MATIC', 'AVAX', 'UNI']
        self.forex_pairs = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'USD/CAD', 'NZD/USD']

    def get_current_price(self, symbol):
        """Get current price for a symbol"""
        try:
            # Determine if crypto or forex
            if symbol in self.crypto_symbols or '/' not in symbol:
                return self._get_crypto_price(symbol)
            else:
                return self._get_forex_price(symbol)
        except Exception as e:
            logger.error(f'Error fetching price for {symbol}: {e}')
            return self._get_mock_price(symbol)

    def _get_crypto_price(self, symbol):
        """Fetch crypto price from CoinGecko (free API)"""
        try:
            # Map common symbols to CoinGecko IDs
            coin_map = {
                'BTC': 'bitcoin',
                'ETH': 'ethereum',
                'SOL': 'solana',
                'ADA': 'cardano',
                'XRP': 'ripple',
                'DOT': 'polkadot',
                'LINK': 'chainlink',
                'MATIC': 'matic-network',
                'AVAX': 'avalanche-2',
                'UNI': 'uniswap'
            }

            coin_id = coin_map.get(symbol, symbol.lower())
            url = f'{self.coingecko_url}/simple/price'
            params = {
                'ids': coin_id,
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_24hr_vol': 'true'
            }

            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if coin_id in data:
                price_info = data[coin_id]
                return {
                    'symbol': symbol,
                    'price': price_info.get('usd', 0),
                    'change_24h': price_info.get('usd_24h_change', 0),
                    'volume_24h': price_info.get('usd_24h_vol', 0),
                    'timestamp': datetime.utcnow().isoformat()
                }
        except Exception as e:
            logger.error(f'CoinGecko API error: {e}')

        return self._get_mock_price(symbol)

    def _get_forex_price(self, pair):
        """Get forex price (using free forex API)"""
        try:
            # Use exchangerate-api.com (free tier)
            base, quote = pair.split('/')
            url = f'https://open.er-api.com/v6/latest/{base}'

            response = requests.get(url, timeout=10)
            data = response.json()

            if 'rates' in data and quote in data['rates']:
                rate = data['rates'][quote]
                return {
                    'symbol': pair,
                    'price': rate,
                    'change_24h': 0.15,  # Mock data for demo
                    'timestamp': datetime.utcnow().isoformat()
                }
        except Exception as e:
            logger.error(f'Forex API error: {e}')

        return self._get_mock_price(pair)

    def _get_mock_price(self, symbol):
        """Generate mock price data for demo purposes"""
        import random

        base_prices = {
            'BTC': 43250.50,
            'ETH': 2280.75,
            'SOL': 98.45,
            'ADA': 0.52,
            'EUR/USD': 1.0845,
            'GBP/USD': 1.2670,
            'USD/JPY': 148.50,
        }

        base_price = base_prices.get(symbol, 100.0)
        variation = random.uniform(-2, 2)

        return {
            'symbol': symbol,
            'price': round(base_price * (1 + variation / 100), 2),
            'change_24h': round(random.uniform(-5, 5), 2),
            'volume_24h': round(random.uniform(1000000, 10000000), 2),
            'timestamp': datetime.utcnow().isoformat()
        }

    def get_multiple_prices(self, symbols):
        """Get prices for multiple symbols"""
        prices = {}
        for symbol in symbols:
            prices[symbol] = self.get_current_price(symbol)
        return prices

    def get_historical_data(self, symbol, timeframe='1h', limit=100):
        """Get historical OHLCV data"""
        try:
            if symbol in self.crypto_symbols:
                return self._get_crypto_historical(symbol, timeframe, limit)
            else:
                return self._get_forex_historical(symbol, timeframe, limit)
        except Exception as e:
            logger.error(f'Error fetching historical data: {e}')
            return self._generate_mock_history(symbol, limit)

    def _get_crypto_historical(self, symbol, timeframe, limit):
        """Fetch crypto historical data from CoinGecko"""
        try:
            coin_map = {
                'BTC': 'bitcoin',
                'ETH': 'ethereum',
                'SOL': 'solana',
                'ADA': 'cardano',
            }

            coin_id = coin_map.get(symbol, symbol.lower())
            url = f'{self.coingecko_url}/coins/{coin_id}/market_chart'

            days = limit // 24 if timeframe == '1h' else limit
            params = {'vs_currency': 'usd', 'days': min(days, 90)}

            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if 'prices' in data:
                ohlcv = []
                for price_point in data['prices'][:limit]:
                    ohlcv.append({
                        'timestamp': price_point[0],
                        'open': price_point[1],
                        'high': price_point[1] * 1.02,
                        'low': price_point[1] * 0.98,
                        'close': price_point[1],
                        'volume': 1000000
                    })
                return ohlcv
        except Exception as e:
            logger.error(f'Error fetching crypto history: {e}')

        return self._generate_mock_history(symbol, limit)

    def _get_forex_historical(self, pair, timeframe, limit):
        """Generate forex historical data (mock for demo)"""
        return self._generate_mock_history(pair, limit)

    def _generate_mock_history(self, symbol, limit):
        """Generate mock historical data"""
        import random

        current_price = self.get_current_price(symbol)['price']
        history = []

        for i in range(limit, 0, -1):
            timestamp = datetime.utcnow() - timedelta(hours=i)
            variation = random.uniform(0.98, 1.02)
            price = current_price * variation

            history.append({
                'timestamp': int(timestamp.timestamp() * 1000),
                'open': round(price, 2),
                'high': round(price * 1.015, 2),
                'low': round(price * 0.985, 2),
                'close': round(price * random.uniform(0.99, 1.01), 2),
                'volume': round(random.uniform(100000, 1000000), 2)
            })

        return history

    def calculate_indicators(self, symbol):
        """Calculate technical indicators"""
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

            # Volume indicators
            indicators['volume'] = float(df['volume'].iloc[-1])
            indicators['volume_sma'] = float(df['volume'].rolling(window=20).mean().iloc[-1])

            return indicators

        except Exception as e:
            logger.error(f'Error calculating indicators: {e}')
            return {}

    def get_supported_assets(self):
        """Get list of supported assets"""
        return {
            'crypto': self.crypto_symbols,
            'forex': self.forex_pairs,
            'all': self.crypto_symbols + self.forex_pairs
        }
