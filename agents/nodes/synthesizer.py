"""
Synthesizer node for combining tool results into final response.
"""
from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from llm_client import LLMClient


class SynthesizerNode:
    """Node that synthesizes tool results into a coherent response."""
    
    def __init__(self):
        self.llm = LLMClient()
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize tool results into final response."""
        user_query = state.get("user_query", "")
        tool_results = state.get("tool_results", {})
        plan = state.get("plan", {})
        
        # If only one tool result, return it directly for now
        if len(tool_results) == 1:
            result = list(tool_results.values())[0]
            state["final_response"] = result
            return state
        
        # For multiple results, combine them
        synthesis_prompt = f"""
        User asked: "{user_query}"
        
        The following tools were used:
        {plan.get('reasoning', 'No reasoning provided')}
        
        Tool Results:
        """
        
        for tool_name, result in tool_results.items():
            synthesis_prompt += f"\n{tool_name}: {result}\n"
        
        synthesis_prompt += """
        
        Please provide a coherent, helpful response that combines the relevant information from the tool results to answer the user's question.
        Be concise and focus on what the user asked for.
        """
        
        try:
            messages = [
                SystemMessage(content="You are a helpful assistant that synthesizes information from multiple sources."),
                HumanMessage(content=synthesis_prompt)
            ]
            
            response = self.llm.get_response(messages)
            state["final_response"] = response
            
        except Exception as e:
            # Fallback: just concatenate results
            combined_results = "\n\n".join([f"{tool}: {result}" for tool, result in tool_results.items()])
            state["final_response"] = combined_results
        
        return state