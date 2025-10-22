from flask import Blueprint, jsonify, request
from services.market_service import MarketService
import logging

logger = logging.getLogger(__name__)
market_bp = Blueprint('market', __name__)
market_service = MarketService()

@market_bp.route('/price/<symbol>', methods=['GET'])
def get_price(symbol):
    """Get current price for a symbol"""
    try:
        price_data = market_service.get_current_price(symbol)
        return jsonify(price_data)
    except Exception as e:
        logger.error(f'Error fetching price for {symbol}: {e}')
        return jsonify({'error': str(e)}), 500

@market_bp.route('/prices', methods=['POST'])
def get_multiple_prices():
    """Get current prices for multiple symbols"""
    try:
        data = request.json
        symbols = data.get('symbols', [])
        prices = market_service.get_multiple_prices(symbols)
        return jsonify(prices)
    except Exception as e:
        logger.error(f'Error fetching multiple prices: {e}')
        return jsonify({'error': str(e)}), 500

@market_bp.route('/history/<symbol>', methods=['GET'])
def get_historical_data(symbol):
    """Get historical price data"""
    try:
        timeframe = request.args.get('timeframe', '1h')
        limit = int(request.args.get('limit', 100))

        history = market_service.get_historical_data(symbol, timeframe, limit)
        return jsonify(history)
    except Exception as e:
        logger.error(f'Error fetching history for {symbol}: {e}')
        return jsonify({'error': str(e)}), 500

@market_bp.route('/indicators/<symbol>', methods=['GET'])
def get_technical_indicators(symbol):
    """Get technical indicators for a symbol"""
    try:
        indicators = market_service.calculate_indicators(symbol)
        return jsonify(indicators)
    except Exception as e:
        logger.error(f'Error calculating indicators for {symbol}: {e}')
        return jsonify({'error': str(e)}), 500

@market_bp.route('/supported-assets', methods=['GET'])
def get_supported_assets():
    """Get list of supported trading pairs"""
    try:
        assets = market_service.get_supported_assets()
        return jsonify(assets)
    except Exception as e:
        logger.error(f'Error fetching supported assets: {e}')
        return jsonify({'error': str(e)}), 500
