from pathlib import Path

import pytest

from ingestion.processor import clean_text, classify_document, make_chunks, make_id


def test_clean_text_removes_common_artifacts():
    text = "Built[cite_start] an app[cite: 1]\n\n\nwithPython"

    assert clean_text(text) == "Built an app\n\nwith Python"


def test_make_chunks_uses_overlap():
    chunks = make_chunks("abcdefghij", chunk_size=5, overlap=2)

    assert chunks == ["abcde", "defgh", "ghij", "j"]


def test_make_chunks_rejects_invalid_overlap():
    with pytest.raises(ValueError):
        make_chunks("abc", chunk_size=3, overlap=3)


def test_make_id_is_deterministic():
    path = Path("resume.md")

    assert make_id(path, 1) == make_id(path, 1)


def test_classify_document_prefers_known_path_markers():
    assert classify_document(Path("GITHUB/project.py")) == "github"
    assert classify_document(Path("resume.pdf")) == "pdf"
