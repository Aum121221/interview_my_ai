from functools import lru_cache

from sentence_transformers import SentenceTransformer


EMBEDDING_MODEL = "BAAI/bge-m3"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """Load the embedding model once and reuse it."""
    return SentenceTransformer(EMBEDDING_MODEL)


def create_embedding(text: str) -> list[float]:
    """Create a normalized BGE-M3 embedding."""
    if not text or not text.strip():
        return []

    embedding = get_embedding_model().encode(
        text.strip(),
        normalize_embeddings=True,
    )

    return embedding.tolist()


def create_query_embedding(query: str) -> list[float]:
    """Create an embedding for a retrieval query."""
    return create_embedding(query)


def create_document_embedding(text: str) -> list[float]:
    """Create an embedding for a knowledge document."""
    return create_embedding(text)