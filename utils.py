"""
Utilities Module

This module contains helper functions and utilities used throughout the project.
It demonstrates important Python concepts like:
- Logging configuration
- String formatting and display
- Environment variable handling
- File operations
- Data validation
"""

import logging
import os
import sys
from typing import Optional
from datetime import datetime

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> None:
    """
    Set up logging configuration for the application.
    
    This demonstrates:
    - Logging configuration
    - File and console handlers
    - Log formatting
    - Environment-based configuration
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file (Optional[str]): Optional log file path
    """
    # Convert string level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not create log file {log_file}: {e}")
    
    # Set specific logger levels
    logging.getLogger("urllib3").setLevel(logging.WARNING)  # Reduce noise from requests
    logging.getLogger("requests").setLevel(logging.WARNING)

def display_banner() -> None:
    """
    Display a welcome banner for the application.
    
    This demonstrates:
    - String formatting and alignment
    - ASCII art and visual design
    - Multi-line strings
    """
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
    """
    Validate that the required environment variables are set.
    
    This demonstrates:
    - Environment variable checking
    - Validation logic
    - User-friendly error messages
    
    Returns:
        bool: True if environment is valid, False otherwise
    """
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
    """
    Format a timestamp for display.
    
    This demonstrates:
    - Default parameter values
    - Datetime handling
    - String formatting
    
    Args:
        timestamp (Optional[datetime]): Timestamp to format. If None, uses current time.
        
    Returns:
        str: Formatted timestamp string
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length with a suffix.
    
    This demonstrates:
    - String manipulation
    - Default parameters
    - Conditional logic
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length before truncation
        suffix (str): Suffix to add when truncating
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def create_directory_if_not_exists(directory_path: str) -> bool:
    """
    Create a directory if it doesn't exist.
    
    This demonstrates:
    - File system operations
    - Error handling
    - Boolean return values
    
    Args:
        directory_path (str): Path to the directory
        
    Returns:
        bool: True if directory exists or was created, False if error
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {directory_path}: {e}")
        return False

def get_project_info() -> dict:
    """
    Get information about the current project.
    
    This demonstrates:
    - Dictionary creation
    - Module information
    - Version handling
    
    Returns:
        dict: Project information
    """
    return {
        "name": "Intelligent Query Router",
        "version": "1.0.0",
        "description": "A Python AI project that routes queries to Google Search or LLM",
        "author": "Python AI Educator",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "created": "2024"
    }

def display_help() -> None:
    """
    Display help information for the application.
    
    This demonstrates:
    - Multi-line string formatting
    - Help documentation
    - Usage examples
    """
    help_text = """
🔍 Intelligent Query Router - Help

USAGE:
    python main.py

DESCRIPTION:
    This application intelligently routes your questions to either Google Search
    or an AI Language Model based on the type of question.

EXAMPLES:
    • "What is the capital of India?" → Google Search
    • "Solve 2x + 5 = 15" → AI Language Model
    • "Explain machine learning" → AI Language Model
    • "Current weather in New York" → Google Search

FEATURES:
    • Automatic query classification
    • Real-time web search results
    • AI-powered analysis and explanations
    • Smart tool selection
    • Interactive command-line interface

SETUP:
    1. Install required packages: pip install -r requirements.txt
    2. Set your OpenAI API key: export OPENAI_API_KEY='your-key'
    3. Run the application: python main.py

COMMANDS:
    • Type any question to get an answer
    • Type 'quit', 'exit', or 'q' to stop
    • Press Ctrl+C to force quit

TROUBLESHOOTING:
    • Make sure you have an internet connection
    • Verify your OpenAI API key is valid
    • Check that all required packages are installed
    """
    print(help_text)

def print_separator(char: str = "=", length: int = 60) -> None:
    """
    Print a separator line.
    
    This demonstrates:
    - String repetition
    - Default parameters
    - Simple utility functions
    
    Args:
        char (str): Character to use for the separator
        length (int): Length of the separator line
    """
    print(char * length)
