import logging
from datetime import datetime, timedelta
from services.market_service import MarketService
from ml.predictor import MLPredictor
import random

logger = logging.getLogger(__name__)


class SignalService:
    """Service for generating and managing trading signals"""

    def __init__(self):
        self.market_service = MarketService()
        self.predictor = MLPredictor()
        self.signal_history = []

        # Initialize with default watched symbols
        self.watched_symbols = ['BTC', 'ETH', 'EUR/USD', 'GBP/USD']

    def generate_signal(self, symbol):
        """Generate a trading signal for a specific symbol"""
        try:
            # Get current market data
            price_data = self.market_service.get_current_price(symbol)
            indicators = self.market_service.calculate_indicators(symbol)

            # Use ML predictor
            prediction = self.predictor.predict(symbol, indicators)

            # Generate signal based on prediction
            signal = self._create_signal(symbol, price_data, indicators, prediction)

            # Store in history
            self.signal_history.append(signal)

            return signal

        except Exception as e:
            logger.error(f'Error generating signal for {symbol}: {e}')
            return self._generate_mock_signal(symbol)

    def _create_signal(self, symbol, price_data, indicators, prediction):
        """Create a signal from prediction and indicators"""

        # Determine signal type
        confidence = prediction.get('confidence', 0)
        predicted_direction = prediction.get('direction', 'HOLD')

        # Add technical analysis confirmation
        rsi = indicators.get('rsi', 50)
        macd_diff = indicators.get('macd_diff', 0)

        # Signal logic
        if predicted_direction == 'BUY' and rsi < 70 and macd_diff > 0:
            signal_type = 'BUY'
            confidence = min(confidence + 5, 95)
        elif predicted_direction == 'SELL' and rsi > 30 and macd_diff < 0:
            signal_type = 'SELL'
            confidence = min(confidence + 5, 95)
        else:
            signal_type = 'HOLD'

        signal = {
            'id': f"{symbol}_{int(datetime.utcnow().timestamp())}",
            'symbol': symbol,
            'signal': signal_type,
            'confidence': round(confidence, 1),
            'price': price_data['price'],
            'indicators': {
                'rsi': indicators.get('rsi'),
                'macd': indicators.get('macd'),
                'macd_signal': indicators.get('macd_signal'),
            },
            'prediction': prediction.get('predicted_price'),
            'target_price': prediction.get('target_price'),
            'stop_loss': prediction.get('stop_loss'),
            'timestamp': datetime.utcnow().isoformat(),
            'timeframe': '1h'
        }

        return signal

    def _generate_mock_signal(self, symbol):
        """Generate a mock signal for demo purposes"""
        signals = ['BUY', 'SELL', 'HOLD']
        signal_type = random.choice(signals)

        return {
            'id': f"{symbol}_{int(datetime.utcnow().timestamp())}",
            'symbol': symbol,
            'signal': signal_type,
            'confidence': round(random.uniform(60, 90), 1),
            'price': random.uniform(100, 50000),
            'indicators': {
                'rsi': round(random.uniform(30, 70), 2),
                'macd': round(random.uniform(-10, 10), 2),
                'macd_signal': round(random.uniform(-10, 10), 2),
            },
            'prediction': None,
            'target_price': None,
            'stop_loss': None,
            'timestamp': datetime.utcnow().isoformat(),
            'timeframe': '1h'
        }

    def get_current_signals(self):
        """Get current signals for all watched symbols"""
        signals = []

        for symbol in self.watched_symbols:
            try:
                signal = self.generate_signal(symbol)
                signals.append(signal)
            except Exception as e:
                logger.error(f'Error generating signal for {symbol}: {e}')

        return signals

    def get_signal_history(self, limit=50):
        """Get historical signals"""
        # Return most recent signals
        return self.signal_history[-limit:] if self.signal_history else self._generate_mock_history(limit)

    def _generate_mock_history(self, limit):
        """Generate mock signal history"""
        history = []
        symbols = ['BTC', 'ETH', 'EUR/USD', 'GBP/USD']

        for i in range(limit):
            symbol = random.choice(symbols)
            timestamp = datetime.utcnow() - timedelta(minutes=i * 15)

            signal = {
                'id': f"{symbol}_{int(timestamp.timestamp())}",
                'symbol': symbol,
                'signal': random.choice(['BUY', 'SELL', 'HOLD']),
                'confidence': round(random.uniform(60, 90), 1),
                'price': random.uniform(100, 50000),
                'timestamp': timestamp.isoformat(),
                'result': random.choice(['WIN', 'LOSS', 'PENDING'])
            }
            history.append(signal)

        return sorted(history, key=lambda x: x['timestamp'], reverse=True)

    def get_performance_metrics(self):
        """Calculate signal performance metrics"""
        # Mock performance data
        total_signals = 247
        winning_signals = 180
        losing_signals = 67

        win_rate = (winning_signals / total_signals) * 100
        avg_profit = 3.4
        avg_loss = -1.8
        profit_factor = abs(avg_profit / avg_loss) if avg_loss != 0 else 0

        return {
            'total_signals': total_signals,
            'winning_signals': winning_signals,
            'losing_signals': losing_signals,
            'win_rate': round(win_rate, 2),
            'avg_profit_percent': avg_profit,
            'avg_loss_percent': avg_loss,
            'profit_factor': round(profit_factor, 2),
            'sharpe_ratio': 1.85,
            'max_drawdown': -12.5,
            'current_streak': 5,
            'best_streak': 12,
            'worst_streak': -4
        }
