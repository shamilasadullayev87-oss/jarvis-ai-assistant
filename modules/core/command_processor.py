"""
Command Processor - Handle all user commands
"""

import logging
import subprocess
import os
import webbrowser
from typing import Optional
from pathlib import Path
from datetime import datetime

from .memory_system import MemorySystem
from modules.features.system_control import SystemControl
from modules.features.browser_control import BrowserControl
from modules.features.news_reader import NewsReader

logger = logging.getLogger(__name__)

class CommandProcessor:
    def __init__(self, memory: MemorySystem):
        """Initialize command processor"""
        self.memory = memory
        self.system_control = SystemControl()
        self.browser_control = BrowserControl()
        self.news_reader = NewsReader()
        
        # Load custom commands
        self.custom_commands = memory.get_custom_commands()
    
    def process(self, user_input: str, language: str = "en") -> str:
        """Process user command"""
        text = user_input.lower().strip()
        
        # Greeting
        if any(word in text for word in ["hello", "hi", "hey", "привет", "привіт", "hola", "bonjour"]):
            return self._handle_greeting()
        
        # System commands
        elif "open" in text:
            return self._handle_open(text)
        elif "close" in text:
            return self._handle_close(text)
        elif "volume" in text:
            return self._handle_volume(text)
        elif "brightness" in text:
            return self._handle_brightness(text)
        elif "time" in text or "what time" in text:
            return self._handle_time()
        elif "date" in text or "today" in text:
            return self._handle_date()
        
        # Browser commands
        elif "search" in text:
            return self._handle_search(text)
        elif "youtube" in text:
            return self._handle_youtube(text)
        elif "news" in text or "headlines" in text:
            return self._handle_news()
        
        # Power commands
        elif "shutdown" in text or "turn off" in text:
            return self._handle_shutdown()
        elif "sleep" in text or "lock" in text:
            return self._handle_sleep()
        
        # Fallback
        else:
            return self._handle_default(user_input)
    
    def check_custom_commands(self, user_input: str) -> Optional[str]:
        """Check if input matches any custom command"""
        text = user_input.lower()
        
        for trigger, action in self.custom_commands.items():
            if trigger in text:
                logger.info(f"Custom command matched: {trigger}")
                self._execute_custom_command(action)
                return f"Executing: {action}"
        
        return None
    
    def learn_command(self, user_input: str) -> str:
        """Learn new custom command"""
        try:
            # Parse: "When I say [trigger], [action]"
            if "when i say" in user_input.lower():
                parts = user_input.lower().split("when i say")
                if len(parts) >= 2:
                    parts = parts[1].split(",", 1)
                    if len(parts) == 2:
                        trigger = parts[0].strip().strip("'\"")
                        action = parts[1].strip().strip("'\"")
                        
                        self.memory.add_custom_command(trigger, action)
                        self.custom_commands[trigger] = action
                        
                        return f"Understood! I will now {action} when you say '{trigger}'"
        
        except Exception as e:
            logger.error(f"Error learning command: {e}")
        
        return "I didn't understand the command. Try: 'When I say [phrase], do [action]'"
    
    def _execute_custom_command(self, action: str):
        """Execute custom command action"""
        try:
            if "open" in action:
                app = action.replace("open", "").strip()
                self.system_control.open_application(app)
            elif "close" in action:
                app = action.replace("close", "").strip()
                self.system_control.close_application(app)
        except Exception as e:
            logger.error(f"Error executing custom command: {e}")
    
    def _handle_greeting(self) -> str:
        return "Hello, Sir! How can I assist you today?"
    
    def _handle_open(self, text: str) -> str:
        """Handle 'open' command"""
        app_name = text.replace("open", "").replace("hey jarvis", "").strip()
        
        if self.system_control.open_application(app_name):
            return f"Opening {app_name}..."
        else:
            return f"I couldn't open {app_name}. Application not found."
    
    def _handle_close(self, text: str) -> str:
        """Handle 'close' command"""
        app_name = text.replace("close", "").strip()
        
        if self.system_control.close_application(app_name):
            return f"Closed {app_name}."
        else:
            return f"Application not found."
    
    def _handle_volume(self, text: str) -> str:
        """Handle volume control"""
        if "increase" in text or "up" in text:
            self.system_control.set_volume("+")
            return "Volume increased."
        elif "decrease" in text or "down" in text:
            self.system_control.set_volume("-")
            return "Volume decreased."
        elif "mute" in text:
            self.system_control.set_volume("mute")
            return "Muted."
        
        return "What would you like me to do with the volume?"
    
    def _handle_brightness(self, text: str) -> str:
        """Handle brightness control"""
        if "increase" in text or "up" in text:
            self.system_control.set_brightness("+")
            return "Brightness increased."
        elif "decrease" in text or "down" in text:
            self.system_control.set_brightness("-")
            return "Brightness decreased."
        
        return "Brightness adjustment completed."
    
    def _handle_time(self) -> str:
        """Handle time request"""
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."
    
    def _handle_date(self) -> str:
        """Handle date request"""
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}."
    
    def _handle_search(self, text: str) -> str:
        """Handle Google search"""
        query = text.replace("search", "").replace("for", "").strip()
        self.browser_control.search_google(query)
        return f"Searching for {query}..."
    
    def _handle_youtube(self, text: str) -> str:
        """Handle YouTube"""
        query = text.replace("youtube", "").strip()
        self.browser_control.open_youtube(query)
        return f"Opening YouTube..."
    
    def _handle_news(self) -> str:
        """Handle news request"""
        headlines = self.news_reader.get_top_headlines(5)
        
        if headlines:
            return "Here are today's top headlines: " + ". ".join(headlines[:3])
        return "I couldn't fetch the news right now."
    
    def _handle_shutdown(self) -> str:
        """Handle shutdown"""
        logger.warning("Shutdown command received")
        self.system_control.shutdown()
        return "Shutting down the system..."
    
    def _handle_sleep(self) -> str:
        """Handle sleep/lock"""
        self.system_control.sleep()
        return "Going to sleep mode..."
    
    def _handle_default(self, user_input: str) -> str:
        """Default response using AI"""
        try:
            import openai
            
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key or api_key == "your_key_here":
                return "Please set your OpenAI API key in .env file to use this feature."
            
            openai.api_key = api_key
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are JARVIS, an intelligent AI assistant. Be concise and helpful. Max 2-3 sentences."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"Error in default handler: {e}")
            return "I'm not sure how to help with that. Could you clarify?"
