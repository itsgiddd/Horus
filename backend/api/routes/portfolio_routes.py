from flask import Blueprint, jsonify, request
from services.portfolio_service import PortfolioService
import logging

logger = logging.getLogger(__name__)
portfolio_bp = Blueprint('portfolio', __name__)
portfolio_service = PortfolioService()

@portfolio_bp.route('/summary', methods=['GET'])
def get_portfolio_summary():
    """Get portfolio summary"""
    try:
        summary = portfolio_service.get_portfolio_summary()
        return jsonify(summary)
    except Exception as e:
        logger.error(f'Error fetching portfolio summary: {e}')
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/positions', methods=['GET'])
def get_positions():
    """Get all portfolio positions"""
    try:
        positions = portfolio_service.get_positions()
        return jsonify(positions)
    except Exception as e:
        logger.error(f'Error fetching positions: {e}')
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/risk-metrics', methods=['GET'])
def get_risk_metrics():
    """Get portfolio risk metrics"""
    try:
        metrics = portfolio_service.calculate_risk_metrics()
        return jsonify(metrics)
    except Exception as e:
        logger.error(f'Error calculating risk metrics: {e}')
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/performance', methods=['GET'])
def get_performance():
    """Get portfolio performance over time"""
    try:
        timeframe = request.args.get('timeframe', '30d')
        performance = portfolio_service.get_performance(timeframe)
        return jsonify(performance)
    except Exception as e:
        logger.error(f'Error fetching performance: {e}')
        return jsonify({'error': str(e)}), 500
