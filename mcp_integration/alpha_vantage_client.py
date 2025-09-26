"""
Alpha Vantage MCP Client
Simple wrapper to connect to Alpha Vantage's hosted MCP server
"""
import os
import requests
import json
from typing import Dict, Any, Optional
from config import Config

class AlphaVantageMCPClient:
    def __init__(self):
        """Initialize the Alpha Vantage MCP client"""
        self.api_key = Config.ALPHA_VANTAGE_API_KEY
        self.mcp_url = f"https://mcp.alphavantage.co/mcp?apikey={self.api_key}"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'RAG-Groq-MCP-Client/1.0'
        })
    
    def _make_mcp_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a JSON-RPC request to the MCP server"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        
        try:
            response = self.session.post(self.mcp_url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if "error" in result:
                raise Exception(f"MCP Error: {result['error']}")
            
            return result.get("result", {})
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")
    
    def list_tools(self) -> Dict[str, Any]:
        """List all available tools from Alpha Vantage MCP server"""
        try:
            return self._make_mcp_request("tools/list", {})
        except Exception as e:
            print(f"Error listing tools: {e}")
            return {}
    
    def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get current stock quote for a symbol
        Uses the GLOBAL_QUOTE tool from Alpha Vantage
        """
        try:
            params = {
                "name": "GLOBAL_QUOTE",
                "arguments": {
                    "symbol": symbol.upper()
                }
            }
            
            result = self._make_mcp_request("tools/call", params)
            
            # Parse the response and extract key information
            if result and "content" in result:
                content = result["content"]
                if isinstance(content, list) and len(content) > 0:
                    data = content[0].get("text", "")
                    return self._parse_stock_quote(data, symbol)
            
            return {"error": "No data received", "symbol": symbol}
            
        except Exception as e:
            return {"error": str(e), "symbol": symbol}
    
    def _parse_stock_quote(self, data: str, symbol: str) -> Dict[str, Any]:
        """Parse the stock quote response"""
        try:
            # Try to parse as JSON first
            if data.startswith('{'):
                parsed = json.loads(data)
                if "Global Quote" in parsed:
                    quote = parsed["Global Quote"]
                    return {
                        "symbol": quote.get("01. symbol", symbol),
                        "price": float(quote.get("05. price", 0)),
                        "change": float(quote.get("09. change", 0)),
                        "change_percent": quote.get("10. change percent", "0%"),
                        "volume": int(quote.get("06. volume", 0)),
                        "latest_trading_day": quote.get("07. latest trading day", ""),
                        "previous_close": float(quote.get("08. previous close", 0)),
                        "success": True
                    }
            
            # If CSV format (like what we're getting)
            elif "symbol,open,high,low,price,volume" in data:
                lines = data.strip().split('\n')
                if len(lines) >= 2:
                    # Parse CSV data
                    headers = lines[0].split(',')
                    values = lines[1].split(',')
                    
                    if len(values) >= 8:
                        return {
                            "symbol": values[0],
                            "price": float(values[4]),
                            "change": float(values[8]),
                            "change_percent": values[9],
                            "volume": int(values[5]),
                            "latest_trading_day": values[6],
                            "previous_close": float(values[7]),
                            "open": float(values[1]),
                            "high": float(values[2]),
                            "low": float(values[3]),
                            "success": True
                        }
            
            # If not JSON or CSV, return raw data
            return {
                "symbol": symbol,
                "raw_data": data,
                "success": True
            }
            
        except Exception as e:
            return {
                "symbol": symbol,
                "error": f"Failed to parse data: {str(e)}",
                "raw_data": data,
                "success": False
            }
    
    def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """Get company overview information"""
        try:
            params = {
                "name": "COMPANY_OVERVIEW", 
                "arguments": {
                    "symbol": symbol.upper()
                }
            }
            
            result = self._make_mcp_request("tools/call", params)
            
            if result and "content" in result:
                content = result["content"]
                if isinstance(content, list) and len(content) > 0:
                    data = content[0].get("text", "")
                    return {"symbol": symbol, "data": data, "success": True}
            
            return {"error": "No data received", "symbol": symbol, "success": False}
            
        except Exception as e:
            return {"error": str(e), "symbol": symbol, "success": False}
    
    def search_symbol(self, keywords: str) -> Dict[str, Any]:
        """Search for stock symbols by keywords"""
        try:
            params = {
                "name": "SYMBOL_SEARCH",
                "arguments": {
                    "keywords": keywords
                }
            }
            
            result = self._make_mcp_request("tools/call", params)
            
            if result and "content" in result:
                content = result["content"]
                if isinstance(content, list) and len(content) > 0:
                    data = content[0].get("text", "")
                    return {"keywords": keywords, "data": data, "success": True}
            
            return {"error": "No data received", "keywords": keywords, "success": False}
            
        except Exception as e:
            return {"error": str(e), "keywords": keywords, "success": False}

# Test the client
if __name__ == "__main__":
    print("🔄 Testing Alpha Vantage MCP Client...")
    
    client = AlphaVantageMCPClient()
    
    # Test stock quote
    print("\n📊 Testing stock quote for AAPL...")
    quote = client.get_stock_quote("AAPL")
    print(f"Result: {quote}")
    
    # Test symbol search
    print("\n🔍 Testing symbol search for 'Apple'...")
    search = client.search_symbol("Apple")
    print(f"Result: {search}")
    
    print("\n✅ MCP Client test completed!")