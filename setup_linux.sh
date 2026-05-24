#!/bin/bash
# JARVIS Setup Script - One Click Setup for Linux/macOS

echo ""
echo "============================================"
echo "     JARVIS AI Assistant - Setup Wizard"
echo "============================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found!"
    echo "Install with: sudo apt-get install python3 python3-venv"
    exit 1
fi

echo "Step 1: Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

echo "Step 2: Installing dependencies..."
pip install -q -r requirements.txt

echo "Step 3: Creating .env file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Edit .env with your API keys!"
    echo ""
    nano .env
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next: Run ./start_jarvis.sh to run JARVIS"
