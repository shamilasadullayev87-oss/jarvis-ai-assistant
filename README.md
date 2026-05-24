# 🤖 JARVIS - Advanced AI Assistant

A fully autonomous AI assistant running locally on your laptop with voice control, memory, custom commands, and system integration.

**Features:**
- 🎤 **Voice I/O**: Wake word detection ("Hey Jarvis"), Whisper STT, pyttsx3 TTS
- 🌍 **Multilingual**: Auto-detect and respond in any language
- 💾 **Memory System**: SQLite database stores all conversations and preferences
- ⚡ **System Control**: Open apps, control volume/brightness, run commands
- 🌐 **Browser Automation**: Search, navigate websites automatically
- 📰 **Real-time News**: Fetch and announce news every 30 minutes
- 🎯 **Custom Commands**: Teach JARVIS new commands at runtime
- 🚀 **Auto-start**: Boot with your system (Windows/Linux)

---

## 📋 Requirements

- **Python**: 3.9+
- **OS**: Windows 10/11 or Ubuntu 22+
- **Hardware**: 
  - 4GB+ RAM
  - Microphone + Speakers
  - Internet connection

**API Keys (Free tiers available):**
- OpenAI: https://platform.openai.com/api-keys
- NewsAPI: https://newsapi.org

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/shamilasadullayev87-oss/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

### 2. Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 5. Run JARVIS

```bash
python jarvis.py
```

When you see `Listening for 'Hey Jarvis'...`, say **"Hey Jarvis"** followed by your command.

---

## 💬 Example Commands

### Basic
- "Hey Jarvis, what time is it?"
- "Hey Jarvis, hello"
- "Hey Jarvis, goodbye"

### Applications
- "Open Chrome"
- "Launch VSCode"
- "Start Spotify"

### System Control
- "Increase volume"
- "Decrease brightness"
- "Shut down"

### Information
- "What's the news?"
- "Search for Python tutorials"
- "Tell me about machine learning"

### Learning
- "When I say 'goodnight', turn off WiFi"
- "Remember: when I say 'focus' close all browsers"

---

## 📁 Project Structure

```
jarvis-ai-assistant/
├── jarvis.py                 # Main entry point
├── setup.py                  # Installation & configuration
├── requirements.txt          # Python dependencies
├── .env.example             # Configuration template
├── README.md                # This file
│
├── modules/
│   ├── core/
│   │   ├── jarvis_core.py        # Main orchestrator
│   │   ├── voice_engine.py       # STT/TTS/Wake word
│   │   ├── memory_system.py      # SQLite database
│   │   └── command_processor.py  # Command handling
│   │
│   └── features/
│       ├── news_reader.py       # News API integration
│       ├── browser_control.py   # Web automation
│       └── system_control.py    # OS commands
│
├── data/
│   ├── jarvis_memory.db      # Conversation database
│   └── custom_commands.json  # User-defined commands
│
├── logs/
│   └── jarvis.log           # Application log
│
└── backups/
    └── jarvis_memory_*.db   # Database backups
```

---

## ⚙️ Configuration

### .env File Options

```env
# API Keys
OPENAI_API_KEY=your_key
NEWS_API_KEY=your_key
ELEVENLABS_API_KEY=your_key

# System
USER_NAME=Sir
USER_LANGUAGE=en
AUTO_START_ON_BOOT=true

# Voice
WHISPER_MODEL=base
TTS_ENGINE=pyttsx3
TTS_VOICE=default

# News
NEWS_UPDATE_INTERVAL=1800
NEWS_COUNTRY=us

# Debug
DEBUG=false
LOG_LEVEL=INFO
```

---

## 🐧 Linux Installation

### Ubuntu/Debian

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3.9 python3.9-venv python3.9-dev
sudo apt-get install portaudio19-dev
sudo apt-get install espeak

# Clone and setup
git clone https://github.com/shamilasadullayev87-oss/jarvis-ai-assistant.git
cd jarvis-ai-assistant
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python jarvis.py
```

### Auto-start as Service

```bash
systemctl --user enable jarvis
systemctl --user start jarvis
systemctl --user status jarvis
```

---

## 🪟 Windows Installation

### PowerShell

```powershell
# Clone
git clone https://github.com/shamilasadullayev87-oss/jarvis-ai-assistant.git
cd jarvis-ai-assistant

# Setup
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Run
python jarvis.py
```

### Auto-start via Task Scheduler

1. Open Task Scheduler
2. Create Basic Task → "JARVIS"
3. Trigger: "At log on"
4. Action: `python C:\path\to\jarvis.py`

---

## 🔐 Security

- **Local Processing**: Conversations stored locally, not sent to cloud
- **API Keys**: Keep `.env` file secure, never commit to Git
- **Microphone**: Only active during listening
- **Data**: Regular backups in `backups/` directory

Add to `.gitignore`:
```
.env
*.db
logs/
data/
backups/
```

---

## 📊 Performance

**Typical Resource Usage:**
- CPU: 5-15% (idle)
- RAM: 150-300 MB
- Disk: 2-5 GB

---

## 🐛 Troubleshooting

### No Audio Input
```bash
python -c "import sounddevice as sd; print(sd.query_devices())"
```

### API Errors
- Check `.env` file has correct keys
- Verify API quotas and billing

### Memory Database Locked
```bash
rm data/jarvis_memory.db
```

---

## 📝 Logs

View logs:
```bash
tail -f logs/jarvis.log
```

---

## 🤝 Contributing

Contributions welcome!

---

## 📄 License

MIT License

---

**Made with ❤️ by Shamil Asadullayev**

Star ⭐ if you find this project useful!
