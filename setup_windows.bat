@echo off
REM JARVIS Setup Script - One Click Setup for Windows

color 0B
echo.
echo ============================================
echo     JARVIS AI Assistant - Setup Wizard
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Step 1: Creating virtual environment...
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat

echo Step 2: Installing dependencies...
pip install -q -r requirements.txt

echo Step 3: Creating .env file...
if not exist ".env" (
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit .env with your API keys!
    echo.
    notepad .env
)

echo.
echo Setup complete!
echo.
echo Next: Double-click start_jarvis.bat to run JARVIS
pause
