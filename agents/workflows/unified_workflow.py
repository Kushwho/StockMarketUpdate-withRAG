"""
Unified workflow for agentic RAG with stock integration.
Supports both LangGraph and simple fallback implementations.
"""
from typing import Dict, Any
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from agents.nodes.planner import PlannerNode
from agents.nodes.executor import ExecutorNode  
from agents.nodes.synthesizer import SynthesizerNode

# Try to import LangGraph
try:
    from langgraph.graph import StateGraph, END
    from typing_extensions import TypedDict
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    TypedDict = dict  # Fallback


class WorkflowState(TypedDict):
    """State schema for the workflow."""
    user_query: str
    session_id: str
    plan: Dict[str, Any]
    tool_results: Dict[str, Any]
    final_response: str


class UnifiedAgenticWorkflow:
    """Unified workflow that uses LangGraph if available, otherwise falls back to simple execution."""
    
    def __init__(self):
        self.planner = PlannerNode()
        self.executor = ExecutorNode()
        self.synthesizer = SynthesizerNode()
        
        if LANGGRAPH_AVAILABLE:
            self.workflow = self._build_langgraph_workflow()
            self.mode = "langgraph"
        else:
            self.workflow = None
            self.mode = "simple"
        
        print(f"✅ Agentic workflow initialized in {self.mode} mode")
    
    def _build_langgraph_workflow(self) -> StateGraph:
        """Build the LangGraph workflow if available."""
        workflow = StateGraph(WorkflowState)
        
        # Add nodes
        workflow.add_node("planner", self.planner)
        workflow.add_node("executor", self.executor)
        workflow.add_node("synthesizer", self.synthesizer)
        
        # Define the flow
        workflow.set_entry_point("planner")
        workflow.add_edge("planner", "executor")
        workflow.add_edge("executor", "synthesizer")
        workflow.add_edge("synthesizer", END)
        
        return workflow.compile()
    
    def _run_langgraph_workflow(self, user_query: str, session_id: str = "default") -> str:
        """Run the LangGraph workflow."""
        initial_state = {
            "user_query": user_query,
            "session_id": session_id,
            "plan": {},
            "tool_results": {},
            "final_response": ""
        }
        
        try:
            result = self.workflow.invoke(initial_state)
            return result.get("final_response", "No response generated")
        except Exception as e:
            return f"Error in LangGraph workflow: {str(e)}"
    
    def run(self, user_query: str, session_id: str = "default") -> str:
        """Run the agentic workflow using the best available method."""
        return self._run_langgraph_workflow(user_query, session_id)
       
    
    def get_status(self) -> Dict[str, Any]:
        """Get workflow status information."""
        return {
            "mode": self.mode,
            "langgraph_available": LANGGRAPH_AVAILABLE,
            "nodes": ["planner", "executor", "synthesizer"],
            "status": "ready"
        }


# Backward compatibility aliases
AgenticRAGWorkflow = UnifiedAgenticWorkflow
SimpleAgenticWorkflow = UnifiedAgenticWorkflow