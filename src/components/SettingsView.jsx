import React, { useState, useEffect } from 'react';
import GlassCard from './GlassCard';
import './SettingsView.css';

function SettingsView() {
  const [settings, setSettings] = useState({
    notifications: true,
    soundAlerts: true,
    emailAlerts: false,
    signalConfidenceThreshold: 70,
    autoTrade: false,
    riskLevel: 'medium',
    theme: 'dark',
    language: 'en',
  });

  const [apiKeys, setApiKeys] = useState({
    cryptocompareApiKey: '',
    oandaApiKey: '',
    oandaAccountId: '',
    oandaEnvironment: 'practice',
  });

  const [apiStatus, setApiStatus] = useState({
    saving: false,
    testing: false,
    message: '',
    type: '', // 'success', 'error', 'info'
  });

  // Load current API configuration on mount
  useEffect(() => {
    loadApiConfig();
  }, []);

  const loadApiConfig = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/config/api-keys');
      if (response.ok) {
        const data = await response.json();
        setApiKeys({
          cryptocompareApiKey: data.cryptocompare_configured ? '••••••••' : '',
          oandaApiKey: data.oanda_configured ? '••••••••' : '',
          oandaAccountId: data.oanda_account_id || '',
          oandaEnvironment: data.oanda_environment || 'practice',
        });
      }
    } catch (error) {
      console.error('Error loading API config:', error);
    }
  };

  const handleApiKeyChange = (key, value) => {
    setApiKeys((prev) => ({ ...prev, [key]: value }));
    setApiStatus({ saving: false, testing: false, message: '', type: '' });
  };

  const saveApiKeys = async () => {
    setApiStatus({ saving: true, testing: false, message: 'Saving API keys...', type: 'info' });

    try {
      const response = await fetch('http://127.0.0.1:5000/api/config/api-keys', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          cryptocompare_api_key: apiKeys.cryptocompareApiKey,
          oanda_api_key: apiKeys.oandaApiKey,
          oanda_account_id: apiKeys.oandaAccountId,
          oanda_environment: apiKeys.oandaEnvironment,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setApiStatus({
          saving: false,
          testing: false,
          message: 'API keys saved successfully! Restart the backend to use them.',
          type: 'success'
        });
        // Reload to show masked keys
        setTimeout(() => loadApiConfig(), 1000);
      } else {
        throw new Error('Failed to save API keys');
      }
    } catch (error) {
      setApiStatus({
        saving: false,
        testing: false,
        message: 'Error saving API keys. Please try again.',
        type: 'error'
      });
    }
  };

  const testApiKeys = async () => {
    setApiStatus({ saving: false, testing: true, message: 'Testing API connections...', type: 'info' });

    try {
      const response = await fetch('http://127.0.0.1:5000/api/config/test-api-keys', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          cryptocompare_api_key: apiKeys.cryptocompareApiKey,
          oanda_api_key: apiKeys.oandaApiKey,
          oanda_account_id: apiKeys.oandaAccountId,
          oanda_environment: apiKeys.oandaEnvironment,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        let message = 'Test Results:\n';
        message += data.oanda_status ? '[OK] OANDA: Connected\n' : '[FAILED] OANDA: Failed\n';
        message += data.cryptocompare_status ? '[OK] CryptoCompare: Connected' : '[FAILED] CryptoCompare: Failed';

        setApiStatus({
          saving: false,
          testing: false,
          message: message,
          type: data.oanda_status || data.cryptocompare_status ? 'success' : 'error'
        });
      } else {
        throw new Error('Failed to test API keys');
      }
    } catch (error) {
      setApiStatus({
        saving: false,
        testing: false,
        message: 'Error testing API keys. Make sure backend is running.',
        type: 'error'
      });
    }
  };

  const handleToggle = (key) => {
    setSettings((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const handleSliderChange = (key, value) => {
    setSettings((prev) => ({ ...prev, [key]: value }));
  };

  const handleSelectChange = (key, value) => {
    setSettings((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <div className="settings-view">
      <div className="settings-header">
        <h2>Settings</h2>
      </div>

      {/* Notifications */}
      <GlassCard variant="strong">
        <h3>Notifications</h3>
        <div className="settings-section">
          <div className="setting-item">
            <div className="setting-info">
              <div className="setting-label">Push Notifications</div>
              <div className="setting-description">Receive desktop notifications for trading signals</div>
            </div>
            <label className="toggle-switch">
              <input
                type="checkbox"
                checked={settings.notifications}
                onChange={() => handleToggle('notifications')}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>

          <div className="setting-item">
            <div className="setting-info">
              <div className="setting-label">Sound Alerts</div>
              <div className="setting-description">Play sound when new signal is generated</div>
            </div>
            <label className="toggle-switch">
              <input
                type="checkbox"
                checked={settings.soundAlerts}
                onChange={() => handleToggle('soundAlerts')}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>

          <div className="setting-item">
            <div className="setting-info">
              <div className="setting-label">Email Alerts</div>
              <div className="setting-description">Send email notifications for high confidence signals</div>
            </div>
            <label className="toggle-switch">
              <input
                type="checkbox"
                checked={settings.emailAlerts}
                onChange={() => handleToggle('emailAlerts')}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
        </div>
      </GlassCard>

      {/* Trading Settings */}
      <GlassCard variant="strong">
        <h3>Trading Settings</h3>
        <div className="settings-section">
          <div className="setting-item">
            <div className="setting-info">
              <div className="setting-label">Signal Confidence Threshold</div>
              <div className="setting-description">
                Minimum confidence level to display signals: {settings.signalConfidenceThreshold}%
              </div>
            </div>
            <input
              type="range"
              min="50"
              max="95"
              value={settings.signalConfidenceThreshold}
              onChange={(e) => handleSliderChange('signalConfidenceThreshold', parseInt(e.target.value))}
              className="slider"
            />
          </div>

          <div className="setting-item">
            <div className="setting-info">
              <div className="setting-label">Risk Level</div>
              <div className="setting-description">Portfolio risk tolerance</div>
            </div>
            <select
              value={settings.riskLevel}
              onChange={(e) => handleSelectChange('riskLevel', e.target.value)}
              className="glass-select"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          <div className="setting-item">
            <div className="setting-info">
              <div className="setting-label">Auto Trading (Coming Soon)</div>
              <div className="setting-description">Automatically execute trades based on signals</div>
            </div>
            <label className="toggle-switch">
              <input
                type="checkbox"
                checked={settings.autoTrade}
                onChange={() => handleToggle('autoTrade')}
                disabled
              />
              <span className="toggle-slider disabled"></span>
            </label>
          </div>
        </div>
      </GlassCard>

      {/* API Configuration */}
      <GlassCard variant="strong">
        <h3>API Configuration</h3>
        <p className="section-info">
          Configure your API keys to access real-time market data. All keys are stored securely and never shared.
        </p>

        <div className="settings-section">
          <div className="api-setting">
            <label>
              CryptoCompare API Key
              <a href="https://min-api.cryptocompare.com/" target="_blank" rel="noopener noreferrer" className="api-link">
                Get Free API Key →
              </a>
            </label>
            <input
              type={apiKeys.cryptocompareApiKey === '••••••••' ? 'password' : 'text'}
              placeholder="Enter your CryptoCompare API key"
              className="api-input"
              value={apiKeys.cryptocompareApiKey}
              onChange={(e) => handleApiKeyChange('cryptocompareApiKey', e.target.value)}
            />
            <span className="api-description">For Bitcoin, Ethereum, and other cryptocurrency data</span>
          </div>

          <div className="api-setting">
            <label>
              OANDA API Key
              <a href="https://www.oanda.com/account/tpa/personal_token" target="_blank" rel="noopener noreferrer" className="api-link">
                Get Free API Key →
              </a>
            </label>
            <input
              type={apiKeys.oandaApiKey === '••••••••' ? 'password' : 'text'}
              placeholder="Enter your OANDA API token"
              className="api-input"
              value={apiKeys.oandaApiKey}
              onChange={(e) => handleApiKeyChange('oandaApiKey', e.target.value)}
            />
            <span className="api-description">For forex pairs data (EUR/USD, GBP/USD, etc.)</span>
          </div>

          <div className="api-setting">
            <label>OANDA Account ID</label>
            <input
              type="text"
              placeholder="XXX-XXX-XXXXXXXX-XXX"
              className="api-input"
              value={apiKeys.oandaAccountId}
              onChange={(e) => handleApiKeyChange('oandaAccountId', e.target.value)}
            />
            <span className="api-description">Found in your OANDA account dashboard</span>
          </div>

          <div className="api-setting">
            <label>OANDA Environment</label>
            <select
              value={apiKeys.oandaEnvironment}
              onChange={(e) => handleApiKeyChange('oandaEnvironment', e.target.value)}
              className="glass-select"
            >
              <option value="practice">Practice (Demo Account - Free)</option>
              <option value="live">Live (Real Money Trading)</option>
            </select>
            <span className="api-description">
              Use "Practice" for testing with fake money, "Live" for real trading
            </span>
          </div>

          {apiStatus.message && (
            <div className={`api-status-message ${apiStatus.type}`}>
              {apiStatus.message.split('\n').map((line, idx) => (
                <div key={idx}>{line}</div>
              ))}
            </div>
          )}

          <div className="api-buttons">
            <button
              className="save-btn secondary"
              onClick={testApiKeys}
              disabled={apiStatus.testing || apiStatus.saving}
            >
              {apiStatus.testing ? 'Testing...' : 'Test Connection'}
            </button>
            <button
              className="save-btn primary"
              onClick={saveApiKeys}
              disabled={apiStatus.saving || apiStatus.testing}
            >
              {apiStatus.saving ? 'Saving...' : 'Save API Keys'}
            </button>
          </div>

          <div className="api-info-box">
            <strong>Note:</strong> API keys are optional. HORUS works without them using simulated data.
            Add your API keys to access real historical candles and live market data.
          </div>
        </div>
      </GlassCard>

      {/* Appearance */}
      <GlassCard variant="strong">
        <h3>Appearance</h3>
        <div className="settings-section">
          <div className="setting-item">
            <div className="setting-info">
              <div className="setting-label">Theme</div>
              <div className="setting-description">Application color theme</div>
            </div>
            <select
              value={settings.theme}
              onChange={(e) => handleSelectChange('theme', e.target.value)}
              className="glass-select"
            >
              <option value="dark">Dark</option>
              <option value="light">Light (Coming Soon)</option>
            </select>
          </div>

          <div className="setting-item">
            <div className="setting-info">
              <div className="setting-label">Language</div>
              <div className="setting-description">Application language</div>
            </div>
            <select
              value={settings.language}
              onChange={(e) => handleSelectChange('language', e.target.value)}
              className="glass-select"
            >
              <option value="en">English</option>
              <option value="es">Español (Coming Soon)</option>
              <option value="fr">Français (Coming Soon)</option>
            </select>
          </div>
        </div>
      </GlassCard>

      {/* About */}
      <GlassCard variant="strong">
        <h3>About HORUS</h3>
        <div className="about-section">
          <div className="about-item">
            <span className="about-label">Version</span>
            <span className="about-value">1.0.0</span>
          </div>
          <div className="about-item">
            <span className="about-label">Backend Status</span>
            <span className="about-value status-connected">Connected</span>
          </div>
          <div className="about-item">
            <span className="about-label">License</span>
            <span className="about-value">Proprietary</span>
          </div>
          <p className="about-description">
            HORUS (High-frequency Optimized Risk Unification System) is an AI-powered trading platform
            for forex and cryptocurrency markets. Built with vision. Powered by AI.
          </p>
        </div>
      </GlassCard>
    </div>
  );
}

export default SettingsView;
