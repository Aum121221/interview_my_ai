from typing import Callable


def process_query(
    query: str,
    trace_callback: Callable | None = None,
) -> str:
    """Validate and normalize an agent-provided retrieval query."""

    if not query or not query.strip():
        if trace_callback:
            trace_callback(
                "PROCESSING",
                {
                    "stage": "QUERY",
                    "status": "WARNING",
                    "query_received": False,
                    "reason": "empty_query",
                },
            )

        return ""

    processed_query = " ".join(query.strip().split())

    if trace_callback:
        trace_callback(
            "PROCESSING",
            {
                "stage": "QUERY",
                "status": "PASS",
                "query_received": True,
                "query": processed_query,
            },
        )

    return processed_query