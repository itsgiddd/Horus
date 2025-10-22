<div align="center">
  <h1>𓂀 HORUS</h1>
  <h3>High-frequency Optimized Risk Unification System</h3>
  <p>
    <b>Your All-Seeing Eye for Smarter Forex & Crypto Trading</b>
  </p>
  
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge&logoColor=white&logo=github" />
  <img src="https://img.shields.io/badge/Trading-Forex_&_Crypto-blueviolet?style=for-the-badge&logo=bitcoin" />
  <img src="https://img.shields.io/badge/Built_with-Electron,_React,_Python-informational?style=for-the-badge&logo=react" />
</div>

---

## 📈 About HORUS

**HORUS** (High-frequency Optimized Risk Unification System) is a next-generation AI-powered platform for live forex and crypto trading. Leveraging advanced machine learning and seamless, frosted-glass UI, HORUS gives traders edge-defining insights, real-time signals, and a unified dashboard for digital asset markets.

> ⚡ **Cut through noise. Trade with vision.**  
> HORUS combines speed, clarity, and risk management—just like the all-seeing Eye.

---

## 🚀 Features

### 📊 **Dashboard & Analytics**
- Real-time portfolio overview with P&L tracking
- Live market data for crypto (BTC, ETH, SOL, etc.) and forex pairs
- Portfolio performance charts and metrics
- Win rate tracking and signal performance analytics

### 📈 **Advanced Charting**
- TradingView integration for professional charts
- Multiple timeframes (1m, 5m, 15m, 30m, 1H, 4H, 1D, 1W)
- Technical indicators (RSI, MACD, SMA, EMA, Bollinger Bands)
- AI-powered signal insights overlay

### ⚡ **AI Trading Signals**
- ML-based signal generation (Buy/Sell/Hold)
- Confidence scoring (0-100%)
- Target price and stop-loss recommendations
- Signal history with performance tracking
- Real-time signal updates via WebSocket

### 💼 **Portfolio Management**
- Multi-asset position tracking
- Real-time P&L calculations
- Performance analytics over time
- Asset allocation visualization
- Cash balance management

### 🛡️ **Risk Management**
- Portfolio risk score calculation
- Value at Risk (VaR) at 95% and 99% confidence
- Sharpe and Sortino ratio metrics
- Max drawdown analysis
- Diversification score and insights
- Position exposure breakdown

### 🔔 **Notifications System**
- Desktop push notifications
- Customizable alert thresholds
- Sound alerts for new signals
- Email alerts (configurable)

### 🎨 **Beautiful Frosted-Glass UI**
- Modern glassmorphism design
- Smooth animations and transitions
- Responsive layout
- Custom window controls
- Dark theme optimized

### 🔧 **Settings & Configuration**
- API key management
- Notification preferences
- Signal confidence thresholds
- Risk tolerance settings
- Multi-language support (coming soon)

### 🌐 **API Integrations**
- CoinGecko (crypto prices - free)
- CryptoCompare (optional)
- OANDA (forex trading - optional)
- Exchangerate API (forex rates - free)

---

## 🛠️ Tech Stack

| Layer                | Technology                          | Role                                          |
|----------------------|-------------------------------------|-----------------------------------------------|
| Presentation         | React + TradingView                 | User interface, live charting, notifications  |
| Application          | Electron                            | Desktop delivery, secure shell integration    |
| Processing           | Python ML, Node.js, REST APIs       | Market data aggregation, predictions, signals |

---

## 🎯 Input & Output

**Input:**  
- Historical & real-time OHLCV market data  
- Technical indicators (MA, RSI, MACD, BBANDS, etc.)  
- User-defined currency/crypto pairs and timeframes  

**Output:**  
- AI-generated trading signals (Buy/Sell/Hold)  
- Confidence scores (%)  
- Visual trade markups & performance analytics  

---

## 🚀 Quick Start

### Prerequisites
- Node.js v18+ and npm
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Horus
```

2. **Install frontend dependencies**
```bash
npm install
```

3. **Set up Python backend**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API keys (optional)
```

### Running the Application

#### Option 1: Development Mode (Recommended)

**Terminal 1 - Start Backend API:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

**Terminal 2 - Start Frontend:**
```bash
npm run dev
```

The app will open automatically. The backend API runs on `http://127.0.0.1:5000`.

#### Option 2: Quick Start Scripts

**macOS/Linux:**
```bash
# Terminal 1
cd backend && ./start.sh

# Terminal 2
npm run dev
```

**Windows:**
```bash
# Terminal 1
cd backend && start.bat

# Terminal 2
npm run dev
```

### Building for Production

**Build for your platform:**
```bash
npm run build:mac    # macOS (.dmg + .zip)
npm run build:win    # Windows (installer + portable)
npm run build:all    # Both platforms
```

## 📖 Documentation

- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Frontend development guide
- **[backend/README.md](backend/README.md)** - Backend API documentation
- **[BROKER_POLICY.md](BROKER_POLICY.md)** - Usage philosophy
- **[TERMS_OF_SERVICE.md](TERMS_OF_SERVICE.md)** - Legal terms

## 📸 Screenshots

*Coming soon*

## ⚠️ Disclaimer

This project is for educational and informational purposes only. Trading is risky—use at your own discretion. Not financial advice.

---

## 🤝 Contributing

This is a proprietary project. See [TERMS_OF_SERVICE.md](TERMS_OF_SERVICE.md) for usage terms.

---

## 📬 Contact

Created by [@itsgiddd](https://github.com/itsgiddd) • Questions? Open an issue!

---

<div align="center">
  <sub>Built with ☕ and vision. Powered by AI.<br/>𓂀 HORUS © 2025</sub>
</div>
