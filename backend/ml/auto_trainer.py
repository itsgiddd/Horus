import logging
import schedule
import time
import threading
import os
from datetime import datetime
from ml.diffusion.diffusion_model import DiffusionForecaster
from services.market_service import MarketService
import pandas as pd

logger = logging.getLogger(__name__)


class AutoTrainer:
    """
    Automatic model training system

    Continuously fetches new data from APIs and retrains the diffusion model
    to keep predictions accurate and up-to-date.
    """

    def __init__(self, training_interval_hours=24):
        self.training_interval_hours = training_interval_hours
        self.market_service = MarketService()
        self.forecaster = None
        self.is_running = False
        self.training_thread = None

        self.symbols_to_train = ['BTC', 'ETH', 'EUR/USD', 'GBP/USD']

        self.model_save_dir = os.path.join(
            os.path.dirname(__file__),
            '../../models'
        )
        os.makedirs(self.model_save_dir, exist_ok=True)

        logger.info(f'AutoTrainer initialized: will train every {training_interval_hours} hours')

    def start(self):
        """Start the automatic training scheduler"""
        if self.is_running:
            logger.warning('AutoTrainer already running')
            return

        self.is_running = True

        schedule.every(self.training_interval_hours).hours.do(self.train_all_models)

        schedule.every().day.at("02:00").do(self.train_all_models)

        self.training_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.training_thread.start()

        logger.info('AutoTrainer started successfully')

        self.train_all_models()

    def stop(self):
        """Stop the automatic training scheduler"""
        self.is_running = False
        schedule.clear()
        logger.info('AutoTrainer stopped')

    def _run_scheduler(self):
        """Internal scheduler loop"""
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)

    def train_all_models(self):
        """Train models for all configured symbols"""
        logger.info('Starting scheduled training for all symbols')

        for symbol in self.symbols_to_train:
            try:
                self.train_model_for_symbol(symbol)
            except Exception as e:
                logger.error(f'Error training model for {symbol}: {e}')

        logger.info('Scheduled training completed for all symbols')

    def train_model_for_symbol(self, symbol, epochs=50, batch_size=16):
        """
        Train diffusion model for a specific symbol using fresh API data

        Args:
            symbol: Trading symbol (e.g., 'BTC', 'EUR/USD')
            epochs: Number of training epochs
            batch_size: Training batch size

        Returns:
            Training history
        """
        logger.info(f'Training model for {symbol}')

        try:
            historical_data = self.market_service.get_historical_data(
                symbol,
                timeframe='1h',
                limit=1000
            )

            if not historical_data or len(historical_data) < 100:
                logger.warning(f'Insufficient data for {symbol}: {len(historical_data) if historical_data else 0} candles')
                return None

            df = pd.DataFrame(historical_data)

            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

            logger.info(f'Fetched {len(df)} candles for {symbol}')

            self.forecaster = DiffusionForecaster(
                lookback_window=60,
                forecast_horizon=10,
                num_traders=100
            )

            history = self.forecaster.train(
                historical_data=df,
                epochs=epochs,
                batch_size=batch_size,
                learning_rate=1e-4,
                use_simulation=True
            )

            model_path = os.path.join(
                self.model_save_dir,
                f'diffusion_{symbol.replace("/", "_")}.pt'
            )
            self.forecaster.save_model(model_path)

            logger.info(f'Model trained and saved for {symbol} at {model_path}')
            logger.info(f'Final training loss: {history[-1]:.6f}')

            self._save_training_metadata(symbol, len(df), epochs, history[-1])

            return history

        except Exception as e:
            logger.error(f'Error training model for {symbol}: {e}', exc_info=True)
            return None

    def _save_training_metadata(self, symbol, data_points, epochs, final_loss):
        """Save training metadata for tracking"""
        metadata = {
            'symbol': symbol,
            'trained_at': datetime.utcnow().isoformat(),
            'data_points': data_points,
            'epochs': epochs,
            'final_loss': final_loss
        }

        metadata_path = os.path.join(
            self.model_save_dir,
            f'metadata_{symbol.replace("/", "_")}.json'
        )

        import json
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        logger.info(f'Training metadata saved for {symbol}')

    def load_trained_model(self, symbol):
        """Load a previously trained model"""
        model_path = os.path.join(
            self.model_save_dir,
            f'diffusion_{symbol.replace("/", "_")}.pt'
        )

        if not os.path.exists(model_path):
            logger.warning(f'No trained model found for {symbol}')
            return None

        forecaster = DiffusionForecaster(
            lookback_window=60,
            forecast_horizon=10,
            num_traders=100
        )

        try:
            forecaster.load_model(model_path)
            logger.info(f'Loaded trained model for {symbol}')
            return forecaster
        except Exception as e:
            logger.error(f'Error loading model for {symbol}: {e}')
            return None

    def get_training_status(self):
        """Get current training status and schedule"""
        status = {
            'is_running': self.is_running,
            'training_interval_hours': self.training_interval_hours,
            'symbols': self.symbols_to_train,
            'next_run': None,
            'trained_models': []
        }

        if self.is_running and schedule.jobs:
            next_job = schedule.next_run()
            status['next_run'] = next_job.isoformat() if next_job else None

        for symbol in self.symbols_to_train:
            model_path = os.path.join(
                self.model_save_dir,
                f'diffusion_{symbol.replace("/", "_")}.pt'
            )
            metadata_path = os.path.join(
                self.model_save_dir,
                f'metadata_{symbol.replace("/", "_")}.json'
            )

            if os.path.exists(model_path):
                model_info = {'symbol': symbol, 'model_exists': True}

                if os.path.exists(metadata_path):
                    import json
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                        model_info.update(metadata)

                status['trained_models'].append(model_info)

        return status

    def add_symbol(self, symbol):
        """Add a symbol to the training schedule"""
        if symbol not in self.symbols_to_train:
            self.symbols_to_train.append(symbol)
            logger.info(f'Added {symbol} to training schedule')

    def remove_symbol(self, symbol):
        """Remove a symbol from the training schedule"""
        if symbol in self.symbols_to_train:
            self.symbols_to_train.remove(symbol)
            logger.info(f'Removed {symbol} from training schedule')
