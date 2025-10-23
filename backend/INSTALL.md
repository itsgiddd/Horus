# HORUS Backend - Installation Guide

This guide will help you set up the HORUS backend on your system.

## Prerequisites

- Python 3.8 or higher (Python 3.9+ recommended)
- pip (Python package manager)
- 4GB RAM minimum (8GB recommended for AI training)

## Installation Methods

### Method 1: Quick Install (Recommended)

This installs all dependencies except optional ML components:

```bash
# Extract the backend
unzip horus_backend_*.zip
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Start the backend
python app.py
```

The backend will start on `http://127.0.0.1:5000`

### Method 2: macOS Apple Silicon (M1/M2/M3)

For Apple Silicon Macs, some packages have optimized ARM versions:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate

# Upgrade pip first
pip install --upgrade pip

# Install dependencies (TensorFlow will auto-install tensorflow-macos)
pip install -r requirements.txt

python app.py
```

## Troubleshooting

### Issue: TensorFlow Installation Slow

TensorFlow is a large package (200MB+). If installation is slow:

```bash
# Install without TensorFlow first
pip install -r requirements.txt --no-deps
pip install flask flask-cors flask-socketio python-socketio requests numpy pandas scikit-learn ta python-dotenv

# Then install TensorFlow separately
pip install tensorflow
```

Note: TensorFlow is only needed for advanced LSTM models. The backend works without it.

### Issue: Package Version Conflicts

If you encounter version conflicts:

```bash
# Install with looser version constraints
pip install flask flask-cors flask-socketio requests numpy pandas ta python-dotenv torch diffusers mesa schedule
```

### Issue: Out of Memory During Installation

Some packages (PyTorch, TensorFlow) are large. If installation fails:

```bash
# Install packages one at a time
pip install flask flask-cors flask-socketio
pip install numpy pandas
pip install torch  # Large download, be patient
pip install diffusers transformers
pip install mesa scipy statsmodels
```

## Configuration

### Self-Contained Mode (Default)

No configuration needed! The backend works immediately with:
- Simulated market data
- AI predictions
- Pattern recognition
- Virtual economy simulation

### Live Trading Mode (Optional)

For real market data, create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# OANDA API (for forex)
OANDA_API_KEY=your_key_here
OANDA_ACCOUNT_ID=your_account_id
OANDA_ENVIRONMENT=practice

# CryptoCompare API (for crypto)
CRYPTOCOMPARE_API_KEY=your_key_here
```

Get API keys:
- OANDA: https://www.oanda.com/
- CryptoCompare: https://min-api.cryptocompare.com/

## Running the Backend

### Start the Server

```bash
cd backend
source venv/bin/activate  # macOS/Linux
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Backend successfully initialized!
```

### Test the API

Open your browser to:
- http://127.0.0.1:5000/api/market/price/BTC - Get Bitcoin price
- http://127.0.0.1:5000/api/market/indicators/EUR_USD - Get EUR/USD indicators

### Enable Auto-Training

Once the backend is running, enable automatic model training:

```bash
curl -X POST http://127.0.0.1:5000/api/training/start
```

## What's Included

The backend provides:

1. **AI Diffusion Model** - DDPM for time series forecasting
2. **Virtual Economy** - 100+ trader agent simulation
3. **Pattern Recognition** - 18+ chart patterns
4. **Trading Anarchy** - 4-push exhaustion detection
5. **API Integration** - OANDA (forex) + CryptoCompare (crypto)
6. **Self-Training** - Automatic model retraining
7. **Export Tools** - Download models and configurations

## API Endpoints

### Market Data
- `GET /api/market/price/<symbol>` - Current price
- `GET /api/market/history/<symbol>` - Historical OHLCV data
- `GET /api/market/indicators/<symbol>` - Technical indicators

### AI Predictions
- `GET /api/signals/patterns/<symbol>` - Chart pattern detection
- `GET /api/signals/push-analysis/<symbol>` - 4-push analysis
- `POST /api/signals/advanced-prediction/<symbol>` - AI predictions
- `GET /api/signals/comprehensive-analysis/<symbol>` - Full analysis

### Training
- `POST /api/training/start` - Start auto-training
- `POST /api/training/stop` - Stop auto-training
- `POST /api/training/train/<symbol>` - Train specific symbol

### Export
- `GET /api/export/models` - Download trained models
- `GET /api/export/backend-full` - Download complete backend
- `GET /api/export/config` - Download configuration files

## System Requirements

- **Python:** 3.8+ (3.9+ recommended)
- **RAM:** 4GB minimum, 8GB recommended for AI training
- **Storage:** 500MB for backend + dependencies + models
- **OS:** macOS, Windows, or Linux

## Support

If you encounter issues:

1. **Check Python version:** `python3 --version` (should be 3.8+)
2. **Verify virtual environment:** `which python` should point to venv
3. **Check logs:** Look for error messages in the terminal
4. **Try minimal install:** Install core packages first, then optional ones

## Notes

- The `ta` library (pure Python) is used for technical analysis, not `ta-lib` (which requires C libraries)
- TensorFlow automatically installs the correct version for your platform (tensorflow-macos on Apple Silicon)
- PyTorch is optimized for Apple Silicon and will use Metal acceleration
- All API keys are optional - backend works in self-contained mode without them

---

**Ready to trade! 𓂀**
