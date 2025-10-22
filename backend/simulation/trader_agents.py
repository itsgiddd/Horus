import numpy as np
from mesa import Agent
import random
from enum import Enum


class TraderType(Enum):
    """Types of traders in the simulation"""
    TREND_FOLLOWER = "trend_follower"
    MEAN_REVERTER = "mean_reverter"
    SCALP_TRADER = "scalp"
    SWING_TRADER = "swing"
    INSTITUTIONAL = "institutional"
    RETAIL = "retail"


class TradeAction(Enum):
    """Trading actions"""
    BUY = 1
    SELL = -1
    HOLD = 0


class BaseTrader(Agent):
    """Base trader agent class"""

    def __init__(self, unique_id, model, trader_type, capital=10000, risk_tolerance=0.02):
        super().__init__(unique_id, model)
        self.trader_type = trader_type
        self.capital = capital
        self.initial_capital = capital
        self.risk_tolerance = risk_tolerance
        self.position = 0
        self.entry_price = 0
        self.trades = []
        self.win_count = 0
        self.loss_count = 0
        self.sentiment = 0.0

    def calculate_position_size(self, current_price, stop_loss_pct=0.02):
        """Calculate position size based on risk tolerance"""
        risk_amount = self.capital * self.risk_tolerance
        price_risk = current_price * stop_loss_pct
        if price_risk > 0:
            position_size = risk_amount / price_risk
            return min(position_size, self.capital / current_price * 0.5)
        return 0

    def execute_trade(self, action, price, size=None):
        """Execute a trade"""
        if size is None:
            size = self.calculate_position_size(price)

        if action == TradeAction.BUY and self.position <= 0:
            cost = price * size
            if cost <= self.capital:
                self.position = size
                self.entry_price = price
                self.capital -= cost
                self.trades.append({
                    'action': 'BUY',
                    'price': price,
                    'size': size,
                    'step': self.model.schedule.steps
                })
                return True

        elif action == TradeAction.SELL and self.position > 0:
            proceeds = price * self.position
            pnl = (price - self.entry_price) * self.position

            if pnl > 0:
                self.win_count += 1
            else:
                self.loss_count += 1

            self.capital += proceeds
            self.trades.append({
                'action': 'SELL',
                'price': price,
                'size': self.position,
                'pnl': pnl,
                'step': self.model.schedule.steps
            })
            self.position = 0
            self.entry_price = 0
            return True

        return False

    def update_sentiment(self, market_state):
        """Update trader sentiment based on market state"""
        pass

    def step(self):
        """Execute one step of the agent"""
        pass


class TrendFollower(BaseTrader):
    """Trend following trader agent"""

    def __init__(self, unique_id, model, capital=10000):
        super().__init__(unique_id, model, TraderType.TREND_FOLLOWER, capital, risk_tolerance=0.025)
        self.trend_threshold = 0.005
        self.lookback = 20

    def update_sentiment(self, market_state):
        """Update sentiment based on trend"""
        if 'trend' in market_state:
            trend = market_state['trend']
            if trend > self.trend_threshold:
                self.sentiment = min(1.0, trend * 2)
            elif trend < -self.trend_threshold:
                self.sentiment = max(-1.0, trend * 2)
            else:
                self.sentiment *= 0.8

    def decide_action(self, current_price, market_state):
        """Decide trading action based on trend"""
        self.update_sentiment(market_state)

        if self.sentiment > 0.6 and self.position == 0:
            return TradeAction.BUY
        elif self.sentiment < -0.4 and self.position > 0:
            return TradeAction.SELL
        elif self.position > 0 and (current_price - self.entry_price) / self.entry_price < -0.02:
            return TradeAction.SELL
        else:
            return TradeAction.HOLD


class MeanReverter(BaseTrader):
    """Mean reversion trader agent"""

    def __init__(self, unique_id, model, capital=10000):
        super().__init__(unique_id, model, TraderType.MEAN_REVERTER, capital, risk_tolerance=0.02)
        self.overbought_threshold = 70
        self.oversold_threshold = 30

    def update_sentiment(self, market_state):
        """Update sentiment based on mean reversion signals"""
        if 'rsi' in market_state:
            rsi = market_state['rsi']
            if rsi < self.oversold_threshold:
                self.sentiment = (self.oversold_threshold - rsi) / 30
            elif rsi > self.overbought_threshold:
                self.sentiment = -(rsi - self.overbought_threshold) / 30
            else:
                self.sentiment *= 0.7

        if 'distance_from_mean' in market_state:
            dist = market_state['distance_from_mean']
            if abs(dist) > 2:
                self.sentiment += -np.sign(dist) * 0.3

    def decide_action(self, current_price, market_state):
        """Decide action based on mean reversion"""
        self.update_sentiment(market_state)

        if self.sentiment > 0.5 and self.position == 0:
            return TradeAction.BUY
        elif self.sentiment < -0.5 and self.position > 0:
            return TradeAction.SELL
        elif self.position > 0:
            pnl_pct = (current_price - self.entry_price) / self.entry_price
            if pnl_pct > 0.015 or pnl_pct < -0.02:
                return TradeAction.SELL
        return TradeAction.HOLD


