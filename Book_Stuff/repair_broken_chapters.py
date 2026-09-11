from pathlib import Path
import re

FOLDER = Path(
    "corrected_translations/The_Sweet_Little_Fulang.epub_corrected"
)

def build_title(filename_stem):

    stem = filename_stem.replace(
        "_corrected",
        ""
    )

    numbers = re.findall(
        r"\d+",
        stem
    )

    if not numbers:
        return None

    chapter_num = numbers[0]

    if "part" in stem.lower():

        if len(numbers) > 1:

            part_num = numbers[1]

            return (
                f"Chapter {chapter_num} "
                f"Part {part_num}"
            )

        return (
            f"Chapter {chapter_num}"
        )

    if len(numbers) > 1:

        extra_num = numbers[1]

        return (
            f"Chapter {chapter_num} "
            f"Part {extra_num}"
        )

    return (
        f"Chapter {chapter_num}"
    )


for file in FOLDER.glob("*.txt"):

    title = build_title(
        file.stem
    )

    if not title:
        continue

    text = file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    lines = text.splitlines()

    if not lines:
        continue

    body = "\n".join(
        lines[1:]
    )

    repaired_text = (
        f"{title}\n\n"
        f"{body}"
    )

    file.write_text(
        repaired_text,
        encoding="utf-8"
    )

    print(
        f"Fixed: {file.name}"
        f" -> {title}"
    )

print()
print("All chapter titles repaired.")