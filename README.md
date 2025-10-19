<div align="center">

# 🚀 **NOX - Neural Optimization eXchange**

### *Your Intelligent Forex Prediction Platform*

![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge&logo=github)
![Trading](https://img.shields.io/badge/Trading-Automated-blueviolet?style=for-the-badge&logo=bitcoin)
![Made With](https://img.shields.io/badge/Made%20With-💜-ff69b4?style=for-the-badge)

</div>

---

## 📋 **About The Project**

**NOX (Neural Optimization eXchange)** is a cutting-edge desktop application for predicting forex market movements using machine learning. Built with Electron, React, and Python, **NOX** empowers traders with AI-driven insights and real-time market analysis.

> ⚠️ **Disclaimer**: This is not financial advice. By installing and using this software, you acknowledge and understand the risks involved in forex trading.

---

## 🎯 **Target Technical Specification**

### **Overview**

NOX is designed with a **multi-layered architecture** that seamlessly integrates machine learning capabilities with a modern desktop interface. This section provides a comprehensive technical overview for both users and developers looking to understand or extend the system.

### **🔧 Core Architecture**

NOX employs a **three-tier architecture** to separate concerns and optimize performance:

| **Layer** | **Technology** | **Purpose** |
|-----------|----------------|-------------|
| **Presentation Layer** | React + TradingView Charts | User interface, data visualization, and user interaction |
| **Application Layer** | Electron Main Process | Desktop app lifecycle, IPC coordination, and security |
| **Processing Layer** | Python ML Backend | Machine learning inference, data processing, and prediction generation |

### **📊 Input/Output Specification**

#### **Input Requirements**
- **Historical Price Data**: OHLCV (Open, High, Low, Close, Volume) time series data
- **Technical Indicators**: Moving averages, RSI, MACD, Bollinger Bands
- **Timeframe Parameters**: User-selected prediction windows (1m, 5m, 15m, 1h, 4h, 1d)
- **Currency Pair Selection**: Major and minor forex pairs (e.g., EUR/USD, GBP/JPY)

#### **Output Format**
- **Prediction Signal**: BUY, SELL, or HOLD recommendation
- **Confidence Score**: Percentage-based confidence level (0-100%)
- **Predicted Price Movement**: Expected price change over selected timeframe
- **Supporting Indicators**: Technical analysis data supporting the prediction

### **🔄 Data Flow & Workflow**

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   React UI  │◄───────►│   Electron   │◄───────►│   Python    │
│  (Frontend) │   IPC   │ Main Process │  stdin/ │   Backend   │
│             │         │              │  stdout │             │
└─────────────┘         └──────────────┘         └─────────────┘
       │                                                 │
       │                                                 │
       ▼                                                 ▼
 ┌──────────┐                                    ┌──────────────┐
 │TradingView│                                    │  ML Model    │
 │  Charts   │                                    │ (Prediction) │
 └──────────┘                                    └──────────────┘
```

**Step-by-Step Workflow:**

1. **User Interaction**: User selects a currency pair and timeframe in the React UI
2. **IPC Request**: Frontend sends prediction request via Electron's IPC mechanism
3. **Backend Processing**: Python backend receives request, loads ML model, and processes input data
4. **ML Inference**: Neural network analyzes historical data and generates prediction
5. **Response Delivery**: Prediction results are serialized and sent back through IPC
6. **Visualization**: React updates the chart with prediction markers and confidence indicators

### **🧠 Main Components Breakdown**

#### **1. React Frontend (`src/`)**
- **Chart.js**: TradingView Lightweight Charts integration for candlestick visualization
- **App.js**: Main application logic, state management, and IPC coordination
- **UI Components**: Controls for currency pair selection, timeframe adjustment, and prediction triggers

#### **2. Electron Main Process (`main.js`)**
- **Window Management**: Creates and manages the desktop application window
- **IPC Handler**: Receives prediction requests from renderer process
- **Python Process Spawner**: Launches and maintains Python backend subprocess
- **Security Layer**: Implements context isolation and secure communication protocols

#### **3. Python ML Backend (`predictor.py`)**
- **Model Loader**: Initializes pre-trained machine learning model
- **Data Preprocessor**: Normalizes and transforms input data for ML inference
- **Prediction Engine**: Executes neural network forward pass to generate predictions
- **Output Formatter**: Serializes predictions into JSON format for IPC transmission

### **💡 Practical Usage Examples**

#### **For Users:**
```markdown
1. Launch NOX application
2. Select EUR/USD from the currency pair dropdown
3. Choose 15-minute timeframe
4. Click "Predict" button
5. View prediction signal (BUY/SELL/HOLD) with confidence score
6. Analyze supporting technical indicators on the chart
```

#### **For Developers:**
```markdown
- Extend ML model by modifying `predictor.py`
- Add new technical indicators in `Chart.js`
- Customize IPC protocol in `main.js` for additional data exchange
- Integrate external data APIs for real-time market feeds
```

### **📚 Detailed Reference**

For **in-depth technical specifications**, including:
- Detailed API documentation
- ML model architecture diagrams
- IPC protocol specifications
- Performance optimization guidelines
- Security considerations and best practices

Please refer to the comprehensive **[`target_tech_spec.pdf`](target_tech_spec.pdf)** provided in this repository.

---

## ✨ **Key Features**

- 🤖 **Real-time forex prediction** using advanced ML models
- 📊 **Interactive chart visualization** powered by TradingView Lightweight Charts
- 📈 **Technical indicators** and comprehensive market analysis
- 💻 **Cross-platform desktop application** (macOS, Windows, Linux)
- 🔒 **Secure IPC communication** between frontend and backend
- ⚡ **Lightning-fast predictions** with optimized Python backend

---

## 🏗️ **Architecture**

The app consists of four main components:

| Component | Description |
|-----------|-------------|
| **React Frontend** | User interface built with React and TradingView Lightweight Charts |
| **Electron Main Process** | Manages the desktop app and coordinates between frontend and backend |
| **Python Backend** | Machine learning model for forex prediction |
| **IPC Communication** | Secure communication bridge between frontend and Python backend |

---

## 📦 **Prerequisites**

Before you begin, ensure you have the following installed:
