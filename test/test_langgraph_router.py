"""
Test script for the LangGraph-based LLM router
This script tests various query types to verify the routing decisions.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph_router import LangGraphRouter
from utils import setup_logging

def test_routing_decisions():
    """Test the routing decisions for various query types"""
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Initialize the router
    try:
        router = LangGraphRouter()
        logger.info("LangGraph Router with Azure OpenAI initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize router: {str(e)}")
        print("Make sure you have set the following environment variables:")
        print("- AZURE_OPENAI_API_KEY")
        print("- AZURE_OPENAI_ENDPOINT") 
        print("- AZURE_OPENAI_DEPLOYMENT")
        return
    
    # Test queries with expected routing decisions
    test_queries = [
        # Queries that should go to Google Search (recent/factual)
        ("What is the current weather in New York?", "google_tool"),
        ("Latest news about AI developments", "google_tool"),
        ("Stock price of Apple today", "google_tool"),
        ("What happened in the world today?", "google_tool"),
        ("Current population of Tokyo", "google_tool"),
        
        # Queries that should go to LLM (reasoning/explanations)
        ("Explain how machine learning works", "llm_tool"),
        ("What are the pros and cons of renewable energy?", "llm_tool"),
        ("How do I solve this math problem: 2x + 5 = 15?", "llm_tool"),
        ("Compare Python and JavaScript programming languages", "llm_tool"),
        ("What is the meaning of life?", "llm_tool"),
        
        # Edge cases
        ("Hello, how are you?", "llm_tool"),
        ("", "llm_tool"),
    ]
    
    print("\n" + "="*80)
    print("TESTING LANGGRAPH LLM ROUTER")
    print("="*80)
    
    correct_predictions = 0
    total_tests = len(test_queries)
    
    for i, (query, expected_tool) in enumerate(test_queries, 1):
        print(f"\nTest {i}/{total_tests}")
        print(f"Query: '{query}'")
        print(f"Expected: {expected_tool}")
        
        try:
            # Get routing explanation
            explanation = router.get_routing_explanation(query)
            actual_tool = explanation.get('tool_decision', 'unknown')
            
            print(f"Actual: {actual_tool}")
            
            # Check if prediction is correct
            if actual_tool == expected_tool:
                print("✅ CORRECT")
                correct_predictions += 1
            else:
                print("❌ INCORRECT")
            
            if explanation.get('error'):
                print(f"Error: {explanation['error']}")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
    
    # Print summary
    print("\n" + "="*80)
    print("ROUTING TEST SUMMARY")
    print("="*80)
    print(f"Total tests: {total_tests}")
    print(f"Correct predictions: {correct_predictions}")
    print(f"Accuracy: {(correct_predictions/total_tests)*100:.1f}%")
    
    if correct_predictions == total_tests:
        print("🎉 ALL TESTS PASSED!")
    else:
        print(f"⚠️  {total_tests - correct_predictions} tests failed")

def test_full_processing():
    """Test the full query processing pipeline"""
    
    print("\n" + "="*80)
    print("TESTING FULL QUERY PROCESSING")
    print("="*80)
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Initialize the router
    try:
        router = LangGraphRouter()
        logger.info("LangGraph Router with Azure OpenAI initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize router: {str(e)}")
        print("Make sure you have set the following environment variables:")
        print("- AZURE_OPENAI_API_KEY")
        print("- AZURE_OPENAI_ENDPOINT") 
        print("- AZURE_OPENAI_DEPLOYMENT")
        return
    
    # Test queries for full processing
    test_queries = [
        "What is the capital of France?",
        "Explain quantum computing in simple terms",
        "What's the weather like today?",
        "How do I implement a binary search algorithm?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: '{query}'")
        print("-" * 50)
        
        try:
            result = router.process_query(query)
            
            print(f"Tool Decision: {result.get('tool_decision', 'unknown')}")
            print(f"Source: {result.get('source', 'unknown')}")
            print(f"Answer: {result.get('answer', 'No answer')[:100]}...")
            
            if result.get('error'):
                print(f"Error: {result['error']}")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    print("Starting LangGraph Router Tests...")
    
    # Test routing decisions
    test_routing_decisions()
    
    # Test full processing (commented out to avoid API calls during testing)
    # Uncomment the line below to test full processing with actual API calls
    # test_full_processing()
    
    print("\nTesting completed!")
