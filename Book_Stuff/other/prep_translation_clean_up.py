from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup

book = epub.read_epub("Transmigration_Farming_Reordered.epub")

for item in book.get_items():
    if item.get_type() == ITEM_DOCUMENT and item.get_name() == "chapter_1.xhtml":

        html = item.get_content().decode(
            "utf-8",
            errors="ignore"
        )

        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text("\n")

        with open(
            "chapter_1.txt",
            "w",
            encoding="utf-8"
        ) as f:
            f.write(text)

        print("Saved chapter_1.txt")
        break