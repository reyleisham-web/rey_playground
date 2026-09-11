from ebooklib import epub
from ebooklib import ITEM_DOCUMENT
from bs4 import BeautifulSoup
from utils.yaml_loader import NOVEL_CONFIG
from pathlib import Path
import csv

# --------------------------
# CONFIG
# --------------------------

SLUG = NOVEL_CONFIG["book"]["slug"]

EPUB_FILENAME = (
    NOVEL_CONFIG["epub"]["filename"]
)

# --------------------------
# PATHS
# --------------------------

BASE_DIR = Path(__file__).parent

EPUB_FILE = (
    BASE_DIR
    / "epubs"
    / EPUB_FILENAME
)

OUTPUT_FILE = (
    BASE_DIR
    / "created_files"
    / f"{SLUG}_chapter_metadata.csv"
)

# --------------------------
# LOAD EPUB
# --------------------------

book = epub.read_epub(
    str(EPUB_FILE)
)

rows = []

# --------------------------
# EXTRACT CHAPTERS
# --------------------------

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

    if not h1:
        continue

    title = h1.get_text(
        strip=True
    )

    rows.append([
        item.get_name(),
        title
    ])

# --------------------------
# SAVE CSV
# --------------------------

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "File",
        "Title"
    ])

    writer.writerows(rows)

print(
    f"Saved {len(rows)} chapter titles"
)

print(
    f"Output: {OUTPUT_FILE}"
)
