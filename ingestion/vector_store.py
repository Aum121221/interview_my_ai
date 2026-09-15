from functools import lru_cache

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
) -> list[dict]:
    """Search Supabase pgvector for similar knowledge."""
    response = get_supabase_client().rpc(
        "match_vault_data",
        {
            "query_embedding": query_embedding,
            "match_threshold": threshold,
            "match_count": top_k,
        },
    ).execute()

    return response.data or []