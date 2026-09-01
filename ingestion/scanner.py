from pathlib import Path
import json


CONFIG_PATH = (
    Path(__file__).resolve().parent.parent
    / "config"
    / "source_map.json"
)


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def scan_sources():
    config = load_config()

    vault_root = Path(config["vault_root"])
    include = config["include"]
    exclude = set(config["exclude"])
    extensions = set(config["extensions"])

    if not vault_root.exists():
        raise FileNotFoundError(
            f"Obsidian vault not found: {vault_root}"
        )

    discovered = []

    for relative_folder in include:
        source_folder = vault_root / relative_folder

        if not source_folder.exists():
            print(f"WARNING: Not found: {source_folder}")
            continue

        for path in source_folder.rglob("*"):
            if not path.is_file():
                continue

            if any(part in exclude for part in path.parts):
                continue

            if path.suffix.lower() not in extensions:
                continue

            discovered.append(path)

    return discovered


if __name__ == "__main__":
    files = scan_sources()

    print(f"\nFound {len(files)} supported files:\n")

    for file in files:
        print(file)