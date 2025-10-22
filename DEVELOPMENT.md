# 🛠️ HORUS Development Guide

## Prerequisites

- **Node.js** (v18 or higher)
- **npm** (v9 or higher)
- **Git**

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Horus
```

2. Install dependencies:
```bash
npm install
```

## Development

Run the application in development mode:
```bash
npm run dev
```

This will:
- Start the Vite dev server on `http://localhost:5173`
- Launch the Electron app with hot-reload enabled
- Open DevTools automatically

## Building

### Build for current platform:
```bash
npm run build
```

### Build for macOS:
```bash
npm run build:mac
```

This creates:
- `.dmg` installer
- `.zip` archive

### Build for Windows:
```bash
npm run build:win
```

This creates:
- NSIS installer (`.exe`)
- Portable executable

### Build for both platforms:
```bash
npm run build:all
```

## Project Structure

```
Horus/
├── electron/              # Electron main process
│   ├── main.js           # Main process entry point
│   └── preload.js        # Preload script for IPC
├── src/                  # React application
│   ├── components/       # React components
│   │   ├── TitleBar.jsx  # Custom window controls
│   │   ├── Dashboard.jsx # Main dashboard
│   │   └── GlassCard.jsx # Reusable glass card
│   ├── styles/           # CSS stylesheets
│   │   ├── index.css     # Global styles & frosted-glass theme
│   │   └── App.css       # App-specific styles
│   ├── App.jsx           # Root React component
│   └── main.jsx          # React entry point
├── build/                # Build assets (icons, etc.)
├── dist-vite/            # Vite build output
├── package.json          # Dependencies & scripts
└── vite.config.js        # Vite configuration
```

## Key Features

### Frosted-Glass UI
The application uses a modern frosted-glass (glassmorphism) design with:
- Translucent backgrounds with backdrop blur
- Smooth animations and transitions
- Custom color gradients
- Responsive layout

### Custom Title Bar
Frameless window with custom controls for:
- Minimize
- Maximize/Restore
- Close

### Platform Support
- **macOS**: Uses native vibrancy effects
- **Windows**: Acrylic-style frosted-glass effect

## Customization

### Theme Colors
Edit `src/styles/index.css` to customize the color scheme:
```css
:root {
  --accent-primary: #00d4ff;
  --accent-secondary: #b967ff;
  /* ... more variables */
}
```

### Window Size
Edit `electron/main.js` to adjust the default window dimensions:
```javascript
width: Math.floor(width * 0.8),
height: Math.floor(height * 0.85),
```

## Next Steps

1. **Install dependencies** when network is available: `npm install`
2. **Add TradingView integration** for live charts
3. **Set up Python ML backend** for AI signals
4. **Integrate market data APIs** (OANDA, CryptoCompare)
5. **Add authentication system**
6. **Implement real-time WebSocket connections**

## Troubleshooting

### Electron fails to install
If you encounter network issues downloading Electron:
```bash
# Use a mirror
npm config set electron_mirror https://npm.taobao.org/mirrors/electron/
npm install
```

### App won't start
1. Clear node_modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

2. Check Node.js version:
```bash
node --version  # Should be v18+
```

### Build fails
Ensure you have the required build tools:
- **macOS**: Xcode Command Line Tools
- **Windows**: Windows Build Tools

## License

PROPRIETARY - See TERMS_OF_SERVICE.md for details.

---

**Built with vision. Powered by AI. 𓂀**
