/**
 * HORUS - High-frequency Optimized Risk Unification System
 * Main Application Component
 */

import React from 'react';
import AdvancedChart from './components/AdvancedChart';
import SettingsView from './components/SettingsView';
import SetupWizard from './components/SetupWizard';
import BackendStatus from './components/BackendStatus';
import { useApp } from './contexts/AppContext';
import './styles/App.css';

function App() {
  const { currentView, setCurrentView, showSetup, completeSetup } = useApp();

  return (
    <div className="app">
      {showSetup && <SetupWizard onComplete={completeSetup} />}

      <div className="app-header">
        <div className="app-logo">
          <span className="logo-icon">𓂀</span>
          <div className="logo-content">
            <span className="logo-text">HORUS</span>
            <span className="logo-subtitle">AI Forex Predictor</span>
          </div>
        </div>

        <nav className="app-nav">
          <button
            className={`nav-btn ${currentView === 'charts' ? 'active' : ''}`}
            onClick={() => setCurrentView('charts')}
            aria-label="View Charts"
          >
            <span className="nav-icon">📊</span>
            <span>Charts</span>
          </button>
          <button
            className={`nav-btn ${currentView === 'settings' ? 'active' : ''}`}
            onClick={() => setCurrentView('settings')}
            aria-label="View Settings"
          >
            <span className="nav-icon">⚙️</span>
            <span>Settings</span>
          </button>
        </nav>
      </div>

      <main className="app-main">
        {currentView === 'charts' ? (
          <AdvancedChart />
        ) : (
          <SettingsView />
        )}
      </main>

      <BackendStatus />
    </div>
  );
}

export default App;
