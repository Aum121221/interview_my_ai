from time import perf_counter
from typing import Callable

from ai_knowledge.bm25 import search_bm25
from ai_knowledge.bge_m3 import create_query_embedding
from ai_knowledge.vector_store import search_vectors
from ingestion.ingest_vectors import load_records
from query.query import process_query
from evidence.evidence import prepare_evidence

from config.settings import KNOWLEDGE_FILE


def search_knowledge(
    query: str,
    top_k: int,
    threshold: float,
    trace_callback: Callable | None = None,
) -> list[dict]:
    """Retrieve candidate evidence using hybrid search."""

    start = perf_counter()

    # 1. Process query
    processed_query = process_query(
        query,
        trace_callback=trace_callback,
    )

    if not processed_query:
        return []

    # 2. Create query embedding
    query_embedding = create_query_embedding(
        processed_query,
        trace_callback=trace_callback,
    )

    # 3. Semantic vector retrieval
    vector_results = search_vectors(
        query_embedding=query_embedding,
        top_k=top_k,
        threshold=threshold,
        trace_callback=trace_callback,
    )

    # 4. Lexical BM25 retrieval
    records = load_records(KNOWLEDGE_FILE)

    bm25_results = search_bm25(
        query=processed_query,
        records=records,
        top_k=top_k,
        trace_callback=trace_callback,
    )

    # 5. Prepare final evidence
    results = prepare_evidence(
        vector_results=vector_results,
        bm25_results=bm25_results,
        top_k=top_k,
    )

    if trace_callback:
        trace_callback(
            "RETRIEVAL",
            {
                "stage": "HYBRID",
                "status": "PASS" if results else "WARNING",
                "vector_results": len(vector_results),
                "bm25_results": len(bm25_results),
                "final_results": len(results),
                "top_k": top_k,
                "duration_ms": round(
                    (perf_counter() - start) * 1000,
                    2,
                ),
            },
        )

    return results