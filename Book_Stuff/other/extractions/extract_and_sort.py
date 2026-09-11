from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
import re

INPUT_EPUB = "Transmigration_Farming.epub"
OUTPUT_EPUB = "Transmigration_Farming_Reordered.epub"

old_book = epub.read_epub(INPUT_EPUB)

chapters = []

for item in old_book.get_items():

    if item.get_type() != ITEM_DOCUMENT:
        continue

    if item.get_name() == "nav.xhtml":
        continue

    content = item.get_content().decode(
        "utf-8",
        errors="ignore"
    )

    soup = BeautifulSoup(content, "html.parser")

    h1 = soup.find("h1")

    if not h1:
        continue

    title = h1.get_text(strip=True)

    chapter_match = re.search(
        r"Chapter\s+(\d+)",
        title,
        re.IGNORECASE
    )

    if not chapter_match:
        chapter_match = re.search(
            r"face\s+(\d+)",
            title,
            re.IGNORECASE
        )

    if not chapter_match:
        print("Skipped:", title)
        continue

    chapter_num = int(chapter_match.group(1))

    part_match = re.search(
        r"Part\s+(\d+)",
        title,
        re.IGNORECASE
    )

    part_num = (
        int(part_match.group(1))
        if part_match
        else 0
    )

    body = soup.find("body")

    if body:
        body_html = "".join(
            str(x) for x in body.contents
        )
    else:
        body_html = str(soup)

    chapters.append({
        "chapter": chapter_num,
        "part": part_num,
        "title": title,
        "body": body_html
    })

print(f"Found {len(chapters)} chapters")

chapters.sort(
    key=lambda x: (
        x["chapter"],
        x["part"]
    )
)

new_book = epub.EpubBook()

new_book.set_identifier("transmigration-farming")
new_book.set_title(
    "My Second Journey: Transmigration Farming"
)
new_book.set_language("en")

epub_chapters = []

for index, chapter in enumerate(chapters, start=1):

    c = epub.EpubHtml(
        title=chapter["title"],
        file_name=f"chapter_{index}.xhtml",
        lang="en"
    )

    c.content = chapter["body"]

    new_book.add_item(c)

    epub_chapters.append(c)

new_book.toc = tuple(epub_chapters)
new_book.spine = ["nav"] + epub_chapters

new_book.add_item(epub.EpubNcx())
new_book.add_item(epub.EpubNav())

epub.write_epub(
    OUTPUT_EPUB,
    new_book
)

print("Done:")
print(OUTPUT_EPUB)