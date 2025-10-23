from flask import Blueprint, jsonify, request
from ml.auto_trainer import AutoTrainer
import logging

logger = logging.getLogger(__name__)
training_bp = Blueprint('training', __name__)

auto_trainer = AutoTrainer(training_interval_hours=24)

@training_bp.route('/start', methods=['POST'])
def start_auto_training():
    """Start automatic model training"""
    try:
        auto_trainer.start()
        return jsonify({
            'status': 'success',
            'message': 'Auto-training started',
            'training_status': auto_trainer.get_training_status()
        })
    except Exception as e:
        logger.error(f'Error starting auto-training: {e}')
        return jsonify({'error': str(e)}), 500

@training_bp.route('/stop', methods=['POST'])
def stop_auto_training():
    """Stop automatic model training"""
    try:
        auto_trainer.stop()
        return jsonify({
            'status': 'success',
            'message': 'Auto-training stopped'
        })
    except Exception as e:
        logger.error(f'Error stopping auto-training: {e}')
        return jsonify({'error': str(e)}), 500

@training_bp.route('/status', methods=['GET'])
def get_training_status():
    """Get current training status"""
    try:
        status = auto_trainer.get_training_status()
        return jsonify(status)
    except Exception as e:
        logger.error(f'Error getting training status: {e}')
        return jsonify({'error': str(e)}), 500

@training_bp.route('/train/<symbol>', methods=['POST'])
def train_symbol(symbol):
    """Manually trigger training for a specific symbol"""
    try:
        epochs = int(request.args.get('epochs', 50))
        batch_size = int(request.args.get('batch_size', 16))

        history = auto_trainer.train_model_for_symbol(symbol, epochs, batch_size)

        if history is None:
            return jsonify({'error': 'Training failed'}), 500

        return jsonify({
            'status': 'success',
            'symbol': symbol,
            'epochs': epochs,
            'final_loss': history[-1] if history else None,
            'message': f'Model trained successfully for {symbol}'
        })
    except Exception as e:
        logger.error(f'Error training {symbol}: {e}')
        return jsonify({'error': str(e)}), 500

@training_bp.route('/symbols', methods=['GET'])
def get_training_symbols():
    """Get list of symbols being trained"""
    try:
        return jsonify({
            'symbols': auto_trainer.symbols_to_train
        })
    except Exception as e:
        logger.error(f'Error getting symbols: {e}')
        return jsonify({'error': str(e)}), 500

@training_bp.route('/symbols/add', methods=['POST'])
def add_training_symbol():
    """Add a symbol to training schedule"""
    try:
        data = request.get_json()
        symbol = data.get('symbol')

        if not symbol:
            return jsonify({'error': 'Symbol required'}), 400

        auto_trainer.add_symbol(symbol)

        return jsonify({
            'status': 'success',
            'message': f'Added {symbol} to training schedule',
            'symbols': auto_trainer.symbols_to_train
        })
    except Exception as e:
        logger.error(f'Error adding symbol: {e}')
        return jsonify({'error': str(e)}), 500

@training_bp.route('/symbols/remove', methods=['POST'])
def remove_training_symbol():
    """Remove a symbol from training schedule"""
    try:
        data = request.get_json()
        symbol = data.get('symbol')

        if not symbol:
            return jsonify({'error': 'Symbol required'}), 400

        auto_trainer.remove_symbol(symbol)

        return jsonify({
            'status': 'success',
            'message': f'Removed {symbol} from training schedule',
            'symbols': auto_trainer.symbols_to_train
        })
    except Exception as e:
        logger.error(f'Error removing symbol: {e}')
        return jsonify({'error': str(e)}), 500
