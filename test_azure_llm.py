#!/usr/bin/env python3
"""
Test script for Azure OpenAI LLM Client integration.
"""

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")

import os
import logging
from llm_client import LLMClient

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_azure_llm():
    """Test the Azure OpenAI LLM client."""
    print("🤖 Testing Azure OpenAI LLM Client")
    print("=" * 50)
    
    try:
        # Initialize the Azure OpenAI client
        print("🔧 Initializing Azure OpenAI client...")
        llm_client = LLMClient()
        print("✅ Azure OpenAI client initialized successfully!")
        
        # Test connection
        print("\n🔍 Testing connection...")
        if llm_client.test_connection():
            print("✅ Connection test successful!")
        else:
            print("❌ Connection test failed!")
            return
        
        # Test queries
        test_queries = [
            "What is Python programming?",
            "Explain machine learning in simple terms",
            "Write a simple Python function to calculate factorial"
        ]
        
        print(f"\n🧪 Testing {len(test_queries)} queries...")
        print("-" * 50)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Query {i}: {query}")
            print("-" * 30)
            
            result = llm_client.query(query, max_tokens=200, temperature=0.7)
            
            if result.get('error'):
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Answer: {result['answer'][:150]}...")
                print(f"📊 Tokens used: {result.get('tokens_used', 'N/A')}")
                print(f"🤖 Model: {result.get('model', 'N/A')}")
        
        # Show usage stats
        print(f"\n📊 Usage Statistics:")
        stats = llm_client.get_usage_stats()
        print(f"  • Total tokens used: {stats['total_tokens_used']}")
        print(f"  • Model: {stats['model']}")
        print(f"  • Estimated cost: ${stats['estimated_cost_usd']:.4f}")
        
        print(f"\n🎉 Azure OpenAI integration test completed successfully!")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_azure_llm()
