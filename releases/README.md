# HORUS Backend Distribution

This directory contains pre-packaged backend releases for easy deployment.

## Contents

### Backend Package (`horus_backend_YYYYMMDD.zip`)

Complete Python backend with all AI/ML components:
- **AI Diffusion Model** - Time series forecasting with DDPM
- **Virtual Economy Simulation** - 100+ trader agents with realistic market dynamics
- **Pattern Recognition** - 18+ chart patterns (Double Bottom/Top, H&S, Flags, Pennants, etc.)
- **Trading Anarchy 4-Push System** - Exhaustion detection
- **API Integration** - OANDA (forex) and CryptoCompare (crypto) support
- **Self-Training Mechanism** - Automatic model retraining
- **Export Functionality** - Download models and configurations

## Quick Start

### 1. Extract the Backend

```bash
unzip horus_backend_YYYYMMDD.zip
cd backend
```

### 2. Install Dependencies

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment (Optional)

For live trading, copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` to add:
- `OANDA_API_KEY` - Your OANDA API key
- `CRYPTOCOMPARE_API_KEY` - Your CryptoCompare API key

**Note:** API keys are optional. The backend works in self-contained mode without them.

### 4. Start the Backend

**Windows:**
```bash
start.bat
```

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

Or manually:
```bash
python app.py
```

The backend will start on `http://127.0.0.1:5000`

## API Endpoints

### Market Data
- `GET /api/market/price/<symbol>` - Get current price
- `GET /api/market/history/<symbol>` - Get historical data
- `GET /api/market/indicators/<symbol>` - Calculate technical indicators

### AI Predictions
- `GET /api/signals/patterns/<symbol>` - Detect chart patterns
- `GET /api/signals/push-analysis/<symbol>` - 4-push exhaustion analysis
- `POST /api/signals/advanced-prediction/<symbol>` - AI diffusion prediction
- `GET /api/signals/comprehensive-analysis/<symbol>` - Full analysis

### Training
- `POST /api/training/start` - Start auto-training
- `POST /api/training/stop` - Stop auto-training
- `POST /api/training/train/<symbol>` - Train for specific symbol

### Export
- `GET /api/export/models` - Download trained models
- `GET /api/export/backend-full` - Download complete backend
- `GET /api/export/config` - Download configuration files

## Supported Assets

### Cryptocurrencies
- BTC, ETH, SOL, ADA, XRP, DOT, LINK, MATIC, AVAX, UNI

### Forex Pairs
- EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD, NZD/USD, USD/CHF

## System Requirements

- **Python:** 3.8 or higher
- **RAM:** 4GB minimum (8GB recommended for AI training)
- **Storage:** 500MB for backend + models
- **OS:** Windows, macOS, or Linux

## Features

### AI Diffusion Model
- 1000-timestep DDPM for price forecasting
- Cosine beta schedule
- Conditional generation based on historical data
- 60-bar lookback, 10-candle forecast

### Virtual Economy
- 100+ simulated trader agents
- 5 trader types: TrendFollower, MeanReverter, ScalpTrader, SwingTrader, InstitutionalTrader
- Realistic market dynamics with supply/demand modeling
- Scenario probability calculation

### Pattern Recognition
Detects 18+ patterns:
- **Reversal:** Double Bottom/Top, H&S, Inverted H&S, Falling Wedge, Diamonds, Tea Cup
- **Continuation:** Bull/Bear Flag, Pennants, Triangles, Wedges, Rectangle, Rounding Top

### Trading Anarchy System
- Push detection with pip unit calculation
- Exhaustion warnings at 4th push
- Aircraft mechanic bolt analogy
- Reversal probability calculation

## Troubleshooting

### Import Errors
```bash
pip install --upgrade -r requirements.txt
```

### Port Already in Use
Edit `backend/.env` and change `FLASK_PORT=5000` to another port.

### API Connection Issues
Check that:
1. Backend is running (`http://127.0.0.1:5000`)
2. No firewall blocking port 5000
3. `.env` file is configured correctly

## License

PROPRIETARY - All rights reserved

## Support

For issues or questions, please check the main repository documentation.
