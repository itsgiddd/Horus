import os
import logging
import requests
from datetime import datetime, timedelta
import pandas as pd

logger = logging.getLogger(__name__)


class CryptoCompareAPI:
    """CryptoCompare API integration for cryptocurrency data"""

    def __init__(self):
        self.api_key = os.getenv('CRYPTOCOMPARE_API_KEY')
        self.base_url = 'https://min-api.cryptocompare.com/data'

        self.headers = {}
        if self.api_key and self.api_key != 'demo':
            self.headers['authorization'] = f'Apikey {self.api_key}'

        # Supported cryptocurrencies
        self.crypto_symbols = [
            'BTC', 'ETH', 'SOL', 'ADA', 'XRP', 'DOT', 'LINK',
            'MATIC', 'AVAX', 'UNI', 'ATOM', 'ALGO', 'FTM', 'NEAR',
            'BNB', 'LTC', 'BCH', 'DOGE', 'SHIB', 'APT'
        ]

    def is_configured(self):
        """Check if API key is configured"""
        return bool(self.api_key and self.api_key != 'demo')

    def get_current_price(self, symbol, convert_to='USD'):
        """Get current price for a cryptocurrency"""
        try:
            url = f'{self.base_url}/price'
            params = {
                'fsym': symbol,
                'tsyms': convert_to
            }

            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if convert_to in data:
                return {
                    'symbol': symbol,
                    'price': data[convert_to],
                    'currency': convert_to,
                    'timestamp': datetime.utcnow().isoformat()
                }

        except requests.RequestException as e:
            logger.error(f'CryptoCompare API error getting price: {e}')
        except Exception as e:
            logger.error(f'Unexpected error: {e}')

        return None

    def get_multiple_prices(self, symbols, convert_to='USD'):
        """Get prices for multiple cryptocurrencies"""
        try:
            url = f'{self.base_url}/pricemulti'
            params = {
                'fsyms': ','.join(symbols),
                'tsyms': convert_to
            }

            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            prices = {}
            for symbol in symbols:
                if symbol in data and convert_to in data[symbol]:
                    prices[symbol] = {
                        'symbol': symbol,
                        'price': data[symbol][convert_to],
                        'currency': convert_to,
                        'timestamp': datetime.utcnow().isoformat()
                    }

            return prices

        except Exception as e:
            logger.error(f'Error getting multiple prices: {e}')
            return {}

    def get_price_with_details(self, symbol, convert_to='USD'):
        """Get detailed price information including 24h change and volume"""
        try:
            url = f'{self.base_url}/pricemultifull'
            params = {
                'fsyms': symbol,
                'tsyms': convert_to
            }

            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'RAW' in data and symbol in data['RAW'] and convert_to in data['RAW'][symbol]:
                raw_data = data['RAW'][symbol][convert_to]

                return {
                    'symbol': symbol,
                    'price': raw_data.get('PRICE', 0),
                    'open_24h': raw_data.get('OPEN24HOUR', 0),
                    'high_24h': raw_data.get('HIGH24HOUR', 0),
                    'low_24h': raw_data.get('LOW24HOUR', 0),
                    'change_24h': raw_data.get('CHANGE24HOUR', 0),
                    'change_pct_24h': raw_data.get('CHANGEPCT24HOUR', 0),
                    'volume_24h': raw_data.get('VOLUME24HOUR', 0),
                    'market_cap': raw_data.get('MKTCAP', 0),
                    'supply': raw_data.get('SUPPLY', 0),
                    'timestamp': datetime.utcnow().isoformat()
                }

        except Exception as e:
            logger.error(f'Error getting detailed price: {e}')

        return None

    def get_historical_hourly(self, symbol, convert_to='USD', limit=168):
        """
        Get hourly historical data

        Args:
            symbol: Cryptocurrency symbol
            convert_to: Currency to convert to
            limit: Number of hours (max 2000)

        Returns:
            List of OHLCV dictionaries
        """
        try:
            url = f'{self.base_url}/v2/histohour'
            params = {
                'fsym': symbol,
                'tsym': convert_to,
                'limit': min(limit, 2000)
            }

            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('Response') == 'Success' and 'Data' in data and 'Data' in data['Data']:
                candles = []
                for candle in data['Data']['Data']:
                    candles.append({
                        'timestamp': candle['time'],
                        'open': candle['open'],
                        'high': candle['high'],
                        'low': candle['low'],
                        'close': candle['close'],
                        'volume_from': candle['volumefrom'],
                        'volume_to': candle['volumeto']
                    })
                return candles

        except Exception as e:
            logger.error(f'Error getting hourly historical data: {e}')

        return []

    def get_historical_daily(self, symbol, convert_to='USD', limit=365):
        """
        Get daily historical data

        Args:
            symbol: Cryptocurrency symbol
            convert_to: Currency to convert to
            limit: Number of days (max 2000)

        Returns:
            List of OHLCV dictionaries
        """
        try:
            url = f'{self.base_url}/v2/histoday'
            params = {
                'fsym': symbol,
                'tsym': convert_to,
                'limit': min(limit, 2000)
            }

            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('Response') == 'Success' and 'Data' in data and 'Data' in data['Data']:
                candles = []
                for candle in data['Data']['Data']:
                    candles.append({
                        'timestamp': candle['time'],
                        'open': candle['open'],
                        'high': candle['high'],
                        'low': candle['low'],
                        'close': candle['close'],
                        'volume_from': candle['volumefrom'],
                        'volume_to': candle['volumeto']
                    })
                return candles

        except Exception as e:
            logger.error(f'Error getting daily historical data: {e}')

        return []

    def get_historical_minute(self, symbol, convert_to='USD', limit=1440):
        """
        Get minute-level historical data

        Args:
            symbol: Cryptocurrency symbol
            convert_to: Currency to convert to
            limit: Number of minutes (max 2000)

        Returns:
            List of OHLCV dictionaries
        """
        try:
            url = f'{self.base_url}/v2/histominute'
            params = {
                'fsym': symbol,
                'tsym': convert_to,
                'limit': min(limit, 2000)
            }

            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('Response') == 'Success' and 'Data' in data and 'Data' in data['Data']:
                candles = []
                for candle in data['Data']['Data']:
                    candles.append({
                        'timestamp': candle['time'],
                        'open': candle['open'],
                        'high': candle['high'],
                        'low': candle['low'],
                        'close': candle['close'],
                        'volume_from': candle['volumefrom'],
                        'volume_to': candle['volumeto']
                    })
                return candles

        except Exception as e:
            logger.error(f'Error getting minute historical data: {e}')

        return []

    def get_historical_data(self, symbol, timeframe='1h', limit=500, convert_to='USD'):
        """
        Get historical OHLCV data based on timeframe

        Args:
            symbol: Cryptocurrency symbol
            timeframe: Time interval (1m, 5m, 15m, 1h, 4h, 1d)
            limit: Number of candles
            convert_to: Currency to convert to

        Returns:
            List of OHLCV dictionaries
        """
        if timeframe in ['1m', '5m', '15m', '30m']:
            return self.get_historical_minute(symbol, convert_to, limit)
        elif timeframe in ['1h', '4h', '12h']:
            return self.get_historical_hourly(symbol, convert_to, limit)
        else:
            return self.get_historical_daily(symbol, convert_to, limit)

    def get_candles_as_dataframe(self, symbol, timeframe='1h', limit=500):
        """Get historical data as pandas DataFrame"""
        candles = self.get_historical_data(symbol, timeframe, limit)

        if not candles:
            return pd.DataFrame()

        df = pd.DataFrame(candles)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df.set_index('timestamp', inplace=True)

        return df

    def get_top_coins(self, limit=100, convert_to='USD'):
        """Get top cryptocurrencies by market cap"""
        try:
            url = f'{self.base_url}/top/mktcapfull'
            params = {
                'limit': limit,
                'tsym': convert_to
            }

            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('Response') == 'Success' and 'Data' in data:
                coins = []
                for coin_data in data['Data']:
                    coin_info = coin_data.get('CoinInfo', {})
                    raw_data = coin_data.get('RAW', {}).get(convert_to, {})

                    coins.append({
                        'symbol': coin_info.get('Name'),
                        'name': coin_info.get('FullName'),
                        'price': raw_data.get('PRICE', 0),
                        'market_cap': raw_data.get('MKTCAP', 0),
                        'volume_24h': raw_data.get('VOLUME24HOUR', 0),
                        'change_pct_24h': raw_data.get('CHANGEPCT24HOUR', 0)
                    })

                return coins

        except Exception as e:
            logger.error(f'Error getting top coins: {e}')

        return []
