from collections import Counter

from ingestion.scanner import scan_sources
from ingestion.loaders import load_file


files = scan_sources()

print("\n" + "=" * 60)
print("INTERVIEW MY AI — STAGE 1")
print("=" * 60)

print(f"\nTotal files: {len(files)}")

counts = Counter(
    path.suffix.lower()
    for path in files
)

print("\nFile types:")

for extension, count in sorted(counts.items()):
    print(f"  {extension}: {count}")

print("\nExtraction test:")

success = 0
failed = 0

for path in files:
    try:
        document = load_file(path)

        if document["content"].strip():
            success += 1
        else:
            failed += 1
            print(f"EMPTY: {path}")

    except Exception as error:
        failed += 1
        print(f"FAILED: {path}")
        print(f"       {error}")

print("\n" + "=" * 60)
print(f"Successfully extracted: {success}")
print(f"Failed/empty:           {failed}")
print("=" * 60)