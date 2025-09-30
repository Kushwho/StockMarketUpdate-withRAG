"""
Combined tool wrappers for RAG and Stock functionality.
"""
from typing import Dict, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import sys
import os

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

# Import using absolute path from project root
import importlib.util
spec = importlib.util.spec_from_file_location("chat_module", os.path.join(project_root, "chat.py"))
chat_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chat_module)
RAGChatSystem = chat_module.RAGChatSystem

from mcp_integration.stock_tools import get_current_price


class RAGQueryInput(BaseModel):
    """Input schema for RAG queries."""
    question: str = Field(description="The question to ask the RAG system")
    session_id: str = Field(default="default", description="Session ID for conversation memory")


class StockQueryInput(BaseModel):
    """Input schema for stock queries."""
    symbol: str = Field(description="The stock symbol to query (e.g., AAPL, MSFT)")


class RAGTool(BaseTool):
    """Tool wrapper around the existing RAG system."""
    
    name: str = "rag_search"
    description: str = """
    Search through the knowledge base to answer questions about documents.
    Use this tool when the user asks questions that might be answered by the document knowledge base.
    """
    args_schema: type = RAGQueryInput
    rag_system: Any = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rag_system = RAGChatSystem()
    
    def _run(self, question: str, session_id: str = "default") -> str:
        """Execute RAG search."""
        try:
            # Use the chat method which exists in RAGChatSystem
            result = self.rag_system.chat(
                session_id=session_id,
                question=question,
                use_agents=False  # Prevent infinite recursion!
            )
            return result["response"]
        except Exception as e:
            return f"Error querying RAG system: {str(e)}"
    
    async def _arun(self, question: str, session_id: str = "default") -> str:
        """Async execution (fallback to sync for now)."""
        return self._run(question, session_id)


class StockTool(BaseTool):
    """Tool wrapper around the existing stock MCP integration."""
    
    name: str = "stock_quote"
    description: str = """
    Get real-time stock market data for a given stock symbol.
    Use this tool when the user asks about stock prices, market data, or financial information.
    """
    args_schema: type = StockQueryInput
    
    def _run(self, symbol: str) -> str:
        """Execute stock query."""
        try:
            result = get_current_price(symbol)
            return result
        except Exception as e:
            return f"Error getting stock data for {symbol}: {str(e)}"
    
    async def _arun(self, symbol: str) -> str:
        """Async execution (fallback to sync for now)."""
        return self._run(symbol)