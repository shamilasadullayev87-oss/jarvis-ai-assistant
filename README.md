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

## 🎯 **QUICK START (One Click!)**

### **Windows Users:**

1. **Double-click:** `start_jarvis.bat`
2. **Wait** for installation (first time only)
3. **Say:** "Hey Jarvis" + your command

### **Linux/macOS Users:**

```bash
chmod +x start_jarvis.sh
./start_jarvis.sh
```

That's it! ✅

---

## 📝 **Setup (If you want to configure first)**

### **Windows:**
Double-click `setup_windows.bat` to configure API keys before running

### **Linux/macOS:**
```bash
chmod +x setup_linux.sh
./setup_linux.sh
```

---

## 🔑 **Get API Keys (5 minutes)**

1. **OpenAI**: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy to `.env`

2. **NewsAPI**: https://newsapi.org/register
   - Free sign up
   - Copy key to `.env`

---

## 🎤 **Use JARVIS**

Say these commands:
- "Hey Jarvis, what time is it?"
- "Hey Jarvis, open Chrome"
- "Hey Jarvis, what's the news?"
- "Hey Jarvis, increase volume"
- "Hey Jarvis, search for Python tutorials"

---

## 📋 Requirements

- **Python**: 3.9+
- **OS**: Windows 10/11 or Ubuntu 22+
- **Hardware**: Microphone + Speakers + 4GB RAM

---

## 🐛 Troubleshooting

### "Python not found"
- Download: https://www.python.org/
- Check "Add Python to PATH"

### "No audio input"
- Check microphone is connected and enabled
- Run: `python -c "import sounddevice as sd; print(sd.query_devices())"`

### "API key errors"
- Edit `.env` file
- Paste correct keys from websites above

---

## 📂 Files Explained

| File | Purpose |
|------|----------|
| `start_jarvis.bat` | Windows: Click to run JARVIS |
| `start_jarvis.sh` | Linux/macOS: Run JARVIS |
| `setup_windows.bat` | Windows: Configure settings |
| `setup_linux.sh` | Linux/macOS: Configure settings |
| `.env` | Your API keys (created automatically) |
| `jarvis.py` | Main application |

---

## 💻 Full Manual Setup (If you prefer)

### Windows:
```powershell
git clone https://github.com/shamilasadullayev87-oss/jarvis-ai-assistant.git
cd jarvis-ai-assistant
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
REM Edit .env with your API keys
python jarvis.py
```

### Linux:
```bash
git clone https://github.com/shamilasadullayev87-oss/jarvis-ai-assistant.git
cd jarvis-ai-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python jarvis.py
```

---

## 📊 Project Structure

```
jarvis-ai-assistant/
├── start_jarvis.bat          ⭐ Windows: One-click launcher
├── start_jarvis.sh           ⭐ Linux/macOS: One-click launcher
├── setup_windows.bat         Setup for Windows
├── setup_linux.sh            Setup for Linux
├── jarvis.py                 Main application
├── requirements.txt          Dependencies
├── .env.example              Configuration template
├── README.md                 This file
└── modules/                  Application code
```

---

## ⌨️ Voice Commands Examples

**Time & Date:**
- "What time is it?"
- "What's today's date?"

**System Control:**
- "Open Chrome"
- "Close Spotify"
- "Increase volume"
- "Decrease brightness"
- "Sleep mode"

**Information:**
- "What's the news?"
- "Search for Python tutorials"
- "Find information about AI"

**Learning:**
- "When I say goodnight, turn off WiFi"
- "Remember: when I say focus, close all browsers"

---

## 🔐 Security

- API keys stored locally in `.env` (never shared)
- Database stored locally (not cloud)
- Add `.env` to `.gitignore` (already done)

---

## 📞 Support

If something doesn't work:
1. Check that Python 3.9+ is installed
2. Make sure API keys are in `.env`
3. Check microphone is connected
4. Look at `logs/jarvis.log` for errors

---

## ✨ Made with ❤️

By: Shamil Asadullayev  
Repo: https://github.com/shamilasadullayev87-oss/jarvis-ai-assistant

⭐ **Star this repo if you like it!**
