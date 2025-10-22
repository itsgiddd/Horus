import React from 'react';
import './Notifications.css';

function Notifications({ notifications, onRemove }) {
  if (!notifications || notifications.length === 0) {
    return null;
  }

  const getIcon = (type) => {
    switch (type) {
      case 'success':
        return '✓';
      case 'warning':
        return '⚠';
      case 'error':
        return '✕';
      case 'info':
      default:
        return 'ℹ';
    }
  };

  return (
    <div className="notifications-container">
      {notifications.map((notification) => (
        <div key={notification.id} className={`notification glass ${notification.type}`}>
          <div className="notification-icon">{getIcon(notification.type)}</div>
          <div className="notification-content">
            <div className="notification-title">{notification.title}</div>
            <div className="notification-message">{notification.message}</div>
          </div>
          <button
            className="notification-close"
            onClick={() => onRemove(notification.id)}
            aria-label="Close notification"
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  );
}

export default Notifications;
