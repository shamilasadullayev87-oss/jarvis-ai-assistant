#!/bin/bash
# JARVIS AI Assistant - One Click Launcher for Linux/macOS
# This script sets up and runs JARVIS automatically

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

clear

echo -e "${GREEN}"
echo "============================================"
echo "     JARVIS AI Assistant - Quick Start"
echo "============================================"
echo -e "${NC}"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python3 is not installed${NC}"
    echo "Please install Python3:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-venv"
    echo "  macOS: brew install python3"
    exit 1
fi

echo -e "${GREEN}[1/4] Checking Python...${NC}"
python3 --version
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo -e "${GREEN}[2/4] Creating virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: Could not create virtual environment${NC}"
        exit 1
    fi
    echo "Virtual environment created!"
else
    echo -e "${GREEN}[2/4] Virtual environment already exists${NC}"
fi
echo ""

# Activate venv
echo -e "${GREEN}[3/4] Activating virtual environment and installing dependencies...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Could not activate virtual environment${NC}"
    exit 1
fi

# Install system dependencies for Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Installing system audio dependencies..."
    sudo apt-get update -qq
    sudo apt-get install -qq -y portaudio19-dev espeak ffmpeg 2>/dev/null
fi

# Install requirements
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}WARNING: Some dependencies may not have installed correctly${NC}"
    echo "Continuing anyway..."
fi
echo "Dependencies installed!"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${GREEN}[4/4] Creating .env file...${NC}"
    cp .env.example .env
    echo ""
    echo -e "${YELLOW}WARNING: .env file created, but API keys are REQUIRED!${NC}"
    echo ""
    echo "Please edit .env and add your API keys:"
    echo "  - OPENAI_API_KEY from https://platform.openai.com/api-keys"
    echo "  - NEWS_API_KEY from https://newsapi.org"
    echo ""
    echo "Opening .env in nano..."
    sleep 2
    nano .env
    echo ""
else
    echo -e "${GREEN}[4/4] .env file already exists${NC}"
fi

echo ""
echo -e "${GREEN}"
echo "============================================"
echo "     Starting JARVIS AI Assistant..."
echo "============================================"
echo -e "${NC}"
echo ""
echo "Say 'Hey Jarvis' followed by your command!"
echo ""

# Run JARVIS
python jarvis.py
