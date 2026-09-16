from time import perf_counter
from typing import Callable

from rank_bm25 import BM25Okapi


def tokenize(text: str) -> list[str]:
    """Tokenize text for BM25 retrieval."""
    return text.lower().split()


def search_bm25(
    query: str,
    records: list[dict],
    top_k: int = 3,
    trace_callback: Callable | None = None,
) -> list[dict]:
    """Search supplied knowledge records using BM25."""

    start = perf_counter()

    if not records:
        if trace_callback:
            trace_callback(
                "RETRIEVAL",
                {
                    "stage": "BM25",
                    "status": "WARNING",
                    "results": 0,
                    "reason": "empty_corpus",
                    "duration_ms": round(
                        (perf_counter() - start) * 1000,
                        2,
                    ),
                },
            )

        return []

    query_tokens = tokenize(query)

    if not query_tokens:
        if trace_callback:
            trace_callback(
                "RETRIEVAL",
                {
                    "stage": "BM25",
                    "status": "WARNING",
                    "results": 0,
                    "reason": "empty_query",
                    "duration_ms": round(
                        (perf_counter() - start) * 1000,
                        2,
                    ),
                },
            )

        return []

    try:
        bm25 = BM25Okapi(
            [
                tokenize(record.get("content", ""))
                for record in records
            ]
        )

        scores = bm25.get_scores(query_tokens)

    except Exception as exc:
        if trace_callback:
            trace_callback(
                "RETRIEVAL",
                {
                    "stage": "BM25",
                    "status": "FAIL",
                    "error": f"{type(exc).__name__}: {exc}",
                    "duration_ms": round(
                        (perf_counter() - start) * 1000,
                        2,
                    ),
                },
            )

        raise

    ranked_indexes = scores.argsort()[::-1]

    results = []

    for index in ranked_indexes:
        score = float(scores[index])

        if score <= 0:
            continue

        record = records[index].copy()
        record["bm25_score"] = score
        results.append(record)

        if len(results) >= top_k:
            break

    if trace_callback:
        trace_callback(
            "RETRIEVAL",
            {
                "stage": "BM25",
                "status": "PASS" if results else "WARNING",
                "results": len(results),
                "corpus_size": len(records),
                "top_k": top_k,
                "duration_ms": round(
                    (perf_counter() - start) * 1000,
                    2,
                ),
            },
        )

    return results