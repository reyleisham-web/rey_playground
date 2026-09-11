# epub_to_txt_chapters.py

from pathlib import Path
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup

from pathlib import Path

root = Path(r"/")

print("Searching for EPUB files...\n")

for file in root.rglob("*.epub"):
    print(file)

EPUB_FILE = r"../The Sweet Little Fulang.epub"

OUTPUT_DIR = Path("../chapters")
OUTPUT_DIR.mkdir(exist_ok=True)

book = epub.read_epub(EPUB_FILE)

chapter_num = 1

for item in book.get_items():

    if item.get_type() != ITEM_DOCUMENT:
        continue

    # Skip navigation files
    if item.get_name().lower() in [
        "nav.xhtml",
        "toc.xhtml"
    ]:
        continue

    html = item.get_content().decode(
        "utf-8",
        errors="ignore"
    )

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    text = soup.get_text("\n")

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if len(lines) < 5:
        continue

    chapter_text = "\n".join(lines)

    output_file = (
        OUTPUT_DIR /
        f"chapter_{chapter_num:03d}.txt"
    )

    output_file.write_text(
        chapter_text,
        encoding="utf-8"
    )

    print(
        f"Saved {output_file.name}"
    )

    chapter_num += 1

print()
print(f"Extracted {chapter_num - 1} chapters.")