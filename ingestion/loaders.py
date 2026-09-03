from pathlib import Path
import frontmatter
import pymupdf


def load_markdown(path: Path):
    post = frontmatter.load(path)

    return {
        "path": str(path),
        "type": "markdown",
        "title": path.stem,
        "content": post.content,
        "metadata": dict(post.metadata),
    }


def load_text(path: Path):
    return {
        "path": str(path),
        "type": "text",
        "title": path.stem,
        "content": path.read_text(
            encoding="utf-8",
            errors="ignore",
        ),
        "metadata": {},
    }


def load_python(path: Path):
    return {
        "path": str(path),
        "type": "code",
        "title": path.stem,
        "content": path.read_text(
            encoding="utf-8",
            errors="ignore",
        ),
        "metadata": {
            "language": "python",
        },
    }


def load_pdf(path: Path):
    document = pymupdf.open(path)

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text().strip()

        if text:
            pages.append(
                f"[Page {page_number}]\n{text}"
            )

    document.close()

    return {
        "path": str(path),
        "type": "pdf",
        "title": path.stem,
        "content": "\n\n".join(pages),
        "metadata": {},
    }


def load_file(path: Path):
    extension = path.suffix.lower()

    if extension == ".md":
        return load_markdown(path)

    if extension == ".txt":
        return load_text(path)

    if extension == ".py":
        return load_python(path)

    if extension == ".pdf":
        return load_pdf(path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )