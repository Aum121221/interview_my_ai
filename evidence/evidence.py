from typing import Callable


def prepare_evidence(
    vector_results: list[dict],
    bm25_results: list[dict],
    top_k: int,
) -> list[dict]:
    """Prepare retrieved results as grounded candidate evidence."""

    combined = []
    seen = set()

    for result in vector_results + bm25_results:
        if result.get("document_type") == "inventory":
            continue

        content = " ".join(
            result.get("content", "").split()
        )

        if not content:
            continue

        content_key = content.lower()

        if content_key in seen:
            continue

        seen.add(content_key)

        combined.append(
            {
                "content": content,
                "source": result.get("source"),
                "filename": result.get("filename"),
                "document_type": result.get("document_type"),
                "chunk_index": result.get("chunk_index"),
                "similarity": result.get("similarity"),
                "bm25_score": result.get("bm25_score"),
            }
        )

        if len(combined) >= top_k:
            break

    return combined


def format_evidence(
    results: list[dict],
    trace_callback: Callable | None = None,
) -> str:
    """Format prepared evidence for the agent."""

    evidence = []

    for result in results:
        content = " ".join(
            result.get("content", "").split()
        )

        if content:
            evidence.append(content)

    formatted_evidence = "\n\n".join(
        f"[Evidence {index}]\n{content}"
        for index, content in enumerate(evidence, 1)
    )

    if trace_callback:
        trace_callback(
            "EVIDENCE",
            {
                "status": "PASS" if formatted_evidence else "WARNING",
                "results_received": len(results),
                "evidence_items": len(evidence),
                "evidence_length": len(formatted_evidence),
            },
        )

    return formatted_evidence