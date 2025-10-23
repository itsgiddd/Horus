from flask import Blueprint, jsonify, request
from services.signal_service import SignalService
from services.market_service import MarketService
from ml.patterns.pattern_detector import PatternDetector
from ml.trading_anarchy import TradingAnarchyAnalyzer
from ml.predictor import MLPredictor
import logging

logger = logging.getLogger(__name__)
signals_bp = Blueprint('signals', __name__)
signal_service = SignalService()
market_service = MarketService()
pattern_detector = PatternDetector()
anarchy_analyzer = TradingAnarchyAnalyzer()
ml_predictor = MLPredictor()

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

@signals_bp.route('/patterns/<symbol>', methods=['GET'])
def detect_patterns(symbol):
    """Detect chart patterns for a symbol"""
    try:
        timeframe = request.args.get('timeframe', '1h')
        limit = int(request.args.get('limit', 100))

        historical_data = market_service.get_historical_data(symbol, timeframe, limit)

        if not historical_data:
            return jsonify({'error': 'No historical data available'}), 404

        patterns = pattern_detector.detect_all_patterns(historical_data)
        summary = pattern_detector.get_pattern_summary(patterns)

        return jsonify({
            'symbol': symbol,
            'timeframe': timeframe,
            'patterns': patterns,
            'summary': summary,
            'timestamp': historical_data[-1].get('timestamp') if historical_data else None
        })

    except Exception as e:
        logger.error(f'Error detecting patterns for {symbol}: {e}')
        return jsonify({'error': str(e)}), 500

@signals_bp.route('/push-analysis/<symbol>', methods=['GET'])
def analyze_pushes(symbol):
    """Analyze market pushes using Trading Anarchy 4-push logic"""
    try:
        timeframe = request.args.get('timeframe', '1h')
        limit = int(request.args.get('limit', 100))
        target_pips = request.args.get('target_pips', type=float)

        historical_data = market_service.get_historical_data(symbol, timeframe, limit)

        if not historical_data:
            return jsonify({'error': 'No historical data available'}), 404

        push_analysis = anarchy_analyzer.analyze_market(historical_data, target_pips)

        recommendation = anarchy_analyzer.get_trading_recommendation(push_analysis)

        return jsonify({
            'symbol': symbol,
            'timeframe': timeframe,
            'analysis': push_analysis,
            'recommendation': recommendation
        })

    except Exception as e:
        logger.error(f'Error analyzing pushes for {symbol}: {e}')
        return jsonify({'error': str(e)}), 500

@signals_bp.route('/advanced-prediction/<symbol>', methods=['POST'])
def get_advanced_prediction(symbol):
    """Get advanced prediction using diffusion model and virtual economy"""
    try:
        timeframe = request.args.get('timeframe', '1h')
        limit = int(request.args.get('limit', 200))

        historical_data = market_service.get_historical_data(symbol, timeframe, limit)
        indicators = market_service.calculate_indicators(symbol)

        if not historical_data or len(historical_data) < 60:
            return jsonify({'error': 'Insufficient historical data for advanced prediction'}), 400

        prediction = ml_predictor.predict_with_diffusion(symbol, historical_data, indicators)

        patterns = pattern_detector.detect_all_patterns(historical_data)
        push_analysis = anarchy_analyzer.analyze_market(historical_data)

        return jsonify({
            'symbol': symbol,
            'timeframe': timeframe,
            'prediction': prediction,
            'detected_patterns': patterns[:3] if patterns else [],
            'push_analysis': {
                'active_pushes': push_analysis['active_pushes'],
                'exhaustion_level': push_analysis['exhaustion_level'],
                'warning_level': push_analysis['warning_level'],
                'should_exit': push_analysis['should_exit']
            },
            'timestamp': prediction.get('timestamp')
        })

    except Exception as e:
        logger.error(f'Error generating advanced prediction for {symbol}: {e}')
        return jsonify({'error': str(e)}), 500

@signals_bp.route('/comprehensive-analysis/<symbol>', methods=['GET'])
def get_comprehensive_analysis(symbol):
    """Get comprehensive analysis including patterns, pushes, and predictions"""
    try:
        timeframe = request.args.get('timeframe', '1h')
        limit = int(request.args.get('limit', 200))

        historical_data = market_service.get_historical_data(symbol, timeframe, limit)
        current_price = market_service.get_current_price(symbol)
        indicators = market_service.calculate_indicators(symbol)

        if not historical_data:
            return jsonify({'error': 'No data available'}), 404

        patterns = pattern_detector.detect_all_patterns(historical_data)
        pattern_summary = pattern_detector.get_pattern_summary(patterns)

        push_analysis = anarchy_analyzer.analyze_market(historical_data)
        push_recommendation = anarchy_analyzer.get_trading_recommendation(push_analysis)

        prediction = None
        if len(historical_data) >= 60:
            try:
                prediction = ml_predictor.predict_with_diffusion(symbol, historical_data, indicators)
            except Exception as e:
                logger.warning(f'Diffusion prediction failed, using fallback: {e}')
                prediction = None

        overall_bias = 'NEUTRAL'
        confidence_score = 50

        if pattern_summary['bullish_count'] > pattern_summary['bearish_count']:
            overall_bias = 'BULLISH'
            confidence_score = min(60 + (pattern_summary['bullish_count'] * 10), 85)
        elif pattern_summary['bearish_count'] > pattern_summary['bullish_count']:
            overall_bias = 'BEARISH'
            confidence_score = min(60 + (pattern_summary['bearish_count'] * 10), 85)

        if prediction and prediction.get('direction'):
            if prediction['direction'] == 'BUY':
                overall_bias = 'BULLISH'
                confidence_score = max(confidence_score, prediction.get('confidence', 50))
            elif prediction['direction'] == 'SELL':
                overall_bias = 'BEARISH'
                confidence_score = max(confidence_score, prediction.get('confidence', 50))

        return jsonify({
            'symbol': symbol,
            'timeframe': timeframe,
            'current_price': current_price,
            'overall_bias': overall_bias,
            'confidence_score': round(confidence_score, 1),
            'indicators': indicators,
            'patterns': {
                'detected': patterns[:5],
                'summary': pattern_summary
            },
            'push_analysis': {
                'active_pushes': push_analysis['active_pushes'],
                'exhaustion_level': push_analysis['exhaustion_level'],
                'warning_level': push_analysis['warning_level'],
                'reversal_probability': push_analysis['reversal_probability'],
                'should_exit': push_analysis['should_exit'],
                'recommendation': push_recommendation
            },
            'prediction': prediction,
            'timestamp': current_price.get('timestamp')
        })

    except Exception as e:
        logger.error(f'Error in comprehensive analysis for {symbol}: {e}')
        return jsonify({'error': str(e)}), 500
