import argparse
import json
from pathlib import Path

from ingestion.bge_m3 import create_document_embedding
from ingestion.vector_store import get_supabase_client

from config.settings import KNOWLEDGE_FILE



def load_records(knowledge_file: Path) -> list[dict]:
    """Load knowledge records from JSONL."""
    with open(knowledge_file, encoding="utf-8") as file:
        return [
            json.loads(line)
            for line in file
            if line.strip()
        ]

def embed_records(records: list[dict]) -> list[dict]:
    """Reuse existing embeddings or create new ones if needed."""
    client = get_supabase_client()

    existing = (
        client
        .table("knowledge")
        .select("id, content, embedding")
        .execute()
    )

    existing_map = {
        row["id"]: row
        for row in (existing.data or [])
    }

    rows = []
    total = len(records)

    for i, record in enumerate(records, 1):
        existing_record = existing_map.get(record["id"])

        if (
            existing_record
            and existing_record.get("content") == record["content"]
            and existing_record.get("embedding")
        ):
            print(f"Reusing embedding {i}/{total}")
            embedding = existing_record["embedding"]

        else:
            print(f"Creating embedding {i}/{total}")
            embedding = create_document_embedding(
                record["content"]
            )

            assert embedding, (
                f"Empty embedding for record {record['id']}"
            )

        rows.append({
            **record,
            "embedding": embedding,
        })

    return rows

def ingest_vectors(
    knowledge_file: Path = KNOWLEDGE_FILE,
) -> list[dict]:
    """Embed all knowledge locally and upload only a complete set."""
    records = load_records(knowledge_file)

    print()
    print("=" * 50)
    print("INTERVIEW MY AI - VECTOR INGESTION")
    print("=" * 50)
    print(f"Chunks: {len(records)}")
    print("Embedding model: BGE-M3")
    print("Mode: Sequential")
    print("=" * 50)

    rows = embed_records(records)

    if len(rows) != len(records):
        raise RuntimeError(
            "Embedding failed: generated embeddings do not "
            "match the number of knowledge records."
        )

    print()
    print(f"Embeddings created: {len(rows)}")

    print("Uploading to Supabase...")

    get_supabase_client().table(
        "knowledge"
    ).upsert(rows).execute()

    print(f"Uploaded: {len(rows)} rows.")

    print()
    print("=" * 50)
    print("DONE")
    print("=" * 50)

    return rows


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(
        description=(
            "Create BGE-M3 embeddings and upload "
            "candidate knowledge to Supabase."
        )
    )

    parser.add_argument(
        "--knowledge-file",
        type=Path,
        default=KNOWLEDGE_FILE,
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    ingest_vectors(
        knowledge_file=args.knowledge_file,
    )