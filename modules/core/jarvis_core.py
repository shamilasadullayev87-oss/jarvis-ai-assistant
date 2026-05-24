"""
JARVIS Core Engine - Main Orchestrator
"""

import os
import json
import logging
from datetime import datetime
from threading import Thread, Event
import time

from .voice_engine import VoiceEngine
from .memory_system import MemorySystem
from .command_processor import CommandProcessor
from modules.features.news_reader import NewsReader
from modules.features.system_control import SystemControl

logger = logging.getLogger(__name__)

class JARVIS:
    def __init__(self):
        """Initialize JARVIS"""
        logger.info("Initializing JARVIS Core...")
        
        self.user_name = os.getenv("USER_NAME", "Sir")
        self.listening = True
        self.stop_event = Event()
        
        # Initialize subsystems
        logger.info("Loading voice engine...")
        self.voice_engine = VoiceEngine()
        
        logger.info("Loading memory system...")
        self.memory = MemorySystem()
        
        logger.info("Loading command processor...")
        self.command_processor = CommandProcessor(self.memory)
        
        logger.info("Loading news reader...")
        self.news_reader = NewsReader()
        
        logger.info("Loading system control...")
        self.system_control = SystemControl()
        
        logger.info(f"JARVIS initialized. Welcome, {self.user_name}!")
    
    def start(self):
        """Start JARVIS assistant"""
        logger.info("JARVIS is now active")
        self.voice_engine.speak(f"Good morning, {self.user_name}. I am JARVIS, at your service.")
        
        # Start background threads
        news_thread = Thread(target=self._news_loop, daemon=True)
        news_thread.start()
        
        # Main listening loop
        self._main_loop()
    
    def _main_loop(self):
        """Main listening and processing loop"""
        self.voice_engine.speak("Listening for your commands.")
        
        while self.listening:
            try:
                # Listen for wake word
                logger.info("Waiting for wake word 'Hey Jarvis'...")
                self.voice_engine.listen_for_wakeword()
                
                # Get user input
                user_input = self.voice_engine.listen()
                if not user_input:
                    continue
                
                logger.info(f"User said: {user_input}")
                
                # Detect language
                language = self.voice_engine.detect_language(user_input)
                logger.info(f"Detected language: {language}")
                
                # Process command
                response = self._process_command(user_input, language)
                
                # Save to memory
                self.memory.add_interaction(user_input, response, language)
                
                # Speak response in detected language
                self.voice_engine.speak(response, language=language)
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                try:
                    self.voice_engine.speak("Sorry, I encountered an error. Please try again.")
                except:
                    pass
    
    def _process_command(self, user_input: str, language: str) -> str:
        """Process user command"""
        
        # Check for custom commands first
        custom_response = self.command_processor.check_custom_commands(user_input)
        if custom_response:
            return custom_response
        
        # Check for learning new commands
        if any(phrase in user_input.lower() for phrase in ["when i say", "remember", "teach me"]):
            return self.command_processor.learn_command(user_input)
        
        # Process standard commands
        return self.command_processor.process(user_input, language)
    
    def _news_loop(self):
        """Background thread for news updates"""
        update_interval = int(os.getenv("NEWS_UPDATE_INTERVAL", 1800))  # 30 minutes
        
        while self.listening:
            try:
                time.sleep(update_interval)
                logger.info("Fetching news update...")
                headlines = self.news_reader.get_top_headlines(5)
                
                if headlines:
                    news_text = "Breaking news: " + ". ".join(headlines[:3])
                    self.voice_engine.speak(news_text)
                    logger.info(f"News announced: {news_text}")
            
            except Exception as e:
                logger.error(f"Error in news loop: {e}")
    
    def shutdown(self):
        """Graceful shutdown"""
        logger.info("Shutting down JARVIS...")
        self.listening = False
        try:
            self.voice_engine.speak(f"Goodbye, {self.user_name}. Until next time.")
        except:
            pass
        self.stop_event.set()
