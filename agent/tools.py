from typing import Callable

import config.settings as settings
from smolagents import Tool

from ai_knowledge.retrieval import search_knowledge
from query.query import process_query
from evidence.evidence import format_evidence


class CandidateKnowledgeSearchTool(Tool):
    """Search candidate knowledge and return grounded evidence."""

    name = "candidate_knowledge_search"

    description = """
    Search the candidate's knowledge base for information relevant to the
    recruiter's question.

    Use this tool for candidate-specific facts such as projects, skills,
    education, experience, technical decisions, implementations,
    achievements, or other candidate background.

    Do not invent candidate-specific information when the returned
    evidence is insufficient.
    """

    inputs = {
        "query": {
            "type": "string",
            "description": (
                "A focused search query based on the recruiter's question."
            ),
        }
    }

    output_type = "string"

    def __init__(
        self,
        retriever: Callable | None = None,
        trace_callback: Callable | None = None,
    ):
        super().__init__()

        self.retriever = retriever or search_knowledge
        self.trace_callback = trace_callback

    def forward(self, query: str) -> str:
        """Process query, retrieve evidence, and return it."""

        processed_query = process_query(
            query,
            trace_callback=self.trace_callback,
        )

        if not processed_query:
            if self.trace_callback:
                self.trace_callback(
                    "TOOL",
                    {
                        "status": "WARNING",
                        "tool": self.name,
                        "reason": "empty_query",
                    },
                )

            return (
                "No search query was provided. "
                "Do not make candidate-specific claims without evidence."
            )

        try:
            results = self.retriever(
                query=processed_query,
                top_k=settings.DEFAULT_TOP_K,
                threshold=settings.DEFAULT_SIMILARITY_THRESHOLD,
                trace_callback=self.trace_callback,
            )

        except Exception as exc:
            if self.trace_callback:
                self.trace_callback(
                    "TOOL",
                    {
                        "status": "FAIL",
                        "tool": self.name,
                        "error": f"{type(exc).__name__}: {exc}",
                    },
                )

            return (
                "Candidate knowledge search is temporarily unavailable. "
                "Do not make candidate-specific claims without evidence."
            )

        if not results:
            if self.trace_callback:
                self.trace_callback(
                    "TOOL",
                    {
                        "status": "WARNING",
                        "tool": self.name,
                        "results": 0,
                    },
                )

            return (
                "No sufficiently relevant candidate evidence was found. "
                "Do not invent candidate-specific information."
            )

        evidence = format_evidence(
            results,
            trace_callback=self.trace_callback,
        )

        if not evidence:
            if self.trace_callback:
                self.trace_callback(
                    "TOOL",
                    {
                        "status": "WARNING",
                        "tool": self.name,
                        "results": len(results),
                        "evidence": False,
                    },
                )

            return (
                "No usable candidate evidence was found. "
                "Do not make candidate-specific claims without evidence."
            )

        if self.trace_callback:
            self.trace_callback(
                "TOOL",
                {
                    "status": "PASS",
                    "tool": self.name,
                    "results": len(results),
                    "evidence": True,
                },
            )

        return evidence