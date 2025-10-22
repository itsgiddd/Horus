import React from 'react';
import './Sidebar.css';

function Sidebar({ currentView, onViewChange }) {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'charts', label: 'Charts', icon: '📈' },
    { id: 'signals', label: 'Signals', icon: '⚡' },
    { id: 'portfolio', label: 'Portfolio', icon: '💼' },
    { id: 'risk', label: 'Risk Management', icon: '🛡️' },
    { id: 'history', label: 'History', icon: '📜' },
    { id: 'settings', label: 'Settings', icon: '⚙️' },
  ];

  return (
    <div className="sidebar glass">
      <div className="sidebar-header">
        <div className="logo">
          <span className="logo-icon">𓂀</span>
          <span className="logo-text">HORUS</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${currentView === item.id ? 'active' : ''}`}
            onClick={() => onViewChange(item.id)}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="status-indicator">
          <span className="status-dot online"></span>
          <span className="status-text">Connected</span>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;
