#!/usr/bin/env python3
"""
Intelligent Query Router - A Python AI Project
This project demonstrates how to build an intelligent system that routes queries
to either Google search or an LLM based on the query type.

Author: Python AI Educator
"""

import os
import sys
from typing import Dict, Any
import logging

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("   Or set environment variables manually.")

# Import our custom modules
from query_classifier import QueryClassifier
from google_search import GoogleSearcher
from llm_client import LLMClient
from utils import setup_logging, display_banner

class IntelligentQueryRouter:
    """
    Main class that orchestrates the intelligent query routing system.
    
    This class demonstrates several important Python concepts:
    - Object-oriented programming
    - Error handling
    - Logging
    - Type hints
    - Module organization
    """
    
    def __init__(self):
        """Initialize the query router with all necessary components."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.classifier = QueryClassifier()
        self.google_searcher = GoogleSearcher()
        self.llm_client = LLMClient()
        
        self.logger.info("Intelligent Query Router initialized successfully")
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query and route it to the appropriate tool.
        
        Args:
            query (str): The user's query
            
        Returns:
            Dict[str, Any]: Response containing the answer and metadata
        """
        try:
            self.logger.info(f"Processing query: {query}")
            
            # Classify the query to determine which tool to use
            query_type = self.classifier.classify_query(query)
            self.logger.info(f"Query classified as: {query_type}")
            
            # Route to appropriate tool
            if query_type == "search":
                result = self.google_searcher.search(query)
                result["source"] = "Google Search"
            elif query_type == "llm":
                result = self.llm_client.query(query)
                result["source"] = "OpenAI LLM"
            else:
                # Fallback to LLM for unknown types
                result = self.llm_client.query(query)
                result["source"] = "OpenAI LLM (fallback)"
            
            result["query_type"] = query_type
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            return {
                "error": str(e),
                "query": query,
                "source": "Error Handler"
            }
    
    def run_interactive_mode(self):
        """
        Run the application in interactive mode.
        This demonstrates Python's input/output handling and loops.
        """
        display_banner()
        
        print("\n Welcome to the Intelligent Query Router!")
        print("Ask me anything - I'll automatically choose the best tool to answer your question.")
        print("\nExamples:")
        print("• 'What is the capital of India?' → Google Search")
        print("• 'Solve 2x + 5 = 15' → AI Language Model")
        print("• 'What is machine learning?' → AI Language Model")
        print("\nType 'quit' or 'exit' to stop the program.\n")
        
        while True:
            try:
                # Get user input
                query = input(" Your question: ").strip()
                
                # Check for exit commands
                if query.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Thanks for using the Intelligent Query Router!")
                    break
                
                if not query:
                    print("Please enter a question.")
                    continue
                
                # Process the query
                print("\n Processing your query...")
                result = self.process_query(query)
                
                # Display results
                self._display_result(result)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {str(e)}")
                self.logger.error(f"Unexpected error in interactive mode: {str(e)}")
    
    def _display_result(self, result: Dict[str, Any]):
        """
        Display the result in a user-friendly format.
        
        Args:
            result (Dict[str, Any]): The result to display
        """
        print("\n" + "="*60)
        
        if "error" in result:
            print(f"Error: {result['error']}")
            return
        
        print(f"📝 Query: {result.get('query', 'N/A')}")
        print(f"🔧 Tool Used: {result.get('source', 'Unknown')}")
        print(f"🏷️  Query Type: {result.get('query_type', 'Unknown')}")
        
        if "answer" in result:
            print(f"\n💡 Answer:\n{result['answer']}")
        
        if "urls" in result and result["urls"]:
            print(f"\n🔗 Sources:")
            for i, url in enumerate(result["urls"][:3], 1):
                print(f"  {i}. {url}")
        
        print("="*60 + "\n")

def main():
    """
    Main function - the entry point of our application.
    This demonstrates Python's if __name__ == "__main__" pattern.
    """
    # Setup logging
    setup_logging()
    
    try:
        # Create and run the query router
        router = IntelligentQueryRouter()
        router.run_interactive_mode()
        
    except Exception as e:
        print(f" Failed to start application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
