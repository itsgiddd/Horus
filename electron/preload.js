const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electron', {
  // Window controls
  minimize: () => ipcRenderer.send('window-minimize'),
  maximize: () => ipcRenderer.send('window-maximize'),
  close: () => ipcRenderer.send('window-close'),

  // Platform info
  platform: process.platform,

  // Backend control
  backend: {
    start: () => ipcRenderer.send('start-backend'),
    stop: () => ipcRenderer.send('stop-backend'),
    check: () => ipcRenderer.send('check-backend'),
    onStatus: (callback) => {
      ipcRenderer.on('backend-status', (event, data) => callback(data));
    },
    removeListener: () => {
      ipcRenderer.removeAllListeners('backend-status');
    },
  },

  // API for Python backend communication
  api: {
    send: (channel, data) => {
      const validChannels = ['get-signals', 'get-market-data', 'update-settings'];
      if (validChannels.includes(channel)) {
        ipcRenderer.send(channel, data);
      }
    },
    receive: (channel, func) => {
      const validChannels = ['signals-update', 'market-data-update', 'settings-updated'];
      if (validChannels.includes(channel)) {
        ipcRenderer.on(channel, (event, ...args) => func(...args));
      }
    },
  },
});
