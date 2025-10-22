import React, { useState, useEffect } from 'react';
import TitleBar from './components/TitleBar';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import ChartsView from './components/ChartsView';
import SignalsView from './components/SignalsView';
import PortfolioView from './components/PortfolioView';
import RiskManagementView from './components/RiskManagementView';
import HistoryView from './components/HistoryView';
import SettingsView from './components/SettingsView';
import Notifications from './components/Notifications';
import './styles/App.css';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [notifications, setNotifications] = useState([]);

  // Simulate receiving notifications
  useEffect(() => {
    // Example: Add a welcome notification on mount
    addNotification('Welcome to HORUS!', 'Your AI-powered trading platform is ready.', 'success');
  }, []);

  const addNotification = (title, message, type = 'info') => {
    const notification = {
      id: Date.now(),
      title,
      message,
      type, // 'success', 'warning', 'error', 'info'
      timestamp: new Date(),
    };

    setNotifications((prev) => [notification, ...prev].slice(0, 5)); // Keep last 5

    // Auto-remove after 5 seconds
    setTimeout(() => {
      removeNotification(notification.id);
    }, 5000);
  };

  const removeNotification = (id) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  };

  const renderView = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard />;
      case 'charts':
        return <ChartsView />;
      case 'signals':
        return <SignalsView />;
      case 'portfolio':
        return <PortfolioView />;
      case 'risk':
        return <RiskManagementView />;
      case 'history':
        return <HistoryView />;
      case 'settings':
        return <SettingsView />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="app">
      <TitleBar />
      <div className="app-layout">
        <Sidebar currentView={currentView} onViewChange={setCurrentView} />
        <div className="app-content">
          {renderView()}
        </div>
      </div>
      <Notifications notifications={notifications} onRemove={removeNotification} />
    </div>
  );
}

export default App;
