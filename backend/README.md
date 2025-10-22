# HORUS Backend API

Python backend for HORUS trading platform with Flask, WebSockets, and ML models.

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add:
- CryptoCompare API key (get from https://www.cryptocompare.com/cryptopian/api-keys)
- OANDA API key (optional, for forex data)

### 4. Run the Server

```bash
python app.py
```

The API will start on `http://127.0.0.1:5000`

## API Endpoints

### Health Check
- `GET /api/health` - Server health status

### Market Data
- `GET /api/market/price/<symbol>` - Get current price for a symbol
- `POST /api/market/prices` - Get prices for multiple symbols
- `GET /api/market/history/<symbol>` - Get historical OHLCV data
- `GET /api/market/indicators/<symbol>` - Get technical indicators
- `GET /api/market/supported-assets` - List supported trading pairs

### Signals
- `GET /api/signals/current` - Get current trading signals
- `POST /api/signals/generate/<symbol>` - Generate signal for a symbol
- `GET /api/signals/history` - Get signal history
- `GET /api/signals/performance` - Get signal performance metrics

### Portfolio
- `GET /api/portfolio/summary` - Get portfolio summary
- `GET /api/portfolio/positions` - Get all positions
- `GET /api/portfolio/risk-metrics` - Get risk metrics
- `GET /api/portfolio/performance` - Get performance over time

## WebSocket Events

### Client → Server
- `subscribe_market_data` - Subscribe to market data updates
- `subscribe_signals` - Subscribe to signal updates

### Server → Client
- `market_update` - Real-time market data
- `signal_update` - New trading signal
- `portfolio_update` - Portfolio changes

## Architecture

```
backend/
├── api/
│   └── routes/           # API route handlers
│       ├── market_routes.py
│       ├── signals_routes.py
│       └── portfolio_routes.py
├── services/             # Business logic
│   ├── market_service.py
│   ├── signal_service.py
│   └── portfolio_service.py
├── ml/                   # Machine learning models
│   └── predictor.py
├── models/               # Data models (future)
├── utils/                # Utilities (future)
└── app.py                # Main Flask application
```

## Features

- **Real-time Market Data**: Fetch crypto and forex prices from multiple sources
- **Technical Indicators**: RSI, MACD, Bollinger Bands, Moving Averages
- **AI Predictions**: ML-based trading signal generation
- **Portfolio Analytics**: Track positions, P&L, and performance
- **Risk Management**: VaR, Sharpe ratio, diversification metrics
- **WebSocket Support**: Real-time data streaming

## Data Sources

- **Crypto**: CoinGecko API (free tier)
- **Forex**: exchangerate-api.com (free tier)
- **Alternative**: CryptoCompare, OANDA (requires API keys)

## ML Models

The predictor uses rule-based trading logic combining multiple technical indicators.
In production, this can be replaced with:
- LSTM neural networks (TensorFlow/Keras)
- Random Forest classifiers (scikit-learn)
- Ensemble models

## Development

To add new features:
1. Add route handler in `api/routes/`
2. Implement business logic in `services/`
3. Register blueprint in `app.py`

## Production Deployment

For production:
1. Set `FLASK_DEBUG=False` in `.env`
2. Use production WSGI server (gunicorn, waitress)
3. Add authentication and rate limiting
4. Set up HTTPS/SSL
5. Use production database (PostgreSQL)

## License

PROPRIETARY - See ../TERMS_OF_SERVICE.md
