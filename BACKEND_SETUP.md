# HORUS Backend Setup Guide

This guide explains how the HORUS app connects to the backend and how to set it up properly.

## Automatic Backend Connection

The HORUS Electron app **automatically detects and connects** to the Python backend. You don't need to manually start the backend in most cases!

### How It Works

1. **On App Launch:**
   - App checks if backend is running at `http://127.0.0.1:5000`
   - If backend is found, app connects immediately
   - If backend is not found, app attempts to start it automatically

2. **Backend Search Locations:**
   The app searches for the backend in these locations:
   - `~/Downloads/backend` (where most users extract it)
   - `~/backend` (user's home directory)
   - App's resource directory (production builds)
   - Development directory (when running in dev mode)

3. **Auto-Start Process:**
   - App locates the backend folder
   - Checks for virtual environment (`venv`)
   - Starts backend using: `venv/bin/python3 app.py` (or `venv/Scripts/python.exe app.py` on Windows)
   - Falls back to system Python if no venv found

4. **Connection Indicator:**
   - Bottom-right corner shows connection status
   - Green dot = Connected and running
   - Yellow dot = Starting backend
   - Blue dot = Checking connection
   - Red dot = Connection error

## Setup Methods

### Method 1: Automatic (Recommended)

**For most users, this is all you need:**

```bash
# 1. Extract backend to ~/Downloads
cd ~/Downloads
unzip horus_backend_20251023.zip

# 2. Install dependencies (one-time setup)
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. Launch HORUS app
# Backend will start automatically!
```

### Method 2: Manual Backend Start

If automatic start fails or you prefer manual control:

**Terminal 1 (Backend):**
```bash
cd ~/Downloads/backend
source venv/bin/activate
python app.py
```

**Terminal 2 (Frontend):**
```bash
# Launch HORUS app
open /Applications/HORUS.app
```

### Method 3: System-Wide Backend

For advanced users who want backend always available:

```bash
# Move backend to home directory
mv ~/Downloads/backend ~/backend

# Create alias for easy starting
echo 'alias horus-backend="cd ~/backend && source venv/bin/activate && python app.py"' >> ~/.zshrc

# Start backend anytime with:
horus-backend
```

## Backend Locations

The app searches these directories in order:

### macOS
1. `~/Downloads/backend` ✓ Most common
2. `~/backend`
3. `/Applications/HORUS.app/Contents/Resources/backend`
4. `~/Library/Application Support/HORUS/backend`

### Windows
1. `C:\Users\[YourName]\Downloads\backend` ✓ Most common
2. `C:\Users\[YourName]\backend`
3. `C:\Program Files\HORUS\resources\backend`
4. `%APPDATA%\HORUS\backend`

### Linux
1. `~/Downloads/backend` ✓ Most common
2. `~/backend`
3. `/opt/HORUS/resources/backend`
4. `~/.config/HORUS/backend`

## Troubleshooting

### "Backend not found" Error

**Solution 1: Check Backend Location**
```bash
# Verify backend exists
ls ~/Downloads/backend/app.py

# If not in Downloads, search for it
find ~ -name "app.py" -path "*/backend/app.py" 2>/dev/null
```

**Solution 2: Move Backend to Expected Location**
```bash
# Move backend to Downloads
mv /path/to/backend ~/Downloads/backend

# Restart HORUS app
```

**Solution 3: Manual Start**
```bash
# Start backend manually
cd ~/Downloads/backend
source venv/bin/activate
python app.py

# Keep this terminal open, launch HORUS in another window
```

### "Backend started but not responding" Error

**Possible causes:**
1. Python dependencies not installed
2. Port 5000 already in use
3. Virtual environment not activated

**Solution:**
```bash
cd ~/Downloads/backend

# Reinstall dependencies
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Check if port 5000 is in use
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Try starting manually to see error messages
python app.py
```

### "Module not found" Errors

**Solution:**
```bash
cd ~/Downloads/backend
source venv/bin/activate

# Reinstall all dependencies
pip install -r requirements.txt

# If specific module missing:
pip install flask flask-cors flask-socketio requests numpy pandas
```

### Backend Won't Stay Running

**Check Python version:**
```bash
python3 --version  # Should be 3.8 or higher
```

**Check app.py for errors:**
```bash
cd ~/Downloads/backend
source venv/bin/activate
python app.py  # Look for error messages
```

## Connection Status Indicator

The app shows backend status in the bottom-right corner:

| Icon | Status | Meaning |
|------|--------|---------|
| 🟢 Green Dot | Running | Backend connected and working |
| 🟡 Yellow Dot | Starting | Backend is starting up |
| 🔵 Blue Dot | Checking | Checking connection |
| 🔴 Red Dot | Error | Backend not available |

### What to Do for Each Status

**🟢 Running:** All good! Start trading.

**🟡 Starting:** Wait 5-10 seconds for backend to fully start.

**🔵 Checking:** App is looking for backend. Should resolve in 2-3 seconds.

**🔴 Error:**
1. Check error message
2. Click "Start Backend" button
3. If that fails, start backend manually

## Manual Controls

### In the App

Click the backend status indicator to see options:
- **Start Backend** - Manually trigger backend start
- **Stop Backend** - Stop the backend process
- **Retry Connection** - Check connection again

### Via Terminal

**Start Backend:**
```bash
cd ~/Downloads/backend
source venv/bin/activate
python app.py
```

**Stop Backend:**
- Press `Ctrl+C` in the terminal running the backend
- Or close the HORUS app (backend stops automatically)

**Check if Backend is Running:**
```bash
# macOS/Linux
lsof -i :5000

# Windows
netstat -ano | findstr :5000

# Via curl
curl http://127.0.0.1:5000/api/market/price/BTC
```

## Advanced Configuration

### Change Backend Port

Edit `backend/.env`:
```env
FLASK_PORT=5001  # Change from 5000 to 5001
```

Also update the frontend to connect to new port (requires rebuild).

### Run Backend as Service

**macOS (launchd):**
Create `~/Library/LaunchAgents/com.horus.backend.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.horus.backend</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/YOUR_USERNAME/backend/venv/bin/python3</string>
        <string>/Users/YOUR_USERNAME/backend/app.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Load service:
```bash
launchctl load ~/Library/LaunchAgents/com.horus.backend.plist
```

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create Basic Task
3. Name: "HORUS Backend"
4. Trigger: At log on
5. Action: Start program
6. Program: `C:\Users\YOUR_USERNAME\backend\venv\Scripts\python.exe`
7. Arguments: `app.py`
8. Start in: `C:\Users\YOUR_USERNAME\backend`

## FAQ

**Q: Do I need to start the backend every time?**
A: No! The HORUS app auto-starts the backend when you launch it.

**Q: Can I move the backend folder?**
A: Yes, but put it in a standard location (Downloads, home directory, or create a symlink).

**Q: Does the backend need internet?**
A: No for self-contained mode. Yes for live trading mode with OANDA/CryptoCompare APIs.

**Q: Can I run multiple instances?**
A: No, only one backend can run on port 5000 at a time.

**Q: How do I update the backend?**
A: Extract the new backend zip, reinstall dependencies, and restart.

**Q: Is the backend secure?**
A: It only listens on localhost (127.0.0.1), not accessible from network.

## Getting Help

If you encounter issues:

1. **Check the connection indicator** for error messages
2. **Try manual backend start** to see error output
3. **Check Python version** (must be 3.8+)
4. **Verify dependencies** are installed in venv
5. **Look for port conflicts** on port 5000

For more help, see:
- `backend/README.md` - Backend documentation
- `backend/INSTALL.md` - Installation guide
- GitHub Issues - Report bugs

---

**Built with vision. Powered by AI. 𓂀**
