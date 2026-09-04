# agent/core.py

# Imports
from smolagents import ToolCallingAgent


# Agent
def create_agent(model, tools, instructions, max_steps: int = 3):
    """Create the Interview My AI ToolCallingAgent."""
    return ToolCallingAgent(
        tools=tools,
        model=model,
        instructions=instructions,
        max_steps=max_steps,
        planning_interval=None,
        add_base_tools=False,
    )
