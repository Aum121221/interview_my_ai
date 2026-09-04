# ingestion/build_knowledge.py

# Imports
import json
from pathlib import Path

from ingestion.scanner import scan_sources
from ingestion.loaders import load_file
from ingestion.processor import (
    classify_document,
    clean_text,
    make_chunks,
    make_id,
)


# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_FILE = PROJECT_ROOT / "data" / "knowledge.jsonl"


# Processing
def process_file(path: Path) -> list[dict]:
    """Load, clean, classify, and chunk one source file."""
    raw_text = load_file(path)
    cleaned_text = clean_text(raw_text)

    if not cleaned_text.strip():
        return []

    document_type = classify_document(path)

    chunks = make_chunks(cleaned_text)

    records = []

    for chunk_index, content in enumerate(chunks):
        records.append(
            {
                "id": make_id(path, chunk_index),
                "content": content,
                "source": str(path),
                "filename": path.name,
                "document_type": document_type,
                "chunk_index": chunk_index,
            }
        )

    return records


# Knowledge Building
def build_knowledge():
    """Build the searchable candidate knowledge dataset."""
    files = scan_sources()

    records = []
    successful_files = 0
    failed_files = 0

    for path in files:
        try:
            file_records = process_file(path)

            if not file_records:
                failed_files += 1
                print(f"WARNING: No usable content: {path}")
                continue

            records.extend(file_records)
            successful_files += 1

        except Exception as exc:
            failed_files += 1
            print(f"WARNING: Failed to process {path}: {exc}")

    # Add deterministic inventory record for broad directory overview queries
    if records:
        all_filenames = sorted(
            list(
                {
                    r.get("filename")
                    for r in records
                    if r.get("filename")
                }
            )
        )
        inventory_text = (
            f"Candidate implemented projects, files, programs, and source code inventory "
            f"({len(all_filenames)} files total): {', '.join(all_filenames)}"
        )
        inventory_record = {
            "id": "source_inventory_summary",
            "content": inventory_text,
            "source": "source_inventory_summary",
            "filename": "source_inventory_summary.txt",
            "document_type": "inventory",
            "chunk_index": 0,
        }
        records.append(inventory_record)

    KNOWLEDGE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        KNOWLEDGE_FILE,
        "w",
        encoding="utf-8",
    ) as file:
        for record in records:
            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )

    print("\nKnowledge build complete.")
    print(f"Files discovered: {len(files)}")
    print(f"Files processed:  {successful_files}")
    print(f"Files failed:     {failed_files}")
    print(f"Chunks created:   {len(records)}")
    print(f"Output:           {KNOWLEDGE_FILE}")

    return records


# Run
if __name__ == "__main__":
    build_knowledge()