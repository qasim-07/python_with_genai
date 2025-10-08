"""
Demo script comparing manual keyword-based routing vs LangGraph LLM routing
This script shows the difference between the old manual approach and the new LLM-driven approach.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query_classifier import QueryClassifier
from langgraph_router import LangGraphRouter
from utils import setup_logging

def compare_routing_methods():
    """Compare manual keyword-based routing vs LangGraph LLM routing"""
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Initialize both routing methods
    try:
        manual_classifier = QueryClassifier()
        langgraph_router = LangGraphRouter()
        logger.info("Both routing methods initialized successfully (LangGraph uses Azure OpenAI)")
    except Exception as e:
        logger.error(f"Failed to initialize routing methods: {str(e)}")
        print("Make sure you have set the following environment variables:")
        print("- AZURE_OPENAI_API_KEY")
        print("- AZURE_OPENAI_ENDPOINT") 
        print("- AZURE_OPENAI_DEPLOYMENT")
        return
    
    # Test queries that might be handled differently
    test_queries = [
        "What is the latest news about artificial intelligence?",
        "Explain the concept of machine learning",
        "What's the current temperature in London?",
        "How does a neural network work?",
        "Who won the Nobel Prize in Physics this year?",
        "Compare supervised and unsupervised learning",
        "What's the stock price of Tesla today?",
        "What are the ethical implications of AI?",
        "What time is it in Tokyo right now?",
        "How do I implement a sorting algorithm?"
    ]
    
    print("\n" + "="*100)
    print("COMPARING MANUAL KEYWORD ROUTING vs LANGGRAPH LLM ROUTING")
    print("="*100)
    
    print(f"{'Query':<50} {'Manual':<15} {'LangGraph':<15} {'Match':<10}")
    print("-" * 100)
    
    matches = 0
    total = len(test_queries)
    
    for query in test_queries:
        try:
            # Get manual classification
            manual_decision = manual_classifier.classify_query(query)
            manual_tool = "google_tool" if manual_decision == "search" else "llm_tool"
            
            # Get LangGraph routing explanation
            langgraph_explanation = langgraph_router.get_routing_explanation(query)
            langgraph_tool = langgraph_explanation.get('tool_decision', 'unknown')
            
            # Check if they match
            match = "✅" if manual_tool == langgraph_tool else "❌"
            if manual_tool == langgraph_tool:
                matches += 1
            
            # Truncate query for display
            display_query = query[:47] + "..." if len(query) > 50 else query
            
            print(f"{display_query:<50} {manual_tool:<15} {langgraph_tool:<15} {match:<10}")
            
        except Exception as e:
            print(f"{query[:47] + '...':<50} {'ERROR':<15} {'ERROR':<15} {'❌':<10}")
            logger.error(f"Error processing query '{query}': {str(e)}")
    
    print("-" * 100)
    print(f"Total queries: {total}")
    print(f"Matching decisions: {matches}")
    print(f"Agreement rate: {(matches/total)*100:.1f}%")
    
    if matches == total:
        print("🎉 Both methods agree on all queries!")
    else:
        print(f"⚠️  Methods disagree on {total - matches} queries")

def show_detailed_comparison():
    """Show detailed comparison for a few specific queries"""
    
    print("\n" + "="*100)
    print("DETAILED COMPARISON FOR SPECIFIC QUERIES")
    print("="*100)
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Initialize both routing methods
    try:
        manual_classifier = QueryClassifier()
        langgraph_router = LangGraphRouter()
    except Exception as e:
        logger.error(f"Failed to initialize routing methods: {str(e)}")
        print("Make sure you have set the following environment variables:")
        print("- AZURE_OPENAI_API_KEY")
        print("- AZURE_OPENAI_ENDPOINT") 
        print("- AZURE_OPENAI_DEPLOYMENT")
        return
    
    # Specific queries for detailed analysis
    detailed_queries = [
        "What is the current weather in Paris?",
        "Explain how blockchain technology works",
        "Latest updates on climate change research"
    ]
    
    for query in detailed_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 80)
        
        try:
            # Manual classification details
            manual_explanation = manual_classifier.get_classification_explanation(query)
            manual_decision = manual_classifier.classify_query(query)
            manual_tool = "google_tool" if manual_decision == "search" else "llm_tool"
            
            print(f"Manual Classification:")
            print(f"  Decision: {manual_decision} -> {manual_tool}")
            print(f"  Search Score: {manual_explanation['search_score']}")
            print(f"  LLM Score: {manual_explanation['llm_score']}")
            print(f"  Matched Search Keywords: {manual_explanation['matched_search_keywords']}")
            print(f"  Matched LLM Keywords: {manual_explanation['matched_llm_keywords']}")
            
            # LangGraph routing
            langgraph_explanation = langgraph_router.get_routing_explanation(query)
            langgraph_tool = langgraph_explanation.get('tool_decision', 'unknown')
            
            print(f"\nLangGraph LLM Routing:")
            print(f"  Decision: {langgraph_tool}")
            print(f"  Method: {langgraph_explanation.get('routing_method', 'unknown')}")
            
            if langgraph_explanation.get('error'):
                print(f"  Error: {langgraph_explanation['error']}")
            
            # Comparison
            print(f"\nComparison:")
            if manual_tool == langgraph_tool:
                print(f"  ✅ Both methods agree: {manual_tool}")
            else:
                print(f"  ❌ Methods disagree: Manual={manual_tool}, LangGraph={langgraph_tool}")
                
        except Exception as e:
            print(f"❌ Error processing query: {str(e)}")
            logger.error(f"Error in detailed comparison for '{query}': {str(e)}")

if __name__ == "__main__":
    print("Starting LangGraph vs Manual Routing Comparison...")
    
    # Compare routing methods
    compare_routing_methods()
    
    # Show detailed comparison
    show_detailed_comparison()
    
    print("\nComparison completed!")
