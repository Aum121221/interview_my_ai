from functools import lru_cache
from time import perf_counter
from typing import Callable

from sentence_transformers import SentenceTransformer


EMBEDDING_MODEL = "BAAI/bge-m3"
EMBEDDING_DIMENSION = 1024


def _trace(
    trace_callback: Callable | None,
    details: dict,
) -> None:
    """Report an observable BGE-M3 event when tracing is enabled."""

    if trace_callback:
        trace_callback(
            "RETRIEVAL",
            {
                "stage": "BGE-M3",
                **details,
            },
        )


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """Load the embedding model once and reuse it."""

    return SentenceTransformer(EMBEDDING_MODEL)


def _validate_embedding(embedding: list[float]) -> None:
    """Validate the basic BGE-M3 embedding contract."""

    if not embedding:
        raise RuntimeError(
            "BGE-M3 produced an empty embedding."
        )

    if len(embedding) != EMBEDDING_DIMENSION:
        raise RuntimeError(
            "Unexpected BGE-M3 embedding dimension: "
            f"{len(embedding)}. Expected {EMBEDDING_DIMENSION}."
        )

    if not all(
        isinstance(value, (int, float))
        for value in embedding
    ):
        raise RuntimeError(
            "BGE-M3 produced a non-numeric embedding."
        )


def create_embedding(
    text: str,
    trace_callback: Callable | None = None,
) -> list[float]:
    """Create and validate a normalized BGE-M3 embedding."""

    if not text or not text.strip():
        _trace(
            trace_callback,
            {
                "status": "WARNING",
                "reason": "empty_text",
            },
        )

        return []

    start = perf_counter()

    try:
        embedding = get_embedding_model().encode(
            text.strip(),
            normalize_embeddings=True,
        )

        embedding = embedding.tolist()

        _validate_embedding(embedding)

    except Exception as exc:
        _trace(
            trace_callback,
            {
                "status": "FAIL",
                "error": f"{type(exc).__name__}: {exc}",
                "duration_ms": round(
                    (perf_counter() - start) * 1000,
                    2,
                ),
            },
        )

        raise

    _trace(
        trace_callback,
        {
            "status": "PASS",
            "model": EMBEDDING_MODEL,
            "dimension": len(embedding),
            "duration_ms": round(
                (perf_counter() - start) * 1000,
                2,
            ),
        },
    )

    return embedding


def create_query_embedding(
    query: str,
    trace_callback: Callable | None = None,
) -> list[float]:
    """Create an embedding for a retrieval query."""

    return create_embedding(
        query,
        trace_callback=trace_callback,
    )


def create_document_embedding(
    text: str,
) -> list[float]:
    """Create an embedding for a knowledge document."""

    return create_embedding(text)