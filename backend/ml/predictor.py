import numpy as np
import logging
from datetime import datetime
import random
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from simulation.virtual_economy import VirtualEconomy
from ml.diffusion.diffusion_model import DiffusionForecaster

logger = logging.getLogger(__name__)


class MLPredictor:
    """Machine Learning predictor for trading signals with diffusion model"""

    def __init__(self):
        self.models = {}
        self.diffusion_forecaster = None
        self.is_trained = False

        try:
            self.diffusion_forecaster = DiffusionForecaster(
                lookback_window=60,
                forecast_horizon=10,
                num_traders=100
            )
            logger.info('Diffusion forecaster initialized')
        except Exception as e:
            logger.error(f'Error initializing diffusion forecaster: {e}')
            self.diffusion_forecaster = None

    def predict(self, symbol, indicators):
        """
        Generate a prediction for a symbol based on indicators

        Args:
            symbol: Trading symbol
            indicators: Dictionary of technical indicators

        Returns:
            Dictionary with prediction, confidence, target, and stop loss
        """
        try:
            # Extract indicator values
            rsi = indicators.get('rsi', 50)
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            macd_diff = indicators.get('macd_diff', 0)
            sma_20 = indicators.get('sma_20', 0)
            sma_50 = indicators.get('sma_50', 0)

            # Simple rule-based prediction (can be replaced with actual ML model)
            prediction = self._rule_based_prediction(
                rsi, macd, macd_signal, macd_diff, sma_20, sma_50
            )

            return prediction

        except Exception as e:
            logger.error(f'Error in ML prediction: {e}')
            return self._default_prediction()

    def _rule_based_prediction(self, rsi, macd, macd_signal, macd_diff, sma_20, sma_50):
        """
        Rule-based trading logic combining multiple indicators

        This simulates an ML model but uses technical analysis rules
        In production, this would be replaced with actual trained models
        """

        score = 0
        confidence_factors = []

        # RSI Analysis
        if rsi < 30:
            score += 3  # Oversold - bullish
            confidence_factors.append(15)
        elif rsi > 70:
            score -= 3  # Overbought - bearish
            confidence_factors.append(15)
        elif 40 <= rsi <= 60:
            score += 1  # Neutral zone - slight bullish
            confidence_factors.append(5)

        # MACD Analysis
        if macd_diff > 0:
            score += 2  # Bullish crossover
            confidence_factors.append(12)
        elif macd_diff < 0:
            score -= 2  # Bearish crossover
            confidence_factors.append(12)

        if macd > macd_signal:
            score += 1
            confidence_factors.append(8)
        else:
            score -= 1
            confidence_factors.append(8)

        # Moving Average Analysis
        if sma_20 > sma_50:
            score += 2  # Bullish trend
            confidence_factors.append(10)
        elif sma_20 < sma_50:
            score -= 2  # Bearish trend
            confidence_factors.append(10)

        # Determine direction
        if score >= 3:
            direction = 'BUY'
            confidence = min(60 + sum(confidence_factors[:3]), 95)
        elif score <= -3:
            direction = 'SELL'
            confidence = min(60 + sum(confidence_factors[:3]), 95)
        else:
            direction = 'HOLD'
            confidence = min(50 + abs(score) * 5, 75)

        # Calculate target and stop loss (simplified)
        current_price = 100  # Placeholder, should come from market data
        target_percent = 0.03 if direction == 'BUY' else -0.03
        stop_percent = -0.015 if direction == 'BUY' else 0.015

        return {
            'direction': direction,
            'confidence': round(confidence, 1),
            'predicted_price': round(current_price * (1 + target_percent), 2),
            'target_price': round(current_price * (1 + target_percent), 2),
            'stop_loss': round(current_price * (1 + stop_percent), 2),
            'score': score,
            'timestamp': datetime.utcnow().isoformat()
        }

    def _default_prediction(self):
        """Return a default prediction when errors occur"""
        return {
            'direction': 'HOLD',
            'confidence': 50.0,
            'predicted_price': None,
            'target_price': None,
            'stop_loss': None,
            'score': 0,
            'timestamp': datetime.utcnow().isoformat()
        }

    def train_model(self, symbol, historical_data):
        """
        Train ML model on historical data

        This is a placeholder for actual model training.
        In production, this would:
        1. Prepare features from historical data
        2. Train LSTM/Random Forest models
        3. Validate model performance
        4. Save trained model
        """
        logger.info(f'Training model for {symbol}...')

        # Placeholder for actual training logic
        # Would use TensorFlow/Keras for LSTM or sklearn for Random Forest

        self.models[symbol] = {
            'trained_at': datetime.utcnow().isoformat(),
            'accuracy': random.uniform(0.65, 0.85),
            'precision': random.uniform(0.70, 0.90)
        }

        logger.info(f'Model trained for {symbol}')
        return self.models[symbol]

    def get_model_info(self, symbol):
        """Get information about trained model"""
        if symbol in self.models:
            return self.models[symbol]
        return None

    def predict_with_diffusion(self, symbol, historical_data, indicators):
        """
        Advanced prediction using diffusion model and virtual economy

        Args:
            symbol: Trading symbol
            historical_data: Historical OHLCV data (list of dicts or DataFrame)
            indicators: Current technical indicators

        Returns:
            Dict with prediction, candles, probabilities, and scenarios
        """
        try:
            if self.diffusion_forecaster is None:
                logger.warning('Diffusion forecaster not available, using fallback')
                return self._fallback_prediction_with_simulation(symbol, historical_data, indicators)

            import pandas as pd

            if isinstance(historical_data, list):
                df = pd.DataFrame(historical_data)
            else:
                df = historical_data

            if len(df) < 60:
                logger.warning('Insufficient historical data for diffusion model')
                return self._fallback_prediction_with_simulation(symbol, historical_data, indicators)

            forecast_result = self.diffusion_forecaster.predict(df, num_samples=5)

            predicted_candles = forecast_result['candles']

            initial_price = df['close'].iloc[-1]
            final_price = predicted_candles[-1]['close']
            price_change_pct = (final_price - initial_price) / initial_price * 100

            if price_change_pct > 1.0:
                direction = 'BUY'
                confidence = min(60 + abs(price_change_pct) * 5, 95)
            elif price_change_pct < -1.0:
                direction = 'SELL'
                confidence = min(60 + abs(price_change_pct) * 5, 95)
            else:
                direction = 'HOLD'
                confidence = 50 + abs(price_change_pct) * 10

            economy = VirtualEconomy(
                num_traders=100,
                initial_price=initial_price,
                historical_data=df,
                simulation_steps=50
            )

            probabilities = economy.calculate_scenario_probabilities(num_scenarios=10)

            base_prediction = self._rule_based_prediction(
                indicators.get('rsi', 50),
                indicators.get('macd', 0),
                indicators.get('macd_signal', 0),
                indicators.get('macd_diff', 0),
                indicators.get('sma_20', initial_price),
                indicators.get('sma_50', initial_price)
            )

            combined_confidence = (confidence * 0.6 + base_prediction['confidence'] * 0.4)

            return {
                'direction': direction,
                'confidence': round(combined_confidence, 1),
                'predicted_price': final_price,
                'target_price': round(final_price, 2),
                'stop_loss': round(initial_price * (0.985 if direction == 'BUY' else 1.015), 2),
                'price_change_pct': round(price_change_pct, 2),
                'predicted_candles': predicted_candles,
                'scenario_probabilities': {
                    'bullish': round(probabilities['bullish'] * 100, 1),
                    'bearish': round(probabilities['bearish'] * 100, 1),
                    'neutral': round(probabilities['neutral'] * 100, 1),
                },
                'confidence_interval': {
                    'lower': round(probabilities['confidence_interval_95'][0], 2),
                    'upper': round(probabilities['confidence_interval_95'][1], 2)
                },
                'timestamp': datetime.utcnow().isoformat(),
                'model_type': 'diffusion'
            }

        except Exception as e:
            logger.error(f'Error in diffusion prediction: {e}')
            return self._fallback_prediction_with_simulation(symbol, historical_data, indicators)

    def _fallback_prediction_with_simulation(self, symbol, historical_data, indicators):
        """Fallback prediction using simulation only"""
        try:
            import pandas as pd

            if isinstance(historical_data, list):
                df = pd.DataFrame(historical_data)
            else:
                df = historical_data

            initial_price = df['close'].iloc[-1] if len(df) > 0 else 100.0

            economy = VirtualEconomy(
                num_traders=100,
                initial_price=initial_price,
                historical_data=df if len(df) >= 20 else None,
                simulation_steps=50
            )

            probabilities = economy.calculate_scenario_probabilities(num_scenarios=5)
            predicted_candles = economy.predict_next_candles(num_candles=10, scenario_count=3)

            final_price = predicted_candles[-1]['close']
            price_change_pct = (final_price - initial_price) / initial_price * 100

            if price_change_pct > 0.5:
                direction = 'BUY'
            elif price_change_pct < -0.5:
                direction = 'SELL'
            else:
                direction = 'HOLD'

            confidence = 50 + abs(price_change_pct) * 5

            return {
                'direction': direction,
                'confidence': round(min(confidence, 85), 1),
                'predicted_price': round(final_price, 2),
                'target_price': round(final_price, 2),
                'stop_loss': round(initial_price * (0.985 if direction == 'BUY' else 1.015), 2),
                'price_change_pct': round(price_change_pct, 2),
                'predicted_candles': predicted_candles,
                'scenario_probabilities': {
                    'bullish': round(probabilities['bullish'] * 100, 1),
                    'bearish': round(probabilities['bearish'] * 100, 1),
                    'neutral': round(probabilities['neutral'] * 100, 1),
                },
                'timestamp': datetime.utcnow().isoformat(),
                'model_type': 'simulation'
            }

        except Exception as e:
            logger.error(f'Error in fallback prediction: {e}')
            return self._default_prediction()


