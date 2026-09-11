from ebooklib import epub
from ebooklib import ITEM_DOCUMENT
from bs4 import BeautifulSoup

book = epub.read_epub("Transmigration_Farming.epub")

count = 0

for item in book.get_items():

    if item.get_type() != ITEM_DOCUMENT:
        continue

    print("-" * 80)
    print(item.get_name())

    try:
        html = item.get_content().decode(
            "utf-8",
            errors="ignore"
        )

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        title = None

        for tag in ["h1", "h2", "h3", "title"]:
            found = soup.find(tag)

            if found:
                title = found.get_text(strip=True)
                break

        if title:
            print("TITLE:", title)
            count += 1

    except Exception as e:
        print(e)

print()
print("Chapters found:", count)