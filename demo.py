#!/usr/bin/env python3
"""
Simple demo of the Intelligent Query Router
Shows how the classification works without external API calls
"""

from query_classifier import QueryClassifier

def demo_classification():
    """Demonstrate query classification"""
    print("🤖 Intelligent Query Router - Classification Demo")
    print("=" * 55)
    print()
    
    classifier = QueryClassifier()
    
    # Sample queries
    queries = [
        "What is the capital of India?",
        "Solve 2x + 5 = 15",
        "Explain machine learning",
        "Current weather in New York",
        "Write a Python function to sort a list",
        "Population of Tokyo",
        "What are the benefits of exercise?",
        "Who is the CEO of Apple?",
        "Calculate the area of a circle with radius 5",
        "How to make chocolate cake"
    ]
    
    print("📝 Query Classification Results:")
    print("-" * 40)
    
    for i, query in enumerate(queries, 1):
        classification = classifier.classify_query(query)
        tool = "🔍 Google Search" if classification == "search" else "🤖 AI Language Model"
        
        print(f"{i:2d}. {query}")
        print(f"    → {tool}")
        print()
    
    print("=" * 55)
    print("✅ Classification demo completed!")
    print()
    print("💡 How it works:")
    print("   • Search queries: Factual, current information")
    print("   • LLM queries: Analytical, creative, mathematical")
    print("   • The system automatically chooses the best tool!")

def demo_detailed_analysis():
    """Show detailed analysis of a few queries"""
    print("🔍 Detailed Classification Analysis")
    print("=" * 40)
    
    classifier = QueryClassifier()
    
    sample_queries = [
        "What is the capital of France?",
        "Solve x^2 + 5x + 6 = 0",
        "Explain the theory of relativity"
    ]
    
    for query in sample_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 30)
        
        explanation = classifier.get_classification_explanation(query)
        
        print(f"Classification: {explanation['classification']}")
        print(f"Search Score: {explanation['search_score']}")
        print(f"LLM Score: {explanation['llm_score']}")
        print(f"Is Mathematical: {explanation['is_mathematical']}")
        print(f"Matched Search Keywords: {explanation['matched_search_keywords']}")
        print(f"Matched LLM Keywords: {explanation['matched_llm_keywords']}")

def main():
    """Run the demo"""
    demo_classification()
    demo_detailed_analysis()
    
    print("\n🎉 Demo completed!")
    print("\n🚀 To run the full application:")
    print("   python main.py")
    print("\n📚 To learn more about the code:")
    print("   • main.py - Main application")
    print("   • query_classifier.py - Classification logic")
    print("   • google_search.py - Web search functionality")
    print("   • llm_client.py - AI language model integration")

if __name__ == "__main__":
    main()
