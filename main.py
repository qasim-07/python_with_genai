"""
Intelligent Query Router - A Python AI Project with LangGraph and Azure OpenAI
This project demonstrates how to build an intelligent system that uses LangGraph
and Azure OpenAI LLM-based routing to dynamically decide whether to route queries 
to Google search or an LLM based on intelligent analysis of the query content.
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

from langgraph_router import LangGraphRouter
from utils import setup_logging, display_banner
from ui_components import UIComponents

class IntelligentQueryRouter:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Use LangGraph-based LLM router instead of manual classifier
        self.router = LangGraphRouter()
        
        self.logger.info("Intelligent Query Router with LangGraph LLM routing (Azure OpenAI) initialized successfully")
    
    def process_query(self, query: str) -> Dict[str, Any]:
        try:
            self.logger.info(f"Processing query with LangGraph router: {query}")
            
            # Use the LangGraph router to process the query
            result = self.router.process_query(query)
            
            self.logger.info(f"Query processed successfully with tool: {result.get('tool_decision', 'unknown')}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            return {
                "error": str(e),
                "query": query,
                "source": "Error Handler",
                "routing_method": "LangGraph Router (Error)"
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
    
    def get_routing_explanation(self, query: str) -> Dict[str, Any]:
        """Get detailed explanation of the routing decision for a query"""
        try:
            return self.router.get_routing_explanation(query)
        except Exception as e:
            self.logger.error(f"Error getting routing explanation: {str(e)}")
            return {
                "query": query,
                "tool_decision": "error",
                "routing_method": "LangGraph Router",
                "error": str(e)
            }
    
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
