# agent/tools.py

# Imports
# pyrefly: ignore [missing-import]
from smolagents import Tool

import config.settings as settings
from ingestion.vector_store import VectorKnowledgeStore


# Candidate Knowledge Search
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
        self.retriever = retriever or VectorKnowledgeStore()

    # Search
    def forward(self, query: str) -> str:
        """Retrieve compact candidate evidence for the agent."""
        if not query or not query.strip():
            return "No search query was provided."

        try:
            results = self.retriever.search(
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

    # Output
    @staticmethod
    def format_results(results: list[dict]) -> str:
        """Convert retrieval results into Karpathy-isolated Markdown evidence with Willison Delimiter-Locked format contracts."""
        if not results:
            return (
                "No relevant candidate information was found in the "
                "available knowledge base."
            )

        # Karpathy Pattern: Immutable vs Mutable Data Split
        # Isolate inventory summary record to prevent dynamic code chunks from corrupting context
        inventory_items = [
            r for r in results
            if "inventory" in r.get("filename", "").lower()
            or r.get("document_type") == "inventory"
            or "inventory" in r.get("id", "").lower()
        ]
        if inventory_items:
            results = inventory_items

        evidence = []
        is_inventory_evidence = False

        for index, result in enumerate(results, start=1):
            raw_content = result.get("content", "").strip()

            if not raw_content:
                continue

            content = " ".join(raw_content.split())
            source = result.get("filename") or (
                result.get("source", "").split("\\")[-1]
            ) or "unknown"

            if "inventory" in source.lower() or "inventory" in result.get("document_type", ""):
                is_inventory_evidence = True
                # Willison Pattern: Delimiter-Locked Structural Container
                evidence.append(
                    f"<candidate_inventory_data>\n{content}\n</candidate_inventory_data>"
                )
            else:
                if len(content) > 400:
                    content = content[:400] + "..."
                evidence.append(
                    f"### Evidence {index} (Source: `{source}`)\n{content}"
                )

        if not evidence:
            return (
                "Search completed, but no usable candidate evidence "
                "was returned."
            )

        output_payload = "\n\n".join(evidence)

        # Willison Pattern: Decoupled Suffix Directive at Payload Boundary
        if is_inventory_evidence:
            output_payload += (
                "\n\n---\n"
                "[OUTPUT FORMAT DIRECTIVE]: Candidate evidence contains a complete project/file inventory in <candidate_inventory_data>. "
                "Render ALL items as a clean, untruncated bulleted list. Do not omit any items. Do not collapse into a prose paragraph."
            )

        return output_payload
