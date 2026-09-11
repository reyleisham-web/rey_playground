from pathlib import Path
from ebooklib import epub
from utils.yaml_loader import NOVEL_CONFIG
import re

# --------------------------
# CONFIG
# --------------------------

BOOK_TITLE = NOVEL_CONFIG["book"]["title"]
SLUG = NOVEL_CONFIG["book"]["slug"]

# --------------------------
# PATHS
# --------------------------

BASE_DIR = Path(__file__).parent

CHAPTERS_DIR = (
    BASE_DIR
    / "corrected_translations"
    / NOVEL_CONFIG["paths"]["corrected_folder"]
)

OUTPUT_FILE = (
    BASE_DIR
    / f"{SLUG}.epub"
)

# --------------------------
# SORT CHAPTER FILES
# --------------------------

def chapter_sort_key(file):

    numbers = [
        int(n)
        for n in re.findall(
            r"\d+",
            file.stem
        )
    ]

    chapter = numbers[0]

    # Ignore garbage part numbers
    if len(numbers) > 1 and numbers[1] < 100:
        part = numbers[1]
    else:
        part = 0

    return (
        chapter,
        part
    )

chapter_files = sorted(
    CHAPTERS_DIR.glob("*.txt"),
    key=chapter_sort_key
)

print("\nFIRST 30 SORTED FILES:\n")

for file in chapter_files[:30]:
    print(file.name)

print()
print(f"Found {len(chapter_files)} chapters")

# --------------------------
# CREATE BOOK
# --------------------------

book = epub.EpubBook()

book.set_identifier(SLUG)
book.set_title(BOOK_TITLE)
book.set_language("en")

chapters = []

# --------------------------
# LOAD CHAPTER FILES
# --------------------------

for file in chapter_files[:30]:
    print(file.name)

print(f"Found {len(chapter_files)} chapters")

# --------------------------
# ADD CHAPTERS
# --------------------------

for index, chapter_file in enumerate(
    chapter_files,
    start=1
):

    text = chapter_file.read_text(
        encoding="utf-8",
        errors="ignore"
    ).strip()

    if not text:
        continue

    lines = text.splitlines()

    chapter_title = (
        lines[0].strip()
        if lines
        else f"Chapter {index}"
    )

    chapter_body = "\n".join(
        lines[1:]
    )

    html_body = ""

    for paragraph in chapter_body.split("\n"):

        paragraph = paragraph.strip()

        if paragraph:
            html_body += (
                f"<p>{paragraph}</p>\n"
            )

    chapter = epub.EpubHtml(
        title=chapter_title,
        file_name=f"chapter_{index:04d}.xhtml",
        lang="en"
    )

    chapter.content = f"""
    <h1>{chapter_title}</h1>
    {html_body}
    """

    book.add_item(chapter)

    chapters.append(chapter)

    print(f"Added: {chapter_title}")

# --------------------------
# TABLE OF CONTENTS
# --------------------------

book.toc = tuple(chapters)

book.spine = ["nav"] + chapters

book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# --------------------------
# SAVE EPUB
# --------------------------

epub.write_epub(
    str(OUTPUT_FILE),
    book
)

print()
print(f"EPUB created: {OUTPUT_FILE}")