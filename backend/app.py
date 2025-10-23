from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

# Import routes
from api.routes.market_routes import market_bp
from api.routes.signals_routes import signals_bp
from api.routes.portfolio_routes import portfolio_bp
from api.routes.training_routes import training_bp
from api.routes.export_routes import export_bp
from api.routes.config_routes import config_bp

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'horus-secret-key-change-in-production')
CORS(app)

# Initialize SocketIO for real-time communication
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Register blueprints
app.register_blueprint(market_bp, url_prefix='/api/market')
app.register_blueprint(signals_bp, url_prefix='/api/signals')
app.register_blueprint(portfolio_bp, url_prefix='/api/portfolio')
app.register_blueprint(training_bp, url_prefix='/api/training')
app.register_blueprint(export_bp, url_prefix='/api/export')
app.register_blueprint(config_bp, url_prefix='/api/config')

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'HORUS Backend API'
    })

# WebSocket events
@socketio.on('connect')
def handle_connect():
    logger.info('Client connected')
    emit('connection_response', {'status': 'connected', 'message': 'Welcome to HORUS'})

@socketio.on('disconnect')
def handle_disconnect():
    logger.info('Client disconnected')

@socketio.on('subscribe_market_data')
def handle_market_subscription(data):
    """Subscribe to real-time market data for specific symbols"""
    symbols = data.get('symbols', [])
    logger.info(f'Client subscribed to market data: {symbols}')
    emit('subscription_confirmed', {'symbols': symbols})

@socketio.on('subscribe_signals')
def handle_signal_subscription():
    """Subscribe to trading signals"""
    logger.info('Client subscribed to trading signals')
    emit('signal_subscription_confirmed', {'status': 'subscribed'})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Internal error: {error}')
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'

    logger.info(f'Starting HORUS Backend API on {host}:{port}')
    socketio.run(app, host=host, port=port, debug=debug)
