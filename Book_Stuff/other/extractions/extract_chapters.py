from ebooklib import epub
from ebooklib import ITEM_DOCUMENT
from bs4 import BeautifulSoup
import os

INPUT_EPUB = "Transmigration_Farming_Reordered.epub"

os.makedirs("../../chapters", exist_ok=True)

book = epub.read_epub(INPUT_EPUB)

chapter_number = 1

for item in book.get_items():

    if item.get_type() != ITEM_DOCUMENT:
        continue

    if item.get_name() == "nav.xhtml":
        continue

    html = item.get_content().decode(
        "utf-8",
        errors="ignore"
    )

    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text("\n")

    filename = (
        f"chapters/chapter_"
        f"{chapter_number:03d}.txt"
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(text)

    print(f"Saved {filename}")

    chapter_number += 1

print("Done")