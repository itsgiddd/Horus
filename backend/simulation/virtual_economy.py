import numpy as np
import pandas as pd
from mesa import Model
from mesa.time import RandomActivation
import logging
from datetime import datetime
from .trader_agents import create_trader_population, TradeAction
from .market_dynamics import MarketDynamics

logger = logging.getLogger(__name__)


class VirtualEconomy(Model):
    """
    Virtual economy simulation for forex/crypto market prediction

    This model simulates a market with multiple trader agents making
    decisions based on technical indicators and market conditions.
    The simulation generates realistic market scenarios for the diffusion model.
    """

    def __init__(
        self,
        num_traders=100,
        initial_price=100.0,
        historical_data=None,
        simulation_steps=100,
        volatility=0.02
    ):
        super().__init__()

        self.num_traders = num_traders
        self.simulation_steps = simulation_steps
        self.current_step = 0

        self.market = MarketDynamics(
            initial_price=initial_price,
            volatility=volatility
        )

        self.historical_data = historical_data
        if historical_data is not None and len(historical_data) > 0:
            self.market.price_history = list(historical_data['close'].values)
            self.market.current_price = self.market.price_history[-1]

        self.schedule = RandomActivation(self)

        self.traders = create_trader_population(self, num_traders)
        for trader in self.traders:
            self.schedule.add(trader)

        self.datacollector_data = {
            'prices': [],
            'volumes': [],
            'buy_pressure': [],
            'sell_pressure': [],
            'trader_sentiment': [],
            'market_state': []
        }

        self.scenario_probabilities = {}

        logger.info(f'Virtual economy initialized with {num_traders} traders')

    def step(self):
        """Execute one step of the simulation"""
        self.current_step += 1

        market_state = self.market.get_market_state()

        trader_actions = []
        buy_count = 0
        sell_count = 0
        total_sentiment = 0

        for trader in self.traders:
            action = trader.decide_action(self.market.current_price, market_state)

            if action == TradeAction.BUY:
                position_size = trader.calculate_position_size(self.market.current_price)
                if trader.execute_trade(TradeAction.BUY, self.market.current_price, position_size):
                    trader_actions.append((1, position_size))
                    buy_count += 1
            elif action == TradeAction.SELL:
                if trader.execute_trade(TradeAction.SELL, self.market.current_price):
                    trader_actions.append((-1, trader.position))
                    sell_count += 1

            total_sentiment += trader.sentiment

        external_factors = self.generate_external_factors()

        new_price = self.market.update_price(trader_actions, external_factors)

        self.datacollector_data['prices'].append(new_price)
        self.datacollector_data['volumes'].append(sum([v for _, v in trader_actions]))
        self.datacollector_data['buy_pressure'].append(buy_count)
        self.datacollector_data['sell_pressure'].append(sell_count)
        self.datacollector_data['trader_sentiment'].append(total_sentiment / len(self.traders))
        self.datacollector_data['market_state'].append(market_state.copy())

        if self.current_step % 20 == 0:
            self.market.normalize_market()

        if np.random.random() < 0.05:
            self.market.introduce_market_shock(shock_magnitude=np.random.uniform(0.02, 0.05))

    def run_simulation(self, steps=None):
        """Run the full simulation"""
        if steps is None:
            steps = self.simulation_steps

        logger.info(f'Running simulation for {steps} steps')

        for i in range(steps):
            self.step()

        logger.info('Simulation completed')

        return self.get_simulation_results()

    def generate_external_factors(self):
        """Generate external market factors"""
        factors = {
            'news_sentiment': np.random.normal(0, 0.5),
            'macro_trend': np.random.normal(0, 0.3)
        }

        return factors

    def get_simulation_results(self):
        """Get simulation results"""
        results = {
            'prices': self.datacollector_data['prices'],
            'volumes': self.datacollector_data['volumes'],
            'buy_pressure': self.datacollector_data['buy_pressure'],
            'sell_pressure': self.datacollector_data['sell_pressure'],
            'trader_sentiment': self.datacollector_data['trader_sentiment'],
            'market_states': self.datacollector_data['market_state'],
            'final_price': self.market.current_price,
            'price_change_pct': (self.market.current_price - self.market.initial_price) / self.market.initial_price * 100
        }

        return results

    def calculate_scenario_probabilities(self, num_scenarios=10):
        """
        Run multiple scenarios to calculate probability distribution

        Returns:
            Dictionary with scenario outcomes and probabilities
        """
        logger.info(f'Calculating {num_scenarios} scenario probabilities')

        scenario_outcomes = []

        for scenario_id in range(num_scenarios):
            self.reset_simulation()

            self.run_simulation(self.simulation_steps)

            outcome = {
                'scenario_id': scenario_id,
                'final_price': self.market.current_price,
                'max_price': max(self.datacollector_data['prices']),
                'min_price': min(self.datacollector_data['prices']),
                'volatility': np.std(np.diff(self.datacollector_data['prices'])),
                'trend': np.polyfit(range(len(self.datacollector_data['prices'])),
                                   self.datacollector_data['prices'], 1)[0],
                'price_path': self.datacollector_data['prices'][-20:]
            }

            scenario_outcomes.append(outcome)

        final_prices = [s['final_price'] for s in scenario_outcomes]

        probabilities = {
            'bullish': sum(1 for p in final_prices if p > self.market.initial_price) / num_scenarios,
            'bearish': sum(1 for p in final_prices if p < self.market.initial_price) / num_scenarios,
            'neutral': sum(1 for p in final_prices if abs(p - self.market.initial_price) < self.market.initial_price * 0.01) / num_scenarios,
            'mean_final_price': np.mean(final_prices),
            'std_final_price': np.std(final_prices),
            'confidence_interval_95': (
                np.percentile(final_prices, 2.5),
                np.percentile(final_prices, 97.5)
            ),
            'scenarios': scenario_outcomes
        }

        logger.info(f'Probability analysis complete: Bullish={probabilities["bullish"]:.2f}, Bearish={probabilities["bearish"]:.2f}')

        return probabilities

    def reset_simulation(self):
        """Reset the simulation to initial state"""
        initial_price = self.market.initial_price

        self.market.reset(initial_price)

        for trader in self.traders:
            trader.position = 0
            trader.entry_price = 0
            trader.capital = trader.initial_capital
            trader.sentiment = 0
            trader.trades = []

        self.datacollector_data = {
            'prices': [],
            'volumes': [],
            'buy_pressure': [],
            'sell_pressure': [],
            'trader_sentiment': [],
            'market_state': []
        }

        self.current_step = 0

    def get_trader_statistics(self):
        """Get statistics about traders"""
        stats = {
            'total_traders': len(self.traders),
            'active_positions': sum(1 for t in self.traders if t.position > 0),
            'total_capital': sum(t.capital for t in self.traders),
            'total_trades': sum(len(t.trades) for t in self.traders),
            'win_rate': 0
        }

        total_wins = sum(t.win_count for t in self.traders)
        total_losses = sum(t.loss_count for t in self.traders)
        if total_wins + total_losses > 0:
            stats['win_rate'] = total_wins / (total_wins + total_losses)

        return stats

    def predict_next_candles(self, num_candles=10, scenario_count=5):
        """
        Predict future price candles using scenario simulation

        Returns:
            List of predicted OHLCV candles
        """
        logger.info(f'Predicting next {num_candles} candles using {scenario_count} scenarios')

        all_scenarios = []

        for _ in range(scenario_count):
            self.reset_simulation()

            scenario_candles = []
            for i in range(num_candles):
                self.step()

                last_idx = max(0, len(self.datacollector_data['prices']) - 5)
                recent_prices = self.datacollector_data['prices'][last_idx:]

                candle = {
                    'open': recent_prices[0] if len(recent_prices) > 0 else self.market.current_price,
                    'high': max(recent_prices) if len(recent_prices) > 0 else self.market.current_price,
                    'low': min(recent_prices) if len(recent_prices) > 0 else self.market.current_price,
                    'close': self.market.current_price,
                    'volume': sum(self.datacollector_data['volumes'][-5:])
                }

                scenario_candles.append(candle)

            all_scenarios.append(scenario_candles)

        predicted_candles = []
        for i in range(num_candles):
            opens = [s[i]['open'] for s in all_scenarios]
            highs = [s[i]['high'] for s in all_scenarios]
            lows = [s[i]['low'] for s in all_scenarios]
            closes = [s[i]['close'] for s in all_scenarios]
            volumes = [s[i]['volume'] for s in all_scenarios]

            predicted_candle = {
                'open': np.mean(opens),
                'high': np.mean(highs),
                'low': np.mean(lows),
                'close': np.mean(closes),
                'volume': np.mean(volumes),
                'confidence': 1.0 - (np.std(closes) / np.mean(closes)) if np.mean(closes) > 0 else 0.5
            }

            predicted_candles.append(predicted_candle)

        return predicted_candles
