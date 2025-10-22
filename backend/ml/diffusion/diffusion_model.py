import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import logging
from datetime import datetime
from typing import List, Dict, Optional
from .time_series_diffusion import TimeSeriesDiffusion
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from simulation.virtual_economy import VirtualEconomy

logger = logging.getLogger(__name__)


class DiffusionForecaster:
    """
    Main diffusion forecaster integrating virtual economy simulation
    with diffusion models for forex/crypto prediction
    """

    def __init__(
        self,
        lookback_window=60,
        forecast_horizon=10,
        num_traders=100,
        device='cpu'
    ):
        self.lookback_window = lookback_window
        self.forecast_horizon = forecast_horizon
        self.num_traders = num_traders
        self.device = torch.device(device)

        self.model = TimeSeriesDiffusion(
            input_dim=5,
            hidden_dim=128,
            num_layers=4,
            num_timesteps=1000,
            lookback_window=lookback_window,
            forecast_horizon=forecast_horizon
        ).to(self.device)

        self.optimizer = None
        self.is_trained = False
        self.training_history = []

        self.feature_mean = None
        self.feature_std = None

        logger.info('DiffusionForecaster initialized')

    def preprocess_data(self, data):
        """
        Preprocess OHLCV data for the model

        Args:
            data: DataFrame or dict with OHLCV data

        Returns:
            Normalized numpy array
        """
        if isinstance(data, dict):
            df = pd.DataFrame(data)
        else:
            df = data.copy()

        required_cols = ['open', 'high', 'low', 'close', 'volume']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f'Missing required column: {col}')

        features = df[required_cols].values.astype(np.float32)

        if self.feature_mean is None:
            self.feature_mean = np.mean(features, axis=0)
            self.feature_std = np.std(features, axis=0) + 1e-8

        normalized = (features - self.feature_mean) / self.feature_std

        return normalized

    def prepare_training_data(self, historical_data):
        """
        Prepare training sequences from historical data

        Returns:
            Tuple of (condition_sequences, target_sequences)
        """
        normalized = self.preprocess_data(historical_data)

        if len(normalized) < self.lookback_window + self.forecast_horizon:
            raise ValueError(f'Insufficient data: need at least {self.lookback_window + self.forecast_horizon} samples')

        conditions = []
        targets = []

        for i in range(len(normalized) - self.lookback_window - self.forecast_horizon + 1):
            condition = normalized[i:i + self.lookback_window]
            target = normalized[i + self.lookback_window:i + self.lookback_window + self.forecast_horizon]

            conditions.append(condition)
            targets.append(target)

        return np.array(conditions), np.array(targets)

    def train(
        self,
        historical_data,
        epochs=100,
        batch_size=32,
        learning_rate=1e-4,
        use_simulation=True
    ):
        """
        Train the diffusion model

        Args:
            historical_data: Historical OHLCV data
            epochs: Number of training epochs
            batch_size: Batch size
            learning_rate: Learning rate
            use_simulation: Whether to augment with simulation data

        Returns:
            Training history
        """
        logger.info(f'Starting training for {epochs} epochs')

        conditions, targets = self.prepare_training_data(historical_data)

        if use_simulation:
            logger.info('Augmenting training data with virtual economy simulations')
            sim_conditions, sim_targets = self._generate_simulation_data(
                historical_data,
                num_simulations=10
            )
            conditions = np.concatenate([conditions, sim_conditions], axis=0)
            targets = np.concatenate([targets, sim_targets], axis=0)

        self.optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=learning_rate,
            weight_decay=0.01
        )

        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer,
            T_max=epochs
        )

        conditions_tensor = torch.tensor(conditions, dtype=torch.float32).to(self.device)
        targets_tensor = torch.tensor(targets, dtype=torch.float32).to(self.device)

        dataset = torch.utils.data.TensorDataset(conditions_tensor, targets_tensor)
        dataloader = torch.utils.data.DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=True
        )

        self.model.train()
        for epoch in range(epochs):
            epoch_loss = 0
            num_batches = 0

            for batch_conditions, batch_targets in dataloader:
                self.optimizer.zero_grad()

                loss = self.model.compute_loss(batch_targets, batch_conditions)

                loss.backward()

                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)

                self.optimizer.step()

                epoch_loss += loss.item()
                num_batches += 1

            avg_loss = epoch_loss / num_batches
            self.training_history.append(avg_loss)

            scheduler.step()

            if (epoch + 1) % 10 == 0:
                logger.info(f'Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.6f}')

        self.is_trained = True
        logger.info('Training completed')

        return self.training_history

    def _generate_simulation_data(self, historical_data, num_simulations=10):
        """Generate synthetic training data using virtual economy"""
        all_conditions = []
        all_targets = []

        for sim_id in range(num_simulations):
            if isinstance(historical_data, dict):
                df = pd.DataFrame(historical_data)
            else:
                df = historical_data.copy()

            initial_price = df['close'].iloc[-1]

            economy = VirtualEconomy(
                num_traders=self.num_traders,
                initial_price=initial_price,
                historical_data=df,
                simulation_steps=self.forecast_horizon + self.lookback_window
            )

            economy.run_simulation()

            sim_prices = economy.datacollector_data['prices']

            if len(sim_prices) < self.lookback_window + self.forecast_horizon:
                continue

            sim_ohlcv = self._reconstruct_ohlcv_from_prices(sim_prices)

            normalized = self.preprocess_data(sim_ohlcv)

            for i in range(len(normalized) - self.lookback_window - self.forecast_horizon + 1):
                condition = normalized[i:i + self.lookback_window]
                target = normalized[i + self.lookback_window:i + self.lookback_window + self.forecast_horizon]

                all_conditions.append(condition)
                all_targets.append(target)

        return np.array(all_conditions), np.array(all_targets)

    def _reconstruct_ohlcv_from_prices(self, prices):
        """Reconstruct OHLCV from price series"""
        ohlcv = []

        for i in range(len(prices)):
            variation = np.random.uniform(0.001, 0.003)

            ohlcv.append({
                'open': prices[i] * (1 - variation / 2),
                'high': prices[i] * (1 + variation),
                'low': prices[i] * (1 - variation),
                'close': prices[i],
                'volume': np.random.uniform(100000, 500000)
            })

        return pd.DataFrame(ohlcv)

    @torch.no_grad()
    def predict(self, historical_data, num_samples=5):
        """
        Generate forecast using the trained model

        Args:
            historical_data: Recent historical OHLCV data
            num_samples: Number of forecast samples to generate

        Returns:
            Dictionary with predictions and confidence
        """
        if not self.is_trained:
            logger.warning('Model not trained, using simulation-based prediction')
            return self._simulation_based_prediction(historical_data)

        self.model.eval()

        if isinstance(historical_data, dict):
            df = pd.DataFrame(historical_data)
        else:
            df = historical_data.copy()

        if len(df) < self.lookback_window:
            raise ValueError(f'Need at least {self.lookback_window} historical samples')

        recent_data = df.iloc[-self.lookback_window:]
        normalized_condition = self.preprocess_data(recent_data)

        condition_tensor = torch.tensor(
            normalized_condition,
            dtype=torch.float32
        ).unsqueeze(0).to(self.device)

        condition_batch = condition_tensor.repeat(num_samples, 1, 1)

        forecasts = []
        for _ in range(num_samples):
            forecast = self.model.p_sample_loop(
                condition_batch,
                shape=(num_samples, self.forecast_horizon, 5)
            )

            forecast_np = forecast.cpu().numpy()

            forecast_denorm = forecast_np * self.feature_std + self.feature_mean

            forecasts.append(forecast_denorm)

        forecasts = np.array(forecasts)

        mean_forecast = np.mean(forecasts, axis=0)
        std_forecast = np.std(forecasts, axis=0)

        predicted_candles = []
        for i in range(self.forecast_horizon):
            candle_mean = mean_forecast[0, i]
            candle_std = std_forecast[0, i]

            confidence = 1.0 - np.mean(candle_std / (np.abs(candle_mean) + 1e-8))
            confidence = np.clip(confidence, 0.0, 1.0)

            predicted_candles.append({
                'open': float(candle_mean[0]),
                'high': float(candle_mean[1]),
                'low': float(candle_mean[2]),
                'close': float(candle_mean[3]),
                'volume': float(candle_mean[4]),
                'confidence': float(confidence)
            })

        return {
            'candles': predicted_candles,
            'mean_forecast': mean_forecast[0],
            'std_forecast': std_forecast[0],
            'timestamp': datetime.utcnow().isoformat()
        }

    def _simulation_based_prediction(self, historical_data):
        """Fallback prediction using only simulation"""
        if isinstance(historical_data, dict):
            df = pd.DataFrame(historical_data)
        else:
            df = historical_data.copy()

        initial_price = df['close'].iloc[-1]

        economy = VirtualEconomy(
            num_traders=self.num_traders,
            initial_price=initial_price,
            historical_data=df,
            simulation_steps=self.forecast_horizon
        )

        predicted_candles = economy.predict_next_candles(
            num_candles=self.forecast_horizon,
            scenario_count=5
        )

        return {
            'candles': predicted_candles,
            'timestamp': datetime.utcnow().isoformat()
        }

    def save_model(self, path):
        """Save model checkpoint"""
        checkpoint = {
            'model_state_dict': self.model.state_dict(),
            'feature_mean': self.feature_mean,
            'feature_std': self.feature_std,
            'lookback_window': self.lookback_window,
            'forecast_horizon': self.forecast_horizon,
            'is_trained': self.is_trained,
            'training_history': self.training_history
        }

        torch.save(checkpoint, path)
        logger.info(f'Model saved to {path}')

    def load_model(self, path):
        """Load model checkpoint"""
        checkpoint = torch.load(path, map_location=self.device)

        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.feature_mean = checkpoint['feature_mean']
        self.feature_std = checkpoint['feature_std']
        self.is_trained = checkpoint['is_trained']
        self.training_history = checkpoint.get('training_history', [])

        logger.info(f'Model loaded from {path}')
