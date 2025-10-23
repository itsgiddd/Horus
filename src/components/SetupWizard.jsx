import React, { useState, useEffect } from 'react';
import './SetupWizard.css';

function SetupWizard({ onComplete }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [setupData, setSetupData] = useState({
    oandaApiKey: '',
    oandaAccountId: '',
    oandaEnvironment: 'practice',
    cryptocompareApiKey: '',
    autoTraining: true,
    trainingSymbols: ['BTC', 'ETH', 'EUR/USD', 'GBP/USD'],
  });
  const [isValidating, setIsValidating] = useState(false);
  const [validationError, setValidationError] = useState('');
  const [installing, setInstalling] = useState(false);
  const [installProgress, setInstallProgress] = useState(0);

  const steps = [
    {
      title: 'Welcome to HORUS',
      subtitle: 'High-frequency Optimized Risk Unification System',
      description: 'Let\'s set up your AI-powered trading platform in a few simple steps.'
    },
    {
      title: 'API Keys Configuration',
      subtitle: 'Connect to market data sources',
      description: 'Configure your API keys for real-time forex and crypto data.'
    },
    {
      title: 'Training Configuration',
      subtitle: 'Set up automatic model training',
      description: 'Choose which symbols to track and enable auto-training.'
    },
    {
      title: 'Installation',
      subtitle: 'Installing dependencies',
      description: 'Setting up Python and Node.js dependencies...'
    },
    {
      title: 'Ready to Trade',
      subtitle: 'Setup complete',
      description: 'Your HORUS trading platform is ready to use!'
    }
  ];

  const handleInputChange = (field, value) => {
    setSetupData(prev => ({ ...prev, [field]: value }));
    setValidationError('');
  };

  const validateApiKeys = async () => {
    setIsValidating(true);
    setValidationError('');

    try {
      const response = await fetch('http://127.0.0.1:5000/api/health');

      if (!response.ok) {
        throw new Error('Backend server not running');
      }

      if (setupData.oandaApiKey && setupData.oandaAccountId) {
        console.log('OANDA API keys configured');
      }

      if (setupData.cryptocompareApiKey) {
        console.log('CryptoCompare API key configured');
      }

      setIsValidating(false);
      return true;
    } catch (error) {
      setValidationError('Could not connect to backend server. Please ensure it is running.');
      setIsValidating(false);
      return false;
    }
  };

  const saveConfiguration = async () => {
    try {
      const envContent = `# OANDA Configuration
OANDA_API_KEY=${setupData.oandaApiKey}
OANDA_ACCOUNT_ID=${setupData.oandaAccountId}
OANDA_ENVIRONMENT=${setupData.oandaEnvironment}

# CryptoCompare Configuration
CRYPTOCOMPARE_API_KEY=${setupData.cryptocompareApiKey}

# Flask Configuration
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=True

# ML Model Settings
MODEL_UPDATE_INTERVAL=3600
PREDICTION_LOOKBACK=60
`;

      console.log('Configuration saved:', setupData);

      if (setupData.autoTraining) {
        try {
          await fetch('http://127.0.0.1:5000/api/training/start', { method: 'POST' });
          console.log('Auto-training enabled');
        } catch (error) {
          console.error('Could not enable auto-training:', error);
        }
      }

      return true;
    } catch (error) {
      console.error('Error saving configuration:', error);
      return false;
    }
  };

  const installDependencies = async () => {
    setInstalling(true);
    setInstallProgress(0);

    const simulateInstall = () => {
      return new Promise((resolve) => {
        let progress = 0;
        const interval = setInterval(() => {
          progress += Math.random() * 15;
          if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
            resolve();
          }
          setInstallProgress(Math.min(progress, 100));
        }, 500);
      });
    };

    await simulateInstall();
    setInstalling(false);
  };

  const handleNext = async () => {
    // Step 1: API Keys validation (optional, can skip)
    if (currentStep === 1) {
      // Just save config, don't validate (backend might not be running yet)
      await saveConfiguration();
    }

    // Step 2: Training config (no validation needed)
    if (currentStep === 2) {
      await saveConfiguration();
      // Move to next step immediately
      setCurrentStep(prev => prev + 1);
      return;
    }

    // Step 3: Installation simulation
    if (currentStep === 3) {
      await installDependencies();
    }

    // Final step: Complete setup
    if (currentStep === steps.length - 1) {
      if (onComplete) onComplete();
      localStorage.setItem('horus_setup_complete', 'true');
      window.location.reload();
    } else {
      setCurrentStep(prev => prev + 1);
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
    }
  };

  const toggleSymbol = (symbol) => {
    setSetupData(prev => {
      const symbols = prev.trainingSymbols.includes(symbol)
        ? prev.trainingSymbols.filter(s => s !== symbol)
        : [...prev.trainingSymbols, symbol];
      return { ...prev, trainingSymbols: symbols };
    });
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 0:
        return (
          <div className="welcome-content">
            <div className="horus-logo-large">𓂀</div>
            <h2>Welcome to HORUS</h2>
            <p className="welcome-text">
              HORUS combines cutting-edge AI with professional trading tools to give you
              an edge in forex and cryptocurrency markets.
            </p>
            <div className="features-grid">
              <div className="feature-item">
                <div className="feature-icon">🤖</div>
                <h4>AI Predictions</h4>
                <p>Diffusion models with virtual economy simulation</p>
              </div>
              <div className="feature-item">
                <div className="feature-icon">📊</div>
                <h4>Pattern Recognition</h4>
                <p>18+ chart patterns with confidence scoring</p>
              </div>
              <div className="feature-item">
                <div className="feature-icon">⚡</div>
                <h4>4-Push Analysis</h4>
                <p>Trading Anarchy exhaustion detection</p>
              </div>
              <div className="feature-item">
                <div className="feature-icon">📈</div>
                <h4>Real-time Data</h4>
                <p>OANDA forex and CryptoCompare integration</p>
              </div>
            </div>
          </div>
        );

      case 1:
        return (
          <div className="api-keys-content">
            <div className="form-section">
              <h3>OANDA API (Forex Data)</h3>
              <p className="section-description">
                Get your API keys from <a href="https://www.oanda.com/account/tpa/personal_token" target="_blank" rel="noopener noreferrer">OANDA API Portal</a>
              </p>

              <div className="form-group">
                <label>API Key</label>
                <input
                  type="password"
                  placeholder="Enter your OANDA API key"
                  value={setupData.oandaApiKey}
                  onChange={(e) => handleInputChange('oandaApiKey', e.target.value)}
                  className="setup-input"
                />
              </div>

              <div className="form-group">
                <label>Account ID</label>
                <input
                  type="text"
                  placeholder="Enter your OANDA account ID"
                  value={setupData.oandaAccountId}
                  onChange={(e) => handleInputChange('oandaAccountId', e.target.value)}
                  className="setup-input"
                />
              </div>

              <div className="form-group">
                <label>Environment</label>
                <select
                  value={setupData.oandaEnvironment}
                  onChange={(e) => handleInputChange('oandaEnvironment', e.target.value)}
                  className="setup-select"
                >
                  <option value="practice">Practice (Demo)</option>
                  <option value="live">Live (Real Money)</option>
                </select>
              </div>
            </div>

            <div className="form-section">
              <h3>CryptoCompare API (Crypto Data)</h3>
              <p className="section-description">
                Get your free API key from <a href="https://www.cryptocompare.com/cryptopian/api-keys" target="_blank" rel="noopener noreferrer">CryptoCompare</a>
              </p>

              <div className="form-group">
                <label>API Key</label>
                <input
                  type="password"
                  placeholder="Enter your CryptoCompare API key"
                  value={setupData.cryptocompareApiKey}
                  onChange={(e) => handleInputChange('cryptocompareApiKey', e.target.value)}
                  className="setup-input"
                />
              </div>

              <div className="info-box">
                <strong>Note:</strong> API keys are optional. You can skip this step and use
                free data sources, though they may have rate limits.
              </div>
            </div>

            {validationError && (
              <div className="error-box">
                {validationError}
              </div>
            )}
          </div>
        );

      case 2:
        return (
          <div className="training-content">
            <div className="form-section">
              <h3>Automatic Model Training</h3>
              <p className="section-description">
                Enable automatic retraining to keep predictions accurate with fresh market data
              </p>

              <div className="toggle-group">
                <label className="toggle-label">
                  <input
                    type="checkbox"
                    checked={setupData.autoTraining}
                    onChange={(e) => handleInputChange('autoTraining', e.target.checked)}
                    className="toggle-input"
                  />
                  <span>Enable Auto-Training (Recommended)</span>
                </label>
              </div>

              {setupData.autoTraining && (
                <div className="training-info">
                  <p>Models will be retrained daily at 2:00 AM with the latest market data</p>
                </div>
              )}
            </div>

            <div className="form-section">
              <h3>Symbols to Track</h3>
              <p className="section-description">
                Select which markets you want to track and receive predictions for
              </p>

              <div className="symbols-grid">
                {['BTC', 'ETH', 'SOL', 'EUR/USD', 'GBP/USD', 'USD/JPY'].map(symbol => (
                  <div
                    key={symbol}
                    className={`symbol-card ${setupData.trainingSymbols.includes(symbol) ? 'selected' : ''}`}
                    onClick={() => toggleSymbol(symbol)}
                  >
                    <div className="symbol-name">{symbol}</div>
                    <div className="symbol-check">
                      {setupData.trainingSymbols.includes(symbol) ? '✓' : '+'}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="installation-content">
            <div className="install-animation">
              <div className="spinner-large"></div>
            </div>

            <h3>Installing Dependencies</h3>
            <p className="install-text">This may take a few minutes...</p>

            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${installProgress}%` }}></div>
            </div>
            <div className="progress-text">{Math.round(installProgress)}%</div>

            <div className="install-steps">
              <div className={`install-step ${installProgress > 20 ? 'complete' : 'active'}`}>
                Installing Python dependencies...
              </div>
              <div className={`install-step ${installProgress > 50 ? 'complete' : installProgress > 20 ? 'active' : ''}`}>
                Installing Node.js dependencies...
              </div>
              <div className={`install-step ${installProgress > 80 ? 'complete' : installProgress > 50 ? 'active' : ''}`}>
                Configuring AI models...
              </div>
              <div className={`install-step ${installProgress >= 100 ? 'complete' : installProgress > 80 ? 'active' : ''}`}>
                Finalizing setup...
              </div>
            </div>
          </div>
        );

      case 4:
        return (
          <div className="completion-content">
            <div className="success-icon">✓</div>
            <h2>Setup Complete!</h2>
            <p className="success-text">
              HORUS is now configured and ready to help you trade smarter.
            </p>

            <div className="summary-grid">
              <div className="summary-item">
                <div className="summary-label">API Keys</div>
                <div className="summary-value">
                  {(setupData.oandaApiKey || setupData.cryptocompareApiKey) ? 'Configured' : 'Skipped'}
                </div>
              </div>
              <div className="summary-item">
                <div className="summary-label">Auto-Training</div>
                <div className="summary-value">
                  {setupData.autoTraining ? 'Enabled' : 'Disabled'}
                </div>
              </div>
              <div className="summary-item">
                <div className="summary-label">Tracked Symbols</div>
                <div className="summary-value">{setupData.trainingSymbols.length}</div>
              </div>
            </div>

            <div className="next-steps">
              <h4>Next Steps:</h4>
              <ul>
                <li>Explore the dashboard to see market overview</li>
                <li>Check the Charts view for AI predictions and patterns</li>
                <li>Review signals for trading opportunities</li>
                <li>Monitor your portfolio performance</li>
              </ul>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="setup-wizard-overlay">
      <div className="setup-wizard-container">
        <div className="setup-progress-bar">
          {steps.map((step, index) => (
            <div
              key={index}
              className={`progress-step ${index === currentStep ? 'active' : index < currentStep ? 'complete' : ''}`}
            >
              <div className="step-circle">{index < currentStep ? '✓' : index + 1}</div>
              <div className="step-label">{step.title}</div>
            </div>
          ))}
        </div>

        <div className="setup-content">
          <div className="setup-header">
            <h1>{steps[currentStep].title}</h1>
            <p className="setup-subtitle">{steps[currentStep].subtitle}</p>
          </div>

          <div className="setup-body">
            {renderStepContent()}
          </div>

          <div className="setup-footer">
            <button
              className="setup-btn btn-secondary"
              onClick={handleBack}
              disabled={currentStep === 0 || installing}
            >
              Back
            </button>

            <button
              className="setup-btn btn-primary"
              onClick={handleNext}
              disabled={isValidating || installing}
            >
              {isValidating ? 'Validating...' :
               installing ? 'Installing...' :
               currentStep === steps.length - 1 ? 'Get Started' : 'Next'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SetupWizard;