class LSTMPredictor:
    """
    LSTM Neural Network for price prediction

    This is a placeholder class structure for actual LSTM implementation.
    Would require TensorFlow/Keras in production.
    """

    def __init__(self, lookback=60, features=5):
        self.lookback = lookback
        self.features = features
        self.model = None

    def build_model(self):
        """Build LSTM model architecture"""
        # Placeholder - would use TensorFlow/Keras
        logger.info('Building LSTM model...')
        pass

    def train(self, X_train, y_train, epochs=50, batch_size=32):
        """Train the LSTM model"""
        # Placeholder - would use TensorFlow/Keras
        logger.info('Training LSTM model...')
        pass

    def predict(self, X):
        """Make predictions"""
        # Placeholder - would use TensorFlow/Keras
        logger.info('Making LSTM predictions...')
        return np.random.random((len(X), 1))


class RandomForestPredictor:
    """
    Random Forest classifier for signal generation

    This is a placeholder class structure for actual RF implementation.
    Would require scikit-learn in production.
    """

    def __init__(self, n_estimators=100):
        self.n_estimators = n_estimators
        self.model = None

    def train(self, X_train, y_train):
        """Train Random Forest model"""
        # Placeholder - would use sklearn
        logger.info('Training Random Forest model...')
        pass

    def predict(self, X):
        """Make predictions"""
        # Placeholder - would use sklearn
        logger.info('Making Random Forest predictions...')
        return np.random.choice(['BUY', 'SELL', 'HOLD'], size=len(X))

    def get_feature_importance(self):
        """Get feature importances"""
        # Placeholder
        return {}
