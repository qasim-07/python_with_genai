
import logging
import os
import sys
from typing import Optional
from datetime import datetime

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> None:
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    root_logger.handlers.clear()
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not create log file {log_file}: {e}")
    
    logging.getLogger("urllib3").setLevel(logging.WARNING)  # Reduce noise from requests
    logging.getLogger("requests").setLevel(logging.WARNING)

def display_banner() -> None:
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🤖 Intelligent Query Router 🤖                           ║
║                                                                              ║
║  A Python AI Project that automatically routes your questions to the        ║
║  best tool: Google Search for facts or AI Language Model for analysis       ║
║                                                                              ║
║  🎯 Features:                                                                ║
║     • Smart query classification                                             ║
║     • Google Search integration                                              ║
║     • OpenAI LLM integration                                                 ║
║     • Automatic tool selection                                               ║
║     • Real-time web scraping                                                ║
║                                                                              ║                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def validate_environment() -> bool:

    required_vars = ['OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   • {var}")
        print("\nPlease set these variables before running the application.")
        print("Example:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    return True

def format_timestamp(timestamp: Optional[datetime] = None) -> str:

    if timestamp is None:
        timestamp = datetime.now()
    
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:

    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def print_separator(char: str = "=", length: int = 60) -> None:
    print(char * length)