class ScalpTrader(BaseTrader):
    """Scalp trader with quick in/out strategy"""

    def __init__(self, unique_id, model, capital=5000):
        super().__init__(unique_id, model, TraderType.SCALP_TRADER, capital, risk_tolerance=0.01)
        self.profit_target = 0.003
        self.stop_loss = 0.002

    def decide_action(self, current_price, market_state):
        """Quick scalp decisions"""
        volatility = market_state.get('volatility', 0.01)

        if self.position == 0:
            if volatility > 0.005 and random.random() > 0.7:
                momentum = market_state.get('momentum', 0)
                if momentum > 0:
                    return TradeAction.BUY
        else:
            pnl_pct = (current_price - self.entry_price) / self.entry_price
            if pnl_pct >= self.profit_target or pnl_pct <= -self.stop_loss:
                return TradeAction.SELL

        return TradeAction.HOLD


class SwingTrader(BaseTrader):
    """Swing trader holding positions for multiple periods"""

    def __init__(self, unique_id, model, capital=15000):
        super().__init__(unique_id, model, TraderType.SWING_TRADER, capital, risk_tolerance=0.03)
        self.holding_period = 0
        self.max_holding = 50
        self.min_holding = 10

    def decide_action(self, current_price, market_state):
        """Swing trading decisions"""
        if self.position > 0:
            self.holding_period += 1
            pnl_pct = (current_price - self.entry_price) / self.entry_price

            if pnl_pct > 0.04 and self.holding_period >= self.min_holding:
                return TradeAction.SELL
            elif pnl_pct < -0.03:
                return TradeAction.SELL
            elif self.holding_period >= self.max_holding:
                return TradeAction.SELL

        else:
            self.holding_period = 0
            trend = market_state.get('trend', 0)
            rsi = market_state.get('rsi', 50)

            if trend > 0.01 and rsi > 40 and rsi < 65:
                return TradeAction.BUY

        return TradeAction.HOLD


class InstitutionalTrader(BaseTrader):
    """Institutional trader with large capital and strategic approach"""

    def __init__(self, unique_id, model, capital=100000):
        super().__init__(unique_id, model, TraderType.INSTITUTIONAL, capital, risk_tolerance=0.015)
        self.order_size_limit = 0.1
        self.strategic_position = None

    def decide_action(self, current_price, market_state):
        """Strategic institutional decisions"""
        market_cap_exposure = market_state.get('total_volume', 1000000)

        max_position_value = market_cap_exposure * self.order_size_limit

        if self.position == 0:
            macd = market_state.get('macd', 0)
            trend = market_state.get('trend', 0)
            volume_ratio = market_state.get('volume_ratio', 1.0)

            if trend > 0.008 and macd > 0 and volume_ratio > 1.2:
                return TradeAction.BUY

        else:
            position_value = self.position * current_price
            pnl_pct = (current_price - self.entry_price) / self.entry_price

            if pnl_pct > 0.05:
                return TradeAction.SELL
            elif pnl_pct < -0.025:
                return TradeAction.SELL

        return TradeAction.HOLD


def create_trader_population(model, num_traders=100):
    """Create a diverse population of traders"""
    traders = []
    trader_id = 0

    trader_distribution = {
        'trend': 0.25,
        'mean_revert': 0.25,
        'scalp': 0.20,
        'swing': 0.20,
        'institutional': 0.10
    }

    for trader_type, proportion in trader_distribution.items():
        count = int(num_traders * proportion)

        for _ in range(count):
            capital = random.uniform(5000, 50000)

            if trader_type == 'trend':
                trader = TrendFollower(trader_id, model, capital)
            elif trader_type == 'mean_revert':
                trader = MeanReverter(trader_id, model, capital)
            elif trader_type == 'scalp':
                trader = ScalpTrader(trader_id, model, capital * 0.5)
            elif trader_type == 'swing':
                trader = SwingTrader(trader_id, model, capital * 1.2)
            elif trader_type == 'institutional':
                trader = InstitutionalTrader(trader_id, model, capital * 10)

            traders.append(trader)
            trader_id += 1

    return traders
