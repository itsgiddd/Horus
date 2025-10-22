import React from 'react';
import './TitleBar.css';

function TitleBar() {
  const handleMinimize = () => {
    if (window.electron) {
      window.electron.minimize();
    }
  };

  const handleMaximize = () => {
    if (window.electron) {
      window.electron.maximize();
    }
  };

  const handleClose = () => {
    if (window.electron) {
      window.electron.close();
    }
  };

  return (
    <div className="title-bar glass" style={{ WebkitAppRegion: 'drag' }}>
      <div className="title-bar-left">
        <span className="app-icon">𓂀</span>
        <span className="app-title">HORUS</span>
        <span className="app-subtitle">Trading Platform</span>
      </div>

      <div className="title-bar-center">
        {/* Add navigation items here in the future */}
      </div>

      <div className="title-bar-right" style={{ WebkitAppRegion: 'no-drag' }}>
        <button className="title-bar-btn" onClick={handleMinimize} aria-label="Minimize">
          <svg width="12" height="12" viewBox="0 0 12 12">
            <rect x="0" y="5" width="12" height="2" fill="currentColor" />
          </svg>
        </button>
        <button className="title-bar-btn" onClick={handleMaximize} aria-label="Maximize">
          <svg width="12" height="12" viewBox="0 0 12 12">
            <rect x="1" y="1" width="10" height="10" fill="none" stroke="currentColor" strokeWidth="2" />
          </svg>
        </button>
        <button className="title-bar-btn close" onClick={handleClose} aria-label="Close">
          <svg width="12" height="12" viewBox="0 0 12 12">
            <path d="M1 1L11 11M11 1L1 11" stroke="currentColor" strokeWidth="2" />
          </svg>
        </button>
      </div>
    </div>
  );
}

export default TitleBar;
