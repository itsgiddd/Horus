import logging
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)


class PortfolioService:
    """Service for portfolio management and risk analytics"""

    def __init__(self):
        self.initial_balance = 50000.0
        self.current_balance = 55892.50

        # Mock positions
        self.positions = [
            {
                'symbol': 'BTC',
                'quantity': 0.5,
                'entry_price': 42000.0,
                'current_price': 43250.50,
                'value': 21625.25,
                'pnl': 625.25,
                'pnl_percent': 2.97,
                'entry_date': (datetime.utcnow() - timedelta(days=15)).isoformat()
            },
            {
                'symbol': 'ETH',
                'quantity': 5.0,
                'entry_price': 2200.0,
                'current_price': 2280.75,
                'value': 11403.75,
                'pnl': 403.75,
                'pnl_percent': 3.67,
                'entry_date': (datetime.utcnow() - timedelta(days=8)).isoformat()
            },
            {
                'symbol': 'EUR/USD',
                'quantity': 10000,
                'entry_price': 1.0820,
                'current_price': 1.0845,
                'value': 10845.0,
                'pnl': 250.0,
                'pnl_percent': 2.36,
                'entry_date': (datetime.utcnow() - timedelta(days=3)).isoformat()
            }
        ]

    def get_portfolio_summary(self):
        """Get portfolio summary statistics"""

        total_value = sum(pos['value'] for pos in self.positions) + (self.current_balance - sum(pos['value'] for pos in self.positions))
        total_pnl = self.current_balance - self.initial_balance
        total_pnl_percent = (total_pnl / self.initial_balance) * 100

        return {
            'total_value': round(total_value, 2),
            'cash_balance': round(self.current_balance - sum(pos['value'] for pos in self.positions), 2),
            'invested': round(sum(pos['value'] for pos in self.positions), 2),
            'total_pnl': round(total_pnl, 2),
            'total_pnl_percent': round(total_pnl_percent, 2),
            'day_pnl': round(random.uniform(100, 500), 2),
            'day_pnl_percent': round(random.uniform(0.5, 2), 2),
            'positions_count': len(self.positions),
            'updated_at': datetime.utcnow().isoformat()
        }

    def get_positions(self):
        """Get all active positions"""
        return self.positions

    def calculate_risk_metrics(self):
        """Calculate portfolio risk metrics"""

        portfolio_value = sum(pos['value'] for pos in self.positions)

        # Value at Risk (VaR)
        var_95 = portfolio_value * 0.05  # 5% VaR
        var_99 = portfolio_value * 0.08  # 8% VaR

        # Position sizes
        position_sizes = [pos['value'] for pos in self.positions]
        max_position_size = max(position_sizes) if position_sizes else 0
        max_position_percent = (max_position_size / portfolio_value * 100) if portfolio_value > 0 else 0

        # Risk/Reward
        winning_positions = [p for p in self.positions if p['pnl'] > 0]
        win_rate = (len(winning_positions) / len(self.positions) * 100) if self.positions else 0

        return {
            'value_at_risk_95': round(var_95, 2),
            'value_at_risk_99': round(var_99, 2),
            'max_drawdown': -12.5,
            'max_position_size': round(max_position_size, 2),
            'max_position_percent': round(max_position_percent, 2),
            'portfolio_beta': 1.15,
            'sharpe_ratio': 1.85,
            'sortino_ratio': 2.34,
            'win_rate': round(win_rate, 2),
            'risk_score': self._calculate_risk_score(),
            'diversification_score': self._calculate_diversification_score()
        }

    def _calculate_risk_score(self):
        """Calculate overall risk score (0-100, higher = more risky)"""
        # Simple risk scoring based on position concentration
        position_sizes = [pos['value'] for pos in self.positions]
        total_value = sum(position_sizes)

        if not position_sizes or total_value == 0:
            return 0

        # Check concentration risk
        max_concentration = max(position_sizes) / total_value
        concentration_risk = max_concentration * 100

        # Volatility risk (mock)
        volatility_risk = random.uniform(20, 40)

        # Average of risks
        risk_score = (concentration_risk + volatility_risk) / 2

        return round(min(risk_score, 100), 1)

    def _calculate_diversification_score(self):
        """Calculate diversification score (0-100, higher = better diversified)"""
        if not self.positions:
            return 0

        # Simple diversification: more positions = better (up to a point)
        num_positions = len(self.positions)

        # Check asset type diversity
        crypto_count = len([p for p in self.positions if '/' not in p['symbol']])
        forex_count = len([p for p in self.positions if '/' in p['symbol']])

        asset_diversity = (min(crypto_count, 1) + min(forex_count, 1)) * 25

        # Position count diversity
        position_diversity = min(num_positions * 15, 50)

        score = asset_diversity + position_diversity

        return round(min(score, 100), 1)

    def get_performance(self, timeframe='30d'):
        """Get portfolio performance over time"""

        # Generate mock performance data
        days = int(timeframe.replace('d', ''))
        performance_data = []

        current_value = self.initial_balance

        for i in range(days):
            date = datetime.utcnow() - timedelta(days=days - i)

            # Simulate growth
            daily_change = random.uniform(-2, 3)
            current_value = current_value * (1 + daily_change / 100)

            performance_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'value': round(current_value, 2),
                'pnl': round(current_value - self.initial_balance, 2),
                'pnl_percent': round((current_value - self.initial_balance) / self.initial_balance * 100, 2)
            })

        return {
            'timeframe': timeframe,
            'data': performance_data,
            'start_value': self.initial_balance,
            'end_value': round(current_value, 2),
            'total_return': round(((current_value - self.initial_balance) / self.initial_balance) * 100, 2)
        }
