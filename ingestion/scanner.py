# ingestion/scanner.py

# Imports
import json
from pathlib import Path


# Configuration
CONFIG_PATH = (
    Path(__file__).resolve().parent.parent
    / "config"
    / "source_map.json"
)


# Configuration Loading
def load_config() -> dict:
    """Load the source scanning configuration."""
    with open(
        CONFIG_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


# File Filtering
def is_supported_file(
    path: Path,
    excluded_parts: set[str],
    extensions: set[str],
) -> bool:
    """Return True when a file passes the source filters."""
    if not path.is_file():
        return False

    if any(
        part in excluded_parts
        for part in path.parts
    ):
        return False

    return path.suffix.lower() in extensions


# Source Scanning
def scan_sources() -> list[Path]:
    """Find all allowed source files in the configured vault."""
    config = load_config()

    vault_root = Path(config["vault_root"])
    include = config["include"]

    excluded_parts = {
        part.lower()
        for part in config.get("exclude", [])
    }

    extensions = {
        extension.lower()
        for extension in config.get("extensions", [])
    }

    if not vault_root.exists():
        raise FileNotFoundError(
            f"Obsidian vault not found: {vault_root}"
        )

    discovered = set()

    for relative_folder in include:
        source_folder = vault_root / relative_folder

        if not source_folder.exists():
            print(
                f"WARNING: Source folder not found: "
                f"{source_folder}"
            )
            continue

        for path in source_folder.rglob("*"):
            if is_supported_file(
                path,
                excluded_parts,
                extensions,
            ):
                discovered.add(path.resolve())

    return sorted(discovered)


# Run
if __name__ == "__main__":
    files = scan_sources()

    print(
        f"\nFound {len(files)} supported files:\n"
    )

    for file in files:
        print(file)