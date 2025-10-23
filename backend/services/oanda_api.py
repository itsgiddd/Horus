import os
import logging
from datetime import datetime, timedelta
from oandapyV20 import API
from oandapyV20.exceptions import V20Error
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import pandas as pd

logger = logging.getLogger(__name__)


class OandaAPI:
    """OANDA API integration for forex data"""

    def __init__(self):
        self.api_key = os.getenv('OANDA_API_KEY')
        self.account_id = os.getenv('OANDA_ACCOUNT_ID')
        self.environment = os.getenv('OANDA_ENVIRONMENT', 'practice')

        if self.environment == 'live':
            self.api_url = 'https://api-fxtrade.oanda.com'
        else:
            self.api_url = 'https://api-fxpractice.oanda.com'

        self.client = None
        if self.api_key:
            self.client = API(access_token=self.api_key, environment=self.environment)

        # Supported forex pairs
        self.forex_pairs = [
            # Major USD pairs
            'EUR_USD', 'GBP_USD', 'USD_JPY', 'AUD_USD', 'USD_CAD',
            'NZD_USD', 'USD_CHF',
            # Additional USD pairs
            'USD_CNY', 'USD_HKD', 'USD_SGD', 'USD_SEK', 'USD_NOK', 'USD_DKK',
            'USD_ZAR', 'USD_MXN', 'USD_TRY', 'USD_INR', 'USD_KRW', 'USD_BRL',
            'USD_PLN', 'USD_THB', 'USD_IDR', 'USD_CZK', 'USD_HUF', 'USD_ILS',
            'USD_CLP', 'USD_PHP', 'USD_AED', 'USD_SAR', 'USD_MYR', 'USD_RON',
            # Cross pairs
            'EUR_GBP', 'EUR_JPY', 'GBP_JPY', 'AUD_JPY', 'EUR_AUD',
            'EUR_CAD', 'GBP_AUD', 'GBP_CAD'
        ]

    def is_configured(self):
        """Check if OANDA API is properly configured"""
        return bool(self.api_key and self.account_id and self.client)

    def get_instruments(self):
        """Get list of available instruments"""
        if not self.is_configured():
            logger.warning('OANDA API not configured')
            return []

        try:
            r = accounts.AccountInstruments(accountID=self.account_id)
            response = self.client.request(r)
            return [inst['name'] for inst in response.get('instruments', [])]
        except V20Error as e:
            logger.error(f'OANDA API error getting instruments: {e}')
            return self.forex_pairs

    def get_current_price(self, instrument):
        """Get current bid/ask price for an instrument"""
        if not self.is_configured():
            return None

        try:
            params = {'instruments': instrument}
            r = pricing.PricingInfo(accountID=self.account_id, params=params)
            response = self.client.request(r)

            if 'prices' in response and len(response['prices']) > 0:
                price_data = response['prices'][0]

                bid = float(price_data.get('bids', [{}])[0].get('price', 0))
                ask = float(price_data.get('asks', [{}])[0].get('price', 0))
                mid = (bid + ask) / 2

                return {
                    'symbol': instrument.replace('_', '/'),
                    'price': mid,
                    'bid': bid,
                    'ask': ask,
                    'spread': ask - bid,
                    'timestamp': price_data.get('time'),
                    'tradeable': price_data.get('tradeable', False)
                }
        except V20Error as e:
            logger.error(f'OANDA API error getting price for {instrument}: {e}')
        except Exception as e:
            logger.error(f'Unexpected error getting price: {e}')

        return None

    def get_historical_data(self, instrument, granularity='H1', count=500):
        """
        Get historical OHLCV data

        Args:
            instrument: Forex pair (e.g., 'EUR_USD')
            granularity: Candle size (S5, S10, S15, S30, M1, M2, M4, M5, M10, M15, M30, H1, H2, H3, H4, H6, H8, H12, D, W, M)
            count: Number of candles (max 5000)

        Returns:
            List of OHLCV dictionaries
        """
        if not self.is_configured():
            logger.warning('OANDA API not configured, returning empty data')
            return []

        try:
            params = {
                'granularity': granularity,
                'count': min(count, 5000)
            }

            r = instruments.InstrumentsCandles(instrument=instrument, params=params)
            response = self.client.request(r)

            candles = []
            for candle in response.get('candles', []):
                if candle.get('complete', False):
                    mid = candle['mid']
                    candles.append({
                        'timestamp': candle['time'],
                        'open': float(mid['o']),
                        'high': float(mid['h']),
                        'low': float(mid['l']),
                        'close': float(mid['c']),
                        'volume': int(candle.get('volume', 0))
                    })

            return candles

        except V20Error as e:
            logger.error(f'OANDA API error getting historical data: {e}')
        except Exception as e:
            logger.error(f'Unexpected error getting historical data: {e}')

        return []

    def get_historical_range(self, instrument, start_time, end_time, granularity='H1'):
        """
        Get historical data for a specific time range

        Args:
            instrument: Forex pair
            start_time: Start datetime
            end_time: End datetime
            granularity: Candle size

        Returns:
            List of OHLCV dictionaries
        """
        if not self.is_configured():
            return []

        try:
            params = {
                'granularity': granularity,
                'from': start_time.isoformat() + 'Z',
                'to': end_time.isoformat() + 'Z'
            }

            r = instruments.InstrumentsCandles(instrument=instrument, params=params)
            response = self.client.request(r)

            candles = []
            for candle in response.get('candles', []):
                if candle.get('complete', False):
                    mid = candle['mid']
                    candles.append({
                        'timestamp': candle['time'],
                        'open': float(mid['o']),
                        'high': float(mid['h']),
                        'low': float(mid['l']),
                        'close': float(mid['c']),
                        'volume': int(candle.get('volume', 0))
                    })

            return candles

        except V20Error as e:
            logger.error(f'OANDA API error: {e}')
        except Exception as e:
            logger.error(f'Error fetching range data: {e}')

        return []

    def convert_granularity(self, timeframe):
        """Convert common timeframe notation to OANDA granularity"""
        granularity_map = {
            '1m': 'M1',
            '5m': 'M5',
            '15m': 'M15',
            '30m': 'M30',
            '1h': 'H1',
            '4h': 'H4',
            '1d': 'D',
            '1w': 'W',
            '1M': 'M'
        }
        return granularity_map.get(timeframe, 'H1')

    def format_instrument(self, pair):
        """Convert pair notation (EUR/USD) to OANDA format (EUR_USD)"""
        return pair.replace('/', '_')

    def get_candles_as_dataframe(self, instrument, granularity='H1', count=500):
        """Get historical data as pandas DataFrame"""
        candles = self.get_historical_data(instrument, granularity, count)

        if not candles:
            return pd.DataFrame()

        df = pd.DataFrame(candles)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)

        return df
