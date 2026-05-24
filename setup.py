#!/usr/bin/env python3
"""
JARVIS Setup Script - Installation and Configuration
"""

import os
import sys
from pathlib import Path
import subprocess
import platform

class Setup:
    def __init__(self):
        self.root = Path(__file__).parent
        self.env_file = self.root / ".env"
        self.log_dir = self.root / "logs"
        self.data_dir = self.root / "data"
        self.backups_dir = self.root / "backups"
    
    def run(self):
        """Run complete setup"""
        print("\n🤖 JARVIS AI Assistant - Setup")
        print("=" * 50)
        
        self._create_directories()
        self._install_dependencies()
        self._configure_env()
        self._download_models()
        self._setup_autostart()
        
        print("\n✅ Setup complete!")
        print("\n📋 Next steps:")
        print("  1. Edit .env file with your API keys")
        print("  2. Run: python jarvis.py")
        print("\n🎤 Say 'Hey Jarvis' to start!\n")
    
    def _create_directories(self):
        """Create required directories"""
        print("\n📁 Creating directories...")
        for dir_path in [self.log_dir, self.data_dir, self.backups_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {dir_path}")
    
    def _install_dependencies(self):
        """Install Python dependencies"""
        print("\n📦 Installing dependencies...")
        print("  (This may take a few minutes)")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "-r", str(self.root / "requirements.txt")
            ])
            print("  ✓ Dependencies installed")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print("  Try running: pip install -r requirements.txt")
    
    def _configure_env(self):
        """Configure environment variables"""
        print("\n⚙️  Configuring environment...")
        
        if not self.env_file.exists():
            print("  Creating .env file...")
            
            env_content = """# JARVIS Configuration

# API Keys (Get from respective platforms)
OPENAI_API_KEY=your_openai_key_here
NEWS_API_KEY=your_newsapi_key_here
PORCUPINE_ACCESS_KEY=your_porcupine_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here

# System
USER_NAME=Sir
USER_LANGUAGE=en
AUTO_START_ON_BOOT=true

# Voice
WHISPER_MODEL=base
TTS_ENGINE=coqui
TTS_VOICE=default

# News
NEWS_UPDATE_INTERVAL=1800
NEWS_COUNTRY=us

# Debug
DEBUG=false
LOG_LEVEL=INFO
"""
            
            self.env_file.write_text(env_content)
            print("  ✓ .env created (configure with your API keys)")
        
        else:
            print("  ✓ .env already exists")
    
    def _download_models(self):
        """Download AI models"""
        print("\n🤖 Downloading AI models...")
        print("  This may take a few minutes...")
        
        try:
            import whisper
            print("  Downloading Whisper model (base)...")
            whisper.load_model("base")
            print("  ✓ Whisper downloaded")
        except Exception as e:
            print(f"  ✗ Whisper error: {e}")
            print("  Models will download on first run")
    
    def _setup_autostart(self):
        """Setup auto-start on boot"""
        print("\n🚀 Auto-start configuration...")
        
        system = platform.system()
        
        if system == "Windows":
            self._setup_windows_autostart()
        elif system == "Linux":
            self._setup_linux_autostart()
        elif system == "Darwin":
            self._setup_macos_autostart()
    
    def _setup_windows_autostart(self):
        """Setup Windows Task Scheduler"""
        print("  Windows: Manual setup required")
        print("  Steps:")
        print("    1. Open Task Scheduler")
        print("    2. Create Basic Task → JARVIS")
        print("    3. Trigger: At log on")
        print(f"    4. Action: python {self.root}/jarvis.py")
    
    def _setup_linux_autostart(self):
        """Setup Linux systemd service"""
        print("  Linux: Creating systemd service...")
        
        python_path = sys.executable
        service_content = f"""[Unit]
Description=JARVIS AI Assistant
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory={self.root}
ExecStart={python_path} {self.root}/jarvis.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
        
        service_path = Path.home() / ".config/systemd/user/jarvis.service"
        service_path.parent.mkdir(parents=True, exist_ok=True)
        service_path.write_text(service_content)
        
        print(f"  ✓ Created {service_path}")
        print("\n  Enable with:")
        print("    systemctl --user enable jarvis")
        print("    systemctl --user start jarvis")
    
    def _setup_macos_autostart(self):
        """Setup macOS LaunchAgent"""
        print("  macOS: Manual setup required")
        print("  See documentation for LaunchAgent setup")

if __name__ == "__main__":
    setup = Setup()
    setup.run()
