# agent/tools.py

import os

from smolagents import Tool

import config.settings as settings
from ingestion.retrieval import search_knowledge


class CandidateKnowledgeSearchTool(Tool):
    """Search the candidate knowledge base for relevant evidence."""

    name = "candidate_knowledge_search"

    description = (
        "Search the candidate's stored knowledge for factual information "
        "about projects, education, skills, technologies, experience, "
        "achievements, learning, and professional background. "
        "Use this tool when candidate-specific evidence is needed."
    )

    inputs = {
        "query": {
            "type": "string",
            "description": (
                "A concise search query describing the candidate "
                "information needed to answer the recruiter's question."
            ),
        }
    }

    output_type = "string"

    def __init__(self, retriever=None):
        super().__init__()
        self.retriever = retriever or search_knowledge

    def forward(self, query: str) -> str:
        """Retrieve compact candidate evidence for the agent."""
        if not query or not query.strip():
            return "No search query was provided."

        try:
            results = self.retriever(
                query=query.strip(),
                top_k=settings.DEFAULT_TOP_K,
                threshold=settings.DEFAULT_SIMILARITY_THRESHOLD,
            )
        except Exception:
            return (
                "Candidate knowledge search is temporarily unavailable. "
                "Do not make candidate-specific claims without evidence."
            )

        return self.format_results(results)

    @staticmethod
    def format_results(results: list[dict]) -> str:
        """Format retrieval results as compact candidate evidence."""
        if not results:
            return (
                "No relevant candidate information was found in the "
                "available knowledge base."
            )

        evidence = []
        evidence_number = 0
        has_inventory = False

        for result in results:
            raw_content = result.get("content", "").strip()

            if not raw_content:
                continue

            content = " ".join(raw_content.split())

            source = (
                result.get("filename")
                or os.path.basename(result.get("source", ""))
                or "unknown"
            )

            is_inventory = (
                "inventory" in source.lower()
                or "inventory"
                in result.get("document_type", "").lower()
                or "inventory" in result.get("id", "").lower()
            )

            if is_inventory:
                has_inventory = True
                evidence.append(
                    f"<candidate_inventory_data>\n"
                    f"{content}\n"
                    f"</candidate_inventory_data>"
                )
                continue

            if len(content) > 400:
                content = content[:400] + "..."

            evidence_number += 1

            evidence.append(
                f"### Evidence {evidence_number} "
                f"(Source: `{source}`)\n"
                f"{content}"
            )

        if not evidence:
            return (
                "Search completed, but no usable candidate evidence "
                "was returned."
            )

        output = "\n\n".join(evidence)

        if has_inventory:
            output += (
                "\n\n---\n"
                "[OUTPUT FORMAT DIRECTIVE]: The evidence contains "
                "candidate inventory data in <candidate_inventory_data>. "
                "Render all inventory items as a clean bulleted list "
                "without omitting items."
            )

        return output