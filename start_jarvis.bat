@echo off
REM JARVIS AI Assistant - One Click Launcher for Windows
REM This script sets up and runs JARVIS automatically

color 0A
echo.
echo ============================================
echo     JARVIS AI Assistant - Quick Start
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    echo Make sure to check 'Add Python to PATH' during installation
    pause
    exit /b 1
)

echo [1/4] Checking Python...
python --version
echo.

REM Check if venv exists
if not exist "venv" (
    echo [2/4] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Could not create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created!
) else (
    echo [2/4] Virtual environment already exists
)
echo.

REM Activate venv
echo [3/4] Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Could not activate virtual environment
    pause
    exit /b 1
)

REM Install requirements
pip install -q -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some dependencies may not have installed correctly
    echo Continuing anyway...
)
echo Dependencies installed!
echo.

REM Check if .env exists
if not exist ".env" (
    echo [4/4] Creating .env file...
    copy .env.example .env >nul
    echo.
    echo WARNING: .env file created, but API keys are REQUIRED!
    echo.
    echo Please edit .env and add your API keys:
    echo   - OPENAI_API_KEY from https://platform.openai.com/api-keys
    echo   - NEWS_API_KEY from https://newsapi.org
    echo.
    echo Opening .env in Notepad...
    timeout /t 2
    notepad .env
    echo.
) else (
    echo [4/4] .env file already exists
)

echo.
echo ============================================
echo     Starting JARVIS AI Assistant...
echo ============================================
echo.
echo Say 'Hey Jarvis' followed by your command!
echo.

REM Run JARVIS
python jarvis.py

pause
