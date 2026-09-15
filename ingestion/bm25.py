from rank_bm25 import BM25Okapi


def tokenize(text: str) -> list[str]:
    """Tokenize text for BM25 retrieval."""
    return text.lower().split()


def search_bm25(
    query: str,
    records: list[dict],
    top_k: int = 3,
) -> list[dict]:
    """Search supplied knowledge records using BM25."""
    if not records:
        return []

    query_tokens = tokenize(query)

    if not query_tokens:
        return []

    bm25 = BM25Okapi(
        [
            tokenize(record.get("content", ""))
            for record in records
        ]
    )

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