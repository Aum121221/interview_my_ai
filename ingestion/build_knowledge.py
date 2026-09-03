import json
from pathlib import Path

from ingestion.scanner import scan_sources
from ingestion.loaders import load_file
from ingestion.processor import (
    clean_text,
    classify_document,
    make_chunks,
    make_id,
)


OUTPUT = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "knowledge.jsonl"
)


def build_knowledge():
    files = scan_sources()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    total_documents = 0
    total_chunks = 0
    failed = 0

    with open(OUTPUT, "w", encoding="utf-8") as output:

        for path in files:

            try:
                document = load_file(path)

                content = clean_text(document["content"])

                if not content:
                    failed += 1
                    continue

                category = classify_document(document)

                chunks = make_chunks(content)

                for index, chunk in enumerate(chunks):

                    record = {
                        "id": make_id(
                            str(path),
                            index,
                            chunk,
                        ),
                        "content": chunk,
                        "source": str(path),
                        "title": document["title"],
                        "type": document["type"],
                        "category": category,
                        "chunk_index": index,
                        "metadata": document["metadata"],
                    }

                    output.write(
                        json.dumps(
                            record,
                            ensure_ascii=False,
                        )
                        + "\n"
                    )

                    total_chunks += 1

                total_documents += 1

            except Exception as error:
                failed += 1

                print(
                    f"FAILED: {path}\n"
                    f"       {error}"
                )

    print()
    print("=" * 60)
    print("INTERVIEW MY AI — STAGE 2")
    print("=" * 60)
    print(f"Documents processed : {total_documents}")
    print(f"Chunks created      : {total_chunks}")
    print(f"Failed/empty        : {failed}")
    print(f"Output              : {OUTPUT}")
    print("=" * 60)


if __name__ == "__main__":
    build_knowledge()