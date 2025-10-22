from flask import Blueprint, jsonify, request
from services.signal_service import SignalService
import logging

logger = logging.getLogger(__name__)
signals_bp = Blueprint('signals', __name__)
signal_service = SignalService()

@signals_bp.route('/current', methods=['GET'])
def get_current_signals():
    """Get current trading signals for all monitored assets"""
    try:
        signals = signal_service.get_current_signals()
        return jsonify(signals)
    except Exception as e:
        logger.error(f'Error fetching current signals: {e}')
        return jsonify({'error': str(e)}), 500

@signals_bp.route('/generate/<symbol>', methods=['POST'])
def generate_signal(symbol):
    """Generate a new signal for a specific symbol"""
    try:
        signal = signal_service.generate_signal(symbol)
        return jsonify(signal)
    except Exception as e:
        logger.error(f'Error generating signal for {symbol}: {e}')
        return jsonify({'error': str(e)}), 500

@signals_bp.route('/history', methods=['GET'])
def get_signal_history():
    """Get historical signals"""
    try:
        limit = int(request.args.get('limit', 50))
        history = signal_service.get_signal_history(limit)
        return jsonify(history)
    except Exception as e:
        logger.error(f'Error fetching signal history: {e}')
        return jsonify({'error': str(e)}), 500

@signals_bp.route('/performance', methods=['GET'])
def get_signal_performance():
    """Get signal performance metrics"""
    try:
        performance = signal_service.get_performance_metrics()
        return jsonify(performance)
    except Exception as e:
        logger.error(f'Error fetching signal performance: {e}')
        return jsonify({'error': str(e)}), 500
