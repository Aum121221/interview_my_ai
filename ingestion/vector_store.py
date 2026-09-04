# ingestion/vector_store.py

# Imports
import json
from functools import lru_cache
from pathlib import Path

from google import genai
from google.genai import types
from rank_bm25 import BM25Okapi
from supabase import create_client

from config.settings import (
    DEFAULT_SIMILARITY_THRESHOLD,
    EMBEDDING_DIMENSION,
    EMBEDDING_MODEL,
    KNOWLEDGE_FILE,
    get_gemini_api_key,
    get_supabase_key,
    get_supabase_url,
)


# Local Knowledge
def load_knowledge(knowledge_file: Path = KNOWLEDGE_FILE) -> list[dict]:
    """Load candidate knowledge chunks for BM25 retrieval."""
    path = Path(knowledge_file)

    if not path.exists():
        return []

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:
        return [
            json.loads(line)
            for line in file
            if line.strip()
        ]


# BM25
def tokenize(text: str) -> list[str]:
    """Create simple tokens for BM25 retrieval."""
    return text.lower().split()


@lru_cache(maxsize=1)
def get_gemini_client():
    """Create the Gemini client when retrieval first needs it."""
    return genai.Client(
        api_key=get_gemini_api_key(),
    )


@lru_cache(maxsize=1)
def get_supabase_client():
    """Create the Supabase client when retrieval first needs it."""
    return create_client(
        get_supabase_url(),
        get_supabase_key(),
    )


@lru_cache(maxsize=1)
def get_knowledge_records() -> tuple[dict, ...]:
    """Return cached local knowledge records."""
    return tuple(load_knowledge())


@lru_cache(maxsize=1)
def get_bm25_index():
    """Return a cached BM25 index for local knowledge."""
    records = get_knowledge_records()

    if not records:
        return None

    return BM25Okapi(
        [
            tokenize(record["content"])
            for record in records
        ]
    )


# Query Processing
def normalize_query(query: str) -> str:
    """Normalize a search query before retrieval."""
    return " ".join(query.strip().split())


# Embedding
@lru_cache(maxsize=128)
def create_query_embedding(
    query: str,
) -> tuple[float, ...]:
    """Create and cache a Gemini retrieval-query embedding."""
    response = get_gemini_client().models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSION,
            task_type="RETRIEVAL_QUERY",
        ),
    )

    return tuple(
        response.embeddings[0].values
    )


# Vector Search
def search_vectors(
    query_embedding: tuple[float, ...],
    top_k: int,
    threshold: float,
) -> list[dict]:
    """Search Supabase pgvector for relevant chunks."""
    response = get_supabase_client().rpc(
        "match_vault_data",
        {
            "query_embedding": list(query_embedding),
            "match_threshold": threshold,
            "match_count": top_k,
        },
    ).execute()

    return response.data or []


# BM25 Search
def search_bm25(
    query: str,
    top_k: int,
) -> list[dict]:
    """Search local knowledge using BM25."""
    records = get_knowledge_records()
    bm25 = get_bm25_index()

    if bm25 is None:
        return []

    query_tokens = tokenize(query)

    if not query_tokens:
        return []

    scores = bm25.get_scores(query_tokens)

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

    return results


# Result Processing
def prepare_results(
    vector_results: list[dict],
    bm25_results: list[dict],
    top_k: int,
) -> list[dict]:
    """Combine and deduplicate vector and BM25 results."""
    combined = []
    seen = set()

    for result in vector_results + bm25_results:
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
                "document_type": result.get(
                    "document_type"
                ),
                "chunk_index": result.get(
                    "chunk_index"
                ),
                "similarity": result.get(
                    "similarity"
                ),
                "bm25_score": result.get(
                    "bm25_score"
                ),
            }
        )

    return combined[:top_k]


# Deterministic Dual-Path Intent Router
def is_inventory_query(query: str) -> bool:
    """Return True when a query asks for a broad directory or file inventory."""
    q = query.lower()
    keywords = {
        "all", "every", "list", "overview", "inventory", "summary",
        "what", "which", "show", "files", "programs", "projects"
    }
    topics = {
        "file", "program", "project", "repository", "repo",
        "implement", "built", "done", "lab"
    }
    return any(k in q for k in keywords) and any(t in q for t in topics)


def get_inventory_record() -> list[dict]:
    """Return the deterministic inventory record alone to prevent context collision."""
    records = get_knowledge_records()
    for record in records:
        if (
            record.get("id") == "source_inventory_summary"
            or record.get("document_type") == "inventory"
        ):
            return [record]
    return []


# Retrieval
class VectorKnowledgeStore:
    """Provide hybrid BM25 and semantic retrieval with dual-path intent routing."""

    def search(
        self,
        query: str,
        top_k: int = 5,
        threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    ) -> list[dict]:
        """Retrieve candidate knowledge using dual-path intent routing."""
        normalized_query = normalize_query(query)

        if not normalized_query:
            return []

        # Path 1: Inventory Requests (Bypasses vector DB to eliminate context collision)
        if is_inventory_query(normalized_query):
            inventory = get_inventory_record()
            if inventory:
                return inventory

        # Path 2: Deep Knowledge Queries (BM25 + Gemini Vectors, excluding inventory clutter)
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

        results = prepare_results(
            vector_results=vector_results,
            bm25_results=bm25_results,
            top_k=top_k,
        )

        # Exclude inventory summary from deep technical/code searches
        return [
            r for r in results
            if r.get("document_type") != "inventory"
        ]
