from pathlib import Path

BASE_DIR = Path(__file__).parent

INPUT_FILE = (
    BASE_DIR
    / "chapters"
    / "chapter_001.txt"
)

print("Input file:")
print(INPUT_FILE)

print()
print("Exists:")
print(INPUT_FILE.exists())

if not INPUT_FILE.exists():
    raise FileNotFoundError(INPUT_FILE)

text = INPUT_FILE.read_text(
    encoding="utf-8",
    errors="ignore"
)

print()
print("First 1000 characters:")
print("=" * 80)
print(text[:1000])
print("=" * 80)

print()
print("Character count:")
print(len(text))

print("Submitting request...")

response = client.responses.create(
    model="gpt-5",
    input=prompt
)

print("\nRESPONSE TYPE:")
print(type(response))

print("\nFIRST 2000 CHARS OF RESPONSE:")
print("=" * 80)
print(str(response)[:2000])
print("=" * 80)

edited_text = str(response)