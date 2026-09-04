import pytest

pytest.importorskip("smolagents")

from agent.factory import create_candidate_agent, create_tools
from agent.tools import CandidateKnowledgeSearchTool


class FakeAgent:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class FakeModel:
    pass


def test_create_tools_accepts_injected_retriever():
    retriever = object()

    tools = create_tools(retriever=retriever)

    assert len(tools) == 1
    assert isinstance(tools[0], CandidateKnowledgeSearchTool)
    assert tools[0].retriever is retriever


def test_create_candidate_agent_delegates_to_core(monkeypatch):
    captured = {}

    def fake_create_agent(**kwargs):
        captured.update(kwargs)
        return FakeAgent(**kwargs)

    monkeypatch.setattr(
        "agent.factory.create_agent",
        fake_create_agent,
    )

    model = FakeModel()
    tools = []

    agent = create_candidate_agent(
        model=model,
        tools=tools,
        instructions="Follow evidence.",
    )

    assert isinstance(agent, FakeAgent)
    assert captured["model"] is model
    assert captured["tools"] == tools
    assert captured["instructions"] == "Follow evidence."
    assert captured["max_steps"] == 3
