# Create test_planner.py
import sys
import os
sys.path.append('.')

from agents.nodes.planner import PlannerNode

planner = PlannerNode()
state = {"user_query": "What's is attention?"}
result = planner(state)
print("Plan:", result["plan"])