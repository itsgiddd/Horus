import React, { useState, useEffect } from 'react';
import './ExportPanel.css';

function ExportPanel() {
  const [packageInfo, setPackageInfo] = useState(null);
  const [downloading, setDownloading] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPackageInfo();
  }, []);

  const fetchPackageInfo = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/export/package-info');
      const data = await response.json();
      setPackageInfo(data);
    } catch (error) {
      console.error('Error fetching package info:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (endpoint, filename) => {
    setDownloading(endpoint);

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/export/${endpoint}`);

      if (!response.ok) {
        throw new Error('Download failed');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename || 'horus_export.zip';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Download error:', error);
      alert('Download failed. Please try again.');
    } finally {
      setDownloading(null);
    }
  };

  if (loading) {
    return (
      <div className="export-panel">
        <div className="loading-state">
          <div className="liquid-loading"></div>
          <p>Loading export options...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="export-panel">
      <div className="export-header">
        <h2>Export & Download</h2>
        <p className="export-description">
          Download trained models, backend source code, and configuration files
        </p>
      </div>

      <div className="export-grid">
        <div className="export-card glass-card">
          <div className="export-icon">🤖</div>
          <h3>Trained Models</h3>
          <p className="export-card-description">
            Download all trained AI diffusion models and metadata
          </p>

          <div className="export-stats">
            <div className="stat-item">
              <span className="stat-label">Models</span>
              <span className="stat-value">
                {packageInfo?.models?.count || 0}
              </span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Size</span>
              <span className="stat-value">
                {packageInfo?.models?.size_mb || 0} MB
              </span>
            </div>
          </div>

          {packageInfo?.models?.available ? (
            <button
              className="liquid-btn primary"
              onClick={() => handleDownload('models', 'horus_models.zip')}
              disabled={downloading === 'models'}
            >
              {downloading === 'models' ? (
                <>
                  <span className="liquid-loading"></span>
                  Downloading...
                </>
              ) : (
                'Download Models'
              )}
            </button>
          ) : (
            <div className="status-indicator warning">
              No models available
            </div>
          )}
        </div>

        <div className="export-card glass-card">
          <div className="export-icon">📦</div>
          <h3>Full Backend Package</h3>
          <p className="export-card-description">
            Complete backend source code with all modules and trained models
          </p>

          <div className="export-features">
            <div className="feature-tag">Python Source</div>
            <div className="feature-tag">AI Models</div>
            <div className="feature-tag">Configs</div>
          </div>

          <button
            className="liquid-btn primary"
            onClick={() => handleDownload('backend-full', 'horus_backend_full.zip')}
            disabled={downloading === 'backend-full'}
          >
            {downloading === 'backend-full' ? (
              <>
                <span className="liquid-loading"></span>
                Downloading...
              </>
            ) : (
              'Download Full Backend'
            )}
          </button>
        </div>

        <div className="export-card glass-card">
          <div className="export-icon">⚙️</div>
          <h3>Configuration Files</h3>
          <p className="export-card-description">
            Setup guide, requirements, and environment configuration
          </p>

          <div className="export-features">
            <div className="feature-tag">Setup Guide</div>
            <div className="feature-tag">Requirements</div>
            <div className="feature-tag">Scripts</div>
          </div>

          <button
            className="liquid-btn primary"
            onClick={() => handleDownload('config', 'horus_config.zip')}
            disabled={downloading === 'config'}
          >
            {downloading === 'config' ? (
              <>
                <span className="liquid-loading"></span>
                Downloading...
              </>
            ) : (
              'Download Config'
            )}
          </button>
        </div>

        <div className="export-card glass-card">
          <div className="export-icon">💾</div>
          <h3>Data Backup</h3>
          <p className="export-card-description">
            Training data, model metadata, and backup manifest
          </p>

          <div className="export-stats">
            <div className="stat-item">
              <span className="stat-label">Status</span>
              <span className={`status-indicator ${packageInfo?.backup?.available ? 'success' : 'warning'}`}>
                {packageInfo?.backup?.available ? 'Available' : 'No Data'}
              </span>
            </div>
          </div>

          {packageInfo?.backup?.available ? (
            <button
              className="liquid-btn primary"
              onClick={() => handleDownload('data-backup', 'horus_backup.zip')}
              disabled={downloading === 'data-backup'}
            >
              {downloading === 'data-backup' ? (
                <>
                  <span className="liquid-loading"></span>
                  Downloading...
                </>
              ) : (
                'Download Backup'
              )}
            </button>
          ) : (
            <button className="liquid-btn" disabled>
              No Backup Available
            </button>
          )}
        </div>
      </div>

      <div className="export-info glass-card">
        <h4>Export Information</h4>
        <div className="info-grid">
          <div className="info-item">
            <div className="info-icon">📁</div>
            <div className="info-content">
              <h5>File Format</h5>
              <p>All exports are provided as ZIP archives for easy distribution</p>
            </div>
          </div>

          <div className="info-item">
            <div className="info-icon">🔒</div>
            <div className="info-content">
              <h5>Security</h5>
              <p>API keys and sensitive data are not included in exports</p>
            </div>
          </div>

          <div className="info-item">
            <div className="info-icon">📝</div>
            <div className="info-content">
              <h5>Setup Guide</h5>
              <p>Configuration package includes detailed setup instructions</p>
            </div>
          </div>

          <div className="info-item">
            <div className="info-icon">🔄</div>
            <div className="info-content">
              <h5>Version Control</h5>
              <p>Each export includes timestamp for version tracking</p>
            </div>
          </div>
        </div>
      </div>

      <div className="export-usage glass-card">
        <h4>Usage Guide</h4>
        <ol className="usage-steps">
          <li>
            <strong>Models:</strong> Download to transfer trained models to another system or create backups
          </li>
          <li>
            <strong>Full Backend:</strong> Complete package for deploying on new servers or sharing with team
          </li>
          <li>
            <strong>Configuration:</strong> Quick setup files for installing HORUS backend on new machines
          </li>
          <li>
            <strong>Data Backup:</strong> Regular backups to protect your training data and model metadata
          </li>
        </ol>
      </div>
    </div>
  );
}

export default ExportPanel;
