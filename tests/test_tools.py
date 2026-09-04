import pytest

pytest.importorskip("smolagents")

from agent.tools import CandidateKnowledgeSearchTool


class FakeRetriever:
    def __init__(self, results=None, error=None):
        self.results = results or []
        self.error = error
        self.calls = []

    def search(self, **kwargs):
        self.calls.append(kwargs)

        if self.error:
            raise self.error

        return self.results


def test_candidate_search_tool_formats_evidence():
    retriever = FakeRetriever(
        results=[
            {
                "content": "Built a Streamlit interview agent.",
                "source": "projects.md",
            }
        ]
    )

    tool = CandidateKnowledgeSearchTool(retriever=retriever)

    result = tool.forward("interview agent project")

    assert "Evidence 1" in result
    assert "projects.md" in result
    assert "Built a Streamlit interview agent." in result
    assert retriever.calls == [
        {
            "query": "interview agent project",
            "top_k": 3,
            "threshold": 0.25,
        }
    ]


def test_candidate_search_tool_rejects_blank_queries():
    tool = CandidateKnowledgeSearchTool(retriever=FakeRetriever())

    assert tool.forward("  ") == "No search query was provided."


def test_candidate_search_tool_fails_closed_on_retriever_error():
    tool = CandidateKnowledgeSearchTool(
        retriever=FakeRetriever(error=RuntimeError("offline"))
    )

    result = tool.forward("skills")

    assert "temporarily unavailable" in result
    assert "Do not make candidate-specific claims" in result
