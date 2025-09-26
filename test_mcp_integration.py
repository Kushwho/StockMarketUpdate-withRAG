"""
Test script for MCP Stock Integration
"""
import sys
import os

# Add the mcp_integration directory to path
sys.path.append('mcp_integration')

def test_mcp_client():
    """Test the Alpha Vantage MCP client"""
    print("🔄 Testing MCP Stock Integration...")
    
    try:
        from alpha_vantage_client import AlphaVantageMCPClient
        print("✅ MCP client imported successfully")
        
        # Initialize client
        client = AlphaVantageMCPClient()
        print("✅ MCP client initialized")
        
        # Test stock quote
        print("\n📊 Testing stock quote for AAPL...")
        quote = client.get_stock_quote("AAPL")
        print(f"Result: {quote}")
        
        if quote.get("success"):
            print("✅ Stock quote successful!")
        else:
            print(f"⚠️ Stock quote failed: {quote.get('error', 'Unknown error')}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_stock_tools():
    """Test the stock tools wrapper"""
    print("\n🔄 Testing Stock Tools...")
    
    try:
        from stock_tools import StockTools
        print("✅ Stock tools imported successfully")
        
        # Initialize tools
        tools = StockTools()
        print("✅ Stock tools initialized")
        
        # Test stock query detection
        test_questions = [
            "What is Apple's stock price?",
            "How is AAPL trading today?",
            "Tell me about the weather",
            "What's the current price of Tesla?"
        ]
        
        print("\n🤔 Testing stock query detection:")
        for question in test_questions:
            is_stock = tools.is_stock_query(question)
            symbol = tools.extract_symbol_from_question(question)
            print(f"  '{question}' -> Stock: {is_stock}, Symbol: {symbol}")
        
        # Test actual stock data
        print("\n📊 Testing stock price retrieval:")
        price_info = tools.get_current_price("AAPL")
        print(f"Apple stock: {price_info}")
        
        print("✅ Stock tools test completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_config():
    """Test configuration"""
    print("\n🔄 Testing Configuration...")
    
    try:
        from config import Config
        print("✅ Config imported successfully")
        
        api_key = Config.ALPHA_VANTAGE_API_KEY
        if api_key:
            print(f"✅ Alpha Vantage API key found: {api_key[:10]}...")
        else:
            print("❌ Alpha Vantage API key not found!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 MCP Stock Integration Test")
    print("=" * 50)
    
    # Test configuration first
    test_config()
    
    # Test MCP client
    test_mcp_client()
    
    # Test stock tools
    test_stock_tools()
    
    print("\n🎯 Test completed!")
    print("If you see errors, check your Alpha Vantage API key in .env file")