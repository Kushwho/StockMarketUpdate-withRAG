"""
Simple stock tools for easy integration with RAG system
"""
from .alpha_vantage_client import AlphaVantageMCPClient
from typing import Dict, Any, Optional

class StockTools:
    def __init__(self):
        """Initialize stock tools with Alpha Vantage MCP client"""
        self.client = AlphaVantageMCPClient()
    
    def get_current_price(self, symbol: str) -> str:
        """
        Get current stock price in a human-readable format
        Perfect for RAG system integration
        """
        try:
            quote = self.client.get_stock_quote(symbol)
            
            if quote.get("success") and "price" in quote:
                price = quote["price"]
                change = quote.get("change", 0)
                change_percent = quote.get("change_percent", "0%")
                volume = quote.get("volume", 0)
                trading_day = quote.get("latest_trading_day", "")
                
                # Format for human reading
                direction = "up" if change >= 0 else "down"
                change_text = f"${abs(change):.2f} ({change_percent})"
                
                result = f"{symbol.upper()} is currently trading at ${price:.2f}, {direction} {change_text} from previous close."
                
                if volume > 0:
                    result += f" Trading volume: {volume:,} shares."
                
                if trading_day:
                    result += f" Last updated: {trading_day}."
                
                # Add additional info if available
                if "open" in quote:
                    result += f" Day's range: ${quote['low']:.2f} - ${quote['high']:.2f}. Opened at ${quote['open']:.2f}."
                
                return result
            
            elif "raw_data" in quote:
                return f"Stock data for {symbol.upper()}: {quote['raw_data']}"
            
            else:
                return f"Unable to get current price for {symbol.upper()}. {quote.get('error', 'Unknown error')}"
        
        except Exception as e:
            return f"Error getting stock price for {symbol.upper()}: {str(e)}"
    
    def get_company_info(self, symbol: str) -> str:
        """Get company overview information"""
        try:
            overview = self.client.get_company_overview(symbol)
            
            if overview.get("success"):
                return f"Company information for {symbol.upper()}: {overview['data']}"
            else:
                return f"Unable to get company information for {symbol.upper()}. {overview.get('error', 'Unknown error')}"
        
        except Exception as e:
            return f"Error getting company info for {symbol.upper()}: {str(e)}"
    
    def search_companies(self, keywords: str) -> str:
        """Search for companies by keywords"""
        try:
            search_result = self.client.search_symbol(keywords)
            
            if search_result.get("success"):
                return f"Search results for '{keywords}': {search_result['data']}"
            else:
                return f"Unable to search for '{keywords}'. {search_result.get('error', 'Unknown error')}"
        
        except Exception as e:
            return f"Error searching for '{keywords}': {str(e)}"

# Convenience function for easy import
def get_current_price(symbol: str) -> str:
    """Standalone function to get current stock price."""
    tools = StockTools()
    return tools.get_current_price(symbol)


def test_stock_tools():
    """Test the stock tools functionality."""
    print("🔄 Testing Stock Tools...")
    
    tools = StockTools()
    
    # Test stock query detection
    test_questions = [
        "What is Apple's stock price?",
        "How is TSLA trading today?",
        "Tell me about the weather",
        "What's the current price of Microsoft?"
    ]
    
    print("\n🤔 Testing stock query detection:")
    for question in test_questions:
        is_stock = tools.is_stock_query(question)
        symbol = tools.extract_symbol_from_question(question)
        print(f"'{question}' -> Stock query: {is_stock}, Symbol: {symbol}")
    
    # Test actual stock data
    print("\n📊 Testing stock price retrieval:")
    price_info = tools.get_current_price("AAPL")
    print(f"Apple stock: {price_info}")
    
    print("\n✅ Stock Tools test completed!")


if __name__ == "__main__":
    test_stock_tools()