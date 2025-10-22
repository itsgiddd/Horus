import React, { useState } from 'react';
import TitleBar from './components/TitleBar';
import Dashboard from './components/Dashboard';
import './styles/App.css';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');

  return (
    <div className="app">
      <TitleBar />
      <div className="app-container">
        {currentView === 'dashboard' && <Dashboard />}
      </div>
    </div>
  );
}

export default App;
