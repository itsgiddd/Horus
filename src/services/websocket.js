// WebSocket Service for real-time data
import { io } from 'socket.io-client';

class WebSocketService {
  constructor() {
    this.socket = null;
    this.connected = false;
    this.listeners = {};
  }

  connect(url = 'http://127.0.0.1:5000') {
    if (this.socket) {
      return;
    }

    this.socket = io(url, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
    });

    this.socket.on('connect', () => {
      console.log('WebSocket connected');
      this.connected = true;
      this.emit('connection_status', { connected: true });
    });

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
      this.connected = false;
      this.emit('connection_status', { connected: false });
    });

    this.socket.on('connection_response', (data) => {
      console.log('Connection response:', data);
    });

    // Market data updates
    this.socket.on('market_update', (data) => {
      this.emit('market_update', data);
    });

    // Signal updates
    this.socket.on('signal_update', (data) => {
      this.emit('signal_update', data);
    });

    // Portfolio updates
    this.socket.on('portfolio_update', (data) => {
      this.emit('portfolio_update', data);
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.connected = false;
    }
  }

  subscribeToMarketData(symbols) {
    if (this.socket && this.connected) {
      this.socket.emit('subscribe_market_data', { symbols });
    }
  }

  subscribeToSignals() {
    if (this.socket && this.connected) {
      this.socket.emit('subscribe_signals');
    }
  }

  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(callback);
  }

  off(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event] = this.listeners[event].filter((cb) => cb !== callback);
    }
  }

  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach((callback) => callback(data));
    }
  }

  isConnected() {
    return this.connected;
  }
}

export default new WebSocketService();
