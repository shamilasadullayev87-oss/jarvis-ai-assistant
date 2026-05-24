"""
Memory System - SQLite Database for Conversations
"""

import sqlite3
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import threading

logger = logging.getLogger(__name__)

class MemorySystem:
    def __init__(self, db_path: str = "data/jarvis_memory.db"):
        """Initialize memory system"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.lock = threading.Lock()
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        self._init_db()
        logger.info(f"Memory system initialized at {self.db_path}")
    
    def _init_db(self):
        """Initialize database tables"""
        with self.lock:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_input TEXT NOT NULL,
                    response TEXT NOT NULL,
                    language TEXT
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS custom_commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    trigger_phrase TEXT UNIQUE,
                    action TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.conn.commit()
    
    def add_interaction(self, user_input: str, response: str, language: str = "en"):
        """Store conversation interaction"""
        try:
            with self.lock:
                self.cursor.execute("""
                    INSERT INTO interactions (user_input, response, language)
                    VALUES (?, ?, ?)
                """, (user_input, response, language))
                self.conn.commit()
            logger.debug(f"Interaction stored: {user_input[:50]}...")
        except Exception as e:
            logger.error(f"Error storing interaction: {e}")
    
    def get_last_interactions(self, limit: int = 50) -> List[Dict]:
        """Retrieve last N interactions"""
        try:
            with self.lock:
                self.cursor.execute("""
                    SELECT timestamp, user_input, response, language
                    FROM interactions
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (limit,))
                
                interactions = []
                for row in self.cursor.fetchall():
                    interactions.append({
                        "timestamp": row[0],
                        "user_input": row[1],
                        "response": row[2],
                        "language": row[3]
                    })
                
                return interactions
        except Exception as e:
            logger.error(f"Error retrieving interactions: {e}")
            return []
    
    def save_preference(self, key: str, value: str):
        """Save user preference"""
        try:
            with self.lock:
                self.cursor.execute("""
                    INSERT OR REPLACE INTO preferences (key, value)
                    VALUES (?, ?)
                """, (key, value))
                self.conn.commit()
        except Exception as e:
            logger.error(f"Error saving preference: {e}")
    
    def get_preference(self, key: str, default=None):
        """Get user preference"""
        try:
            with self.lock:
                self.cursor.execute("""
                    SELECT value FROM preferences WHERE key = ?
                """, (key,))
                result = self.cursor.fetchone()
                return result[0] if result else default
        except Exception as e:
            logger.error(f"Error getting preference: {e}")
            return default
    
    def add_custom_command(self, trigger: str, action: str):
        """Add custom command"""
        try:
            with self.lock:
                self.cursor.execute("""
                    INSERT OR REPLACE INTO custom_commands (trigger_phrase, action)
                    VALUES (?, ?)
                """, (trigger.lower(), action))
                self.conn.commit()
            logger.info(f"Custom command added: {trigger}")
        except Exception as e:
            logger.error(f"Error adding custom command: {e}")
    
    def get_custom_commands(self) -> Dict[str, str]:
        """Get all custom commands"""
        try:
            with self.lock:
                self.cursor.execute("""
                    SELECT trigger_phrase, action FROM custom_commands
                """)
                return {row[0]: row[1] for row in self.cursor.fetchall()}
        except Exception as e:
            logger.error(f"Error retrieving custom commands: {e}")
            return {}
