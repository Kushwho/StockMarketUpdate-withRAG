"""
Planner node for determining which tools to use.
"""
from typing import Dict, Any, List, Set
from langchain_core.messages import HumanMessage, SystemMessage
import sys
import os
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from llm_client import LLMClient
from config import Config


class PlannerNode:
    """Node that analyzes user queries and plans tool usage."""
    
    def __init__(self):
        self.llm = LLMClient()
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Plan which tools to use based on the user query."""
        user_query = state.get("user_query", "")
        
        planning_prompt = f"""
        Analyze the following user query and determine which tools should be used:
        
        User Query: "{user_query}"
        
        Available Tools:
        1. rag_search - For questions about documents in the knowledge base
        2. stock_quote - For stock market data and financial information
        
        Rules:
        - If the query is about stock prices, market data, or mentions stock symbols, use stock_quote
        - If the query is about general knowledge, documents, or technical topics, use rag_search
        - If unclear, default to rag_search
        - Extract stock symbols if mentioned (e.g., AAPL, MSFT, GOOGL)
        
        Respond with a JSON object:
        {{
            "tools_to_use": ["tool_name"],
            "parameters": {{"tool_name": {{"param": "value"}}}},
            "reasoning": "Brief explanation of choice"
        }}

        Examples:
        - "What's Apple's stock price?" → {{"tools_to_use": ["stock_quote"], "parameters": {{"stock_quote": {{"symbol": "AAPL"}}}}, "reasoning": "User asking for AAPL stock price"}}
        - "Explain machine learning" → {{"tools_to_use": ["rag_search"], "parameters": {{"rag_search": {{"question": "Explain machine learning"}}}}, "reasoning": "General knowledge question"}}
        """
        
        try:
            messages = [
                SystemMessage(content="You are a planning assistant that determines which tools to use."),
                HumanMessage(content=planning_prompt)
            ]
    
            response = self.llm.generate_response(question="You are a planning assistant that determines which tools to use.", context=planning_prompt)
            # Simple string matching to determine tool
            plan = self._extract_plan_from_response(response, user_query)
            
            print(f"✅ Extracted plan: {plan}")
            state["plan"] = plan
            return state
            
        except Exception as e:
            print(f"❌ Planning error: {e}")
            state["plan"] = {
                "tools_to_use": [],
                "parameters": {},
                "reasoning": f"Error during planning: {str(e)}"
            }
            return state
        
    def _extract_plan_from_response(self, response_text: str, user_query: str) -> dict:
        """Extract plan using simple string matching."""
        response_lower = response_text.lower()
        
        # Check if LLM mentioned stock_quote tool
        if "stock_quote" in response_lower:
            # Extract symbol from response or query
            symbol = self._extract_symbol_from_text(response_text + " " + user_query)
            return {
                "tools_to_use": ["stock_quote"],
                "parameters": {"stock_quote": {"symbol": symbol}},
                "reasoning": "LLM selected stock_quote tool"
            }
        
        # Check if LLM mentioned rag_search tool
        elif "rag_search" in response_lower:
            return {
                "tools_to_use": ["rag_search"],
                "parameters": {"rag_search": {"question": user_query}},
                "reasoning": "LLM selected rag_search tool"
            }
        
    def _extract_symbol_from_text(self, text: str) -> str:
        """Extract stock symbol from any text."""
        text_upper = text.upper()
        
        # Check for direct symbol mentions
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NFLX", "NVDA", "AMD", "INTC"]
        for symbol in symbols:
            if symbol in text_upper:
                return symbol
        
        # Check for company names
        company_map = {
            "APPLE": "AAPL",
            "MICROSOFT": "MSFT", 
            "GOOGLE": "GOOGL",
            "ALPHABET": "GOOGL",
            "AMAZON": "AMZN",
            "TESLA": "TSLA",
            "META": "META",
            "FACEBOOK": "META",
            "NETFLIX": "NFLX",
            "NVIDIA": "NVDA",
            "AMD": "AMD",
            "INTEL": "INTC"
        }
        
        for company, symbol in company_map.items():
            if company in text_upper:
                return symbol
                
        return "AAPL"  # Default fallback