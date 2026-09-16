import time
from config.settings import EMBEDDING_DIMENSION, KNOWLEDGE_FILE
from ingestion.scanner import scan_sources
from ingestion.loaders import load_file
from ingestion.processor import clean_text, classify_document, make_chunks, make_id
from ingestion.build_knowledge import build_knowledge
from ai_knowledge.bge_m3 import create_document_embedding
from ai_knowledge.bm25 import tokenize
from ingestion.ingest_vectors import embed_records
from ai_knowledge.vector_store import get_supabase_client


def safe_run(name, func, *args):
    try:
        result = func(*args)
        print(f"{name}: PASS")
        return result
    except Exception as e:
        print(f"{name}: FAIL -> {e}")
        choice = input("Continue? (y/n): ").strip().lower()
        if choice == "y":
            return None   # continue pipeline with None
        else:
            print("Pipeline stopped.")
            exit(1)


def check_settings():
    assert KNOWLEDGE_FILE, "KNOWLEDGE_FILE missing"
    assert EMBEDDING_DIMENSION > 0, "Invalid embedding dimension"


def check_scanner():
    files = scan_sources()
    assert isinstance(files, list), "Scanner did not return list"
    return files


def check_loader(files):
    return [f for f in files if load_file(f).strip()]


def check_processor(files):
    for f in files:
        text = clean_text(load_file(f))
        assert text.strip(), f"Empty text in {f}"
        assert classify_document(f), f"No type for {f}"
        chunks = make_chunks(text)
        assert chunks, f"No chunks for {f}"
        for i, c in enumerate(chunks):
            assert make_id(f, i), f"No ID for {f}"
            assert c.strip(), f"Empty chunk in {f}"


def check_knowledge():
    records = build_knowledge()
    assert records, "No records built"
    assert KNOWLEDGE_FILE.exists(), "Knowledge file not created"
    return records


def check_embedding(records):
    emb = create_document_embedding(records[0]["content"])
    assert emb and len(emb) == EMBEDDING_DIMENSION, "Bad embedding"
    return emb


def check_bm25(records):
    usable = sum(1 for r in records if tokenize(r["content"]))
    assert usable, "No BM25 tokens"
    return usable


def check_vectors(records):
    rows = embed_records(records)
    assert len(rows) == len(records), "Row count mismatch"
    return rows


def check_supabase(rows):
    client = get_supabase_client()
    resp = client.table("knowledge").upsert(rows).execute()
    assert resp, "No Supabase response"


def run_pipeline():
    start = time.perf_counter()
    safe_run("Settings", check_settings)
    files = safe_run("Scanner", check_scanner)
    loaded = safe_run("Loader", check_loader, files or [])
    safe_run("Processor", check_processor, loaded or [])
    records = safe_run("Knowledge", check_knowledge)
    safe_run("Embedding", check_embedding, records or [{}])
    safe_run("BM25", check_bm25, records or [])
    rows = safe_run("Vectors", check_vectors, records or [])
    safe_run("Supabase", check_supabase, rows or [])
    print(f"Pipeline finished in {time.perf_counter()-start:.2f}s")


if __name__ == "__main__":
    run_pipeline()
