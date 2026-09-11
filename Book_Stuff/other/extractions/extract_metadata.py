from ebooklib import epub
from ebooklib import ITEM_DOCUMENT
from bs4 import BeautifulSoup
import csv

EPUB_FILE = "sweet_little_fulang.epub"

print("Current working directory:")
print(Path.cwd())

book = epub.read_epub(EPUB_FILE)

rows = []
index = 1

for item in book.get_items():

    if item.get_type() != ITEM_DOCUMENT:
        continue

    html = item.get_content().decode(
        "utf-8",
        errors="ignore"
    )

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    h1 = soup.find("h1")

    if h1:

        title = h1.get_text(
            strip=True
        )

        rows.append([
            index,
            title
        ])

        index += 1

with open(
    "chapter_metadata.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "Index",
        "Title"
    ])

    writer.writerows(rows)

print(
    f"Extracted {len(rows)} chapters"
)

from pathlib import Path

