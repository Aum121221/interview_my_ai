from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_FILE = PROJECT_ROOT / "packed_codebase.example.txt"

ALLOWED_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".json",
}

EXCLUDED_DIRECTORIES = {
    ".git",
    ".streamlit",
    ".venv",
    "__pycache__",
    "node_modules",
    "personal",
    "ROUGHWORK",
}

EXCLUDED_FILES = {
    ".env",
    "secrets.toml",
    "knowledge.jsonl",
    "packed_codebase.txt",
}

EXCLUDED_PREFIXES = {
    "pytest-cache-files-",
}


def should_include(path: Path) -> bool:
    if any(part in EXCLUDED_DIRECTORIES for part in path.parts):
        return False

    if path.name in EXCLUDED_FILES:
        return False

    if any(path.name.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return False

    return path.suffix.lower() in ALLOWED_EXTENSIONS


def pack_codebase() -> None:
    files = sorted(
        path
        for path in PROJECT_ROOT.rglob("*")
        if path.is_file() and should_include(path)
    )

    with OUTPUT_FILE.open("w", encoding="utf-8") as output:
        for path in files:
            relative_path = path.relative_to(PROJECT_ROOT)

            output.write("\n")
            output.write("=" * 40)
            output.write(f"\nFILE: {relative_path}\n")
            output.write("=" * 40)
            output.write("\n\n")

            try:
                output.write(path.read_text(encoding="utf-8"))
            except UnicodeDecodeError:
                output.write("[Unable to decode file as UTF-8]\n")

            output.write("\n")

    print("Codebase packed successfully!")


if __name__ == "__main__":
    pack_codebase()
