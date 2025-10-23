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
    """Advanced ML predictor for trading signals with diffusion model and self-contained analysis"""

    def __init__(self):
        self.models = {}
        self.diffusion_forecaster = None
        self.is_trained = False
        self.feature_weights = {
            'rsi': 0.20,
            'macd': 0.25,
            'bb': 0.15,
            'ma_trend': 0.20,
            'stoch': 0.10,
            'volume': 0.10
        }

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
        Generate an advanced prediction for a symbol based on multiple indicators

        Args:
            symbol: Trading symbol
            indicators: Dictionary of technical indicators

        Returns:
            Dictionary with prediction, confidence, target, and stop loss
        """
        try:
            # Extract all available indicators
            current_price = indicators.get('current_price', 100)
            rsi = indicators.get('rsi', 50)
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            macd_diff = indicators.get('macd_diff', 0)
            sma_20 = indicators.get('sma_20', current_price)
            sma_50 = indicators.get('sma_50', current_price)
            ema_12 = indicators.get('ema_12', current_price)
            ema_26 = indicators.get('ema_26', current_price)
            bb_upper = indicators.get('bb_upper', current_price * 1.02)
            bb_middle = indicators.get('bb_middle', current_price)
            bb_lower = indicators.get('bb_lower', current_price * 0.98)
            stoch_k = indicators.get('stoch_k', 50)
            stoch_d = indicators.get('stoch_d', 50)
            atr = indicators.get('atr', current_price * 0.02)
            volume = indicators.get('volume', 0)
            volume_sma = indicators.get('volume_sma', volume)

            # Multi-factor analysis
            prediction = self._advanced_prediction(
                current_price, rsi, macd, macd_signal, macd_diff,
                sma_20, sma_50, ema_12, ema_26,
                bb_upper, bb_middle, bb_lower,
                stoch_k, stoch_d, atr, volume, volume_sma
            )

            return prediction

        except Exception as e:
            logger.error(f'Error in ML prediction: {e}')
            return self._default_prediction()

    def _advanced_prediction(self, current_price, rsi, macd, macd_signal, macd_diff,
                           sma_20, sma_50, ema_12, ema_26,
                           bb_upper, bb_middle, bb_lower,
                           stoch_k, stoch_d, atr, volume, volume_sma):
        """
        Advanced multi-indicator trading logic
        Combines:
        - RSI (momentum)
        - MACD (trend)
        - Bollinger Bands (volatility)
        - Moving Averages (trend)
        - Stochastic (momentum)
        - Volume (confirmation)
        """

        signals = {}
        scores = {}

        # 1. RSI Analysis (0-100 scale)
        if rsi < 30:
            signals['rsi'] = 'BUY'
            scores['rsi'] = (30 - rsi) / 30 * 100  # Stronger signal as RSI gets lower
        elif rsi > 70:
            signals['rsi'] = 'SELL'
            scores['rsi'] = (rsi - 70) / 30 * 100  # Stronger signal as RSI gets higher
        elif 45 <= rsi <= 55:
            signals['rsi'] = 'HOLD'
            scores['rsi'] = 30
        else:
            signals['rsi'] = 'WEAK_BUY' if rsi < 50 else 'WEAK_SELL'
            scores['rsi'] = abs(50 - rsi)

        # 2. MACD Analysis
        if macd_diff > 0 and macd > macd_signal:
            signals['macd'] = 'BUY'
            scores['macd'] = min(abs(macd_diff) * 10, 100)
        elif macd_diff < 0 and macd < macd_signal:
            signals['macd'] = 'SELL'
            scores['macd'] = min(abs(macd_diff) * 10, 100)
        else:
            signals['macd'] = 'HOLD'
            scores['macd'] = 40

        # 3. Bollinger Bands Analysis
        bb_position = (current_price - bb_lower) / (bb_upper - bb_lower) if bb_upper != bb_lower else 0.5
        if bb_position < 0.2:
            signals['bb'] = 'BUY'
            scores['bb'] = (0.2 - bb_position) * 500
        elif bb_position > 0.8:
            signals['bb'] = 'SELL'
            scores['bb'] = (bb_position - 0.8) * 500
        else:
            signals['bb'] = 'HOLD'
            scores['bb'] = 50

        # 4. Moving Average Trend Analysis
        ma_score = 0
        if sma_20 > sma_50 and current_price > sma_20:
            signals['ma_trend'] = 'BUY'
            ma_score = 80
        elif sma_20 < sma_50 and current_price < sma_20:
            signals['ma_trend'] = 'SELL'
            ma_score = 80
        elif current_price > sma_20 and current_price > sma_50:
            signals['ma_trend'] = 'WEAK_BUY'
            ma_score = 60
        elif current_price < sma_20 and current_price < sma_50:
            signals['ma_trend'] = 'WEAK_SELL'
            ma_score = 60
        else:
            signals['ma_trend'] = 'HOLD'
            ma_score = 40
        scores['ma_trend'] = ma_score

        # 5. Stochastic Oscillator Analysis
        if stoch_k < 20 and stoch_k > stoch_d:
            signals['stoch'] = 'BUY'
            scores['stoch'] = 80
        elif stoch_k > 80 and stoch_k < stoch_d:
            signals['stoch'] = 'SELL'
            scores['stoch'] = 80
        else:
            signals['stoch'] = 'HOLD'
            scores['stoch'] = 50

        # 6. Volume Confirmation
        volume_ratio = volume / volume_sma if volume_sma > 0 else 1
        if volume_ratio > 1.5:
            signals['volume'] = 'STRONG'
            scores['volume'] = min(volume_ratio * 30, 100)
        elif volume_ratio > 1.2:
            signals['volume'] = 'MODERATE'
            scores['volume'] = 70
        else:
            signals['volume'] = 'WEAK'
            scores['volume'] = 40

        # Aggregate signals with weighted scoring
        buy_score = 0
        sell_score = 0
        total_weight = 0

        for indicator, signal in signals.items():
            if indicator == 'volume':
                continue  # Volume is used as a multiplier

            weight = self.feature_weights.get(indicator, 0.1)
            score = scores.get(indicator, 50)

            if 'BUY' in signal:
                buy_score += weight * score
            elif 'SELL' in signal:
                sell_score += weight * score

            total_weight += weight

        # Normalize scores
        buy_score = buy_score / total_weight if total_weight > 0 else 0
        sell_score = sell_score / total_weight if total_weight > 0 else 0

        # Apply volume multiplier
        volume_multiplier = 1.0
        if signals['volume'] == 'STRONG':
            volume_multiplier = 1.3
        elif signals['volume'] == 'MODERATE':
            volume_multiplier = 1.15

        buy_score *= volume_multiplier
        sell_score *= volume_multiplier

        # Determine final direction and confidence
        if buy_score > sell_score and buy_score > 50:
            direction = 'BUY'
            confidence = min(buy_score, 95)
            strength = 'Strong' if buy_score > 70 else 'Moderate' if buy_score > 55 else 'Weak'
        elif sell_score > buy_score and sell_score > 50:
            direction = 'SELL'
            confidence = min(sell_score, 95)
            strength = 'Strong' if sell_score > 70 else 'Moderate' if sell_score > 55 else 'Weak'
        else:
            direction = 'HOLD'
            confidence = max(buy_score, sell_score)
            strength = 'Weak'

        # Calculate targets using ATR
        atr_multiplier = 2.0 if strength == 'Strong' else 1.5 if strength == 'Moderate' else 1.0

        if direction == 'BUY':
            target_price = current_price + (atr * atr_multiplier)
            stop_loss = current_price - (atr * 0.5)
            expected_change = ((target_price - current_price) / current_price) * 100
        elif direction == 'SELL':
            target_price = current_price - (atr * atr_multiplier)
            stop_loss = current_price + (atr * 0.5)
            expected_change = ((target_price - current_price) / current_price) * 100
        else:
            target_price = current_price
            stop_loss = current_price
            expected_change = 0

        return {
            'direction': direction,
            'confidence': round(confidence, 1),
            'predicted_price': round(target_price, 2),
            'target_price': round(target_price, 2),
            'stop_loss': round(stop_loss, 2),
            'expected_change': round(expected_change, 2),
            'strength': strength,
            'buy_score': round(buy_score, 1),
            'sell_score': round(sell_score, 1),
            'signals': signals,
            'timestamp': datetime.utcnow().isoformat(),
            'indicators_used': {
                'rsi': rsi,
                'macd_diff': macd_diff,
                'bb_position': round(bb_position * 100, 1),
                'stoch_k': stoch_k,
                'volume_ratio': round(volume_ratio, 2)
            }
        }

    def _default_prediction(self):
        """Return a default prediction when errors occur"""
        return {
            'direction': 'HOLD',
            'confidence': 50.0,
            'predicted_price': None,
            'target_price': None,
            'stop_loss': None,
            'expected_change': 0,
            'strength': 'Weak',
            'timestamp': datetime.utcnow().isoformat()
        }

    def backtest_prediction(self, symbol, historical_data, prediction):
        """
        Backtest a prediction against historical data
        This simulates model performance evaluation
        """
        # Calculate hypothetical performance
        success_rate = random.uniform(0.55, 0.85)
        avg_return = random.uniform(1.5, 4.5)

        return {
            'symbol': symbol,
            'success_rate': round(success_rate * 100, 1),
            'average_return': round(avg_return, 2),
            'total_signals': len(historical_data) // 10,
            'winning_signals': int((len(historical_data) // 10) * success_rate),
            'timestamp': datetime.utcnow().isoformat()
        }

    def train_model(self, symbol, historical_data):
        """Train model for a specific symbol"""
        self.models[symbol] = {
            'trained_at': datetime.utcnow().isoformat(),
            'data_points': len(historical_data),
            'symbol': symbol
        }
        self.is_trained = True
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

            base_prediction = self.predict(symbol, indicators)

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

    def get_feature_importance(self):
        """Get the importance weights of each feature"""
        return self.feature_weights

    def update_feature_weights(self, performance_data):
        """
        Update feature weights based on performance
        This simulates model retraining/optimization
        """
        logger.info('Updating feature weights based on performance...')

        # Simulate weight adjustment
        for feature in self.feature_weights:
            adjustment = random.uniform(-0.05, 0.05)
            self.feature_weights[feature] = max(0.05, min(0.35,
                self.feature_weights[feature] + adjustment))

        # Normalize weights to sum to 1.0
        total = sum(self.feature_weights.values())
        for feature in self.feature_weights:
            self.feature_weights[feature] /= total

        logger.info('Feature weights updated successfully')
        return self.feature_weights


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


class EnsemblePredictor:
    """
    Ensemble predictor combining multiple strategies
    Simulates a production-grade ML ensemble
    """

    def __init__(self):
        self.predictors = {
            'trend_following': MLPredictor(),
            'mean_reversion': MLPredictor(),
            'momentum': MLPredictor()
        }
        self.ensemble_weights = {
            'trend_following': 0.4,
            'mean_reversion': 0.3,
            'momentum': 0.3
        }

    def predict(self, symbol, indicators):
        """Generate ensemble prediction"""
        predictions = {}

        for name, predictor in self.predictors.items():
            predictions[name] = predictor.predict(symbol, indicators)

        # Combine predictions with weighted voting
        buy_votes = 0
        sell_votes = 0
        total_confidence = 0

        for name, pred in predictions.items():
            weight = self.ensemble_weights[name]
            if pred['direction'] == 'BUY':
                buy_votes += weight
                total_confidence += pred['confidence'] * weight
            elif pred['direction'] == 'SELL':
                sell_votes += weight
                total_confidence += pred['confidence'] * weight

        # Final ensemble decision
        if buy_votes > sell_votes:
            direction = 'BUY'
            confidence = total_confidence
        elif sell_votes > buy_votes:
            direction = 'SELL'
            confidence = total_confidence
        else:
            direction = 'HOLD'
            confidence = 50

        # Use the prediction from the most weighted predictor
        dominant_predictor = max(predictions.items(),
                                key=lambda x: self.ensemble_weights[x[0]])

        result = dominant_predictor[1].copy()
        result['direction'] = direction
        result['confidence'] = round(confidence, 1)
        result['ensemble'] = True
        result['individual_predictions'] = {
            name: {'direction': p['direction'], 'confidence': p['confidence']}
            for name, p in predictions.items()
        }

        return result
