# agent/factory.py

# Imports
from smolagents import OpenAIModel

from agent.core import create_agent
from agent.instructions import CANDIDATE_INSTRUCTIONS
from agent.tools import CandidateKnowledgeSearchTool
from config.settings import (
    DEFAULT_MAX_AGENT_STEPS,
    DEFAULT_MODEL_MAX_TOKENS,
    DEFAULT_MODEL_TEMPERATURE,
    OPENROUTER_BASE_URL,
    get_openrouter_model,
    get_openrouter_api_key,
)


# Model
def create_model() -> OpenAIModel:
    """Create the language model used by the candidate agent."""
    return OpenAIModel(
        model_id=get_openrouter_model(),
        api_base=OPENROUTER_BASE_URL,
        api_key=get_openrouter_api_key(),
        temperature=DEFAULT_MODEL_TEMPERATURE,
        max_tokens=DEFAULT_MODEL_MAX_TOKENS,
    )


# Tools
def create_tools(retriever=None) -> list[CandidateKnowledgeSearchTool]:
    """Create the tools available to the candidate agent."""
    return [
        CandidateKnowledgeSearchTool(retriever=retriever),
    ]


# Agent
def create_candidate_agent(model=None, tools=None, instructions=None):
    """Create the Interview My AI candidate agent."""
    return create_agent(
        model=create_model() if model is None else model,
        tools=create_tools() if tools is None else tools,
        instructions=(
            CANDIDATE_INSTRUCTIONS
            if instructions is None
            else instructions
        ),
        max_steps=DEFAULT_MAX_AGENT_STEPS,
    )
