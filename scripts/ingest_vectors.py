# scripts/ingest_vectors.py

# Imports
import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from google import genai
from google.genai import types
from supabase import create_client

from config.settings import (
    EMBEDDING_DIMENSION,
    EMBEDDING_MODEL,
    KNOWLEDGE_FILE,
    get_gemini_api_key,
    get_supabase_key,
    get_supabase_url,
)


# Embeddings
def create_embedding(client, record: dict) -> dict:
    """Create one retrieval-document embedding row."""
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=record["content"],
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSION,
            task_type="RETRIEVAL_DOCUMENT",
        ),
    )

    return {
        "id": record["id"],
        "content": record["content"],
        "source": record.get("source"),
        "filename": record.get("filename"),
        "document_type": record.get("document_type"),
        "knowledge_status": record.get("knowledge_status"),
        "chunk_index": record.get("chunk_index"),
        "embedding": response.embeddings[0].values,
    }


# Data Loading
def load_records(knowledge_file: Path) -> list[dict]:
    """Load knowledge records from a JSONL file."""
    with open(knowledge_file, encoding="utf-8") as file:
        return [
            json.loads(line)
            for line in file
            if line.strip()
        ]


# Ingestion
def ingest_vectors(
    knowledge_file: Path = KNOWLEDGE_FILE,
    max_workers: int = 10,
) -> list[dict]:
    """Embed candidate knowledge records and upsert them to Supabase."""
    records = load_records(knowledge_file)
    gemini = genai.Client(api_key=get_gemini_api_key())
    supabase = create_client(
        get_supabase_url(),
        get_supabase_key(),
    )

    print()
    print("=" * 50)
    print("INTERVIEW MY AI - VECTOR INGESTION")
    print("=" * 50)
    print(f"Chunks: {len(records)}")
    print(f"Workers: {max_workers}")
    print("=" * 50)

    rows = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(create_embedding, gemini, record)
            for record in records
        ]

        for number, future in enumerate(as_completed(futures), 1):
            try:
                rows.append(future.result())
                print(f"Embedded {number}/{len(records)}")
            except Exception as error:
                print(f"ERROR: {error}")

    print()
    print(f"Embeddings created: {len(rows)}")

    if rows:
        supabase.table("knowledge").upsert(rows).execute()
        print(f"Uploaded {len(rows)} rows.")

    print()
    print("=" * 50)
    print("DONE")
    print("=" * 50)

    return rows


# CLI
def parse_args() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(
        description="Embed candidate knowledge and upload it to Supabase."
    )
    parser.add_argument(
        "--knowledge-file",
        type=Path,
        default=KNOWLEDGE_FILE,
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=10,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    ingest_vectors(
        knowledge_file=args.knowledge_file,
        max_workers=args.max_workers,
    )
