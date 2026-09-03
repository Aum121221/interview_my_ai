import hashlib
import re


def clean_text(text: str) -> str:
    # Remove citation artifacts
    text = re.sub(r"\[cite_start\]", "", text)
    text = re.sub(r"\[cite:\s*[^\]]*\]", "", text)

    # Remove null characters
    text = text.replace("\x00", " ")

    # Fix common missing spaces caused by PDF/text extraction
    text = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)

    # Normalize spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize blank lines
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

    return text.strip()


def classify_document(document):
    path = document["path"].lower()
    title = document["title"].lower()

    if document["type"] == "code":
        category = "technical_implementation"

    elif "linkedin" in path:
        category = "professional"

    elif "github" in path:
        category = "technical"

    elif "project" in path:
        category = "project"

    elif "ai lab" in path:
        category = "academic_ai"

    elif any(
        word in title
        for word in [
            "roadmap",
            "overview",
            "profile",
            "resume",
            "about",
        ]
    ):
        category = "candidate_profile"

    else:
        category = "academic"

    return category


def make_chunks(text: str, max_chars: int = 1800):
    paragraphs = [
        p.strip()
        for p in text.split("\n\n")
        if p.strip()
    ]

    chunks = []
    current = ""

    for paragraph in paragraphs:

        if len(current) + len(paragraph) + 2 <= max_chars:
            current = (
                f"{current}\n\n{paragraph}"
                if current
                else paragraph
            )
        else:
            if current:
                chunks.append(current)

            current = paragraph

    if current:
        chunks.append(current)

    return chunks


def make_id(path, chunk_index, content):
    raw = f"{path}:{chunk_index}:{content}".encode(
        "utf-8"
    )

    return hashlib.sha256(raw).hexdigest()[:16]