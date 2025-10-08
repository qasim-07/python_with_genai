"""
Intelligent Query Router - A Python AI Project
This project demonstrates how to build an intelligent system that routes queries
to either Google search or an LLM based on the query type.
"""

import os
import sys
from typing import Dict, Any
import logging

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Install with: pip install python-dotenv")
    print("Or set environment variables manually.")

from query_classifier import QueryClassifier
from google_search import GoogleSearcher
from llm_client import LLMClient
from utils import setup_logging, display_banner
from ui_components import UIComponents

class IntelligentQueryRouter:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        self.classifier = QueryClassifier()
        self.google_searcher = GoogleSearcher()
        self.llm_client = LLMClient()
        
        self.logger.info("Intelligent Query Router initialized successfully")
    
    def process_query(self, query: str) -> Dict[str, Any]:
        try:
            self.logger.info(f"Processing query: {query}")
            
            query_type = self.classifier.classify_query(query)
            self.logger.info(f"Query classified as: {query_type}")
            
            if query_type == "search":
                result = self.google_searcher.search(query)
                result["source"] = "Google Search"
            elif query_type == "llm":
                result = self.llm_client.query(query)
                result["source"] = "OpenAI LLM"
            else:
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
        """Run the interactive CLI mode with beautiful UI"""
        UIComponents.print_banner()
        UIComponents.print_welcome()
        
        while True:
            try:
                query = UIComponents.get_user_input()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    UIComponents.print_goodbye()
                    break
                
                if not query:
                    UIComponents.print_warning("Please enter a question.")
                    continue
                
                UIComponents.show_processing()
                result = self.process_query(query)
                
                UIComponents.display_result(result)
                
            except KeyboardInterrupt:
                UIComponents.print_goodbye()
                break
            except Exception as e:
                UIComponents.print_error(f"An error occurred: {str(e)}")
                self.logger.error(f"Unexpected error in interactive mode: {str(e)}")
    
    def _display_result(self, result: Dict[str, Any]):
        """Display result using the new UI components"""
        UIComponents.display_result(result)

def main():
    """Main entry point for the application"""
    setup_logging()
    
    try:
        router = IntelligentQueryRouter()
        router.run_interactive_mode()
        
    except Exception as e:
        UIComponents.print_error(f"Failed to start application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
