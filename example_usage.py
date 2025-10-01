#!/usr/bin/env python3
"""
Example Usage Script

This script demonstrates how to use the Intelligent Query Router programmatically.
It shows various ways to interact with the system and is perfect for learning
how to integrate this functionality into other projects.

Key Python concepts demonstrated:
- Import statements and module usage
- Exception handling
- Programmatic API usage
- Batch processing
- Result analysis
"""

import os
import sys
from typing import List, Dict, Any

# Add the current directory to Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import IntelligentQueryRouter
from query_classifier import QueryClassifier
from utils import display_banner, print_separator

def run_example_queries():
    """
    Run a series of example queries to demonstrate the system.
    
    This function shows:
    - How to create and use the query router
    - Different types of queries and their classifications
    - Error handling
    - Result processing
    """
    print("🚀 Running Example Queries")
    print_separator()
    
    # Initialize the query router
    try:
        router = IntelligentQueryRouter()
        print("✅ Query router initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize query router: {e}")
        print("Make sure you have set your OPENAI_API_KEY environment variable.")
        return
    
    # Example queries that demonstrate different classifications
    example_queries = [
        # Google Search queries (factual, current information)
        "What is the capital of France?",
        "Current population of Tokyo",
        "Who is the CEO of Apple?",
        "Weather in New York today",
        
        # LLM queries (analytical, mathematical, creative)
        "Solve the equation 2x + 5 = 15",
        "Explain how machine learning works",
        "Write a Python function to calculate factorial",
        "What are the advantages and disadvantages of solar energy?",
        
        # Edge cases
        "Hello, how are you?",
        "What time is it?",
    ]
    
    print(f"📝 Processing {len(example_queries)} example queries...\n")
    
    for i, query in enumerate(example_queries, 1):
        print(f"Query {i}: {query}")
        print("-" * 50)
        
        try:
            # Process the query
            result = router.process_query(query)
            
            # Display the result
            print(f"🔧 Tool Used: {result.get('source', 'Unknown')}")
            print(f"🏷️  Query Type: {result.get('query_type', 'Unknown')}")
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
            else:
                answer = result.get('answer', 'No answer available')
                # Truncate long answers for display
                if len(answer) > 200:
                    answer = answer[:200] + "..."
                print(f"💡 Answer: {answer}")
            
            print()
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            print()
    
    print_separator()
    print("✅ Example queries completed!")

def demonstrate_classifier():
    """
    Demonstrate the query classifier in detail.
    
    This function shows:
    - How the classifier works internally
    - Classification scores and reasoning
    - Different types of query patterns
    """
    print("🧠 Query Classifier Demonstration")
    print_separator()
    
    classifier = QueryClassifier()
    
    # Test queries with explanations
    test_queries = [
        "What is the capital of India?",
        "Solve 3x + 7 = 22",
        "Explain quantum computing",
        "Current stock price of Tesla",
        "Write a Python function to reverse a string",
        "Who is the president of the United States?",
        "Compare Python and JavaScript",
        "Weather forecast for tomorrow",
    ]
    
    for query in test_queries:
        print(f"Query: {query}")
        
        # Get detailed classification explanation
        explanation = classifier.get_classification_explanation(query)
        
        print(f"  Classification: {explanation['classification']}")
        print(f"  Search Score: {explanation['search_score']}")
        print(f"  LLM Score: {explanation['llm_score']}")
        print(f"  Is Mathematical: {explanation['is_mathematical']}")
        
        if explanation['matched_search_keywords']:
            print(f"  Matched Search Keywords: {', '.join(explanation['matched_search_keywords'])}")
        
        if explanation['matched_llm_keywords']:
            print(f"  Matched LLM Keywords: {', '.join(explanation['matched_llm_keywords'])}")
        
        print()

def run_interactive_demo():
    """
    Run an interactive demonstration.
    
    This function shows:
    - How to create a custom interactive interface
    - User input handling
    - Custom result formatting
    """
    print("🎮 Interactive Demo")
    print_separator()
    
    try:
        router = IntelligentQueryRouter()
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    print("Enter your questions (type 'quit' to exit):")
    print()
    
    while True:
        try:
            query = input("🔍 Your question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not query:
                continue
            
            print("🔄 Processing...")
            result = router.process_query(query)
            
            # Custom formatting
            print(f"\n📊 Result Summary:")
            print(f"   Tool: {result.get('source', 'Unknown')}")
            print(f"   Type: {result.get('query_type', 'Unknown')}")
            
            if 'tokens_used' in result:
                print(f"   Tokens Used: {result['tokens_used']}")
            
            if 'urls' in result and result['urls']:
                print(f"   Sources: {len(result['urls'])} URLs found")
            
            print(f"\n💡 Answer:\n{result.get('answer', 'No answer available')}")
            print("\n" + "="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """
    Main function to run different demonstrations.
    
    This demonstrates:
    - Command-line argument handling
    - Menu-driven interfaces
    - Function organization
    """
    display_banner()
    
    print("Choose a demonstration:")
    print("1. Run example queries")
    print("2. Demonstrate query classifier")
    print("3. Interactive demo")
    print("4. Run all demonstrations")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                run_example_queries()
                break
            elif choice == '2':
                demonstrate_classifier()
                break
            elif choice == '3':
                run_interactive_demo()
                break
            elif choice == '4':
                run_example_queries()
                print()
                demonstrate_classifier()
                print()
                run_interactive_demo()
                break
            else:
                print("Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
