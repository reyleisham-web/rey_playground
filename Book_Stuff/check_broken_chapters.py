from pathlib import Path

FOLDER = Path(
    "corrected_translations/The_Sweet_Little_Fulang.epub_corrected"
)

for file in sorted(FOLDER.glob("*.txt")):

    lines = file.read_text(
        encoding="utf-8",
        errors="ignore"
    ).splitlines()

    if not lines:
        continue

    first_line = lines[0].strip()

    print(
        f"{file.name} -> {first_line}"
    )