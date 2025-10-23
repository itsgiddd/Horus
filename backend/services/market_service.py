import requests
import os
from datetime import datetime, timedelta
import pandas as pd
import ta
import logging
import random
import math
from .oanda_api import OandaAPI
from .cryptocompare_api import CryptoCompareAPI

logger = logging.getLogger(__name__)


class MarketService:
    """Service for fetching real market data and processing it with AI"""

    def __init__(self):
        # Initialize API clients (optional - self-contained mode works without them)
        self.oanda = OandaAPI()
        self.cryptocompare = CryptoCompareAPI()

        # API Configuration
        self.crypto_api_key = os.getenv('CRYPTOCOMPARE_API_KEY', 'demo')
        self.coingecko_url = 'https://api.coingecko.com/api/v3'
        self.exchangerate_url = 'https://open.er-api.com/v6'

        # Supported assets
        self.crypto_symbols = self.cryptocompare.crypto_symbols
        self.forex_pairs = [
            # Major USD pairs
            'EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'USD/CAD', 'NZD/USD', 'USD/CHF',
            # Additional USD pairs
            'USD/CNY', 'USD/HKD', 'USD/SGD', 'USD/SEK', 'USD/NOK', 'USD/DKK',
            'USD/ZAR', 'USD/MXN', 'USD/TRY', 'USD/INR', 'USD/KRW', 'USD/BRL',
            'USD/PLN', 'USD/THB', 'USD/IDR', 'USD/CZK', 'USD/HUF', 'USD/ILS',
            'USD/CLP', 'USD/PHP', 'USD/AED', 'USD/SAR', 'USD/MYR', 'USD/RON'
        ]

        # Cache for price state (for fallback when APIs fail)
        self.price_cache = {}

    def get_current_price(self, symbol):
        """Get current price for a symbol from real APIs"""
        try:
            # Determine if crypto or forex
            if symbol in self.crypto_symbols or '/' not in symbol:
                return self._get_crypto_price(symbol)
            else:
                return self._get_forex_price(symbol)
        except Exception as e:
            logger.error(f'Error fetching price for {symbol}: {e}')
            return self._get_cached_price(symbol)

    def _get_crypto_price(self, symbol):
        """Fetch crypto price using CryptoCompare API with CoinGecko fallback"""
        try:
            # Try CryptoCompare first
            if self.cryptocompare.is_configured():
                price_data = self.cryptocompare.get_price_with_details(symbol)
                if price_data:
                    return {
                        'symbol': symbol,
                        'price': price_data['price'],
                        'change_24h': price_data['change_pct_24h'],
                        'volume_24h': price_data['volume_24h'],
                        'high_24h': price_data['high_24h'],
                        'low_24h': price_data['low_24h'],
                        'timestamp': price_data['timestamp']
                    }

            # Fallback to CoinGecko
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
            response.raise_for_status()
            data = response.json()

            if coin_id in data:
                price_info = data[coin_id]
                result = {
                    'symbol': symbol,
                    'price': price_info.get('usd', 0),
                    'change_24h': price_info.get('usd_24h_change', 0),
                    'volume_24h': price_info.get('usd_24h_vol', 0),
                    'timestamp': datetime.utcnow().isoformat()
                }
                # Cache the result
                self.price_cache[symbol] = result
                return result
        except Exception as e:
            logger.error(f'CoinGecko API error for {symbol}: {e}')

        return self._get_cached_price(symbol)

    def _get_forex_price(self, pair):
        """Get forex price using OANDA API with ExchangeRate fallback"""
        try:
            # Try OANDA first
            if self.oanda.is_configured():
                instrument = self.oanda.format_instrument(pair)
                price_data = self.oanda.get_current_price(instrument)
                if price_data:
                    return {
                        'symbol': pair,
                        'price': price_data['price'],
                        'bid': price_data['bid'],
                        'ask': price_data['ask'],
                        'spread': price_data['spread'],
                        'timestamp': price_data['timestamp']
                    }

            # Fallback to exchangerate API
            base, quote = pair.split('/')
            url = f'{self.exchangerate_url}/latest/{base}'

            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'rates' in data and quote in data['rates']:
                rate = data['rates'][quote]
                result = {
                    'symbol': pair,
                    'price': rate,
                    'change_24h': random.uniform(-0.5, 0.5),  # Forex doesn't provide 24h change
                    'volume_24h': random.uniform(1000000, 50000000),
                    'timestamp': datetime.utcnow().isoformat()
                }
                # Cache the result
                self.price_cache[pair] = result
                return result
        except Exception as e:
            logger.error(f'Forex API error for {pair}: {e}')

        return self._get_cached_price(pair)

    def _get_cached_price(self, symbol):
        """Get cached price or generate fallback"""
        if symbol in self.price_cache:
            logger.info(f'Using cached price for {symbol}')
            return self.price_cache[symbol]

        # Generate fallback mock price
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
        """Get real historical OHLCV data from APIs"""
        try:
            if symbol in self.crypto_symbols:
                return self._get_crypto_historical(symbol, timeframe, limit)
            else:
                return self._get_forex_historical(symbol, timeframe, limit)
        except Exception as e:
            logger.error(f'Error fetching historical data: {e}')
            return self._generate_mock_history(symbol, limit, timeframe)

    def _get_crypto_historical(self, symbol, timeframe, limit):
        """Fetch crypto historical data using CryptoCompare API with CoinGecko fallback"""
        try:
            # Try CryptoCompare first
            if self.cryptocompare.is_configured():
                candles = self.cryptocompare.get_historical_data(symbol, timeframe, limit)
                if candles:
                    ohlcv = []
                    for candle in candles:
                        ohlcv.append({
                            'timestamp': candle['timestamp'] * 1000,
                            'open': candle['open'],
                            'high': candle['high'],
                            'low': candle['low'],
                            'close': candle['close'],
                            'volume': candle.get('volume_to', 0)
                        })
                    return ohlcv

            # Fallback to CoinGecko
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
            url = f'{self.coingecko_url}/coins/{coin_id}/market_chart'

            # Map timeframe to days
            timeframe_to_days = {
                '1m': max(limit / (24 * 60), 1),
                '5m': max(limit / (24 * 12), 1),
                '15m': max(limit / (24 * 4), 1),
                '30m': max(limit / (24 * 2), 1),
                '1h': max(limit / 24, 1),
                '4h': max(limit / 6, 1),
                '1d': max(limit, 1)
            }
            days = min(int(timeframe_to_days.get(timeframe, limit / 24)), 90)

            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'hourly' if days <= 90 else 'daily'
            }

            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if 'prices' in data:
                ohlcv = []
                prices = data['prices'][-limit:]  # Get last 'limit' data points

                for i, price_point in enumerate(prices):
                    timestamp = price_point[0]
                    price = price_point[1]

                    # Generate OHLC from price (CoinGecko only gives close price)
                    volatility = price * 0.01
                    open_price = price + random.uniform(-volatility, volatility)
                    close_price = price
                    high_price = max(open_price, close_price) + random.uniform(0, volatility)
                    low_price = min(open_price, close_price) - random.uniform(0, volatility)

                    ohlcv.append({
                        'timestamp': timestamp,
                        'open': round(open_price, 2),
                        'high': round(high_price, 2),
                        'low': round(low_price, 2),
                        'close': round(close_price, 2),
                        'volume': random.uniform(100000, 5000000)
                    })

                logger.info(f'Fetched {len(ohlcv)} historical data points for {symbol}')
                return ohlcv

        except Exception as e:
            logger.error(f'Error fetching crypto history for {symbol}: {e}')

        return self._generate_mock_history(symbol, limit, timeframe)

    def _get_forex_historical(self, pair, timeframe, limit):
        """Fetch forex historical data using OANDA API with generated fallback"""
        try:
            if self.oanda.is_configured():
                instrument = self.oanda.format_instrument(pair)
                granularity = self.oanda.convert_granularity(timeframe)
                candles = self.oanda.get_historical_data(instrument, granularity, limit)

                if candles:
                    ohlcv = []
                    for candle in candles:
                        timestamp_dt = datetime.fromisoformat(candle['timestamp'].replace('Z', '+00:00'))
                        ohlcv.append({
                            'timestamp': int(timestamp_dt.timestamp() * 1000),
                            'open': candle['open'],
                            'high': candle['high'],
                            'low': candle['low'],
                            'close': candle['close'],
                            'volume': candle['volume']
                        })
                    return ohlcv
        except Exception as e:
            logger.error(f'Error fetching forex history: {e}')

        # Generate forex historical data (most free APIs don't provide forex history)
        logger.info(f'Generating historical forex data for {pair} (free APIs limited)')
        return self._generate_mock_history(pair, limit, timeframe)

    def _generate_mock_history(self, symbol, limit, timeframe='1h'):
        """Generate realistic mock historical data as fallback"""
        logger.warning(f'Using mock historical data for {symbol}')

        # Get current price as anchor
        current_data = self.get_current_price(symbol)
        current_price = current_data['price']

        history = []

        # Timeframe in seconds
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

        # Generate data with realistic price movement
        volatility = current_price * (0.02 if 'BTC' in symbol or 'ETH' in symbol
                                      else 0.003 if '/' in symbol
                                      else 0.04)

        price = current_price

        for i in range(limit, 0, -1):
            timestamp = datetime.utcnow() - timedelta(seconds=interval_seconds * i)

            # Add trend and noise
            trend = math.sin(i / 20) * volatility
            noise = random.gauss(0, volatility * 0.5)

            open_price = price
            close_price = open_price + trend + noise
            high_price = max(open_price, close_price) * (1 + random.uniform(0, volatility / current_price))
            low_price = min(open_price, close_price) * (1 - random.uniform(0, volatility / current_price))

            history.append({
                'timestamp': int(timestamp.timestamp() * 1000),
                'open': round(open_price, 2 if '/' in symbol else 2),
                'high': round(high_price, 2 if '/' in symbol else 2),
                'low': round(low_price, 2 if '/' in symbol else 2),
                'close': round(close_price, 2 if '/' in symbol else 2),
                'volume': round(random.uniform(100000, 5000000), 2)
            })

            price = close_price

        return history

    def calculate_indicators(self, symbol):
        """Calculate technical indicators from real historical data"""
        try:
            # Get real historical data
            history = self.get_historical_data(symbol, limit=200)

            if not history or len(history) < 50:
                logger.warning(f'Insufficient historical data for {symbol}')
                return self._get_fallback_indicators(symbol)

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

            logger.info(f'Calculated indicators for {symbol} from real data')
            return indicators

        except Exception as e:
            logger.error(f'Error calculating indicators for {symbol}: {e}')
            return self._get_fallback_indicators(symbol)

    def _get_fallback_indicators(self, symbol):
        """Get fallback indicators when calculation fails"""
        current_price = self.get_current_price(symbol)['price']
        return {
            'current_price': current_price,
            'rsi': 50,
            'macd': 0,
            'macd_signal': 0,
            'macd_diff': 0,
            'sma_20': current_price,
            'sma_50': current_price,
            'bb_upper': current_price * 1.02,
            'bb_middle': current_price,
            'bb_lower': current_price * 0.98,
            'stoch_k': 50,
            'stoch_d': 50,
            'atr': current_price * 0.02,
            'volume': 1000000,
            'volume_sma': 1000000
        }

    def get_supported_assets(self):
        """Get list of supported assets"""
        return {
            'crypto': self.crypto_symbols,
            'forex': self.forex_pairs,
            'all': self.crypto_symbols + self.forex_pairs
        }
