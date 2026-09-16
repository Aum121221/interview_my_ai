from functools import lru_cache
from time import perf_counter
from typing import Callable

from supabase import create_client

from config.settings import (
    get_supabase_key,
    get_supabase_url,
)


@lru_cache(maxsize=1)
def get_supabase_client():
    """Create and cache the Supabase client."""
    return create_client(
        get_supabase_url(),
        get_supabase_key(),
    )


def search_vectors(
    query_embedding: list[float],
    top_k: int,
    threshold: float,
    trace_callback: Callable | None = None,
) -> list[dict]:
    """Search Supabase pgvector for similar knowledge."""

    start = perf_counter()

    if not query_embedding:
        if trace_callback:
            trace_callback(
                "RETRIEVAL",
                {
                    "stage": "VECTOR_SEARCH",
                    "status": "WARNING",
                    "results": 0,
                    "reason": "empty_query_embedding",
                },
            )

        return []

    try:
        response = get_supabase_client().rpc(
            "match_vault_data",
            {
                "query_embedding": query_embedding,
                "match_threshold": threshold,
                "match_count": top_k,
            },
        ).execute()

        results = response.data or []

    except Exception as exc:
        if trace_callback:
            trace_callback(
                "RETRIEVAL",
                {
                    "stage": "VECTOR_SEARCH",
                    "status": "FAIL",
                    "error": f"{type(exc).__name__}: {exc}",
                    "duration_ms": round(
                        (perf_counter() - start) * 1000,
                        2,
                    ),
                },
            )

        raise

    if trace_callback:
        trace_callback(
            "RETRIEVAL",
            {
                "stage": "VECTOR_SEARCH",
                "status": "PASS" if results else "WARNING",
                "results": len(results),
                "top_k": top_k,
                "threshold": threshold,
                "duration_ms": round(
                    (perf_counter() - start) * 1000,
                    2,
                ),
            },
        )

    return results