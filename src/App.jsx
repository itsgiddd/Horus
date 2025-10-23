import React, { useState, useEffect } from 'react';
import AdvancedChart from './components/AdvancedChart';
import SettingsView from './components/SettingsView';
import SetupWizard from './components/SetupWizard';
import './styles/App.css';

function App() {
  const [currentView, setCurrentView] = useState('charts');
  const [showSetup, setShowSetup] = useState(false);

  useEffect(() => {
    const setupComplete = localStorage.getItem('horus_setup_complete');
    if (!setupComplete) {
      setShowSetup(true);
    }
  }, []);

  return (
    <div className="app">
      {showSetup && <SetupWizard onComplete={() => setShowSetup(false)} />}

      <div className="app-header">
        <div className="app-logo">
          <span className="logo-icon">𓂀</span>
          <span className="logo-text">HORUS</span>
        </div>

        <div className="app-nav">
          <button
            className={`nav-btn ${currentView === 'charts' ? 'active' : ''}`}
            onClick={() => setCurrentView('charts')}
          >
            Charts
          </button>
          <button
            className={`nav-btn ${currentView === 'settings' ? 'active' : ''}`}
            onClick={() => setCurrentView('settings')}
          >
            Settings
          </button>
        </div>
      </div>

      <div className="app-main">
        {currentView === 'charts' ? (
          <AdvancedChart />
        ) : (
          <SettingsView />
        )}
      </div>
    </div>
  );
}

export default App;
