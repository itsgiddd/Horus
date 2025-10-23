import React, { useState, useEffect } from 'react';
import './BackendStatus.css';

function BackendStatus() {
  const [status, setStatus] = useState({
    status: 'checking',
    message: 'Checking backend connection...',
    timestamp: Date.now(),
  });

  useEffect(() => {
    // Check if running in Electron
    if (window.electron && window.electron.backend) {
      // Listen for backend status updates
      window.electron.backend.onStatus((data) => {
        setStatus(data);
      });

      // Initial check
      window.electron.backend.check();

      // Cleanup
      return () => {
        window.electron.backend.removeListener();
      };
    } else {
      // Running in browser, check backend via HTTP
      checkBackendHTTP();
      const interval = setInterval(checkBackendHTTP, 5000);
      return () => clearInterval(interval);
    }
  }, []);

  const checkBackendHTTP = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/market/price/BTC', {
        method: 'GET',
        timeout: 2000,
      });
      if (response.ok || response.status === 404) {
        setStatus({
          status: 'running',
          message: 'Backend connected',
          timestamp: Date.now(),
        });
      } else {
        setStatus({
          status: 'error',
          message: 'Backend not responding correctly',
          timestamp: Date.now(),
        });
      }
    } catch (error) {
      setStatus({
        status: 'error',
        message: 'Backend not running. Please start the backend manually.',
        timestamp: Date.now(),
      });
    }
  };

  const handleStartBackend = () => {
    if (window.electron && window.electron.backend) {
      window.electron.backend.start();
    } else {
      alert('Please start the backend manually:\n\ncd backend\nsource venv/bin/activate\npython app.py');
    }
  };

  const getStatusIcon = () => {
    switch (status.status) {
      case 'running':
        return '●';
      case 'starting':
        return '◐';
      case 'checking':
        return '○';
      case 'error':
      case 'stopped':
        return '○';
      default:
        return '○';
    }
  };

  const getStatusColor = () => {
    switch (status.status) {
      case 'running':
        return '#26a69a';
      case 'starting':
        return '#ffc107';
      case 'checking':
        return '#2196f3';
      case 'error':
      case 'stopped':
        return '#ef5350';
      default:
        return '#666';
    }
  };

  const getStatusText = () => {
    switch (status.status) {
      case 'running':
        return 'Backend Connected';
      case 'starting':
        return 'Starting Backend...';
      case 'checking':
        return 'Checking Connection...';
      case 'error':
        return 'Backend Error';
      case 'stopped':
        return 'Backend Stopped';
      default:
        return 'Unknown Status';
    }
  };

  return (
    <div className="backend-status">
      <div className="status-indicator">
        <span
          className={`status-icon ${status.status}`}
          style={{ color: getStatusColor() }}
        >
          {getStatusIcon()}
        </span>
        <span className="status-text">{getStatusText()}</span>
      </div>

      {status.status === 'error' && (
        <div className="status-actions">
          <button className="retry-btn" onClick={handleStartBackend}>
            Start Backend
          </button>
          <div className="error-message">{status.message}</div>
        </div>
      )}

      {status.status === 'starting' && (
        <div className="status-message">
          Please wait while the backend starts...
        </div>
      )}
    </div>
  );
}

export default BackendStatus;
