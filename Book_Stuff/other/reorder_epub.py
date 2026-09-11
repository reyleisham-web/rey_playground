from ebooklib import epub
from ebooklib import ITEM_DOCUMENT
import ebooklib
import re

INPUT_EPUB = "Transmigration_Farming.epub"
OUTPUT_EPUB = "Transmigration_Farming_Reordered.epub"

book = epub.read_epub(INPUT_EPUB)

chapters = []

for item in book.get_items():

    if item.get_type() != ITEM_DOCUMENT:
        continue

    if item.get_name() == "nav.xhtml":
        continue

    content = item.get_content().decode(
        "utf-8",
        errors="ignore"
    )

    title_match = re.search(
        r"<h1>(.*?)</h1>",
        content,
        re.IGNORECASE | re.DOTALL
    )

    if not title_match:
        continue

    title = title_match.group(1).strip()

    chapter_match = re.search(
        r"Chapter\s+(\d+)",
        title,
        re.IGNORECASE
    )

    if not chapter_match:
        print(f"Skipping: {title}")
        continue

    chapter_num = int(chapter_match.group(1))

    part_match = re.search(
        r"Part\s+(\d+)",
        title,
        re.IGNORECASE
    )

    if part_match:
        part_num = int(part_match.group(1))
    else:
        part_num = 0

    chapters.append({
        "chapter": chapter_num,
        "part": part_num,
        "title": title,
        "content": content
    })

# Sort by chapter then part
chapters.sort(
    key=lambda x: (
        x["chapter"],
        x["part"]
    )
)

print(f"Sorting {len(chapters)} chapters")

new_book = epub.EpubBook()

new_book.set_identifier("transmigration-farming")
new_book.set_title(
    "Transmigration: Farming, Slapping in the Face and Plotting"
)
new_book.set_language("en")

epub_chapters = []

for idx, chapter in enumerate(chapters, start=1):

    epub_chapter = epub.EpubHtml(
        title=chapter["title"],
        file_name=f"chapter_{idx}.xhtml",
        lang="en"
    )

    epub_chapter.content = chapter["content"]

    new_book.add_item(epub_chapter)

    epub_chapters.append(epub_chapter)

new_book.toc = tuple(epub_chapters)
new_book.spine = ["nav"] + epub_chapters

new_book.add_item(epub.EpubNcx())
new_book.add_item(epub.EpubNav())

epub.write_epub(
    OUTPUT_EPUB,
    new_book
)

print(f"Created: {OUTPUT_EPUB}")