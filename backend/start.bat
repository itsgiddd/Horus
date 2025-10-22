@echo off
REM HORUS Backend Startup Script for Windows

echo Starting HORUS Backend API...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo No .env file found. Copying from .env.example...
    copy .env.example .env
    echo Please edit .env and add your API keys!
)

REM Start the server
echo Starting Flask server...
python app.py

pause
