#!/usr/bin/env python3
"""
JARVIS - Advanced AI Assistant
Main entry point
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Setup paths
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment
load_dotenv(PROJECT_ROOT / ".env")

# Create directories
for dir_path in [PROJECT_ROOT / "logs", PROJECT_ROOT / "data", PROJECT_ROOT / "backups"]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(PROJECT_ROOT / "logs" / "jarvis.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

from modules.core.jarvis_core import JARVIS

def main():
    """Main entry point"""
    logger.info("Starting JARVIS AI Assistant...")
    
    try:
        jarvis = JARVIS()
        jarvis.start()
    except KeyboardInterrupt:
        logger.info("JARVIS shutting down...")
        print("\nGoodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
