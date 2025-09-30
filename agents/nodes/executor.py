"""
Executor node for running planned tools.
"""
from typing import Dict, Any
from agents.tools.combined_tools import RAGTool, StockTool


class ExecutorNode:
    """Node that executes the planned tools."""
    
    def __init__(self):
        self.tools = {
            "rag_search": RAGTool(),
            "stock_quote": StockTool()
        }
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the planned tools."""
        plan = state.get("plan", {})
        tools_to_use = plan.get("tools_to_use", ["rag_search"])
        parameters = plan.get("parameters", {})
        
        results = {}
        
        for tool_name in tools_to_use:
            if tool_name in self.tools:
                tool = self.tools[tool_name]
                tool_params = parameters.get(tool_name, {})
                
                try:
                    if tool_name == "rag_search":
                        result = tool._run(
                            question=tool_params.get("question", state.get("user_query", "")),
                            session_id=tool_params.get("session_id", "default")
                        )
                    elif tool_name == "stock_quote":
                        result = tool._run(symbol=tool_params.get("symbol", "AAPL"))
                    else:
                        result = "Unknown tool"
                    
                    results[tool_name] = result
                    
                except Exception as e:
                    results[tool_name] = f"Error executing {tool_name}: {str(e)}"
            else:
                results[tool_name] = f"Tool {tool_name} not found"
        
        state["tool_results"] = results
        return state