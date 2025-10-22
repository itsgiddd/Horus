import numpy as np
import pandas as pd
from scipy import stats
import logging

logger = logging.getLogger(__name__)


class MarketDynamics:
    """Simulates market dynamics and price movements"""

    def __init__(self, initial_price=100.0, volatility=0.02, drift=0.0001):
        self.current_price = initial_price
        self.initial_price = initial_price
        self.volatility = volatility
        self.drift = drift

        self.price_history = [initial_price]
        self.volume_history = []
        self.order_book = {'bids': [], 'asks': []}

        self.supply = 0
        self.demand = 0

    def calculate_price_impact(self, buy_pressure, sell_pressure, total_volume):
        """Calculate price impact from order flow"""
        if total_volume == 0:
            return 0

        net_pressure = (buy_pressure - sell_pressure) / total_volume

        impact = net_pressure * self.volatility * np.random.uniform(0.5, 1.5)

        return impact

    def update_price(self, trader_actions, external_factors=None):
        """
        Update price based on trader actions and market dynamics

        Args:
            trader_actions: List of (action, size) tuples
            external_factors: Dict of external market factors

        Returns:
            New price
        """
        buy_volume = sum([size for action, size in trader_actions if action == 1])
        sell_volume = sum([size for action, size in trader_actions if action == -1])
        total_volume = buy_volume + sell_volume

        if total_volume > 0:
            self.volume_history.append(total_volume)
        else:
            self.volume_history.append(self.get_average_volume() * 0.3)

        price_impact = self.calculate_price_impact(buy_volume, sell_volume, total_volume)

        random_walk = np.random.normal(self.drift, self.volatility)

        external_impact = 0
        if external_factors:
            if 'news_sentiment' in external_factors:
                external_impact += external_factors['news_sentiment'] * 0.001
            if 'macro_trend' in external_factors:
                external_impact += external_factors['macro_trend'] * 0.0005

        total_change = price_impact + random_walk + external_impact

        self.current_price *= (1 + total_change)

        self.current_price = max(self.current_price, self.initial_price * 0.5)
        self.current_price = min(self.current_price, self.initial_price * 2.0)

        self.price_history.append(self.current_price)

        return self.current_price

    def get_market_state(self):
        """Calculate current market state indicators"""
        if len(self.price_history) < 20:
            return {
                'price': self.current_price,
                'trend': 0,
                'volatility': self.volatility,
                'rsi': 50,
                'momentum': 0,
                'volume_ratio': 1.0,
                'distance_from_mean': 0
            }

        prices = np.array(self.price_history[-100:])

        returns = np.diff(prices) / prices[:-1]
        current_volatility = np.std(returns) if len(returns) > 1 else self.volatility

        sma_20 = np.mean(prices[-20:])
        sma_50 = np.mean(prices[-50:]) if len(prices) >= 50 else sma_20

        trend = (sma_20 - sma_50) / sma_50 if sma_50 > 0 else 0

        rsi = self.calculate_rsi(prices[-14:]) if len(prices) >= 14 else 50

        momentum = (prices[-1] - prices[-10]) / prices[-10] if len(prices) >= 10 else 0

        volume_ratio = 1.0
        if len(self.volume_history) >= 20:
            avg_volume = np.mean(self.volume_history[-20:])
            current_volume = self.volume_history[-1]
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0

        mean_price = np.mean(prices)
        std_price = np.std(prices)
        distance_from_mean = (self.current_price - mean_price) / std_price if std_price > 0 else 0

        macd_line, signal_line = self.calculate_macd(prices)

        return {
            'price': self.current_price,
            'trend': trend,
            'volatility': current_volatility,
            'rsi': rsi,
            'momentum': momentum,
            'volume_ratio': volume_ratio,
            'distance_from_mean': distance_from_mean,
            'macd': macd_line,
            'macd_signal': signal_line,
            'total_volume': sum(self.volume_history[-10:]) if self.volume_history else 0
        }

    def calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator"""
        if len(prices) < 2:
            return 50

        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        avg_gain = np.mean(gains) if len(gains) > 0 else 0
        avg_loss = np.mean(losses) if len(losses) > 0 else 0

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def calculate_macd(self, prices):
        """Calculate MACD indicator"""
        if len(prices) < 26:
            return 0, 0

        ema_12 = self.calculate_ema(prices, 12)
        ema_26 = self.calculate_ema(prices, 26)

        macd_line = ema_12 - ema_26
        signal_line = macd_line * 0.9

        return macd_line, signal_line

    def calculate_ema(self, prices, period):
        """Calculate exponential moving average"""
        if len(prices) < period:
            return np.mean(prices)

        multiplier = 2 / (period + 1)
        ema = np.mean(prices[:period])

        for price in prices[period:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))

        return ema

    def get_average_volume(self):
        """Get average volume"""
        if len(self.volume_history) >= 20:
            return np.mean(self.volume_history[-20:])
        elif len(self.volume_history) > 0:
            return np.mean(self.volume_history)
        else:
            return 1000

    def introduce_market_shock(self, shock_magnitude=0.05):
        """Introduce a market shock event"""
        shock_direction = np.random.choice([-1, 1])
        shock_impact = shock_magnitude * shock_direction

        self.current_price *= (1 + shock_impact)
        self.volatility *= 1.5

        logger.info(f'Market shock introduced: {shock_impact*100:.2f}%')

    def normalize_market(self, decay_rate=0.05):
        """Gradually normalize volatility after shocks"""
        self.volatility = self.volatility * (1 - decay_rate) + (0.02 * decay_rate)

    def get_support_resistance_levels(self):
        """Calculate support and resistance levels"""
        if len(self.price_history) < 50:
            return {'support': self.current_price * 0.95, 'resistance': self.current_price * 1.05}

        prices = np.array(self.price_history[-100:])

        local_maxima = []
        local_minima = []

        for i in range(2, len(prices) - 2):
            if prices[i] > prices[i-1] and prices[i] > prices[i+1]:
                local_maxima.append(prices[i])
            if prices[i] < prices[i-1] and prices[i] < prices[i+1]:
                local_minima.append(prices[i])

        resistance = np.mean(local_maxima) if local_maxima else self.current_price * 1.05
        support = np.mean(local_minima) if local_minima else self.current_price * 0.95

        return {'support': support, 'resistance': resistance}

    def reset(self, initial_price=None):
        """Reset market dynamics"""
        if initial_price:
            self.initial_price = initial_price
            self.current_price = initial_price
        else:
            self.current_price = self.initial_price

        self.price_history = [self.current_price]
        self.volume_history = []
        self.volatility = 0.02
