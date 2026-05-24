"""
System Control - OS Integration
"""

import logging
import platform
import subprocess
import os
import time

logger = logging.getLogger(__name__)

class SystemControl:
    def __init__(self):
        """Initialize system control"""
        self.os_name = platform.system()
        logger.info(f"System: {self.os_name}")
    
    def open_application(self, app_name: str) -> bool:
        """Open application"""
        try:
            app_name = app_name.lower().strip()
            
            if self.os_name == "Windows":
                # Windows app names
                app_map = {
                    "chrome": "chrome.exe",
                    "firefox": "firefox.exe",
                    "vscode": "code.exe",
                    "notepad": "notepad.exe",
                    "spotify": "spotify.exe",
                    "vlc": "vlc.exe",
                    "edge": "msedge.exe"
                }
                
                cmd = app_map.get(app_name, app_name + ".exe")
                subprocess.Popen(cmd, shell=True)
            
            elif self.os_name == "Linux":
                subprocess.Popen([app_name])
            
            elif self.os_name == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", app_name])
            
            logger.info(f"Opened: {app_name}")
            return True
        
        except Exception as e:
            logger.error(f"Error opening {app_name}: {e}")
            return False
    
    def close_application(self, app_name: str) -> bool:
        """Close application"""
        try:
            if self.os_name == "Windows":
                subprocess.run(f"taskkill /IM {app_name}.exe /F", shell=True)
            elif self.os_name == "Linux":
                subprocess.run(["killall", app_name])
            elif self.os_name == "Darwin":
                subprocess.run(["killall", app_name])
            
            return True
        except Exception as e:
            logger.error(f"Error closing {app_name}: {e}")
            return False
    
    def set_volume(self, action: str):
        """Control volume"""
        try:
            if self.os_name == "Windows":
                if action == "+":
                    os.system("powershell -Command [Windows.Media.SystemMediaTransportControls]::VolumeUp")
                elif action == "-":
                    os.system("powershell -Command [Windows.Media.SystemMediaTransportControls]::VolumeDown")
            
            elif self.os_name == "Linux":
                if action == "+":
                    subprocess.run(["amixer", "sset", "Master", "5%+"])
                elif action == "-":
                    subprocess.run(["amixer", "sset", "Master", "5%-"])
                elif action == "mute":
                    subprocess.run(["amixer", "sset", "Master", "toggle"])
        
        except Exception as e:
            logger.error(f"Volume error: {e}")
    
    def set_brightness(self, action: str):
        """Control brightness"""
        try:
            if self.os_name == "Linux":
                brightness_path = "/sys/class/backlight/intel_backlight/brightness"
                
                if os.path.exists(brightness_path):
                    with open(brightness_path, 'r') as f:
                        current = int(f.read().strip())
                    
                    if action == "+":
                        new_brightness = min(current + 50, 400)
                    else:
                        new_brightness = max(current - 50, 50)
                    
                    os.system(f"echo {new_brightness} | sudo tee {brightness_path} > /dev/null")
        
        except Exception as e:
            logger.error(f"Brightness error: {e}")
    
    def shutdown(self):
        """Shutdown system"""
        try:
            if self.os_name == "Windows":
                subprocess.run("shutdown /s /t 30", shell=True)
            elif self.os_name == "Linux":
                subprocess.run(["sudo", "shutdown", "-h", "now"])
            elif self.os_name == "Darwin":
                subprocess.run(["osascript", "-e", "tell app \"System Events\" to shut down"])
        except Exception as e:
            logger.error(f"Shutdown error: {e}")
    
    def sleep(self):
        """Put system to sleep"""
        try:
            if self.os_name == "Windows":
                subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
            elif self.os_name == "Linux":
                subprocess.run(["systemctl", "suspend"])
            elif self.os_name == "Darwin":
                subprocess.run(["osascript", "-e", "tell app \"System Events\" to sleep"])
        except Exception as e:
            logger.error(f"Sleep error: {e}")
