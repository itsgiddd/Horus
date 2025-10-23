const { app, BrowserWindow, screen, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

let mainWindow;
let backendProcess = null;
let backendStatus = 'checking'; // checking, running, starting, stopped, error

function createWindow() {
  // Get primary display dimensions
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;

  mainWindow = new BrowserWindow({
    width: Math.floor(width * 0.8),
    height: Math.floor(height * 0.85),
    minWidth: 1200,
    minHeight: 700,
    frame: false, // Frameless for custom title bar
    transparent: true, // Enable transparency for frosted-glass effect
    backgroundColor: '#00000000', // Transparent background
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
    titleBarStyle: 'hidden',
    vibrancy: 'under-window', // macOS frosted-glass effect
    visualEffectState: 'active',
  });

  // Load the app
  const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist-vite/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Window control handlers
  ipcMain.on('window-minimize', () => {
    if (mainWindow) mainWindow.minimize();
  });

  ipcMain.on('window-maximize', () => {
    if (mainWindow) {
      if (mainWindow.isMaximized()) {
        mainWindow.unmaximize();
      } else {
        mainWindow.maximize();
      }
    }
  });

  ipcMain.on('window-close', () => {
    if (mainWindow) mainWindow.close();
  });

  // Start checking backend status
  checkBackendStatus();
}

// Check if backend is running
function checkBackendStatus() {
  const options = {
    hostname: '127.0.0.1',
    port: 5000,
    path: '/api/market/price/BTC',
    method: 'GET',
    timeout: 2000,
  };

  const req = http.request(options, (res) => {
    if (res.statusCode === 200 || res.statusCode === 404) {
      // Backend is running (200 = success, 404 = endpoint exists but route not found)
      updateBackendStatus('running');
    } else {
      // Backend returned unexpected status
      attemptStartBackend();
    }
  });

  req.on('error', () => {
    // Backend is not running, try to start it
    attemptStartBackend();
  });

  req.on('timeout', () => {
    req.destroy();
    attemptStartBackend();
  });

  req.end();
}

// Find backend directory
function findBackendPath() {
  const possiblePaths = [
    // When running from app bundle (production)
    path.join(process.resourcesPath, 'backend'),
    // When running in development
    path.join(__dirname, '..', 'backend'),
    // macOS: Check in user's Downloads
    path.join(app.getPath('downloads'), 'backend'),
    // macOS: Check in user's home directory
    path.join(app.getPath('home'), 'backend'),
    // Check in app's userData directory
    path.join(app.getPath('userData'), 'backend'),
  ];

  for (const backendPath of possiblePaths) {
    if (fs.existsSync(path.join(backendPath, 'app.py'))) {
      return backendPath;
    }
  }

  return null;
}

// Attempt to start the backend
function attemptStartBackend() {
  if (backendStatus === 'starting') return; // Already attempting to start

  const backendPath = findBackendPath();

  if (!backendPath) {
    updateBackendStatus('error', 'Backend not found. Please ensure the backend folder is installed.');
    return;
  }

  updateBackendStatus('starting');

  // Determine Python command (try python3, then python)
  const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';

  // Check if venv exists
  const venvPath = path.join(backendPath, 'venv');
  const venvExists = fs.existsSync(venvPath);

  let pythonExecutable;
  if (venvExists) {
    // Use venv Python
    if (process.platform === 'win32') {
      pythonExecutable = path.join(venvPath, 'Scripts', 'python.exe');
    } else {
      pythonExecutable = path.join(venvPath, 'bin', 'python3');
    }
  } else {
    // Use system Python
    pythonExecutable = pythonCmd;
  }

  // Start the backend process
  try {
    backendProcess = spawn(pythonExecutable, ['app.py'], {
      cwd: backendPath,
      stdio: ['ignore', 'pipe', 'pipe'],
      detached: false,
    });

    // Log backend output (for debugging)
    backendProcess.stdout.on('data', (data) => {
      console.log(`[Backend]: ${data.toString()}`);
      // Check if backend has started successfully
      if (data.toString().includes('Running on')) {
        updateBackendStatus('running');
      }
    });

    backendProcess.stderr.on('data', (data) => {
      console.error(`[Backend Error]: ${data.toString()}`);
    });

    backendProcess.on('close', (code) => {
      console.log(`Backend process exited with code ${code}`);
      backendProcess = null;
      if (backendStatus !== 'stopped') {
        updateBackendStatus('error', `Backend exited with code ${code}`);
      }
    });

    backendProcess.on('error', (err) => {
      console.error('Failed to start backend:', err);
      updateBackendStatus('error', `Failed to start backend: ${err.message}`);
    });

    // Give backend time to start, then verify
    setTimeout(() => {
      verifyBackendRunning();
    }, 3000);

  } catch (error) {
    console.error('Error starting backend:', error);
    updateBackendStatus('error', `Error starting backend: ${error.message}`);
  }
}

// Verify backend is actually running
function verifyBackendRunning() {
  const options = {
    hostname: '127.0.0.1',
    port: 5000,
    path: '/api/market/price/BTC',
    method: 'GET',
    timeout: 2000,
  };

  const req = http.request(options, (res) => {
    if (res.statusCode === 200 || res.statusCode === 404) {
      updateBackendStatus('running');
    } else {
      updateBackendStatus('error', 'Backend started but not responding correctly');
    }
  });

  req.on('error', () => {
    updateBackendStatus('error', 'Backend process started but HTTP endpoint not available');
  });

  req.on('timeout', () => {
    req.destroy();
    updateBackendStatus('error', 'Backend timeout');
  });

  req.end();
}

// Update backend status and notify renderer
function updateBackendStatus(status, message = '') {
  backendStatus = status;

  if (mainWindow && mainWindow.webContents) {
    mainWindow.webContents.send('backend-status', {
      status,
      message,
      timestamp: Date.now(),
    });
  }

  console.log(`Backend status: ${status}${message ? ' - ' + message : ''}`);
}

// Handle backend control from renderer
ipcMain.on('start-backend', () => {
  if (backendStatus !== 'running') {
    attemptStartBackend();
  }
});

ipcMain.on('stop-backend', () => {
  if (backendProcess) {
    updateBackendStatus('stopped');
    backendProcess.kill();
    backendProcess = null;
  }
});

ipcMain.on('check-backend', () => {
  checkBackendStatus();
});

// Cleanup on app quit
app.on('before-quit', () => {
  if (backendProcess) {
    console.log('Shutting down backend...');
    backendProcess.kill();
    backendProcess = null;
  }
});

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
