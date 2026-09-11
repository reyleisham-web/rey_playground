from ebooklib import epub, ITEM_DOCUMENT
import re
from ebooklib import epub, ITEM_DOCUMENT
import re

book = epub.read_epub("Transmigration_Farming.epub")

for item in book.get_items():

    if item.get_type() != ITEM_DOCUMENT:
        continue

    if item.get_name() == "nav.xhtml":
        continue

    try:
        content = item.get_content().decode(
            "utf-8",
            errors="ignore"
        )

        body_match = re.search(
            r"<body.*?>(.*?)</body>",
            content,
            re.IGNORECASE | re.DOTALL
        )

        if not body_match:
            print("NO BODY:", item.get_name())
            continue

        body_content = body_match.group(1).strip()

        if len(body_content) < 20:
            print("VERY SHORT:", item.get_name())

    except Exception as e:
        print(item.get_name(), e)


INPUT_EPUB = "Transmigration_Farming.epub"
OUTPUT_EPUB = "Transmigration_Farming_Reordered.epub"

print("Loading EPUB...")

old_book = epub.read_epub(INPUT_EPUB)

chapters = []

for item in old_book.get_items():

    if item.get_type() != ITEM_DOCUMENT:
        continue

    if item.get_name() == "nav.xhtml":
        continue

    try:
        content = item.get_content().decode(
            "utf-8",
            errors="ignore"
        )

    except Exception:
        continue

    if not content.strip():
        continue

    title_match = re.search(
        r"<h1.*?>(.*?)</h1>",
        content,
        re.IGNORECASE | re.DOTALL
    )

    if not title_match:
        continue

    title = title_match.group(1).strip()

    # Find chapter number
    chapter_match = re.search(
        r"Chapter\s+(\d+)",
        title,
        re.IGNORECASE
    )

    # Handle weird title:
    # "...face 38 Part 2"
    if not chapter_match:

        chapter_match = re.search(
            r"face\s+(\d+)",
            title,
            re.IGNORECASE
        )

    if not chapter_match:
        print(f"Skipped: {title}")
        continue

    chapter_number = int(chapter_match.group(1))

    # Part number (optional)
    part_match = re.search(
        r"Part\s+(\d+)",
        title,
        re.IGNORECASE
    )

    if part_match:
        part_number = int(part_match.group(1))
    else:
        part_number = 0

    chapters.append({
        "chapter": chapter_number,
        "part": part_number,
        "title": title,
        "content": content
    })

print(f"Found {len(chapters)} chapters")

# Sort chapters correctly
chapters.sort(
    key=lambda c: (
        c["chapter"],
        c["part"]
    )
)

print("Rebuilding EPUB...")

new_book = epub.EpubBook()

new_book.set_identifier("transmigration-farming")
new_book.set_title(
    "My Second Journey: Transmigration Farming"
)
new_book.set_language("en")

epub_chapters = []

for index, chapter in enumerate(chapters, start=1):

    item = epub.EpubHtml(
        title=chapter["title"],
        file_name=f"chapter_{index}.xhtml",
        lang="en"
    )

    item.content = chapter["content"]

    new_book.add_item(item)

    epub_chapters.append(item)

new_book.toc = tuple(epub_chapters)

new_book.spine = ["nav"] + epub_chapters

new_book.add_item(epub.EpubNcx())
new_book.add_item(epub.EpubNav())

epub.write_epub(
    OUTPUT_EPUB,
    new_book
)

print("Done!")
print(f"Created: {OUTPUT_EPUB}")