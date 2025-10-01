#!/usr/bin/env python3
"""
Setup Script for Intelligent Query Router

This script helps set up the project environment and dependencies.
It demonstrates Python concepts like:
- Command-line argument parsing
- File operations
- Environment variable handling
- System integration
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_python_version():
    """
    Check if Python version is compatible.
    
    Returns:
        bool: True if compatible, False otherwise
    """
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """
    Install required dependencies from requirements.txt.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print("📦 Installing dependencies...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ pip not found. Please install pip first.")
        return False

def setup_environment():
    """
    Set up environment variables and configuration.
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("🔧 Setting up environment...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_content = """# Environment Variables Configuration
# Fill in your actual values

# OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your-openai-api-key-here

# Optional: OpenAI Model Configuration
OPENAI_MODEL=gpt-3.5-turbo

# Optional: Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=query_router.log
"""
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("✅ .env file created")
        print("⚠️  Please edit .env file and add your OpenAI API key")
    else:
        print("✅ .env file already exists")
    
    return True

def verify_setup():
    """
    Verify that the setup is complete and working.
    
    Returns:
        bool: True if setup is complete, False otherwise
    """
    print("🔍 Verifying setup...")
    
    # Check if required files exist
    required_files = [
        "main.py",
        "query_classifier.py", 
        "google_search.py",
        "llm_client.py",
        "utils.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files present")
    
    # Check if dependencies can be imported
    try:
        import requests
        import bs4
        print("✅ Core dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False
    
    # Check environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your-openai-api-key-here':
        print("⚠️  OpenAI API key not set. Please set OPENAI_API_KEY environment variable")
        print("   You can do this by editing the .env file or running:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    print("✅ OpenAI API key is set")
    return True

def run_tests():
    """
    Run basic tests to verify everything works.
    
    Returns:
        bool: True if tests pass, False otherwise
    """
    print("🧪 Running basic tests...")
    
    try:
        # Test query classifier
        from query_classifier import QueryClassifier
        classifier = QueryClassifier()
        
        # Test classification
        test_query = "What is the capital of France?"
        classification = classifier.classify_query(test_query)
        print(f"✅ Query classifier working: '{test_query}' → {classification}")
        
        # Test Google search (without making actual request)
        from google_search import GoogleSearcher
        searcher = GoogleSearcher()
        print("✅ Google searcher initialized")
        
        # Test LLM client (without making actual request)
        from llm_client import LLMClient
        try:
            llm_client = LLMClient()
            print("✅ LLM client initialized")
        except ValueError as e:
            print(f"⚠️  LLM client needs API key: {e}")
        
        print("✅ Basic tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """
    Main setup function.
    
    This demonstrates:
    - Argument parsing
    - Function orchestration
    - Error handling
    - User feedback
    """
    parser = argparse.ArgumentParser(description="Setup Intelligent Query Router")
    parser.add_argument("--skip-deps", action="store_true", 
                       help="Skip dependency installation")
    parser.add_argument("--skip-tests", action="store_true",
                       help="Skip running tests")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    
    args = parser.parse_args()
    
    print("🚀 Setting up Intelligent Query Router")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not args.skip_deps:
        if not install_dependencies():
            print("❌ Setup failed at dependency installation")
            sys.exit(1)
    else:
        print("⏭️  Skipping dependency installation")
    
    # Setup environment
    if not setup_environment():
        print("❌ Setup failed at environment setup")
        sys.exit(1)
    
    # Verify setup
    if not verify_setup():
        print("❌ Setup verification failed")
        print("Please check the errors above and try again")
        sys.exit(1)
    
    # Run tests
    if not args.skip_tests:
        if not run_tests():
            print("⚠️  Some tests failed, but setup is mostly complete")
    else:
        print("⏭️  Skipping tests")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run: python main.py")
    print("3. Or run: python example_usage.py")
    print("\nHappy coding! 🐍✨")

if __name__ == "__main__":
    main()
