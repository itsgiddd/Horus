import React, { useState } from 'react';
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
        <div className="settings-section">
          <div className="api-setting">
            <label>CryptoCompare API Key</label>
            <input type="password" placeholder="Enter API key" className="api-input" />
          </div>

          <div className="api-setting">
            <label>OANDA API Key</label>
            <input type="password" placeholder="Enter API key" className="api-input" />
          </div>

          <div className="api-setting">
            <label>OANDA Account ID</label>
            <input type="text" placeholder="Enter account ID" className="api-input" />
          </div>

          <button className="save-btn">Save API Keys</button>
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
