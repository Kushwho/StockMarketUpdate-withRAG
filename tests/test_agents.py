"""
Test the basic agentic workflow setup.
"""
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from agents.workflows.unified_workflow import UnifiedAgenticWorkflow


def test_basic_workflow():
    """Test the basic workflow functionality."""
    print("Testing Unified Agentic Workflow...")
    
    workflow = UnifiedAgenticWorkflow()
    
    # Test RAG query
    print("\n1. Testing RAG query:")
    rag_query = "What is machine learning?"
    try:
        response = workflow.run(rag_query)
        print(f"Query: {rag_query}")
        print(f"Response: {response[:200]}...")
    except Exception as e:
        print(f"Error in RAG test: {str(e)}")
    
    # Test Stock query
    print("\n2. Testing Stock query:")
    stock_query = "What is the current price of AAPL?"
    try:
        response = workflow.run(stock_query)
        print(f"Query: {stock_query}")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error in Stock test: {str(e)}")
    
    print("\nBasic workflow test completed!")


if __name__ == "__main__":
    test_basic_workflow()