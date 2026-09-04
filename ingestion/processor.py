# ingestion/processor.py

# Imports
import hashlib
import re
from pathlib import Path


# Text Processing
def clean_text(text: str) -> str:
    """Clean common extraction artifacts and normalize whitespace."""
    if not text:
        return ""

    text = text.replace("\x00", " ")

    text = re.sub(
        r"\[cite_start\]",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\[cite:\s*[^\]]*\]",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"(?<=[a-z])(?=[A-Z])",
        " ",
        text,
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


# Document Classification
def classify_document(path: Path) -> str:
    """Classify a source document using its path and extension."""
    path_text = str(path).lower()

    if "github" in path_text:
        return "github"

    if "linkedin" in path_text:
        return "linkedin"

    if "project" in path_text:
        return "project"

    if path.suffix.lower() == ".pdf":
        return "pdf"

    if path.suffix.lower() == ".py":
        return "code"

    return "document"


# Chunking
def make_chunks(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200,
) -> list[str]:
    """Split text into overlapping chunks."""
    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    chunks = []
    start = 0
    step = chunk_size - overlap

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += step

    return chunks


# IDs
def make_id(path: Path, chunk_index: int) -> str:
    """Create a deterministic ID for a source chunk."""
    source = f"{path.resolve()}::{chunk_index}"

    return hashlib.sha256(
        source.encode("utf-8")
    ).hexdigest()