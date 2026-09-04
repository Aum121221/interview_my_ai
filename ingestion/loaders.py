# ingestion/loaders.py

# Imports
from pathlib import Path

import fitz


# Text Files
def load_text_file(path: Path) -> str:
    """Read a text-based source file."""
    return path.read_text(
        encoding="utf-8",
        errors="ignore",
    )


# PDF Files
def load_pdf_file(path: Path) -> str:
    """Extract readable text from a PDF."""
    pages = []

    with fitz.open(path) as document:
        for page in document:
            pages.append(page.get_text())

    return "\n".join(pages)


# File Loading
def load_file(path: Path) -> str:
    """Load a supported source file as raw text."""
    extension = path.suffix.lower()

    if extension in {".md", ".txt", ".py"}:
        return load_text_file(path)

    if extension == ".pdf":
        return load_pdf_file(path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )