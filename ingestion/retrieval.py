from ingestion.bm25 import search_bm25
from ingestion.bge_m3 import create_query_embedding
from ingestion.vector_store import search_vectors


def normalize_query(query: str) -> str:
    """Normalize a recruiter query."""
    if not query:
        return ""

    return " ".join(query.strip().split())


def prepare_results(
    vector_results: list[dict],
    bm25_results: list[dict],
    top_k: int,
) -> list[dict]:
    """Combine, filter, and deduplicate retrieval results."""
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


def search_knowledge(
    query: str,
    top_k: int,
    threshold: float,
) -> list[dict]:
    """Retrieve candidate evidence using hybrid search."""
    normalized_query = normalize_query(query)

    if not normalized_query:
        return []

    query_embedding = create_query_embedding(
        normalized_query
    )

    vector_results = search_vectors(
        query_embedding=query_embedding,
        top_k=top_k,
        threshold=threshold,
    )

    bm25_results = search_bm25(
        query=normalized_query,
        top_k=top_k,
    )

    return prepare_results(
        vector_results=vector_results,
        bm25_results=bm25_results,
        top_k=top_k,
    )